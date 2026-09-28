"""Deterministic specialist-agent role contracts (M5)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SpecialistRole(StrEnum):
    RECON = "recon"
    SECURITY = "security"
    ARCHITECTURE = "architecture"
    TEST = "test"
    DEPENDENCY = "dependency"
    CI = "ci"
    REMEDIATION = "remediation"
    REVIEW = "review"


@dataclass(frozen=True, slots=True)
class SpecialistSpec:
    role: SpecialistRole
    objective: str
    read_only: bool
    required_evidence: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.objective.strip():
            raise ValueError("specialist objective is required")
        if not self.required_evidence or any(
            not evidence.strip() for evidence in self.required_evidence
        ):
            raise ValueError("specialist must declare non-empty evidence requirements")


class SpecialistRegistry:
    def __init__(self, specs: tuple[SpecialistSpec, ...]) -> None:
        roles = [spec.role for spec in specs]
        if len(roles) != len(set(roles)):
            raise ValueError("duplicate specialist role")
        self._specs = {spec.role: spec for spec in specs}

    def get(self, role: SpecialistRole) -> SpecialistSpec:
        try:
            return self._specs[role]
        except KeyError as exc:
            raise ValueError("unknown specialist role") from exc

    def roles(self) -> tuple[SpecialistRole, ...]:
        return tuple(sorted(self._specs, key=lambda role: role.value))
