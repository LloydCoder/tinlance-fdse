"""Ports for governed execution through the Agent Platform."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


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
