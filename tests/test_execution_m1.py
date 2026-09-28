from dataclasses import replace
from uuid import uuid4

import pytest

from fdse.domain import EngineeringPlan, PlanStatus
from fdse.execution import ExecutionGateway
from fdse.ports import AgentExecutionResult


class FakeExecutor:
    def __init__(self) -> None:
        self.request = None

    def execute(self, request: object) -> AgentExecutionResult:
        self.request = request
        return AgentExecutionResult(uuid4(), "accepted", ())


def test_execution_gateway_requires_explicit_executing_state() -> None:
    executor = FakeExecutor()
    gateway = ExecutionGateway(executor)
    plan = EngineeringPlan.create(
        uuid4(),
        "remediate",
        ("inspect", "patch", "verify"),
        "high",
    )
    with pytest.raises(ValueError):
        gateway.execute_plan(
            uuid4(),
            "abc123",
            plan,
            "remediation-engineer",
        )


def test_execution_gateway_is_approval_gated_and_revision_bound() -> None:
    executor = FakeExecutor()
    gateway = ExecutionGateway(executor)
    plan = EngineeringPlan.create(
        uuid4(),
        "remediate",
        ("inspect", "patch", "verify"),
        "high",
    )
    executing = replace(plan, status=PlanStatus.EXECUTING)
    result = gateway.execute_plan(
        uuid4(),
        "abc123",
        executing,
        "remediation-engineer",
    )
    assert result.status == "accepted"
    assert executor.request.required_approval is True
    assert executor.request.repository_revision == "abc123"
