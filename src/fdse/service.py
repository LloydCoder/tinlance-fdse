"""M0 domain service: validate engineering intent before platform submission."""

from .contracts import AgentPlatformGateway, ExecutionHandle, ExecutionRequest
from .errors import BoundaryViolation, ContractViolation
from .security import validate_workspace_relative_path

_ALLOWED_RISKS = {"low", "medium", "high", "critical"}
_ALLOWED_STATUSES = {"accepted", "rejected", "completed", "failed", "cancelled"}


class EngineeringService:
    def __init__(self, gateway: AgentPlatformGateway) -> None:
        self._gateway = gateway

    def submit(self, request: ExecutionRequest) -> ExecutionHandle:
        if not request.approval_required:
            raise BoundaryViolation("consequential execution requires approval gating")
        task = request.task
        if not task.task_id.strip():
            raise BoundaryViolation("task_id is required")
        if not task.scope.tenant_id.strip() or not task.scope.repository_id.strip():
            raise BoundaryViolation("tenant/repository scope is required")
        if not task.description.strip():
            raise BoundaryViolation("task description is required")
        if task.risk not in _ALLOWED_RISKS:
            raise BoundaryViolation("task risk is invalid")
        validate_workspace_relative_path(request.workspace_id)
        result = self._gateway.submit(request)
        if not result.execution_id.strip():
            raise ContractViolation("Agent Platform returned an empty execution_id")
        if result.status not in _ALLOWED_STATUSES:
            raise ContractViolation("Agent Platform returned an unsupported status")
        return result


def make_request(task, workspace_id: str) -> ExecutionRequest:
    if not workspace_id.strip():
        raise BoundaryViolation("workspace_id is required")
    validate_workspace_relative_path(workspace_id)
    return ExecutionRequest(task=task, workspace_id=workspace_id)
