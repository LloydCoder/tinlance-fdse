"""Explicit domain lifecycle transition rules."""
from fdse import domain


_PLAN = {
    domain.PlanStatus.DRAFT: frozenset({domain.PlanStatus.READY, domain.PlanStatus.FAILED}),
    domain.PlanStatus.READY: frozenset(
        {
            domain.PlanStatus.EXECUTING,
            domain.PlanStatus.AWAITING_APPROVAL,
            domain.PlanStatus.FAILED,
        }
    ),
    domain.PlanStatus.EXECUTING: frozenset(
        {
            domain.PlanStatus.AWAITING_APPROVAL,
            domain.PlanStatus.COMPLETED,
            domain.PlanStatus.FAILED,
        }
    ),
    domain.PlanStatus.AWAITING_APPROVAL: frozenset(
        {
            domain.PlanStatus.EXECUTING,
            domain.PlanStatus.COMPLETED,
            domain.PlanStatus.FAILED,
        }
    ),
    domain.PlanStatus.COMPLETED: frozenset(),
    domain.PlanStatus.FAILED: frozenset(),
}

_CHANGE = {
    domain.ChangeStatus.PROPOSED: frozenset(
        {domain.ChangeStatus.APPLIED, domain.ChangeStatus.REJECTED}
    ),
    domain.ChangeStatus.APPLIED: frozenset(
        {domain.ChangeStatus.VERIFIED, domain.ChangeStatus.REJECTED}
    ),
    domain.ChangeStatus.VERIFIED: frozenset(),
    domain.ChangeStatus.REJECTED: frozenset(),
}

_FINDING = {
    domain.FindingStatus.OPEN: frozenset(
        {
            domain.FindingStatus.ACCEPTED,
            domain.FindingStatus.REJECTED,
        }
    ),
    domain.FindingStatus.ACCEPTED: frozenset(
        {
            domain.FindingStatus.REMEDIATION_PLANNED,
            domain.FindingStatus.REJECTED,
        }
    ),
    domain.FindingStatus.REMEDIATION_PLANNED: frozenset(
        {
            domain.FindingStatus.REMEDIATED,
            domain.FindingStatus.REJECTED,
        }
    ),
    domain.FindingStatus.REMEDIATED: frozenset({domain.FindingStatus.VERIFIED}),
    domain.FindingStatus.VERIFIED: frozenset(),
    domain.FindingStatus.REJECTED: frozenset(),
}


def transition_plan(current: domain.PlanStatus, target: domain.PlanStatus) -> domain.PlanStatus:
    if target not in _PLAN[current]:
        raise ValueError(f"invalid plan transition: {current} -> {target}")
    return target


def transition_change(current: domain.ChangeStatus, target: domain.ChangeStatus) -> domain.ChangeStatus:
    if target not in _CHANGE[current]:
        raise ValueError(f"invalid change transition: {current} -> {target}")
    return target


def transition_finding(
    current: domain.FindingStatus,
    target: domain.FindingStatus,
) -> domain.FindingStatus:
    if target not in _FINDING[current]:
        raise ValueError(f"invalid finding transition: {current} -> {target}")
    return target
