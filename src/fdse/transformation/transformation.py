# fmt: off
# ruff: noqa: E501
"""Transformation aggregate and target-state contract."""
from __future__ import annotations

from dataclasses import dataclass

from ._common import required, unique_ids
from .classification import Classification
from .process import Process


@dataclass(frozen=True, slots=True)
class TargetState:
    process_id: str
    desired_topology: tuple[str, ...]
    classifications: tuple[Classification, ...]
    human_responsibilities: tuple[str, ...]
    system_responsibilities: tuple[str, ...]
    integration_requirements: tuple[str, ...] = ()
    governance_requirements: tuple[str, ...] = ()
    acceptance_criteria: tuple[str, ...] = ()
    exception_handling: tuple[str, ...] = ()
    human_decision_rights: tuple[str, ...] = ()
    recovery_requirements: tuple[str, ...] = ()
    observability_requirements: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "process_id", required(self.process_id, "process_id"))
        if not self.desired_topology:
            raise ValueError("target state requires desired topology")
        for name in (
            "desired_topology", "human_responsibilities", "system_responsibilities",
            "integration_requirements", "governance_requirements", "acceptance_criteria",
            "exception_handling", "human_decision_rights", "recovery_requirements",
            "observability_requirements",
        ):
            object.__setattr__(self, name, tuple(required(v, name) for v in getattr(self, name)))
        if not self.classifications:
            raise ValueError("target state requires classifications")
        if any(not isinstance(c, Classification) for c in self.classifications):
            raise TypeError("target state classifications must be Classification objects")
        if not self.acceptance_criteria:
            raise ValueError("target state requires acceptance criteria")
        if not self.human_decision_rights:
            raise ValueError("target state requires human decision rights")
        unique_ids(tuple(c.classification_id for c in self.classifications), "classification_id")
        unique_ids(tuple(c.step_id for c in self.classifications), "classification step_id")


@dataclass(frozen=True, slots=True)
class Transformation:
    transformation_id: str
    tenant_id: str
    revision: str
    version: str
    process: Process
    target_state: TargetState

    def __post_init__(self) -> None:
        for value, name in (
            (self.transformation_id, "transformation_id"),
            (self.tenant_id, "tenant_id"),
            (self.revision, "revision"),
            (self.version, "version"),
        ):
            required(value, name)
        for name in ("transformation_id", "tenant_id", "revision", "version"):
            object.__setattr__(self, name, required(getattr(self, name), name))
        if not isinstance(self.process, Process):
            raise TypeError("transformation process must be Process")
        if not isinstance(self.target_state, TargetState):
            raise TypeError("transformation target_state must be TargetState")
        if self.process.tenant_id != self.tenant_id or self.process.revision != self.revision:
            raise ValueError("transformation scope does not match process")
        if self.target_state.process_id != self.process.process_id:
            raise ValueError("target state process_id does not match process")
        process_steps = {step.step_id for step in self.process.steps}
        classifications = self.target_state.classifications
        if {item.step_id for item in classifications} != process_steps:
            raise ValueError("target state must classify every process step exactly once")
        if any(item.tenant_id != self.tenant_id or item.revision != self.revision for item in classifications):
            raise ValueError("classification scope does not match transformation")
