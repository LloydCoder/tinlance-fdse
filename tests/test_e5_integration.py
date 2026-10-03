import pytest

from fdse import (
    IntegrationContract,
    IntegrationDirection,
    IntegrationEvidence,
    IntegrationStatus,
    IntegrationSystem,
    SystemOfSystemsGraph,
)


def contract(identifier: str = "fdse-agent-platform") -> IntegrationContract:
    return IntegrationContract(
        identifier,
        "1.0",
        IntegrationSystem.FDSE,
        IntegrationSystem.AGENT_PLATFORM,
        IntegrationDirection.BIDIRECTIONAL,
        ("engineering_intent", "execution_receipt"),
        IntegrationSystem.AGENT_PLATFORM,
        ("request", "receipt", "attestation"),
    )


def evidence(
    status: IntegrationStatus = IntegrationStatus.VERIFIED,
) -> IntegrationEvidence:
    return IntegrationEvidence(
        "fdse-agent-platform",
        status,
        "evidence-1",
        "sha",
        "a" * 64,
    )


def test_system_of_systems_contracts_are_deterministic_and_verifiable() -> None:
    graph = SystemOfSystemsGraph()
    graph.add_contract(contract())
    graph.add_evidence(evidence())
    verified = graph.require_verified("fdse-agent-platform", "1.0")
    assert verified.status is IntegrationStatus.VERIFIED

    reverse = SystemOfSystemsGraph()
    reverse.add_evidence(evidence())
    reverse.add_contract(contract())
    assert reverse.snapshot_digest() == graph.snapshot_digest()


def test_integration_contracts_fail_closed_on_invalid_identity_or_scope() -> None:
    with pytest.raises(ValueError):
        IntegrationContract(
            "fdse-agent-platform",
            "1.0",
            IntegrationSystem.FDSE,
            IntegrationSystem.FDSE,
            IntegrationDirection.OUTBOUND,
            ("intent",),
            IntegrationSystem.FDSE,
            ("receipt",),
        )
    with pytest.raises(ValueError):
        IntegrationContract(
            "",
            "1.0",
            IntegrationSystem.FDSE,
            IntegrationSystem.AGENT_PLATFORM,
            IntegrationDirection.OUTBOUND,
            ("intent",),
            IntegrationSystem.AGENT_PLATFORM,
            ("receipt",),
        )


def test_verification_requires_exactly_one_verified_evidence_record() -> None:
    graph = SystemOfSystemsGraph()
    graph.add_contract(contract())
    graph.add_evidence(evidence(IntegrationStatus.CONNECTED))
    with pytest.raises(ValueError):
        graph.require_verified("fdse-agent-platform", "1.0")
