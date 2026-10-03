"""E5 production-integration and system-of-systems validation contracts.

FDSE owns the versioned meaning of cross-system engineering contracts and the
evidence required to establish an integration claim. External systems remain
the authorities for execution, authentication, approvals, storage, deployment,
observability, and provider operations.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .evidence import digest


class IntegrationSystem(StrEnum):
    FDSE = "fdse"
    FDE_MASTERY = "fde_mastery"
    AGENT_PLATFORM = "agent_platform"
    TINLANCE = "tinlance"
    GITHUB = "github"
    CICD = "cicd"
    ARTIFACT_REGISTRY = "artifact_registry"
    PROVENANCE = "provenance"
    DEPLOYMENT = "deployment"
    OBSERVABILITY = "observability"
    CUSTOMER_ENVIRONMENT = "customer_environment"


class IntegrationDirection(StrEnum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    BIDIRECTIONAL = "bidirectional"


class IntegrationStatus(StrEnum):
    DECLARED = "declared"
    CONNECTED = "connected"
    VERIFIED = "verified"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class IntegrationContract:
    contract_id: str
    version: str
    source: IntegrationSystem
    target: IntegrationSystem
    direction: IntegrationDirection
    required_capabilities: tuple[str, ...]
    authority_owner: IntegrationSystem
    evidence_requirements: tuple[str, ...]

    def __post_init__(self) -> None:
        values = (self.contract_id, self.version)
        if any(not value.strip() for value in values):
            raise ValueError("integration contract identity is required")
        if self.source == self.target:
            raise ValueError("integration contract cannot connect a system to itself")
        if not self.required_capabilities:
            raise ValueError("integration contract requires capabilities")
        if not self.evidence_requirements:
            raise ValueError("integration contract requires evidence requirements")
        if any(
            not value.strip()
            for value in (*self.required_capabilities, *self.evidence_requirements)
        ):
            raise ValueError("integration contract values cannot be blank")


@dataclass(frozen=True, slots=True)
class IntegrationEvidence:
    contract_id: str
    status: IntegrationStatus
    evidence_id: str
    revision: str
    payload_digest: str

    def __post_init__(self) -> None:
        if any(not value.strip() for value in (self.contract_id, self.evidence_id, self.revision)):
            raise ValueError("integration evidence identity is required")
        if len(self.payload_digest) != 64 or any(
            character not in "0123456789abcdef" for character in self.payload_digest
        ):
            raise ValueError("integration evidence digest must be SHA-256")


class SystemOfSystemsGraph:
    """Deterministic integration graph; it does not execute external systems."""

    def __init__(self) -> None:
        self._contracts: dict[tuple[str, str], IntegrationContract] = {}
        self._evidence: dict[tuple[str, str], IntegrationEvidence] = {}

    def add_contract(self, contract: IntegrationContract) -> None:
        key = (contract.contract_id, contract.version)
        existing = self._contracts.get(key)
        if existing is not None and existing != contract:
            raise ValueError("integration contract identity collision")
        self._contracts[key] = contract

    def add_evidence(self, evidence: IntegrationEvidence) -> None:
        key = (evidence.contract_id, evidence.evidence_id)
        existing = self._evidence.get(key)
        if existing is not None and existing != evidence:
            raise ValueError("integration evidence identity collision")
        self._evidence[key] = evidence

    def require_verified(self, contract_id: str, version: str) -> IntegrationEvidence:
        contract = self._contracts.get((contract_id, version))
        if contract is None:
            raise ValueError("integration contract is not declared")
        candidates = [
            evidence
            for evidence in self._evidence.values()
            if evidence.contract_id == contract.contract_id
            and evidence.status is IntegrationStatus.VERIFIED
        ]
        if len(candidates) != 1:
            raise ValueError("integration contract requires exactly one verified evidence record")
        return candidates[0]

    def snapshot_digest(self) -> str:
        contracts = sorted(
            (
                contract.contract_id,
                contract.version,
                contract.source.value,
                contract.target.value,
                contract.direction.value,
                tuple(sorted(contract.required_capabilities)),
                contract.authority_owner.value,
                tuple(sorted(contract.evidence_requirements)),
            )
            for contract in self._contracts.values()
        )
        evidence = sorted(
            (
                item.contract_id,
                item.status.value,
                item.evidence_id,
                item.revision,
                item.payload_digest,
            )
            for item in self._evidence.values()
        )
        return digest({"contracts": contracts, "evidence": evidence})

    @property
    def contracts(self) -> tuple[IntegrationContract, ...]:
        return tuple(
            sorted(
                self._contracts.values(),
                key=lambda item: (item.contract_id, item.version),
            )
        )

    @property
    def evidence(self) -> tuple[IntegrationEvidence, ...]:
        return tuple(
            sorted(
                self._evidence.values(),
                key=lambda item: (item.contract_id, item.evidence_id),
            )
        )
