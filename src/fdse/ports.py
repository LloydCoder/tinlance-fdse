"""Dependency-inversion ports owned by FDSE and implemented by adapters."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from .domain import Evidence, Finding, Project, VerificationResult


class ProjectStore(Protocol):
    def save(self, project: Project) -> None: ...

    def get(self, project_id: UUID) -> Project | None: ...


class FindingStore(Protocol):
    def save(self, finding: Finding) -> None: ...

    def get(self, finding_id: UUID) -> Finding | None: ...


class EvidenceStore(Protocol):
    def save(self, evidence: Evidence) -> None: ...

    def get(self, evidence_id: UUID) -> Evidence | None: ...


class VerificationStore(Protocol):
    def save(self, result: VerificationResult) -> None: ...

    def get_for_finding(self, finding_id: UUID) -> tuple[VerificationResult, ...]: ...


@dataclass(frozen=True, slots=True)
class AgentExecutionRequest:
    tenant_id: UUID
    project_id: UUID
    repository_revision: str
    role: str
    objective: str
    risk_level: str
    required_approval: bool = True


@dataclass(frozen=True, slots=True)
class AgentExecutionResult:
    execution_id: UUID
    status: str
    evidence_ids: tuple[UUID, ...]


class GovernedExecutor(Protocol):
    def execute(self, request: AgentExecutionRequest) -> AgentExecutionResult: ...


class RepositoryProvider(Protocol):
    def validate_revision(self, project: Project) -> bool: ...

    def create_change_request(
        self,
        project: Project,
        title: str,
        body: str,
    ) -> str: ...


class PolicyGateway(Protocol):
    def authorize(
        self,
        tenant_id: UUID,
        action: str,
        risk_level: str,
    ) -> bool: ...
