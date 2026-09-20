from __future__ import annotations
from uuid import UUID
from .ports import AgentExecutionRequest, AgentExecutionResult, GovernedExecutor
from .workflow import EngineeringPlan

class ExecutionGateway:
    """Maps FDSE engineering plans to the external Agent Platform contract."""

    def __init__(self, executor: GovernedExecutor):
        self.executor = executor

    def execute_plan(self, tenant_id: UUID, plan: EngineeringPlan, role: str) -> AgentExecutionResult:
        request = AgentExecutionRequest(
            tenant_id=tenant_id,
            project_id=plan.project_id,
            role=role,
            objective=plan.objective,
            risk_level=plan.risk_level,
            required_approval=True,
        )
        return self.executor.execute(request)
