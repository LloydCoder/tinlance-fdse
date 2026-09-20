from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class FindingStatus(StrEnum):
    OPEN = "open"
    ACCEPTED = "accepted"
    REMEDIATION_PLANNED = "remediation_planned"
    REMEDIATED = "remediated"
    VERIFIED = "verified"
    REJECTED = "rejected"

class VerificationStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    UNKNOWN = "unknown"

@dataclass(frozen=True, slots=True)
class RepositoryRef:
    provider: str
    owner: str
    name: str
    revision: str
    def __post_init__(self) -> None:
        if any(not v.strip() for v in (self.provider,self.owner,self.name,self.revision)):
            raise ValueError("repository reference fields must be non-empty")

@dataclass(frozen=True, slots=True)
class Project:
    project_id: UUID
    tenant_id: UUID
    name: str
    repository: RepositoryRef
    created_at: datetime = field(default_factory=utc_now)
    @classmethod
    def create(cls, tenant_id: UUID, name: str, repository: RepositoryRef) -> "Project":
        if not name.strip(): raise ValueError("project name must be non-empty")
        return cls(uuid4(), tenant_id, name.strip(), repository)

@dataclass(frozen=True, slots=True)
class Evidence:
    evidence_id: UUID
    kind: str
    summary: str
    payload_digest: str
    source: str
    collected_at: datetime = field(default_factory=utc_now)
    @classmethod
    def create(cls, kind: str, summary: str, payload_digest: str, source: str) -> "Evidence":
        if any(not v.strip() for v in (kind,summary,payload_digest,source)):
            raise ValueError("evidence fields must be non-empty")
        return cls(uuid4(),kind,summary,payload_digest,source)

@dataclass(frozen=True, slots=True)
class Finding:
    finding_id: UUID
    project_id: UUID
    title: str
    category: str
    severity: str
    status: FindingStatus
    evidence_ids: tuple[UUID,...]
    created_at: datetime = field(default_factory=utc_now)
    @classmethod
    def create(cls, project_id: UUID, title: str, category: str, severity: str, evidence_ids: tuple[UUID,...]=()) -> "Finding":
        if any(not v.strip() for v in (title,category,severity)):
            raise ValueError("finding title, category, and severity must be non-empty")
        return cls(uuid4(),project_id,title.strip(),category.strip(),severity.strip(),FindingStatus.OPEN,tuple(evidence_ids))

@dataclass(frozen=True, slots=True)
class VerificationResult:
    verification_id: UUID
    finding_id: UUID
    status: VerificationStatus
    checks: tuple[str,...]
    evidence_ids: tuple[UUID,...]
    verified_at: datetime = field(default_factory=utc_now)
    @classmethod
    def create(cls, finding_id: UUID, status: VerificationStatus, checks: tuple[str,...], evidence_ids: tuple[UUID,...]=()) -> "VerificationResult":
        if not checks: raise ValueError("verification requires at least one check")
        return cls(uuid4(),finding_id,status,tuple(checks),tuple(evidence_ids))

@dataclass(frozen=True, slots=True)
class Assessment:
    assessment_id: UUID
    project_id: UUID
    purpose: str
    findings: tuple[UUID,...] = ()
    evidence: tuple[UUID,...] = ()
    created_at: datetime = field(default_factory=utc_now)
    @classmethod
    def create(cls, project_id: UUID, purpose: str) -> "Assessment":
        if not purpose.strip(): raise ValueError("assessment purpose must be non-empty")
        return cls(uuid4(),project_id,purpose.strip())
