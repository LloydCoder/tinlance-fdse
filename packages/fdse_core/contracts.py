"""Ports to the generic Tinlance Agent Platform and external engineering systems."""

from dataclasses import dataclass
from typing import Protocol, Sequence


@dataclass(frozen=True, slots=True)
class ExecutionRequest:
    """Domain request; the platform assigns identity, policy and execution authority."""

    tenant_id: str
    project_id: str
    workflow_id: str
    task: str
    risk_tier: str
    requested_capabilities: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ExecutionHandle:
    execution_id: str
    trajectory_ref: str


class AgentPlatformPort(Protocol):
    """Minimal FDSE-to-Agent-Platform boundary.

    Implementations must delegate authorization, policy, approvals, sandboxing,
    budgets and evidence/trajectory recording to Agent Platform rather than
    recreating those controls inside FDSE.
    """

    def submit(self, request: ExecutionRequest) -> ExecutionHandle: ...


class EvidencePort(Protocol):
    def record(self, tenant_id: str, evidence: object) -> str: ...


class GitProviderPort(Protocol):
    def repository_metadata(self, repository: str) -> object: ...

    def read_file(self, repository: str, path: str, ref: str) -> str: ...

    def create_branch(self, repository: str, branch: str, base_ref: str) -> str: ...

    def create_change(self, repository: str, branch: str, changes: Sequence[object]) -> str: ...
