"""Single source of truth for FDSE domain lifecycle transition rules."""

from __future__ import annotations

from .domain import ChangeStatus, FindingStatus, PlanStatus
from .transformation.execution import ExecutionReceiptState
from .transformation.handoff import OwnershipTransferStatus
from .transformation.replication import ReplicationStage

_FINDING: dict[FindingStatus, frozenset[FindingStatus]] = {
    FindingStatus.OPEN: frozenset({FindingStatus.ACCEPTED, FindingStatus.REJECTED}),
    FindingStatus.ACCEPTED: frozenset({FindingStatus.REMEDIATION_PLANNED, FindingStatus.REJECTED}),
    FindingStatus.REMEDIATION_PLANNED: frozenset(
        {FindingStatus.REMEDIATED, FindingStatus.REJECTED}
    ),
    FindingStatus.REMEDIATED: frozenset({FindingStatus.VERIFIED}),
    FindingStatus.VERIFIED: frozenset(),
    FindingStatus.REJECTED: frozenset(),
}

_PLAN: dict[PlanStatus, frozenset[PlanStatus]] = {
    PlanStatus.DRAFT: frozenset({PlanStatus.READY, PlanStatus.FAILED}),
    PlanStatus.READY: frozenset({PlanStatus.AWAITING_APPROVAL, PlanStatus.FAILED}),
    PlanStatus.AWAITING_APPROVAL: frozenset({PlanStatus.EXECUTING, PlanStatus.FAILED}),
    PlanStatus.EXECUTING: frozenset({PlanStatus.COMPLETED, PlanStatus.FAILED}),
    PlanStatus.COMPLETED: frozenset(),
    PlanStatus.FAILED: frozenset(),
}

_CHANGE: dict[ChangeStatus, frozenset[ChangeStatus]] = {
    ChangeStatus.PROPOSED: frozenset({ChangeStatus.APPLIED, ChangeStatus.REJECTED}),
    ChangeStatus.APPLIED: frozenset({ChangeStatus.VERIFIED, ChangeStatus.REJECTED}),
    ChangeStatus.VERIFIED: frozenset(),
    ChangeStatus.REJECTED: frozenset(),
}


def transition_finding(current: FindingStatus, target: FindingStatus) -> FindingStatus:
    if target not in _FINDING[current]:
        raise ValueError(f"invalid finding transition: {current} -> {target}")
    return target


def transition_plan(current: PlanStatus, target: PlanStatus) -> PlanStatus:
    if target not in _PLAN[current]:
        raise ValueError(f"invalid plan transition: {current} -> {target}")
    return target


def transition_change(current: ChangeStatus, target: ChangeStatus) -> ChangeStatus:
    if target not in _CHANGE[current]:
        raise ValueError(f"invalid change transition: {current} -> {target}")
    return target


_EXECUTION: dict[ExecutionReceiptState, frozenset[ExecutionReceiptState]] = {
    ExecutionReceiptState.PLANNED: frozenset(
        {
            ExecutionReceiptState.RUNNING,
            ExecutionReceiptState.FAILED,
            ExecutionReceiptState.CANCELLED,
        }
    ),
    ExecutionReceiptState.RUNNING: frozenset(
        {
            ExecutionReceiptState.SUCCEEDED,
            ExecutionReceiptState.FAILED,
            ExecutionReceiptState.CANCELLED,
            ExecutionReceiptState.PARTIAL,
        }
    ),
    ExecutionReceiptState.SUCCEEDED: frozenset(),
    ExecutionReceiptState.FAILED: frozenset(),
    ExecutionReceiptState.CANCELLED: frozenset(),
    ExecutionReceiptState.PARTIAL: frozenset(),
}

_REPLICATION: dict[ReplicationStage, frozenset[ReplicationStage]] = {
    ReplicationStage.PLANNED: frozenset(
        {ReplicationStage.CONFIGURED, ReplicationStage.FAILED}
    ),
    ReplicationStage.CONFIGURED: frozenset(
        {ReplicationStage.DEPLOYED, ReplicationStage.FAILED}
    ),
    ReplicationStage.DEPLOYED: frozenset(
        {ReplicationStage.MEASURED, ReplicationStage.FAILED}
    ),
    ReplicationStage.MEASURED: frozenset(
        {ReplicationStage.ACCEPTED, ReplicationStage.FAILED}
    ),
    ReplicationStage.ACCEPTED: frozenset(),
    ReplicationStage.FAILED: frozenset(),
}

_HANDOFF: dict[OwnershipTransferStatus, frozenset[OwnershipTransferStatus]] = {
    OwnershipTransferStatus.PENDING: frozenset({OwnershipTransferStatus.ACCEPTED}),
    OwnershipTransferStatus.ACCEPTED: frozenset({OwnershipTransferStatus.TRANSFERRED}),
    OwnershipTransferStatus.TRANSFERRED: frozenset(),
}


def transition_execution(
    current: ExecutionReceiptState, target: ExecutionReceiptState
) -> ExecutionReceiptState:
    """Validate a Transformation execution receipt state transition."""
    if target not in _EXECUTION[current]:
        raise ValueError(f"invalid execution transition: {current} -> {target}")
    return target


def transition_replication(current: ReplicationStage, target: ReplicationStage) -> ReplicationStage:
    """Validate a Transformation replication lifecycle transition."""
    if target not in _REPLICATION[current]:
        raise ValueError(f"invalid replication transition: {current} -> {target}")
    return target


def transition_handoff(
    current: OwnershipTransferStatus, target: OwnershipTransferStatus
) -> OwnershipTransferStatus:
    """Validate a Transformation customer-ownership handoff transition."""
    if target not in _HANDOFF[current]:
        raise ValueError(f"invalid handoff transition: {current} -> {target}")
    return target
