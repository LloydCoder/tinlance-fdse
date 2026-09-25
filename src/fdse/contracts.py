"""Explicit contracts between FDSE and the private Agent Platform."""

from dataclasses import dataclass
from typing import Literal, Protocol

ExecutionRisk = Literal["low", "medium", "high", "critical"]


@dataclass(frozen=True, slots=True)
class EngineeringTask:
    """An engineering intent; it contains no executable command or host credential."""

    task_id: str
    tenant_id: str
    repository_id: str
    description: str
    risk: ExecutionRisk


@dataclass(frozen=True, slots=True)
class ExecutionRequest:
    """Request handed to the Agent Platform authority for governed execution."""

    task: EngineeringTask
    workspace_id: str
    approval_required: bool = True


@dataclass(frozen=True, slots=True)
class ExecutionHandle:
    """Opaque reference to an Agent Platform execution."""

    execution_id: str
    status: Literal["accepted", "rejected", "completed", "failed", "cancelled"]


class AgentPlatformGateway(Protocol):
    """Minimal FDSE integration boundary.

    FDSE owns engineering semantics. The Agent Platform owns identity,
    authorization, policy, approvals, sandboxing, execution, budgets,
    evidence, trajectory, observability, and audit primitives.
    """

    def submit(self, request: ExecutionRequest) -> ExecutionHandle:
        """Submit an already-authorized domain request to the platform."""
        ...
