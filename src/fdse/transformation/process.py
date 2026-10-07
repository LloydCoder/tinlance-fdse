# fmt: off
# ruff: noqa: E501
"""Operational process semantics."""
from __future__ import annotations

from dataclasses import dataclass
import math

from ._common import required, unique_ids


@dataclass(frozen=True, slots=True)
class ProcessStep:
    step_id: str
    name: str
    actor: str
    system: str
    dependencies: tuple[str, ...] = ()
    exception_classes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("step_id", "name", "actor", "system"):
            object.__setattr__(self, name, required(getattr(self, name), f"step {name}" if name != "step_id" else name))
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
        for value, name in (
            (self.process_id, "process_id"), (self.tenant_id, "tenant_id"),
            (self.revision, "revision"), (self.version, "version"), (self.purpose, "process purpose"),
        ):
            required(value, name)
        for name in ("process_id", "tenant_id", "revision", "version", "purpose"):
            object.__setattr__(self, name, required(getattr(self, name), name))
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
        object.__setattr__(self, "actors", unique_ids(self.actors, "actor"))
        object.__setattr__(self, "systems", unique_ids(self.systems, "system"))
        object.__setattr__(self, "boundaries", unique_ids(self.boundaries, "boundary"))
        if self.volume is not None:
            if isinstance(self.volume, bool) or not isinstance(self.volume, (int, float)):
                raise TypeError("process volume must be numeric")
            if not math.isfinite(float(self.volume)) or self.volume < 0:
                raise ValueError("process volume must be finite and non-negative")
            object.__setattr__(self, "volume", float(self.volume))
        if self.frequency is not None:
            object.__setattr__(self, "frequency", required(self.frequency, "frequency"))
        object.__setattr__(self, "evidence_ids", unique_ids(self.evidence_ids, "evidence_id"))
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
