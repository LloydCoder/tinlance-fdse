"""Explicit domain lifecycle transition rules."""
from .domain import ChangeStatus, PlanStatus

_PLAN = {
    PlanStatus.DRAFT: frozenset({PlanStatus.READY, PlanStatus.FAILED}),
    PlanStatus.READY: frozenset({PlanStatus.EXECUTING, PlanStatus.FAILED}),
    PlanStatus.EXECUTING: frozenset({PlanStatus.COMPLETED, PlanStatus.FAILED}),
    PlanStatus.COMPLETED: frozenset(),
    PlanStatus.FAILED: frozenset(),
}

_CHANGE = {
    ChangeStatus.PROPOSED: frozenset({ChangeStatus.APPLIED, ChangeStatus.REJECTED}),
    ChangeStatus.APPLIED: frozenset({ChangeStatus.VERIFIED}),
    ChangeStatus.VERIFIED: frozenset(),
    ChangeStatus.REJECTED: frozenset(),
}


def transition_plan(current: PlanStatus, target: PlanStatus) -> PlanStatus:
    if target not in _PLAN[current]:
        raise ValueError(f"invalid plan transition: {current} -> {target}")
    return target


def transition_change(current: ChangeStatus, target: ChangeStatus) -> ChangeStatus:
    if target not in _CHANGE[current]:
        raise ValueError(f"invalid change transition: {current} -> {target}")
    return target
