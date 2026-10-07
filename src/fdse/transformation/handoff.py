# fmt: off
# ruff: noqa: E501, I001
# ruff: noqa: E501, I001
"""Customer ownership handoff semantics."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ._common import required

# fmt: off
class OwnershipTransferStatus(StrEnum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    TRANSFERRED = "TRANSFERRED"
@dataclass(frozen=True, slots=True)
class Handoff:
    handoff_id: str
    transformation_id: str
    tenant_id: str
    technical_owner: str
    operational_owner: str
    delivered_artifacts: tuple[str, ...]
    training: tuple[str, ...]
    runbooks: tuple[str, ...]
    escalation: tuple[str, ...]
    rollback: tuple[str, ...]
    acceptance: str
    ownership_status: OwnershipTransferStatus
    def __post_init__(self) -> None:
        for value, name in ((self.handoff_id, "handoff_id"), (self.transformation_id, "transformation_id"), (self.tenant_id, "tenant_id"), (self.technical_owner, "technical_owner"), (self.operational_owner, "operational_owner"), (self.acceptance, "acceptance")):
            required(value, name)
        for name in ("handoff_id", "transformation_id", "tenant_id", "technical_owner", "operational_owner", "acceptance"):
            object.__setattr__(self, name, required(getattr(self, name), name))
        for name in ("delivered_artifacts", "training", "runbooks", "escalation", "rollback"):
            object.__setattr__(self, name, tuple(required(v, name) for v in getattr(self, name)))
        if not self.delivered_artifacts or not self.runbooks or not self.rollback:
            raise ValueError("handoff requires artifacts, runbooks, and rollback")
