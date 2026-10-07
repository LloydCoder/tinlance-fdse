# fmt: off
# ruff: noqa: E501
"""Authority-boundary proof contract for FDSE -> Tinlance Agent System."""
from __future__ import annotations

from dataclasses import dataclass

from ._common import required, unique_ids


@dataclass(frozen=True, slots=True)
class AgentPlatformIntegrationProof:
    """A trace-only proof that execution authority remains in Agent Platform."""

    proof_id: str
    fdse_transformation_id: str
    fdse_transformation_version: str
    agent_developer_transformation_id: str
    agent_developer_transformation_version: int
    agent_os_workspace_ref: str
    agent_os_task_ref: str
    sdk_contract_version: str
    platform_run_ref: str
    platform_policy_refs: tuple[str, ...]
    platform_approval_refs: tuple[str, ...]
    execution_receipt_ref: str
    evidence_refs: tuple[str, ...]
    measurement_refs: tuple[str, ...]
    outcome_ref: str
    authority_owner: str = "agent-platform"
    production_verified: bool = False

    def __post_init__(self) -> None:
        for value, name in (
            (self.proof_id, "proof_id"),
            (self.fdse_transformation_id, "fdse_transformation_id"),
            (self.fdse_transformation_version, "fdse_transformation_version"),
            (self.agent_developer_transformation_id, "agent_developer_transformation_id"),
            (self.agent_os_workspace_ref, "agent_os_workspace_ref"),
            (self.agent_os_task_ref, "agent_os_task_ref"),
            (self.sdk_contract_version, "sdk_contract_version"),
            (self.platform_run_ref, "platform_run_ref"),
            (self.execution_receipt_ref, "execution_receipt_ref"),
            (self.outcome_ref, "outcome_ref"),
            (self.authority_owner, "authority_owner"),
        ):
            required(value, name)
        for name in (
            "proof_id",
            "fdse_transformation_id",
            "fdse_transformation_version",
            "agent_developer_transformation_id",
            "agent_os_workspace_ref",
            "agent_os_task_ref",
            "sdk_contract_version",
            "platform_run_ref",
            "execution_receipt_ref",
            "outcome_ref",
            "authority_owner",
        ):
            object.__setattr__(self, name, required(getattr(self, name), name))
        if isinstance(self.agent_developer_transformation_version, bool) or not isinstance(
            self.agent_developer_transformation_version, int
        ):
            raise TypeError("agent developer transformation version must be int")
        if self.agent_developer_transformation_version < 1:
            raise ValueError("agent developer transformation version must be positive")
        if self.authority_owner != "agent-platform":
            raise ValueError("execution authority must remain Agent Platform")
        if not isinstance(self.production_verified, bool):
            raise TypeError("production_verified must be bool")
        object.__setattr__(
            self,
            "platform_policy_refs",
            unique_ids(self.platform_policy_refs, "platform_policy_ref"),
        )
        object.__setattr__(
            self,
            "platform_approval_refs",
            unique_ids(self.platform_approval_refs, "platform_approval_ref"),
        )
        object.__setattr__(
            self,
            "evidence_refs",
            unique_ids(self.evidence_refs, "evidence_ref"),
        )
        object.__setattr__(
            self,
            "measurement_refs",
            unique_ids(self.measurement_refs, "measurement_ref"),
        )
        if not self.platform_policy_refs:
            raise ValueError("integration proof requires Agent Platform policy references")
        if not self.platform_approval_refs:
            raise ValueError("integration proof requires Agent Platform approval references")
        if not self.evidence_refs or not self.measurement_refs:
            raise ValueError("integration proof requires evidence and measurement references")

    def validate(self) -> None:
        """Validate the authority boundary without claiming production health."""
        if self.production_verified:
            raise ValueError(
                "production_verified cannot be self-certified by an FDSE contract"
            )


__all__ = ["AgentPlatformIntegrationProof"]
