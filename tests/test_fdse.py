from uuid import uuid4
import pytest
from fdse import FindingStatus, FdseService, RepositoryRef, VerificationStatus
from fdse.evidence import digest
from fdse.store import MemoryEvidenceStore, MemoryFindingStore, MemoryProjectStore, MemoryVerificationStore
from fdse.policy import DenyByDefaultPolicy

def service(policy=None):
    return FdseService(MemoryProjectStore(),MemoryFindingStore(),MemoryEvidenceStore(),MemoryVerificationStore(),policy)

def test_project_and_finding_are_tenant_scoped():
    tenant,other=uuid4(),uuid4(); app=service()
    project=app.create_project(tenant,"demo",RepositoryRef("github","LloydCoder","example","abc123"))
    evidence=app.record_evidence("test","fixture",{"x":1},"unit-test")
    finding=app.record_finding(tenant,project.project_id,"Unsafe sink","injection","high",(evidence.evidence_id,))
    assert finding.status is FindingStatus.OPEN
    with pytest.raises(PermissionError): app.record_finding(other,project.project_id,"x","y","low")

def test_evidence_digest_is_deterministic():
    assert digest({"b":2,"a":1}) == digest({"a":1,"b":2})

def test_verification_requires_external_authority():
    tenant=uuid4(); app=service(); project=app.create_project(tenant,"demo",RepositoryRef("github","o","r","rev"))
    finding=app.record_finding(tenant,project.project_id,"x","security","high")
    with pytest.raises(PermissionError): app.verify_finding(tenant,finding.finding_id,VerificationStatus.PASSED,("tests passed",))

def test_authorized_verification_is_recorded():
    tenant=uuid4(); policy=DenyByDefaultPolicy({(tenant,"verify_remediation","high")}); app=service(policy)
    project=app.create_project(tenant,"demo",RepositoryRef("github","o","r","rev"))
    finding=app.record_finding(tenant,project.project_id,"x","security","high")
    result=app.verify_finding(tenant,finding.finding_id,VerificationStatus.PASSED,("tests passed",))
    assert result.status is VerificationStatus.PASSED
