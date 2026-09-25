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
    """Request for Agent Platform governance and, if authorized, execution.

    approval_required is a governance requirement, not proof that approval
    has been granted. FDSE never creates or attests to approval evidence.
    """

    task: EngineeringTask
    workspace_id: str
    approval_required: bool = True


@dataclass(frozen=True, slots=True)
class ExecutionHandle:
    """Opaque reference to an Agent Platform execution lifecycle.

    submit is a boundary operation. M0 does not define polling, lifecycle
    queries, evidence retrieval, cancellation, or execution control APIs.
    """

    execution_id: str
    status: Literal["accepted", "rejected", "completed", "failed", "cancelled"]


class AgentPlatformGateway(Protocol):
    """Minimal FDSE integration boundary.

    FDSE owns engineering semantics. The Agent Platform owns identity,
    authorization, policy, approvals, sandboxing, execution, budgets,
    evidence, trajectory, observability, and audit primitives.
    """

    def submit(self, request: ExecutionRequest) -> ExecutionHandle:
        """Submit a domain request for platform governance and execution.

        A returned handle identifies the platform-owned lifecycle. FDSE must
        not interpret approval_required=True as approval having occurred.
        Lifecycle queries and control operations are deferred beyond M0.
        """
        ...
