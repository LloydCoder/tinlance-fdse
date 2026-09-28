from uuid import uuid4

import pytest

from fdse.domain import (
    Assessment,
    ChangeSet,
    ChangeStatus,
    EngineeringContext,
    EngineeringPlan,
    EngineeringReport,
    Evidence,
    Finding,
    FindingStatus,
    PlanStatus,
    Project,
    RepositoryRef,
    VerificationResult,
    VerificationStatus,
)
from fdse.evidence import digest
from fdse.integrity import chain_digest, record_digest
from fdse.transitions import transition_change, transition_finding, transition_plan


def repo() -> RepositoryRef:
    return RepositoryRef("github", "owner", "repo", "abc123")


def test_project_assessment_context_are_immutable_and_scoped() -> None:
    project = Project.create(uuid4(), "demo", repo())
    assessment = Assessment.create(project.project_id, "security assessment")
    context = EngineeringContext.create(
        project.project_id,
        "abc123",
        ("no prod writes",),
        ("src/",),
    )
    assert assessment.project_id == project.project_id
    assert context.revision == "abc123"
    with pytest.raises((AttributeError, TypeError)):
        project.name = "changed"  # type: ignore[misc]


def test_evidence_finding_verification_bind_revision() -> None:
    project = Project.create(uuid4(), "demo", repo())
    evidence = Evidence.create(
        project.project_id,
        "test_result",
        "pytest passed",
        "sha256:x",
        "ci",
        "abc123",
    )
    finding = Finding.create(
        project.project_id,
        "unsafe sink",
        "security",
        "high",
        (evidence.evidence_id,),
    )
    verification = VerificationResult.create(
        finding.finding_id,
        VerificationStatus.PASSED,
        ("pytest",),
        (evidence.evidence_id,),
        "abc123",
    )
    assert finding.status is FindingStatus.OPEN
    assert verification.status is VerificationStatus.PASSED
    assert verification.revision == "abc123"


def test_plans_changes_and_reports_have_explicit_lifecycle() -> None:
    project = Project.create(uuid4(), "demo", repo())
    plan = EngineeringPlan.create(
        project.project_id,
        "fix finding",
        ("reproduce", "patch", "verify"),
        "high",
    )
    change = ChangeSet.create(
        plan.plan_id,
        "abc123",
        "def456",
        "validated patch",
    )
    report = EngineeringReport.create(
        project.project_id,
        "def456",
        "verified",
        (uuid4(),),
    )
    assert plan.status is PlanStatus.DRAFT
    assert change.status is ChangeStatus.PROPOSED
    assert report.revision == "def456"


def test_invalid_transitions_are_rejected() -> None:
    with pytest.raises(ValueError):
        transition_plan(PlanStatus.DRAFT, PlanStatus.COMPLETED)
    with pytest.raises(ValueError):
        transition_change(ChangeStatus.PROPOSED, ChangeStatus.VERIFIED)


def test_integrity_and_canonical_evidence_are_deterministic() -> None:
    assert digest({"b": 2, "a": 1}) == digest({"a": 1, "b": 2})
    first = record_digest({"id": "1"})
    assert chain_digest(first, {"id": "2"}) != chain_digest(first, {"id": "1"})


def test_plan_and_finding_lifecycles_include_governance_states() -> None:
    assert transition_plan(PlanStatus.READY, PlanStatus.AWAITING_APPROVAL) is PlanStatus.AWAITING_APPROVAL
    assert transition_plan(
        PlanStatus.AWAITING_APPROVAL,
        PlanStatus.EXECUTING,
    ) is PlanStatus.EXECUTING
    assert transition_finding(FindingStatus.OPEN, FindingStatus.ACCEPTED) is FindingStatus.ACCEPTED
    assert transition_finding(
        FindingStatus.REMEDIATED,
        FindingStatus.VERIFIED,
    ) is FindingStatus.VERIFIED


def test_terminal_finding_transition_is_rejected() -> None:
    with pytest.raises(ValueError):
        transition_finding(FindingStatus.VERIFIED, FindingStatus.OPEN)
