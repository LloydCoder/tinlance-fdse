# fmt: off
# ruff: noqa: E501, I001
# ruff: noqa: E501, I001
"""Operational process semantics."""
from __future__ import annotations

from dataclasses import dataclass
import math

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
        step_ids = unique_ids(tuple(step.step_id for step in self.steps), "step_id")
        step_id_set = set(step_ids)
        for step in self.steps:
            for dependency in step.dependencies:
                if dependency.startswith("external:"):
                    required(dependency.removeprefix("external:"), "external dependency")
                elif dependency not in step_id_set:
                    raise ValueError(f"unknown process dependency: {dependency}")
        object.__setattr__(self, "actors", tuple(required(v, "actor") for v in self.actors))
        object.__setattr__(self, "systems", tuple(required(v, "system") for v in self.systems))
        object.__setattr__(self, "boundaries", tuple(required(v, "boundary") for v in self.boundaries))
        if self.volume is not None and (not math.isfinite(float(self.volume)) or self.volume < 0):
            raise ValueError("process volume must be finite and non-negative")
        graph = {step.step_id: tuple(d for d in step.dependencies if not d.startswith("external:")) for step in self.steps}
        visiting: set[str] = set()
        visited: set[str] = set()
        def visit(step_id: str) -> None:
            if step_id in visiting:
                raise ValueError("process dependencies contain a cycle")
            if step_id in visited:
                return
            visiting.add(step_id)
            for dependency in graph[step_id]:
                visit(dependency)
            visiting.remove(step_id)
            visited.add(step_id)
        for step_id in graph:
            visit(step_id)
        if self.frequency is not None:
            object.__setattr__(self, "frequency", required(self.frequency, "frequency"))
        object.__setattr__(self, "evidence_ids", unique_ids(self.evidence_ids, "evidence_id"))
