# fmt: off
# ruff: noqa: E501
"""Authority-neutral FDSE-to-Agent System transformation binding."""
from __future__ import annotations

from dataclasses import dataclass

from ._common import enum_required, required, unique_ids


@dataclass(frozen=True, slots=True)
class AgentSystemBinding:
    """Correlate business transformation semantics with governed agent execution.

    This object carries references only. It cannot authorize, approve, execute,
    grant capabilities, access secrets, or replace Agent Platform controls.
    """

    binding_id: str
    transformation_id: str
    transformation_version: str
    agent_transformation_id: str
    agent_transformation_version: int
    tenant_id: str
    agent_ref: str
    agent_version: str
    workspace_ref: str
    task_ref: str
    capability_refs: tuple[str, ...]
    execution_ref: str | None = None
    evidence_refs: tuple[str, ...] = ()
    measurement_refs: tuple[str, ...] = ()
    outcome_ref: str | None = None

    def __post_init__(self) -> None:
        for value, name in (
            (self.binding_id, "binding_id"), (self.transformation_id, "transformation_id"),
            (self.transformation_version, "transformation_version"), (self.agent_transformation_id, "agent_transformation_id"),
            (self.tenant_id, "tenant_id"), (self.agent_ref, "agent_ref"), (self.agent_version, "agent_version"),
            (self.workspace_ref, "workspace_ref"), (self.task_ref, "task_ref"),
        ):
            required(value, name)
        for name in (
            "binding_id", "transformation_id", "transformation_version", "agent_transformation_id",
            "tenant_id", "agent_ref", "agent_version", "workspace_ref", "task_ref",
        ):
            object.__setattr__(self, name, required(getattr(self, name), name))
        if isinstance(self.agent_transformation_version, bool) or not isinstance(self.agent_transformation_version, int):
            raise TypeError("agent transformation version must be int")
        if self.agent_transformation_version < 1:
            raise ValueError("agent transformation version must be positive")
        object.__setattr__(self, "capability_refs", unique_ids(self.capability_refs, "capability_ref"))
        if not self.capability_refs:
            raise ValueError("binding requires at least one capability reference")
        if self.execution_ref is not None:
            object.__setattr__(self, "execution_ref", required(self.execution_ref, "execution_ref"))
        object.__setattr__(self, "evidence_refs", unique_ids(self.evidence_refs, "evidence_ref"))
        object.__setattr__(self, "measurement_refs", unique_ids(self.measurement_refs, "measurement_ref"))
        if self.outcome_ref is not None:
            object.__setattr__(self, "outcome_ref", required(self.outcome_ref, "outcome_ref"))
