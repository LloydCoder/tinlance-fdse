"""Explicit domain lifecycle transition rules."""
from __future__ import annotations  # noqa: I001

import fdse.domain


_PLAN = {
    fdse.domain.PlanStatus.DRAFT: frozenset(
        {fdse.domain.PlanStatus.READY, fdse.domain.PlanStatus.FAILED}
    ),
    fdse.domain.PlanStatus.READY: frozenset(
        {
            fdse.domain.PlanStatus.EXECUTING,
            fdse.domain.PlanStatus.AWAITING_APPROVAL,
            fdse.domain.PlanStatus.FAILED,
        }
    ),
    fdse.domain.PlanStatus.EXECUTING: frozenset(
        {
            fdse.domain.PlanStatus.AWAITING_APPROVAL,
            fdse.domain.PlanStatus.COMPLETED,
            fdse.domain.PlanStatus.FAILED,
        }
    ),
    fdse.domain.PlanStatus.AWAITING_APPROVAL: frozenset(
        {
            fdse.domain.PlanStatus.EXECUTING,
            fdse.domain.PlanStatus.COMPLETED,
            fdse.domain.PlanStatus.FAILED,
        }
    ),
    fdse.domain.PlanStatus.COMPLETED: frozenset(),
    fdse.domain.PlanStatus.FAILED: frozenset(),
}

_CHANGE = {
    fdse.domain.ChangeStatus.PROPOSED: frozenset(
        {
            fdse.domain.ChangeStatus.APPLIED,
            fdse.domain.ChangeStatus.REJECTED,
        }
    ),
    fdse.domain.ChangeStatus.APPLIED: frozenset(
        {
            fdse.domain.ChangeStatus.VERIFIED,
            fdse.domain.ChangeStatus.REJECTED,
        }
    ),
    fdse.domain.ChangeStatus.VERIFIED: frozenset(),
    fdse.domain.ChangeStatus.REJECTED: frozenset(),
}

_FINDING = {
    fdse.domain.FindingStatus.OPEN: frozenset(
        {
            fdse.domain.FindingStatus.ACCEPTED,
            fdse.domain.FindingStatus.REJECTED,
        }
    ),
    fdse.domain.FindingStatus.ACCEPTED: frozenset(
        {
            fdse.domain.FindingStatus.REMEDIATION_PLANNED,
            fdse.domain.FindingStatus.REJECTED,
        }
    ),
    fdse.domain.FindingStatus.REMEDIATION_PLANNED: frozenset(
        {
            fdse.domain.FindingStatus.REMEDIATED,
            fdse.domain.FindingStatus.REJECTED,
        }
    ),
    fdse.domain.FindingStatus.REMEDIATED: frozenset(
        {fdse.domain.FindingStatus.VERIFIED}
    ),
    fdse.domain.FindingStatus.VERIFIED: frozenset(),
    fdse.domain.FindingStatus.REJECTED: frozenset(),
}


def transition_plan(
    current: fdse.domain.PlanStatus,
    target: fdse.domain.PlanStatus,
) -> fdse.domain.PlanStatus:
    if target not in _PLAN[current]:
        raise ValueError(f"invalid plan transition: {current} -> {target}")
    return target


def transition_change(
    current: fdse.domain.ChangeStatus,
    target: fdse.domain.ChangeStatus,
) -> fdse.domain.ChangeStatus:
    if target not in _CHANGE[current]:
        raise ValueError(f"invalid change transition: {current} -> {target}")
    return target


def transition_finding(
    current: fdse.domain.FindingStatus,
    target: fdse.domain.FindingStatus,
) -> fdse.domain.FindingStatus:
    if target not in _FINDING[current]:
        raise ValueError(f"invalid finding transition: {current} -> {target}")
    return target
