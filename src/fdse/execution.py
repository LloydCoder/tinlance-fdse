"""Adapter boundary from FDSE plans to Agent Platform authority."""

from __future__ import annotations

from uuid import UUID

from .domain import EngineeringPlan, PlanStatus
from .ports import AgentExecutionRequest, AgentExecutionResult, GovernedExecutor


class ExecutionGateway:
    def __init__(self, executor: GovernedExecutor) -> None:
        self._executor = executor

    def execute_plan(
        self,
        tenant_id: UUID,
        project_revision: str,
        plan: EngineeringPlan,
        role: str,
    ) -> AgentExecutionResult:
        if not role.strip():
            raise ValueError("role is required")
        if not project_revision.strip():
            raise ValueError("project revision is required")
        if plan.status is not PlanStatus.EXECUTING:
            raise ValueError("plan must be in EXECUTING state before submission")
        request = AgentExecutionRequest(
            tenant_id=tenant_id,
            project_id=plan.project_id,
            repository_revision=project_revision,
            role=role.strip(),
            objective=plan.objective,
            risk_level=plan.risk_level,
            required_approval=True,
        )
        return self._executor.execute(request)
