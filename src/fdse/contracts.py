"""Explicit FDSE domain contracts."""
from dataclasses import dataclass
from typing import Literal, Protocol

ExecutionRisk = Literal["low", "medium", "high", "critical"]
ExecutionStatus = Literal["accepted", "rejected", "completed", "failed", "cancelled"]
EvidenceKind = Literal["observation", "artifact", "test_result", "tool_result", "report"]
VerificationStatus = Literal["unverified", "verified", "failed", "unknown"]


@dataclass(frozen=True, slots=True)
class TenantScope:
    """Atomic tenant/repository domain scope; not an authorization decision."""

    tenant_id: str
    repository_id: str

    def __post_init__(self) -> None:
        if not self.tenant_id.strip() or not self.repository_id.strip():
            raise ValueError("tenant_id and repository_id are required")


@dataclass(frozen=True, slots=True)
class ProvenanceRef:
    source_id: str
    revision: str

    def __post_init__(self) -> None:
        if not self.source_id.strip() or not self.revision.strip():
            raise ValueError("source_id and revision are required")


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    evidence_id: str
    kind: EvidenceKind
    provenance: ProvenanceRef
    integrity_digest: str

    def __post_init__(self) -> None:
        if not self.evidence_id.strip() or not self.integrity_digest.strip():
            raise ValueError("evidence_id and integrity_digest are required")


@dataclass(frozen=True, slots=True)
class VerificationRef:
    verification_id: str
    evidence_id: str
    status: VerificationStatus

    def __post_init__(self) -> None:
        if not self.verification_id.strip() or not self.evidence_id.strip():
            raise ValueError("verification_id and evidence_id are required")


@dataclass(frozen=True, slots=True)
class EngineeringTask:
    task_id: str
    scope: TenantScope
    description: str
    risk: ExecutionRisk

    @property
    def tenant_id(self) -> str:
        return self.scope.tenant_id

    @property
    def repository_id(self) -> str:
        return self.scope.repository_id


@dataclass(frozen=True, slots=True)
class ExecutionRequest:
    """approval_required requests governance; it does not prove approval."""

    task: EngineeringTask
    workspace_id: str
    approval_required: bool = True


@dataclass(frozen=True, slots=True)
class ExecutionHandle:
    execution_id: str
    status: ExecutionStatus


class AgentPlatformGateway(Protocol):
    """FDSE engineering semantics -> Agent Platform authority boundary."""

    def submit(self, request: ExecutionRequest) -> ExecutionHandle:
        ...
