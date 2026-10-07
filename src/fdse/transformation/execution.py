"""Authority-neutral receipt for governed Agent-System execution."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ._common import enum_required, required, unique_ids


class ExecutionReceiptState(StrEnum):
    PLANNED = "PLANNED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    PARTIAL = "PARTIAL"


@dataclass(frozen=True, slots=True)
class GovernedExecutionReceipt:
    """Record references proving that execution crossed the governance boundary."""

    receipt_id: str
    transformation_id: str
    binding_id: str
    tenant_id: str
    run_ref: str
    state: ExecutionReceiptState
    policy_refs: tuple[str, ...]
    approval_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    output_refs: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for value, name in (
            (self.receipt_id, "receipt_id"), (self.transformation_id, "transformation_id"),
            (self.binding_id, "binding_id"), (self.tenant_id, "tenant_id"), (self.run_ref, "run_ref"),
        ):
            required(value, name)
        for name in ("receipt_id", "transformation_id", "binding_id", "tenant_id", "run_ref"):
            object.__setattr__(self, name, required(getattr(self, name), name))
        object.__setattr__(self, "state", enum_required(self.state, ExecutionReceiptState, "state"))
        object.__setattr__(self, "policy_refs", unique_ids(self.policy_refs, "policy_ref"))
        if not self.policy_refs:
            raise ValueError("execution receipt requires policy references")
        for name in ("approval_refs", "evidence_refs", "output_refs", "limitations"):
            object.__setattr__(self, name, unique_ids(getattr(self, name), name))
        if self.state in {
            ExecutionReceiptState.SUCCEEDED, ExecutionReceiptState.FAILED,
            ExecutionReceiptState.CANCELLED, ExecutionReceiptState.PARTIAL,
        } and not self.evidence_refs:
            raise ValueError("terminal execution receipt requires evidence references")
