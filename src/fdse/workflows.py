"""Explicit workflow state machines (M6)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class WorkflowState(StrEnum):
    INTAKE = "intake"
    CONTEXT = "context"
    ANALYSIS = "analysis"
    PLAN = "plan"
    APPROVAL = "approval"
    EXECUTION = "execution"
    VERIFICATION = "verification"
    REPORT = "report"
    COMPLETED = "completed"
    FAILED = "failed"


_ALLOWED: dict[WorkflowState, frozenset[WorkflowState]] = {
    WorkflowState.INTAKE: frozenset({WorkflowState.CONTEXT, WorkflowState.FAILED}),
    WorkflowState.CONTEXT: frozenset({WorkflowState.ANALYSIS, WorkflowState.FAILED}),
    WorkflowState.ANALYSIS: frozenset({WorkflowState.PLAN, WorkflowState.FAILED}),
    WorkflowState.PLAN: frozenset({WorkflowState.APPROVAL, WorkflowState.FAILED}),
    WorkflowState.APPROVAL: frozenset({WorkflowState.EXECUTION, WorkflowState.FAILED}),
    WorkflowState.EXECUTION: frozenset({WorkflowState.VERIFICATION, WorkflowState.FAILED}),
    WorkflowState.VERIFICATION: frozenset({WorkflowState.REPORT, WorkflowState.FAILED}),
    WorkflowState.REPORT: frozenset({WorkflowState.COMPLETED, WorkflowState.FAILED}),
    WorkflowState.COMPLETED: frozenset(),
    WorkflowState.FAILED: frozenset(),
}


def transition(current: WorkflowState, target: WorkflowState) -> WorkflowState:
    if target not in _ALLOWED[current]:
        raise ValueError(f"invalid workflow transition: {current} -> {target}")
    return target


@dataclass(frozen=True, slots=True)
class WorkflowInstance:
    workflow_id: str
    tenant_id: str
    repository_id: str
    revision: str
    state: WorkflowState = WorkflowState.INTAKE

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.workflow_id,
                self.tenant_id,
                self.repository_id,
                self.revision,
            )
        ):
            raise ValueError("workflow scope and identifier are required")

    def advance(self, target: WorkflowState) -> WorkflowInstance:
        return WorkflowInstance(
            self.workflow_id,
            self.tenant_id,
            self.repository_id,
            self.revision,
            transition(self.state, target),
        )
