"""Authoritative Transformation lifecycle transition rules."""

from __future__ import annotations

from .execution import ExecutionReceiptState
from .handoff import OwnershipTransferStatus
from .replication import ReplicationStage


_EXECUTION: dict[ExecutionReceiptState, frozenset[ExecutionReceiptState]] = {
    ExecutionReceiptState.PLANNED: frozenset(
        {ExecutionReceiptState.RUNNING, ExecutionReceiptState.FAILED, ExecutionReceiptState.CANCELLED}
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
    ReplicationStage.PLANNED: frozenset({ReplicationStage.CONFIGURED, ReplicationStage.FAILED}),
    ReplicationStage.CONFIGURED: frozenset({ReplicationStage.DEPLOYED, ReplicationStage.FAILED}),
    ReplicationStage.DEPLOYED: frozenset({ReplicationStage.MEASURED, ReplicationStage.FAILED}),
    ReplicationStage.MEASURED: frozenset({ReplicationStage.ACCEPTED, ReplicationStage.FAILED}),
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
    """Validate an execution receipt state transition."""
    if target not in _EXECUTION[current]:
        raise ValueError(f"invalid execution transition: {current} -> {target}")
    return target


def transition_replication(
    current: ReplicationStage, target: ReplicationStage
) -> ReplicationStage:
    """Validate a replication lifecycle transition."""
    if target not in _REPLICATION[current]:
        raise ValueError(f"invalid replication transition: {current} -> {target}")
    return target


def transition_handoff(
    current: OwnershipTransferStatus, target: OwnershipTransferStatus
) -> OwnershipTransferStatus:
    """Validate a customer-ownership handoff transition."""
    if target not in _HANDOFF[current]:
        raise ValueError(f"invalid handoff transition: {current} -> {target}")
    return target


__all__ = ["transition_execution", "transition_handoff", "transition_replication"]
