"""Explicit domain lifecycle transition rules."""
from .domain import ChangeStatus, FindingStatus, PlanStatus


_PLAN = {
    PlanStatus.DRAFT: frozenset({PlanStatus.READY, PlanStatus.FAILED}),
    PlanStatus.READY: frozenset(
        {
            PlanStatus.EXECUTING,
            PlanStatus.AWAITING_APPROVAL,
            PlanStatus.FAILED,
        }
    ),
    PlanStatus.EXECUTING: frozenset(
        {
            PlanStatus.AWAITING_APPROVAL,
            PlanStatus.COMPLETED,
            PlanStatus.FAILED,
        }
    ),
    PlanStatus.AWAITING_APPROVAL: frozenset(
        {
            PlanStatus.EXECUTING,
            PlanStatus.COMPLETED,
            PlanStatus.FAILED,
        }
    ),
    PlanStatus.COMPLETED: frozenset(),
    PlanStatus.FAILED: frozenset(),
}

_CHANGE = {
    ChangeStatus.PROPOSED: frozenset(
        {ChangeStatus.APPLIED, ChangeStatus.REJECTED}
    ),
    ChangeStatus.APPLIED: frozenset(
        {ChangeStatus.VERIFIED, ChangeStatus.REJECTED}
    ),
    ChangeStatus.VERIFIED: frozenset(),
    ChangeStatus.REJECTED: frozenset(),
}

_FINDING = {
    FindingStatus.OPEN: frozenset(
        {
            FindingStatus.ACCEPTED,
            FindingStatus.REJECTED,
        }
    ),
    FindingStatus.ACCEPTED: frozenset(
        {
            FindingStatus.REMEDIATION_PLANNED,
            FindingStatus.REJECTED,
        }
    ),
    FindingStatus.REMEDIATION_PLANNED: frozenset(
        {
            FindingStatus.REMEDIATED,
            FindingStatus.REJECTED,
        }
    ),
    FindingStatus.REMEDIATED: frozenset({FindingStatus.VERIFIED}),
    FindingStatus.VERIFIED: frozenset(),
    FindingStatus.REJECTED: frozenset(),
}


def transition_plan(current: PlanStatus, target: PlanStatus) -> PlanStatus:
    if target not in _PLAN[current]:
        raise ValueError(f"invalid plan transition: {current} -> {target}")
    return target


def transition_change(current: ChangeStatus, target: ChangeStatus) -> ChangeStatus:
    if target not in _CHANGE[current]:
        raise ValueError(f"invalid change transition: {current} -> {target}")
    return target


def transition_finding(
    current: FindingStatus,
    target: FindingStatus,
) -> FindingStatus:
    if target not in _FINDING[current]:
        raise ValueError(f"invalid finding transition: {current} -> {target}")
    return target
