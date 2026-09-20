"""Stable ports at the FDSE integration boundary."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, Sequence


class ExecutionStatus(StrEnum):
    ACCEPTED = "accepted"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class AuthorityContext:
    tenant_id: str
    actor_id: str
    correlation_id: str
    idempotency_key: str

    def __post_init__(self) -> None:
        for name, value in (
            ("tenant_id", self.tenant_id),
            ("actor_id", self.actor_id),
            ("correlation_id", self.correlation_id),
            ("idempotency_key", self.idempotency_key),
        ):
            if not value.strip():
                raise ValueError(f"{name} must be non-empty")


@dataclass(frozen=True, slots=True)
class ExecutionRequest:
    """Request for platform-governed execution; it contains no local authority grant."""

    authority: AuthorityContext
    project_id: str
    assessment_id: str
    workflow_id: str
    task: str
    risk_tier: str
    requested_capabilities: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name, value in (
            ("project_id", self.project_id),
            ("assessment_id", self.assessment_id),
            ("workflow_id", self.workflow_id),
            ("task", self.task),
            ("risk_tier", self.risk_tier),
        ):
            if not value.strip():
                raise ValueError(f"{name} must be non-empty")
        if any(not capability.strip() for capability in self.requested_capabilities):
            raise ValueError("requested capabilities must be non-empty strings")


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    execution_id: str
    status: ExecutionStatus
    evidence_refs: tuple[str, ...]
    provenance_ref: str
    error_code: str | None = None

    def __post_init__(self) -> None:
        if not self.execution_id.strip() or not self.provenance_ref.strip():
            raise ValueError("execution_id and provenance_ref must be non-empty")
        if self.status is ExecutionStatus.FAILED and not self.error_code:
            raise ValueError("failed execution requires an error_code")
        if self.status is not ExecutionStatus.FAILED and self.error_code is not None:
            raise ValueError("error_code is only valid for failed execution")
        if any(not ref.strip() for ref in self.evidence_refs):
            raise ValueError("evidence references must be non-empty")


def validate_tenant_scope(request: ExecutionRequest, target_tenant_id: str) -> None:
    """Reject a request whose authority tenant differs from its target context."""
    if not target_tenant_id.strip():
        raise ValueError("target tenant id must be non-empty")
    if request.authority.tenant_id != target_tenant_id:
        raise PermissionError("tenant mismatch")


class AgentPlatformPort(Protocol):
    """Minimal FDSE-to-Agent-Platform contract.

    The implementation must perform authorization, policy, approval, sandboxing,
    budgeting, secrets isolation, provenance and audit in Agent Platform.
    """

    def submit(self, request: ExecutionRequest) -> ExecutionResult: ...


class EvidencePort(Protocol):
    def record(self, tenant_id: str, evidence: object) -> str: ...


class GitProviderPort(Protocol):
    def repository_metadata(self, repository: str) -> object: ...

    def read_file(self, repository: str, path: str, ref: str) -> str: ...

    def create_branch(self, repository: str, branch: str, base_ref: str) -> str: ...

    def create_change(self, repository: str, branch: str, changes: Sequence[object]) -> str: ...
