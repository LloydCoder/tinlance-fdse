import pytest
from fdse.transitions import transition_plan, transition_change
from fdse.workflow import PlanStatus, ChangeStatus

def test_valid_plan_transition():
    assert transition_plan(PlanStatus.DRAFT,PlanStatus.READY) is PlanStatus.READY

def test_invalid_plan_transition_is_rejected():
    with pytest.raises(ValueError):
        transition_plan(PlanStatus.DRAFT,PlanStatus.COMPLETED)

def test_change_requires_verification_after_apply():
    with pytest.raises(ValueError):
        transition_change(ChangeStatus.PROPOSED,ChangeStatus.VERIFIED)
