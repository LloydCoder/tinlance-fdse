"""Framework-neutral FDSE engineering-domain primitives.

Generic identity, authorization, approval, execution, budgets, trajectory and audit
authority remain owned by Tinlance Agent Platform.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


def _require_id(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be non-empty")


class Severity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FindingStatus(StrEnum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    PLANNED = "planned"
    REMEDIATING = "remediating"
    VERIFIED = "verified"
    ACCEPTED = "accepted"
    CLOSED = "closed"


@dataclass(frozen=True, slots=True)
class Tenant:
    id: str
    name: str

    def __post_init__(self) -> None:
        _require_id(self.id, "tenant id")
        if not self.name.strip():
            raise ValueError("tenant name must be non-empty")


@dataclass(frozen=True, slots=True)
class Project:
    id: str
    tenant_id: str
    name: str

    def __post_init__(self) -> None:
        _require_id(self.id, "project id")
        _require_id(self.tenant_id, "project tenant id")
        if not self.name.strip():
            raise ValueError("project name must be non-empty")


@dataclass(frozen=True, slots=True)
class Repository:
    id: str
    tenant_id: str
    project_id: str
    provider: str
    canonical_url: str
    default_branch: str

    def __post_init__(self) -> None:
        _require_id(self.id, "repository id")
        _require_id(self.tenant_id, "repository tenant id")
        _require_id(self.project_id, "repository project id")
        if not self.provider.strip() or not self.canonical_url.strip() or not self.default_branch.strip():
            raise ValueError(
                "repository provider, canonical_url and default_branch must be non-empty"
            )


@dataclass(frozen=True, slots=True)
class Assessment:
    id: str
    tenant_id: str
    project_id: str
    repository_id: str
    created_at: datetime
    objective: str

    def __post_init__(self) -> None:
        _require_id(self.id, "assessment id")
        _require_id(self.tenant_id, "assessment tenant id")
        _require_id(self.project_id, "assessment project id")
        _require_id(self.repository_id, "assessment repository id")
        if not self.objective.strip():
            raise ValueError("assessment objective must be non-empty")


@dataclass(frozen=True, slots=True)
class Finding:
    id: str
    tenant_id: str
    assessment_id: str
    title: str
    severity: Severity
    confidence: float
    status: FindingStatus = FindingStatus.OPEN
    source_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        _require_id(self.id, "finding id")
        _require_id(self.tenant_id, "finding tenant id")
        _require_id(self.assessment_id, "finding assessment id")
        if not self.title.strip():
            raise ValueError("finding title must be non-empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class Evidence:
    id: str
    tenant_id: str
    assessment_id: str
    kind: str
    digest: str
    source_ref: str
    captured_at: datetime
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        _require_id(self.id, "evidence id")
        _require_id(self.tenant_id, "evidence tenant id")
        _require_id(self.assessment_id, "evidence assessment id")
        if not self.kind.strip() or not self.digest.strip() or not self.source_ref.strip():
            raise ValueError("evidence kind, digest and source_ref must be non-empty")
