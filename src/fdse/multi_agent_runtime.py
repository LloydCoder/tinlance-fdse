"""Fail-closed multi-agent runtime semantics (M17).

FDSE owns delegation/task/message/provenance semantics. Agent identity,
authentication, authorization, capability grants, runtime isolation, and model
execution remain Agent Platform responsibilities.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol

from .evidence import digest


class AgentTaskStatus(StrEnum):
    CREATED = "created"
    RUNNING = "running"
    WAITING = "waiting"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    ESCALATED = "escalated"
    CANCELLED = "cancelled"


class MessageKind(StrEnum):
    REQUEST = "request"
    RESULT = "result"
    EVENT = "event"
    ESCALATION = "escalation"


@dataclass(frozen=True, slots=True)
class AgentIdentity:
    agent_id: str
    issuer: str
    key_id: str

    def __post_init__(self) -> None:
        if not all(value.strip() for value in (self.agent_id, self.issuer, self.key_id)):
            raise ValueError("agent identity fields are required")


@dataclass(frozen=True, slots=True)
class IdentityAttestation:
    identity: AgentIdentity
    issued_at: datetime
    expires_at: datetime
    nonce: str
    signature_digest: str

    def __post_init__(self) -> None:
        if self.expires_at <= self.issued_at:
            raise ValueError("identity attestation expiry must be after issuance")
        if not self.nonce.strip():
            raise ValueError("identity attestation nonce is required")
        if len(self.signature_digest) != 64 or any(
            char not in "0123456789abcdef" for char in self.signature_digest.lower()
        ):
            raise ValueError("identity attestation digest must be SHA-256 hex")


@dataclass(frozen=True, slots=True)
class SharedContextRef:
    tenant_id: str
    repository_id: str
    revision: str
    context_digest: str
    read_only: bool = True

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.tenant_id,
                self.repository_id,
                self.revision,
                self.context_digest,
            )
        ):
            raise ValueError("shared context scope is required")
        if not self.read_only:
            raise ValueError("multi-agent shared context must be read-only")


@dataclass(frozen=True, slots=True)
class AgentTask:
    task_id: str
    agent: AgentIdentity
    tenant_id: str
    repository_id: str
    revision: str
    parent_task_id: str | None
    depth: int
    context: SharedContextRef
    requested_capabilities: tuple[str, ...] = ()
    status: AgentTaskStatus = AgentTaskStatus.CREATED
    result_digest: str | None = None

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.task_id,
                self.tenant_id,
                self.repository_id,
                self.revision,
            )
        ):
            raise ValueError("agent task scope is required")
        if self.depth < 0:
            raise ValueError("agent task depth cannot be negative")
        if (
            self.context.tenant_id,
            self.context.repository_id,
            self.context.revision,
        ) != (self.tenant_id, self.repository_id, self.revision):
            raise ValueError("task and shared context scopes must match")
        if len(set(self.requested_capabilities)) != len(self.requested_capabilities):
            raise ValueError("requested capabilities must be unique")


@dataclass(frozen=True, slots=True)
class DelegationRequest:
    request_id: str
    parent_task_id: str
    child_agent: AgentIdentity
    child_attestation: IdentityAttestation
    purpose: str
    requested_capabilities: tuple[str, ...]
    context: SharedContextRef

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.request_id,
                self.parent_task_id,
                self.purpose,
            )
        ):
            raise ValueError("delegation fields are required")


@dataclass(frozen=True, slots=True)
class AgentMessage:
    message_id: str
    conversation_id: str
    sender: AgentIdentity
    recipient: AgentIdentity
    tenant_id: str
    repository_id: str
    revision: str
    sequence: int
    kind: MessageKind
    payload_digest: str
    attestation: IdentityAttestation

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.message_id,
                self.conversation_id,
                self.tenant_id,
                self.repository_id,
                self.revision,
                self.payload_digest,
            )
        ):
            raise ValueError("agent message fields are required")
        if self.sequence < 1:
            raise ValueError("message sequence must be positive")
        if self.attestation.identity != self.sender:
            raise ValueError("message sender does not match attested identity")
        if len(self.payload_digest) != 64:
            raise ValueError("message payload digest must be SHA-256 hex")


@dataclass(frozen=True, slots=True)
class Escalation:
    escalation_id: str
    task_id: str
    reason: str
    evidence_digest: str
    target: str

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.escalation_id,
                self.task_id,
                self.reason,
                self.evidence_digest,
                self.target,
            )
        ):
            raise ValueError("escalation fields are required")


class IdentityVerifier(Protocol):
    def verify(
        self,
        attestation: IdentityAttestation,
        *,
        now: datetime,
    ) -> bool: ...


class DenyIdentityVerifier:
    def verify(
        self,
        attestation: IdentityAttestation,
        *,
        now: datetime,
    ) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class MultiAgentPolicy:
    max_depth: int = 4
    max_children_per_parent: int = 8

    def __post_init__(self) -> None:
        if self.max_depth < 0 or self.max_children_per_parent < 1:
            raise ValueError("multi-agent policy bounds are invalid")


class MultiAgentRuntime:
    """Deterministic supervision/delegation registry with fail-closed identity checks."""

    def __init__(
        self,
        *,
        identity_verifier: IdentityVerifier,
        policy: MultiAgentPolicy,
    ) -> None:
        self.identity_verifier = identity_verifier
        self.policy = policy
        self.tasks: dict[str, AgentTask] = {}
        self.messages: dict[str, AgentMessage] = {}
        self.conversation_sequences: dict[str, int] = {}
        self.children: dict[str, set[str]] = {}

    def register_root(
        self,
        task_id: str,
        agent: AgentIdentity,
        tenant_id: str,
        repository_id: str,
        revision: str,
        context: SharedContextRef,
    ) -> AgentTask:
        if task_id in self.tasks:
            raise ValueError("task identifier already exists")
        task = AgentTask(
            task_id,
            agent,
            tenant_id,
            repository_id,
            revision,
            None,
            0,
            context,
        )
        self.tasks[task_id] = task
        return task

    def delegate(
        self,
        request: DelegationRequest,
        *,
        now: datetime,
    ) -> AgentTask:
        parent = self._task(request.parent_task_id)
        if not self.identity_verifier.verify(
            request.child_attestation,
            now=now,
        ):
            raise PermissionError("child identity is not authenticated")
        if parent.status in {
            AgentTaskStatus.FAILED,
            AgentTaskStatus.CANCELLED,
        }:
            raise ValueError("cannot delegate from a terminal failed task")
        if parent.depth + 1 > self.policy.max_depth:
            raise PermissionError("multi-agent delegation depth exceeded")
        children = self.children.setdefault(parent.task_id, set())
        if len(children) >= self.policy.max_children_per_parent:
            raise PermissionError("multi-agent child-task limit exceeded")
        if (
            request.context.tenant_id,
            request.context.repository_id,
            request.context.revision,
        ) != (parent.tenant_id, parent.repository_id, parent.revision):
            raise PermissionError("delegation context crosses task scope")
        child = AgentTask(
            request.request_id,
            request.child_agent,
            parent.tenant_id,
            parent.repository_id,
            parent.revision,
            parent.task_id,
            parent.depth + 1,
            request.context,
            tuple(sorted(set(request.requested_capabilities))),
        )
        if child.task_id in self.tasks:
            raise ValueError("delegation request identifier already exists")
        self.tasks[child.task_id] = child
        children.add(child.task_id)
        return child

    def send(
        self,
        message: AgentMessage,
        *,
        payload: object,
        now: datetime,
    ) -> AgentMessage:
        if not self.identity_verifier.verify(message.attestation, now=now):
            raise PermissionError("agent message identity is not authenticated")
        if message.attestation.identity != message.sender:
            raise PermissionError("agent message identity mismatch")
        if message.message_id in self.messages:
            existing = self.messages[message.message_id]
            if existing != message:
                raise ValueError("message identifier is already bound")
            return existing
        if digest(payload) != message.payload_digest:
            raise ValueError("message payload digest mismatch")
        sequence = self.conversation_sequences.get(message.conversation_id, 0) + 1
        if message.sequence != sequence:
            raise ValueError("message sequence is not monotonic")
        sender_scope = self._agent_scope(message.sender.agent_id)
        recipient_scope = self._agent_scope(message.recipient.agent_id)
        if sender_scope != recipient_scope:
            raise PermissionError("agent message participants have different scopes")
        if sender_scope != (
            message.tenant_id,
            message.repository_id,
            message.revision,
        ):
            raise PermissionError("agent message violates tenant/repository/revision scope")
        self.messages[message.message_id] = message
        self.conversation_sequences[message.conversation_id] = sequence
        return message

    def complete(
        self,
        task_id: str,
        result: object,
    ) -> AgentTask:
        task = self._task(task_id)
        if task.status in {
            AgentTaskStatus.SUCCEEDED,
            AgentTaskStatus.FAILED,
            AgentTaskStatus.CANCELLED,
        }:
            return task
        updated = _task_with_result(task, digest(result))
        self.tasks[task_id] = updated
        return updated

    def fail(self, task_id: str, result: object | None = None) -> AgentTask:
        task = self._task(task_id)
        updated = _task_with_status(
            _task_with_result(task, digest(result if result is not None else {})),
            AgentTaskStatus.FAILED,
        )
        self.tasks[task_id] = updated
        return updated

    def aggregate(self, parent_task_id: str) -> str:
        parent = self._task(parent_task_id)
        child_tasks = [
            self.tasks[child_id] for child_id in sorted(self.children.get(parent.task_id, set()))
        ]
        if any(
            task.status not in {AgentTaskStatus.SUCCEEDED, AgentTaskStatus.FAILED}
            for task in child_tasks
        ):
            raise ValueError("cannot aggregate unfinished child tasks")
        if any(
            (task.tenant_id, task.repository_id, task.revision)
            != (parent.tenant_id, parent.repository_id, parent.revision)
            for task in child_tasks
        ):
            raise PermissionError("child task scope mismatch")
        return digest(
            [
                (task.task_id, task.agent.agent_id, task.status.value, task.result_digest)
                for task in child_tasks
            ]
        )

    def escalate(self, task_id: str, reason: str, target: str) -> Escalation:
        task = self._task(task_id)
        if not reason.strip() or not target.strip():
            raise ValueError("escalation reason and target are required")
        escalation = Escalation(
            escalation_id=f"escalation:{task.task_id}:{len(self.messages) + 1}",
            task_id=task.task_id,
            reason=reason,
            evidence_digest=digest(
                {
                    "task": task.task_id,
                    "parent": task.parent_task_id,
                    "context": task.context.context_digest,
                    "reason": reason,
                }
            ),
            target=target,
        )
        self.tasks[task_id] = _task_with_status(task, AgentTaskStatus.ESCALATED)
        return escalation

    def _task(self, task_id: str) -> AgentTask:
        try:
            return self.tasks[task_id]
        except KeyError as exc:
            raise KeyError(f"unknown agent task: {task_id}") from exc

    def _agent_scope(self, agent_id: str) -> tuple[str, str, str]:
        scopes = {
            (task.tenant_id, task.repository_id, task.revision)
            for task in self.tasks.values()
            if task.agent.agent_id == agent_id
        }
        if not scopes:
            raise PermissionError("agent is not registered in a task scope")
        if len(scopes) != 1:
            raise PermissionError("agent is registered in multiple scopes")
        return next(iter(scopes))


def _task_with_status(task: AgentTask, status: AgentTaskStatus) -> AgentTask:
    return AgentTask(
        task_id=task.task_id,
        agent=task.agent,
        tenant_id=task.tenant_id,
        repository_id=task.repository_id,
        revision=task.revision,
        parent_task_id=task.parent_task_id,
        depth=task.depth,
        context=task.context,
        requested_capabilities=task.requested_capabilities,
        status=status,
        result_digest=task.result_digest,
    )


def _task_with_result(task: AgentTask, result_digest: str) -> AgentTask:
    return AgentTask(
        task_id=task.task_id,
        agent=task.agent,
        tenant_id=task.tenant_id,
        repository_id=task.repository_id,
        revision=task.revision,
        parent_task_id=task.parent_task_id,
        depth=task.depth,
        context=task.context,
        requested_capabilities=task.requested_capabilities,
        status=AgentTaskStatus.SUCCEEDED,
        result_digest=result_digest,
    )
