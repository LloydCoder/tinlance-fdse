import pytest

from fdse.contracts import EvidenceRef, ProvenanceRef, TenantScope, VerificationRef


def test_tenant_scope_is_atomic() -> None:
    scope = TenantScope("tenant-1", "repo-1")
    assert scope.tenant_id == "tenant-1"
    assert scope.repository_id == "repo-1"


@pytest.mark.parametrize("tenant,repo", [("", "repo-1"), ("tenant-1", "")])
def test_tenant_scope_rejects_incomplete_scope(tenant: str, repo: str) -> None:
    with pytest.raises(ValueError):
        TenantScope(tenant, repo)


def test_evidence_provenance_and_verification_are_distinct() -> None:
    provenance = ProvenanceRef("scanner-1", "abc123")
    evidence = EvidenceRef("e-1", "test_result", provenance, "sha256:deadbeef")
    verification = VerificationRef("v-1", evidence.evidence_id, "verified")
    assert evidence.provenance is provenance
    assert verification.evidence_id == evidence.evidence_id
    assert verification.status == "verified"


def test_empty_evidence_identity_is_rejected() -> None:
    with pytest.raises(ValueError):
        EvidenceRef(" ", "artifact", ProvenanceRef("scanner", "rev"), "sha256:x")
