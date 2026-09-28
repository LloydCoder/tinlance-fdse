"""Core FDSE engineering-domain entities and lifecycle values."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4


def utc_now() -> datetime:
    return datetime.now(UTC)


def _required(value: str, field_name: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError(f"{field_name} is required")
    if "\x00" in value:
        raise ValueError(f"{field_name} contains a NUL byte")
    return value


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


class PlanStatus(StrEnum):
    DRAFT = "draft"
    READY = "ready"
    EXECUTING = "executing"
    AWAITING_APPROVAL = "awaiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"


class ChangeStatus(StrEnum):
    PROPOSED = "proposed"
    APPLIED = "applied"
    VERIFIED = "verified"
    REJECTED = "rejected"


_FINDING_TRANSITIONS: dict[FindingStatus, frozenset[FindingStatus]] = {
    FindingStatus.OPEN: frozenset({FindingStatus.ACCEPTED, FindingStatus.REJECTED}),
    FindingStatus.ACCEPTED: frozenset({FindingStatus.REMEDIATION_PLANNED, FindingStatus.REJECTED}),
    FindingStatus.REMEDIATION_PLANNED: frozenset({FindingStatus.REMEDIATED, FindingStatus.REJECTED}),
    FindingStatus.REMEDIATED: frozenset({FindingStatus.VERIFIED}),
    FindingStatus.VERIFIED: frozenset(),
    FindingStatus.REJECTED: frozenset(),
}

_PLAN_TRANSITIONS: dict[PlanStatus, frozenset[PlanStatus]] = {
    PlanStatus.DRAFT: frozenset({PlanStatus.READY, PlanStatus.FAILED}),
    PlanStatus.READY: frozenset({PlanStatus.EXECUTING, PlanStatus.AWAITING_APPROVAL, PlanStatus.FAILED}),
    PlanStatus.EXECUTING: frozenset({PlanStatus.COMPLETED, PlanStatus.FAILED}),
    PlanStatus.AWAITING_APPROVAL: frozenset({PlanStatus.EXECUTING, PlanStatus.FAILED}),
    PlanStatus.COMPLETED: frozenset(),
    PlanStatus.FAILED: frozenset(),
}

_CHANGE_TRANSITIONS: dict[ChangeStatus, frozenset[ChangeStatus]] = {
    ChangeStatus.PROPOSED: frozenset({ChangeStatus.APPLIED, ChangeStatus.REJECTED}),
    ChangeStatus.APPLIED: frozenset({ChangeStatus.VERIFIED, ChangeStatus.REJECTED}),
    ChangeStatus.VERIFIED: frozenset(),
    ChangeStatus.REJECTED: frozenset(),
}


def transition_finding(current: FindingStatus, target: FindingStatus) -> FindingStatus:
    if target not in _FINDING_TRANSITIONS[current]:
        raise ValueError(
            f"invalid finding transition: {current} -> {target}"
        )
    return target


def transition_plan(current: PlanStatus, target: PlanStatus) -> PlanStatus:
    if target not in _PLAN_TRANSITIONS[current]:
        raise ValueError(
            f"invalid plan transition: {current} -> {target}"
        )
    return target


def transition_change(current: ChangeStatus, target: ChangeStatus) -> ChangeStatus:
    if target not in _CHANGE_TRANSITIONS[current]:
        raise ValueError(
            f"invalid change transition: {current} -> {target}"
        )
    return target


@dataclass(frozen=True, slots=True)
class RepositoryRef:
    provider: str
    owner: str
    name: str
    revision: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.provider, "provider"),
            (self.owner, "owner"),
            (self.name, "name"),
            (self.revision, "revision"),
        ):
            _required(value, name)


@dataclass(frozen=True, slots=True)
class Project:
    project_id: UUID
    tenant_id: UUID
    name: str
    repository: RepositoryRef
    created_at: datetime = field(default_factory=utc_now)

    @classmethod
    def create(cls, tenant_id: UUID, name: str, repository: RepositoryRef) -> Project:
        return cls(uuid4(), tenant_id, _required(name, "project name"), repository)


@dataclass(frozen=True, slots=True)
class Assessment:
    assessment_id: UUID
    project_id: UUID
    purpose: str
    created_at: datetime = field(default_factory=utc_now)

    @classmethod
    def create(cls, project_id: UUID, purpose: str) -> Assessment:
        return cls(uuid4(), project_id, _required(purpose, "assessment purpose"))


@dataclass(frozen=True, slots=True)
class EngineeringContext:
    context_id: UUID
    project_id: UUID
    revision: str
    constraints: tuple[str, ...] = ()
    relevant_paths: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=utc_now)

    @classmethod
    def create(
        cls,
        project_id: UUID,
        revision: str,
        constraints: tuple[str, ...] = (),
        relevant_paths: tuple[str, ...] = (),
    ) -> EngineeringContext:
        return cls(
            uuid4(),
            project_id,
            _required(revision, "context revision"),
            tuple(_required(item, "context constraint") for item in constraints),
            tuple(_required(item, "context path") for item in relevant_paths),
        )


@dataclass(frozen=True, slots=True)
class Evidence:
    evidence_id: UUID
    project_id: UUID
    kind: str
    summary: str
    payload_digest: str
    source: str
    revision: str
    collected_at: datetime = field(default_factory=utc_now)

    @classmethod
    def create(
        cls,
        project_id: UUID,
        kind: str,
        summary: str,
        payload_digest: str,
        source: str,
        revision: str,
    ) -> Evidence:
        return cls(
            uuid4(),
            project_id,
            _required(kind, "evidence kind"),
            _required(summary, "evidence summary"),
            _required(payload_digest, "evidence digest"),
            _required(source, "evidence source"),
            _required(revision, "evidence revision"),
        )


@dataclass(frozen=True, slots=True)
class Finding:
    finding_id: UUID
    project_id: UUID
    title: str
    category: str
    severity: str
    status: FindingStatus
    evidence_ids: tuple[UUID, ...] = ()
    created_at: datetime = field(default_factory=utc_now)

    @classmethod
    def create(
        cls,
        project_id: UUID,
        title: str,
        category: str,
        severity: str,
        evidence_ids: tuple[UUID, ...] = (),
    ) -> Finding:
        return cls(
            uuid4(),
            project_id,
            _required(title, "finding title"),
            _required(category, "finding category"),
            _required(severity, "finding severity"),
            FindingStatus.OPEN,
            tuple(evidence_ids),
        )


@dataclass(frozen=True, slots=True)
class VerificationResult:
    verification_id: UUID
    finding_id: UUID
    status: VerificationStatus
    checks: tuple[str, ...]
    evidence_ids: tuple[UUID, ...]
    revision: str
    verified_at: datetime = field(default_factory=utc_now)

    @classmethod
    def create(
        cls,
        finding_id: UUID,
        status: VerificationStatus,
        checks: tuple[str, ...],
        evidence_ids: tuple[UUID, ...],
        revision: str,
    ) -> VerificationResult:
        if not checks or any(not check.strip() for check in checks):
            raise ValueError("verification requires non-empty checks")
        return cls(
            uuid4(),
            finding_id,
            status,
            tuple(checks),
            tuple(evidence_ids),
            _required(revision, "verification revision"),
        )


@dataclass(frozen=True, slots=True)
class EngineeringPlan:
    plan_id: UUID
    project_id: UUID
    objective: str
    steps: tuple[str, ...]
    risk_level: str
    status: PlanStatus = PlanStatus.DRAFT
    created_at: datetime = field(default_factory=utc_now)

    @classmethod
    def create(
        cls,
        project_id: UUID,
        objective: str,
        steps: tuple[str, ...],
        risk_level: str,
    ) -> EngineeringPlan:
        if not steps or any(not step.strip() for step in steps):
            raise ValueError("plan requires non-empty steps")
        return cls(
            uuid4(),
            project_id,
            _required(objective, "plan objective"),
            tuple(_required(step, "plan step") for step in steps),
            _required(risk_level, "plan risk level"),
        )


@dataclass(frozen=True, slots=True)
class ChangeSet:
    change_id: UUID
    plan_id: UUID
    base_revision: str
    proposed_revision: str
    summary: str
    status: ChangeStatus = ChangeStatus.PROPOSED
    created_at: datetime = field(default_factory=utc_now)

    @classmethod
    def create(
        cls,
        plan_id: UUID,
        base_revision: str,
        proposed_revision: str,
        summary: str,
    ) -> ChangeSet:
        return cls(
            uuid4(),
            plan_id,
            _required(base_revision, "base revision"),
            _required(proposed_revision, "proposed revision"),
            _required(summary, "change summary"),
        )


@dataclass(frozen=True, slots=True)
class EngineeringReport:
    report_id: UUID
    project_id: UUID
    revision: str
    outcome: str
    evidence_ids: tuple[UUID, ...]
    generated_at: datetime = field(default_factory=utc_now)

    @classmethod
    def create(
        cls,
        project_id: UUID,
        revision: str,
        outcome: str,
        evidence_ids: tuple[UUID, ...],
    ) -> EngineeringReport:
        return cls(
            uuid4(),
            project_id,
            _required(revision, "report revision"),
            _required(outcome, "report outcome"),
            tuple(evidence_ids),
        )
