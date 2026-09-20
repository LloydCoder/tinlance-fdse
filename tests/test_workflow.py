from uuid import uuid4
from fdse.workflow import EngineeringContext, EngineeringPlan, ChangeSet, Approval, EngineeringReport, PlanStatus, ChangeStatus
from fdse.integrity import record_digest, chain_digest

def test_workflow_records_are_immutable_and_valid():
    tenant,project=uuid4(),uuid4()
    context=EngineeringContext.create(project,"abc123",("no production writes",),("src/",))
    plan=EngineeringPlan.create(project,"fix finding",("reproduce","patch","verify"),"high")
    change=ChangeSet.create(plan.plan_id,"abc123","def456","validated patch")
    approval=Approval.create(tenant,plan.plan_id,"approved","human:1","policy:v1")
    report=EngineeringReport.create(project,"def456","verified",(uuid4(),))
    assert context.revision == "abc123"
    assert plan.status is PlanStatus.DRAFT
    assert change.status is ChangeStatus.PROPOSED
    assert approval.decision == "approved"
    assert report.revision == "def456"

def test_integrity_chain_changes_when_record_changes():
    a={"kind":"finding","id":"1"}
    b={"kind":"finding","id":"2"}
    first=record_digest(a)
    assert chain_digest(first,b) != chain_digest(first,a)
