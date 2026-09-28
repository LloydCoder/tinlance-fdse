"""Explicit workflow state machines (M6)."""
from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum

class WorkflowState(StrEnum):
    INTAKE="intake"; CONTEXT="context"; ANALYSIS="analysis"; PLAN="plan"
    APPROVAL="approval"; EXECUTION="execution"; VERIFICATION="verification"; REPORT="report"
    COMPLETED="completed"; FAILED="failed"

_ALLOWED={
WorkflowState.INTAKE:{WorkflowState.CONTEXT,WorkflowState.FAILED},
WorkflowState.CONTEXT:{WorkflowState.ANALYSIS,WorkflowState.FAILED},
WorkflowState.ANALYSIS:{WorkflowState.PLAN,WorkflowState.FAILED},
WorkflowState.PLAN:{WorkflowState.APPROVAL,WorkflowState.FAILED},
WorkflowState.APPROVAL:{WorkflowState.EXECUTION,WorkflowState.FAILED},
WorkflowState.EXECUTION:{WorkflowState.VERIFICATION,WorkflowState.FAILED},
WorkflowState.VERIFICATION:{WorkflowState.REPORT,WorkflowState.FAILED},
WorkflowState.REPORT:{WorkflowState.COMPLETED,WorkflowState.FAILED},
WorkflowState.COMPLETED:set(),WorkflowState.FAILED:set(),
}

def transition(current:WorkflowState,target:WorkflowState)->WorkflowState:
    if target not in _ALLOWED[current]: raise ValueError(f"invalid workflow transition: {current} -> {target}")
    return target

@dataclass(frozen=True,slots=True)
class WorkflowInstance:
    workflow_id:str
    tenant_id:str
    repository_id:str
    revision:str
    state:WorkflowState=WorkflowState.INTAKE
    def advance(self,target:WorkflowState)->"WorkflowInstance":
        return WorkflowInstance(self.workflow_id,self.tenant_id,self.repository_id,self.revision,transition(self.state,target))
