from datetime import datetime, timezone

import pytest

from fdse_core.contracts import AuthorityContext, ExecutionResult, ExecutionStatus
from fdse_core.domain import (
    Assessment,\n    Evidence,\n    Finding,\n    FindingStatus,\n    Project,\n    Repository,\n    Severity,\n    Tenant,\n)


def test_sha256_digest_is_deterministic() -> None:
    assert sha256_digest(b"evidence") == sha256_digest(b"evidence")
    assert sha256_digest(b"evidence") != sha256_digest(b"tampered")


def test_core_domain_objects_preserve_tenant_and_traceability() -> None:
    tenant = Tenant(id="t-1", name="Example")
    project = Project(id="p-1", tenant_id=tenant.id, name="Payments")
    repository = Repository(
        id="r-1", tenant_id=tenant.id, project_id=project.id,
        provider="github", canonical_url="https://github.com/example/payments", default_branch="main",
    )
    assessment = Assessment(
        id="a-1", tenant_id=tenant.id, project_id=project.id, repository_id=repository.id,
        created_at=datetime.now(timezone.utc), objective="Assess reliability and security",
    )
    finding = Finding(
        id="f-1", tenant_id=tenant.id, assessment_id=assessment.id,
        title="Missing authorization check", severity=Severity.HIGH, confidence=0.95,
        source_refs=("e-1",),
    )
    evidence = Evidence(
        id="e-1", tenant_id=tenant.id, assessment_id=assessment.id, kind="source_location",
        digest="sha256:example", source_ref="src/auth.py:42", captured_at=assessment.created_at,
    )

    assert project.tenant_id == tenant.id
    assert repository.tenant_id == project.tenant_id
    assert assessment.tenant_id == repository.tenant_id
    assert finding.tenant_id == assessment.tenant_id
    assert evidence.tenant_id == finding.tenant_id
    assert finding.status is FindingStatus.OPEN


def test_invalid_domain_state_is_rejected() -> None:
    with pytest.raises(ValueError, match="confidence"):
        Finding("f-1", "t-1", "a-1", "Invalid", Severity.MEDIUM, 1.1)


def test_evidence_digest_is_explicit_integrity_metadata() -> None:
    evidence = Evidence(
        id="e-1", tenant_id="t-1", assessment_id="a-1", kind="test",
        digest="sha256:abc", source_ref="test.log", captured_at=datetime.now(timezone.utc),
    )
    assert evidence.digest.startswith("sha256:")


def test_cross_tenant_ancestry_is_not_silently_equal() -> None:
    project = Project(id="p-1", tenant_id="tenant-a", name="Project")
    repository = Repository(
        id="r-1", tenant_id="tenant-b", project_id=project.id,
        provider="github", canonical_url="https://example.invalid/repo", default_branch="main",
    )
    assert repository.tenant_id != project.tenant_id


def test_missing_authority_context_fails_closed() -> None:
    with pytest.raises(ValueError):
        AuthorityContext("", "actor", "corr", "idem")


def test_malformed_execution_failure_is_rejected() -> None:
    with pytest.raises(ValueError, match="error_code"):
        ExecutionResult("exec-1", ExecutionStatus.FAILED, (), "prov-1")



def test_execution_tenant_mismatch_is_denied() -> None:
    from fdse_core.contracts import ExecutionRequest, validate_tenant_scope

    request = ExecutionRequest(
        authority=AuthorityContext("tenant-a", "actor", "corr", "idem"),
        project_id="p",\n        assessment_id="a",\n        workflow_id="w",\n        task="read",\n        risk_tier="read_only",
    )
    with pytest.raises(PermissionError, match="tenant mismatch"):
        validate_tenant_scope(request, "tenant-b")
