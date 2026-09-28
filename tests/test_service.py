from dataclasses import dataclass

import pytest

from fdse.contracts import EngineeringTask, ExecutionHandle, ExecutionRequest, TenantScope
from fdse.errors import BoundaryViolation, ContractViolation
from fdse.service import EngineeringService, make_request


@dataclass
class FakeGateway:
    calls: list[ExecutionRequest]
    result: ExecutionHandle = ExecutionHandle("exec-1", "accepted")

    def submit(self, request: ExecutionRequest) -> ExecutionHandle:
        self.calls.append(request)
        return self.result


def task() -> EngineeringTask:
    return EngineeringTask(
        task_id="task-1",
        scope=TenantScope("tenant-1", "repo-1"),
        description="inspect repository",
        risk="low",
    )


def test_service_delegates_to_platform_gateway() -> None:
    gateway = FakeGateway([])
    result = EngineeringService(gateway).submit(make_request(task(), "workspace-1"))

    assert result.status == "accepted"
    assert gateway.calls[0].task.repository_id == "repo-1"


def test_consequential_execution_requires_approval() -> None:
    gateway = FakeGateway([])
    request = ExecutionRequest(task=task(), workspace_id="workspace-1", approval_required=False)

    with pytest.raises(BoundaryViolation):
        EngineeringService(gateway).submit(request)

    assert gateway.calls == []


def test_service_rejects_escaping_workspace() -> None:
    gateway = FakeGateway([])
    request = ExecutionRequest(task=task(), workspace_id="../escape")
    with pytest.raises(BoundaryViolation):
        EngineeringService(gateway).submit(request)
    assert gateway.calls == []


def test_blank_identity_is_rejected() -> None:
    with pytest.raises(ValueError):
        TenantScope("  ", "repo-1")


@pytest.mark.parametrize(
    "bad_task",
    [
        EngineeringTask("", TenantScope("tenant-1", "repo-1"), "inspect", "low"),
        EngineeringTask("task-1", TenantScope("tenant-1", "repo-1"), " ", "low"),
        EngineeringTask("task-1", TenantScope("tenant-1", "repo-1"), "inspect", "unknown"),  # type: ignore[arg-type]
    ],
)
def test_invalid_task_contract_is_rejected(bad_task: EngineeringTask) -> None:
    gateway = FakeGateway([])
    with pytest.raises(BoundaryViolation):
        EngineeringService(gateway).submit(
            ExecutionRequest(task=bad_task, workspace_id="workspace-1")
        )


def test_invalid_gateway_handle_is_rejected() -> None:
    gateway = FakeGateway([], ExecutionHandle("", "accepted"))
    with pytest.raises(ContractViolation):
        EngineeringService(gateway).submit(make_request(task(), "workspace-1"))


def test_unsupported_gateway_status_is_rejected() -> None:
    gateway = FakeGateway([], ExecutionHandle("exec-1", "bogus"))  # type: ignore[arg-type]
    with pytest.raises(ContractViolation):
        EngineeringService(gateway).submit(make_request(task(), "workspace-1"))
