from uuid import uuid4
from fdse.domain import EngineeringPlan
from fdse.execution import ExecutionGateway
from fdse.ports import AgentExecutionResult

class FakeExecutor:
    def __init__(self): self.request=None
    def execute(self,request): self.request=request; return AgentExecutionResult(uuid4(),"accepted",())

def test_execution_gateway_is_approval_gated_and_revision_bound():
    executor=FakeExecutor(); gateway=ExecutionGateway(executor); plan=EngineeringPlan.create(uuid4(),"remediate",("inspect","patch","verify"),"high")
    result=gateway.execute_plan(uuid4(),"abc123",plan,"remediation-engineer")
    assert result.status=="accepted" and executor.request.required_approval is True and executor.request.repository_revision=="abc123"
