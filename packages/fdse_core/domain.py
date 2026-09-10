"""Core FDSE domain objects.

These objects intentionally contain engineering-domain state only. Generic identity,
authorization, approvals, execution, budgets, trajectory and audit authority belong
to Tinlance Agent Platform.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


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


@dataclass(frozen=True, slots=True)
class Project:
    id: str
    tenant_id: str
    name: str


@dataclass(frozen=True, slots=True)
class Repository:
    id: str
    project_id: str
    provider: str
    canonical_url: str
    default_branch: str


@dataclass(frozen=True, slots=True)
class Assessment:
    id: str
    project_id: str
    repository_id: str
    created_at: datetime
    objective: str


@dataclass(frozen=True, slots=True)
class Finding:
    id: str
    assessment_id: str
    title: str
    severity: Severity
    confidence: float
    status: FindingStatus = FindingStatus.OPEN
    source_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
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
