from datetime import datetime, timezone

import pytest

from fdse_core.domain import Assessment, Evidence, Finding, FindingStatus, Project, Repository, Severity, Tenant


def test_core_domain_objects_preserve_tenant_and_traceability() -> None:
    tenant = Tenant(id="t-1", name="Example")
    project = Project(id="p-1", tenant_id=tenant.id, name="Payments")
    repository = Repository(
        id="r-1",
        project_id=project.id,
        provider="github",
        canonical_url="https://github.com/example/payments",
        default_branch="main",
    )
    assessment = Assessment(
        id="a-1",
        project_id=project.id,
        repository_id=repository.id,
        created_at=datetime.now(timezone.utc),
        objective="Assess reliability and security",
    )
    finding = Finding(
        id="f-1",
        assessment_id=assessment.id,
        title="Missing authorization check",
        severity=Severity.HIGH,
        confidence=0.95,
        source_refs=("e-1",),
    )
    evidence = Evidence(
        id="e-1",
        tenant_id=tenant.id,
        assessment_id=assessment.id,
        kind="source_location",
        digest="sha256:example",
        source_ref="src/auth.py:42",
        captured_at=assessment.created_at,
    )

    assert project.tenant_id == tenant.id
    assert repository.project_id == project.id
    assert assessment.repository_id == repository.id
    assert finding.assessment_id == assessment.id
    assert evidence.tenant_id == tenant.id
    assert finding.status is FindingStatus.OPEN


def test_finding_confidence_is_bounded() -> None:
    with pytest.raises(ValueError, match="confidence"):
        Finding(
            id="f-1",
            assessment_id="a-1",
            title="Invalid",
            severity=Severity.MEDIUM,
            confidence=1.1,
        )
