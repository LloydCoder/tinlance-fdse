# fmt: off
"""Authority-neutral engineering realization of a transformation target state."""
from __future__ import annotations

from dataclasses import dataclass

from ._common import required, unique_ids


@dataclass(frozen=True, slots=True)
class EngineeringRealization:
    """Describe how a target state maps to engineering work and verification."""

    realization_id: str
    transformation_id: str
    transformation_version: str
    target_process_id: str
    engineering_owner: str
    requirements: tuple[str, ...]
    repository_refs: tuple[str, ...] = ()
    integration_refs: tuple[str, ...] = ()
    agent_refs: tuple[str, ...] = ()
    evaluation_refs: tuple[str, ...] = ()
    verification_refs: tuple[str, ...] = ()
    acceptance_criteria: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for value, name in (
            (self.realization_id, "realization_id"),
            (self.transformation_id, "transformation_id"),
            (self.transformation_version, "transformation_version"),
            (self.target_process_id, "target_process_id"),
            (self.engineering_owner, "engineering_owner"),
        ):
            required(value, name)

        for name in (
            "realization_id",
            "transformation_id",
            "transformation_version",
            "target_process_id",
            "engineering_owner",
        ):
            object.__setattr__(self, name, required(getattr(self, name), name))

        object.__setattr__(
            self,
            "requirements",
            tuple(required(value, "engineering requirement") for value in self.requirements),
        )
        if not self.requirements:
            raise ValueError("engineering realization requires requirements")

        for name in (
            "repository_refs",
            "integration_refs",
            "agent_refs",
            "evaluation_refs",
            "verification_refs",
            "acceptance_criteria",
        ):
            object.__setattr__(
                self,
                name,
                unique_ids(getattr(self, name), name),
            )

        if not self.acceptance_criteria:
            raise ValueError("engineering realization requires acceptance criteria")


__all__ = ["EngineeringRealization"]
