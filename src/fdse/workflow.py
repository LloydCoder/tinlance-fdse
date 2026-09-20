from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID, uuid4
from .domain import utc_now

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

@dataclass(frozen=True, slots=True)
class EngineeringContext:
    context_id: UUID
    project_id: UUID
    revision: str
    constraints: tuple[str,...]
    relevant_paths: tuple[str,...]
    created_at: object = field(default_factory=utc_now)

    @classmethod
    def create(cls, project_id: UUID, revision: str, constraints: tuple[str,...]=(), relevant_paths: tuple[str,...]=()):
        if not revision.strip(): raise ValueError("revision must be non-empty")
        return cls(uuid4(),project_id,revision,tuple(constraints),tuple(relevant_paths))

@dataclass(frozen=True, slots=True)
class EngineeringPlan:
    plan_id: UUID
    project_id: UUID
    objective: str
    steps: tuple[str,...]
    risk_level: str
    status: PlanStatus = PlanStatus.DRAFT
    created_at: object = field(default_factory=utc_now)

    @classmethod
    def create(cls, project_id: UUID, objective: str, steps: tuple[str,...], risk_level: str):
        if not objective.strip() or not steps or not risk_level.strip():
            raise ValueError("plan objective, steps, and risk level are required")
        return cls(uuid4(),project_id,objective.strip(),tuple(steps),risk_level.strip())

@dataclass(frozen=True, slots=True)
class ChangeSet:
    change_id: UUID
    plan_id: UUID
    base_revision: str
    proposed_revision: str
    summary: str
    status: ChangeStatus = ChangeStatus.PROPOSED
    created_at: object = field(default_factory=utc_now)

    @classmethod
    def create(cls, plan_id: UUID, base_revision: str, proposed_revision: str, summary: str):
        if any(not x.strip() for x in (base_revision,proposed_revision,summary)):
            raise ValueError("change fields are required")
        return cls(uuid4(),plan_id,base_revision,proposed_revision,summary.strip())

@dataclass(frozen=True, slots=True)
class Approval:
    approval_id: UUID
    tenant_id: UUID
    subject_id: UUID
    decision: str
    actor_ref: str
    policy_ref: str
    created_at: object = field(default_factory=utc_now)

    @classmethod
    def create(cls, tenant_id: UUID, subject_id: UUID, decision: str, actor_ref: str, policy_ref: str):
        if any(not x.strip() for x in (decision,actor_ref,policy_ref)):
            raise ValueError("approval fields are required")
        return cls(uuid4(),tenant_id,subject_id,decision,actor_ref,policy_ref)

@dataclass(frozen=True, slots=True)
class EngineeringReport:
    report_id: UUID
    project_id: UUID
    revision: str
    outcome: str
    evidence_ids: tuple[UUID,...]
    generated_at: object = field(default_factory=utc_now)

    @classmethod
    def create(cls, project_id: UUID, revision: str, outcome: str, evidence_ids: tuple[UUID,...]):
        if any(not x.strip() for x in (revision,outcome)):
            raise ValueError("report revision and outcome are required")
        return cls(uuid4(),project_id,revision,outcome.strip(),tuple(evidence_ids))
