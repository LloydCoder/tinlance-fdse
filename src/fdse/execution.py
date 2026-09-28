"""Adapter boundary from FDSE plans to Agent Platform authority."""
from __future__ import annotations
from uuid import UUID
from .domain import EngineeringPlan
from .ports import AgentExecutionRequest,AgentExecutionResult,GovernedExecutor
class ExecutionGateway:
    def __init__(self,executor:GovernedExecutor)->None: self._executor=executor
    def execute_plan(self,tenant_id:UUID,project_revision:str,plan:EngineeringPlan,role:str)->AgentExecutionResult:
        if not role.strip(): raise ValueError("role is required")
        if not project_revision.strip(): raise ValueError("project revision is required")
        return self._executor.execute(AgentExecutionRequest(tenant_id,plan.project_id,project_revision,role.strip(),plan.objective,plan.risk_level,True))
