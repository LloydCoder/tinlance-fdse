"""Governance references owned by the Agent Platform (M9)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ApprovalStatus(StrEnum):
    REQUIRED = "required"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


@dataclass(frozen=True, slots=True)
class GovernanceReference:
    approval_id: str
    policy_id: str
    status: ApprovalStatus
    authority: str = "agent-platform"

    def __post_init__(self) -> None:
        if self.authority != "agent-platform":
            raise ValueError("FDSE cannot claim governance authority")
        if not self.approval_id.strip() or not self.policy_id.strip():
            raise ValueError("governance references are required")


class GovernanceBoundary:
    def validate(self, reference: GovernanceReference) -> None:
        if reference.status is ApprovalStatus.APPROVED and reference.authority != "agent-platform":
            raise ValueError("approval authority must remain external")
