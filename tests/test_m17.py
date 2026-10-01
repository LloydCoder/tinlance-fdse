from datetime import UTC, datetime, timedelta

import pytest

from fdse.multi_agent_runtime import (
    AgentIdentity,
    AgentMessage,
    AgentTaskStatus,
    AllowIdentityVerifier,
    DelegationRequest,
    IdentityAttestation,
    MessageKind,
    MultiAgentPolicy,
    MultiAgentRuntime,
    SharedContextRef,
)


NOW = datetime(2026, 10, 1, tzinfo=UTC)


def identity(agent_id: str) -> AgentIdentity:
    return AgentIdentity(agent_id, "agent-platform", f"key-{agent_id}")


def attestation(agent: AgentIdentity) -> IdentityAttestation:
    return IdentityAttestation(
        agent,
        NOW - timedelta(minutes=1),
        NOW + timedelta(minutes=5),
        f"nonce-{agent.agent_id}",
        "a" * 64,
    )


def runtime() -> MultiAgentRuntime:
    return MultiAgentRuntime(
        identity_verifier=AllowIdentityVerifier(),
        policy=MultiAgentPolicy(max_depth=2, max_children_per_parent=2),
    )


def context() -> SharedContextRef:
    return SharedContextRef("t", "repo", "sha", "b" * 64)


def test_delegation_preserves_scope_and_depth() -> None:
    rt = runtime()
    root = rt.register_root("root", identity("a"), "t", "repo", "sha", context())
    child = rt.delegate(
        DelegationRequest(
            "child",
            root.task_id,
            identity("b"),
            attestation(identity("b")),
            "inspect",
            ("repository.read",),
            context(),
        ),
        now=NOW,
    )
    assert child.parent_task_id == root.task_id
    assert child.depth == 1
    assert child.requested_capabilities == ("repository.read",)


def test_delegation_rejects_scope_escape() -> None:
    rt = runtime()
    root = rt.register_root("root", identity("a"), "t", "repo", "sha", context())
    with pytest.raises(PermissionError):
        rt.delegate(
            DelegationRequest(
                "child",
                root.task_id,
                identity("b"),
                attestation(identity("b")),
                "inspect",
                (),
                SharedContextRef("other", "repo", "sha", "b" * 64),
            ),
            now=NOW,
        )


def test_message_requires_authenticated_sender_and_monotonic_sequence() -> None:
    rt = runtime()
    sender = identity("a")
    recipient = identity("b")
    rt.register_root("sender", sender, "t", "repo", "sha", context())
    rt.delegate(
        DelegationRequest(
            "recipient",
            "sender",
            recipient,
            attestation(recipient),
            "receive",
            (),
            context(),
        ),
        now=NOW,
    )
    payload = {"result": "ok"}
    message = AgentMessage(
        "m1",
        "c1",
        sender,
        recipient,
        "t",
        "repo",
        "sha",
        1,
        MessageKind.RESULT,
        digest(payload),
        attestation(sender),
    )
    assert rt.send(message, payload=payload, now=NOW) == message
    with pytest.raises(ValueError):
        rt.send(
            AgentMessage(
                "m2",
                "c1",
                sender,
                recipient,
                "t",
                "repo",
                "sha",
                3,
                MessageKind.EVENT,
                digest({"event": 1}),
                attestation(sender),
            ),
            payload={"event": 1},
            now=NOW,
        )


def test_expired_identity_is_rejected() -> None:
    rt = MultiAgentRuntime(
        identity_verifier=AllowIdentityVerifier(),
        policy=MultiAgentPolicy(),
    )
    sender = identity("a")
    recipient = identity("b")
    rt.register_root("sender", sender, "t", "repo", "sha", context())
    rt.delegate(
        DelegationRequest(
            "recipient",
            "sender",
            recipient,
            attestation(recipient),
            "receive",
            (),
            context(),
        ),
        now=NOW,
    )
    payload = {"x": 1}
    with pytest.raises(PermissionError):
        rt.send(
            AgentMessage(
                "m1",
                "c1",
                sender,
                recipient,
                "t",
                "repo",
                "sha",
                1,
                MessageKind.REQUEST,
                digest(payload),
                IdentityAttestation(
                    sender,
                    NOW - timedelta(minutes=10),
                    NOW - timedelta(minutes=1),
                    "nonce",
                    "a" * 64,
                ),
            ),
            payload=payload,
            now=NOW,
        )


def test_aggregation_is_deterministic_and_scope_safe() -> None:
    rt = runtime()
    root = rt.register_root("root", identity("a"), "t", "repo", "sha", context())
    child_a = rt.delegate(
        DelegationRequest(
            "a-child",
            "root",
            identity("b"),
            attestation(identity("b")),
            "a",
            (),
            context(),
        ),
        now=NOW,
    )
    child_b = rt.delegate(
        DelegationRequest(
            "b-child",
            "root",
            identity("c"),
            attestation(identity("c")),
            "b",
            (),
            context(),
        ),
        now=NOW,
    )
    rt.complete(child_a.task_id, {"a": 1})
    rt.complete(child_b.task_id, {"b": 2})
    first = rt.aggregate(root.task_id)
    second = rt.aggregate(root.task_id)
    assert first == second


def test_escalation_is_explicit_and_does_not_grant_authority() -> None:
    rt = runtime()
    root = rt.register_root("root", identity("a"), "t", "repo", "sha", context())
    escalation = rt.escalate(root.task_id, "requires approval", "platform-governance")
    assert escalation.target == "platform-governance"
    assert rt.tasks[root.task_id].status is AgentTaskStatus.ESCALATED
