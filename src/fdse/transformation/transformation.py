"""Transformation aggregate and target-state contract."""
from __future__ import annotations

from dataclasses import dataclass

from ._common import required, unique_ids
from .classification import Classification
from .process import Process

# fmt: off
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
    def __post_init__(self) -> None:
        object.__setattr__(self, "process_id", required(self.process_id, "process_id"))
        if not self.desired_topology:
            raise ValueError("target state requires desired topology")
        object.__setattr__(self, "desired_topology", tuple(required(v, "topology item") for v in self.desired_topology))
        object.__setattr__(self, "human_responsibilities", tuple(required(v, "human responsibility") for v in self.human_responsibilities))
        object.__setattr__(self, "system_responsibilities", tuple(required(v, "system responsibility") for v in self.system_responsibilities))
        object.__setattr__(self, "integration_requirements", tuple(required(v, "integration requirement") for v in self.integration_requirements))
        object.__setattr__(self, "governance_requirements", tuple(required(v, "governance requirement") for v in self.governance_requirements))
        object.__setattr__(self, "acceptance_criteria", tuple(required(v, "acceptance criterion") for v in self.acceptance_criteria))
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
        for value, name in ((self.transformation_id, "transformation_id"), (self.tenant_id, "tenant_id"), (self.revision, "revision"), (self.version, "version")):
            required(value, name)
        object.__setattr__(self, "transformation_id", required(self.transformation_id, "transformation_id"))
        object.__setattr__(self, "tenant_id", required(self.tenant_id, "tenant_id"))
        object.__setattr__(self, "revision", required(self.revision, "revision"))
        object.__setattr__(self, "version", required(self.version, "version"))
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
