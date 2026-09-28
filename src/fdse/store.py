"""Deterministic in-memory adapters for tests."""
from __future__ import annotations

from uuid import UUID

from .domain import Evidence, Finding, Project, VerificationResult


class MemoryProjectStore:
    def __init__(self) -> None:
        self._items: dict[UUID, Project] = {}

    def save(self, project: Project) -> None:
        self._items[project.project_id] = project

    def get(self, project_id: UUID) -> Project | None:
        return self._items.get(project_id)


class MemoryFindingStore:
    def __init__(self) -> None:
        self._items: dict[UUID, Finding] = {}

    def save(self, finding: Finding) -> None:
        self._items[finding.finding_id] = finding

    def get(self, finding_id: UUID) -> Finding | None:
        return self._items.get(finding_id)


class MemoryEvidenceStore:
    def __init__(self) -> None:
        self._items: dict[UUID, Evidence] = {}

    def save(self, evidence: Evidence) -> None:
        self._items[evidence.evidence_id] = evidence

    def get(self, evidence_id: UUID) -> Evidence | None:
        return self._items.get(evidence_id)


class MemoryVerificationStore:
    def __init__(self) -> None:
        self._items: dict[UUID, list[VerificationResult]] = {}

    def save(self, result: VerificationResult) -> None:
        self._items.setdefault(result.finding_id, []).append(result)

    def get_for_finding(self, finding_id: UUID) -> tuple[VerificationResult, ...]:
        return tuple(self._items.get(finding_id, ()))
