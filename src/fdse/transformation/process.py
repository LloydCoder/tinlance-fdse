# fmt: off
# ruff: noqa: E501, I001
# ruff: noqa: E501, I001
"""Operational process semantics."""
from __future__ import annotations

from dataclasses import dataclass

from ._common import required, unique_ids

# fmt: off
@dataclass(frozen=True, slots=True)
class ProcessStep:
    step_id: str
    name: str
    actor: str
    system: str
    dependencies: tuple[str, ...] = ()
    exception_classes: tuple[str, ...] = ()
    def __post_init__(self) -> None:
        object.__setattr__(self, "step_id", required(self.step_id, "step_id"))
        object.__setattr__(self, "name", required(self.name, "step name"))
        object.__setattr__(self, "actor", required(self.actor, "step actor"))
        object.__setattr__(self, "system", required(self.system, "step system"))
        object.__setattr__(self, "dependencies", unique_ids(self.dependencies, "dependency"))
        object.__setattr__(self, "exception_classes", tuple(required(v, "exception class") for v in self.exception_classes))

@dataclass(frozen=True, slots=True)
class Process:
    process_id: str
    tenant_id: str
    revision: str
    version: str
    purpose: str
    steps: tuple[ProcessStep, ...]
    actors: tuple[str, ...] = ()
    systems: tuple[str, ...] = ()
    boundaries: tuple[str, ...] = ()
    volume: float | int | None = None
    frequency: str | None = None
    evidence_ids: tuple[str, ...] = ()
    def __post_init__(self) -> None:
        for value, name in ((self.process_id, "process_id"), (self.tenant_id, "tenant_id"), (self.revision, "revision"), (self.version, "version"), (self.purpose, "process purpose")):
            required(value, name)
        object.__setattr__(self, "process_id", required(self.process_id, "process_id"))
        object.__setattr__(self, "tenant_id", required(self.tenant_id, "tenant_id"))
        object.__setattr__(self, "revision", required(self.revision, "revision"))
        object.__setattr__(self, "version", required(self.version, "version"))
        object.__setattr__(self, "purpose", required(self.purpose, "process purpose"))
        if not self.steps:
            raise ValueError("process requires at least one step")
        unique_ids(tuple(step.step_id for step in self.steps), "step_id")
        object.__setattr__(self, "actors", tuple(required(v, "actor") for v in self.actors))
        object.__setattr__(self, "systems", tuple(required(v, "system") for v in self.systems))
        object.__setattr__(self, "boundaries", tuple(required(v, "boundary") for v in self.boundaries))
        if self.volume is not None and self.volume < 0:
            raise ValueError("process volume must be non-negative")
        if self.frequency is not None:
            object.__setattr__(self, "frequency", required(self.frequency, "frequency"))
        object.__setattr__(self, "evidence_ids", unique_ids(self.evidence_ids, "evidence_id"))
