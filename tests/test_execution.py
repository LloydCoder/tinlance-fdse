from uuid import uuid4
from fdse.execution import ExecutionGateway
from fdse.ports import AgentExecutionResult
from fdse.workflow import EngineeringPlan

class FakeExecutor:
    def __init__(self): self.request=None
    def execute(self, request):
        self.request=request
        return AgentExecutionResult(uuid4(),"completed",("ok",),())

def test_execution_gateway_preserves_domain_constraints():
    executor=FakeExecutor()
    gateway=ExecutionGateway(executor)
    plan=EngineeringPlan.create(uuid4(),"remediate finding",("inspect","patch","verify"),"high")
    result=gateway.execute_plan(uuid4(),plan,"remediation-engineer")
    assert result.status == "completed"
    assert executor.request.role == "remediation-engineer"
    assert executor.request.required_approval is True
    assert executor.request.risk_level == "high"
