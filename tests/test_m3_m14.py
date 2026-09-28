from uuid import uuid4
from datetime import UTC, datetime
import pytest

from fdse.context import ContextBuilder, ContextItem, ContextKind, ContextQuality, ContextSource, ContextStore, filter_secret_like
from fdse.platform import AgentPlatformAdapter, PlatformCapabilities, PlatformCompatibility, PlatformIntent
from fdse.agents import SpecialistRegistry, SpecialistRole, SpecialistSpec
from fdse.workflows import WorkflowInstance, WorkflowState
from fdse.git_ci import CheckResult, RepositorySnapshot
from fdse.evidence_graph import EvidenceEdge, EvidenceGraph, EvidenceNode, EvidenceRelation
from fdse.governance import ApprovalStatus, GovernanceBoundary, GovernanceReference
from fdse.evaluation import EvaluationCase, EvaluationOutcome, EvaluationResult, EvaluationSuite
from fdse.product import TenantBoundary
from fdse.security_hardening import redact
from fdse.production import HealthStatus, IdempotencyRecord, Readiness
from fdse.certification import CertificationBundle, CertificationStatus, CertificationValidator
from fdse.evidence import digest

def source()->ContextSource:
    return ContextSource("git","abc","repository",datetime.now(UTC),"tenant/repo",0,ContextQuality.HIGH)

def test_m3_snapshot_is_deterministic_and_scoped():
    a=ContextItem(ContextKind.REPOSITORY,"language","python",source())
    b=ContextItem(ContextKind.TEST,"runner","pytest",source())
    one=ContextBuilder().build("t","r","abc",(b,a))
    two=ContextBuilder().build("t","r","abc",(a,b))
    assert one.snapshot_digest==two.snapshot_digest
    store=ContextStore(); store.put(one)
    assert store.get("t","r","abc")==one

def test_m3_secret_filter():
    assert filter_secret_like("token=abc")=="[REDACTED]"

def test_m4_requires_platform_authority_capabilities():
    PlatformCompatibility().validate(PlatformCapabilities("1.0",True,True,True,True,True))
    with pytest.raises(ValueError): PlatformCompatibility().validate(PlatformCapabilities("1.0",True,False,True,True,True))

def test_m5_registry_rejects_duplicates():
    spec=SpecialistSpec(SpecialistRole.TEST,"test changes",True,("test-result",))
    SpecialistRegistry((spec,)).get(SpecialistRole.TEST)
    with pytest.raises(ValueError): SpecialistRegistry((spec,spec))

def test_m6_invalid_workflow_transition():
    w=WorkflowInstance("w","t","r","abc")
    assert w.advance(WorkflowState.CONTEXT).state is WorkflowState.CONTEXT
    with pytest.raises(ValueError): w.advance(WorkflowState.EXECUTION)

def test_m7_revision_bound_contracts():
    assert RepositorySnapshot("github","r","abc","main").revision=="abc"
    assert CheckResult("ci","completed","success","abc").revision=="abc"

def test_m8_graph_is_integrity_digestable():
    a=EvidenceNode(uuid4(),"test","abc","d1","ci"); b=EvidenceNode(uuid4(),"report","abc","d2","report")
    g=EvidenceGraph(); g.add_node(a); g.add_node(b); g.add_edge(EvidenceEdge(a.evidence_id,b.evidence_id,EvidenceRelation.SUPPORTS))
    assert len(g.snapshot_digest())==64

def test_m9_authority_is_external():
    ref=GovernanceReference("a","p",ApprovalStatus.APPROVED)
    GovernanceBoundary().validate(ref)
    with pytest.raises(ValueError): GovernanceReference("a","p",ApprovalStatus.APPROVED,"fdse")

def test_m10_evaluation_is_fail_closed():
    case=EvaluationCase("1","objective",("invariant",))
    assert EvaluationSuite().evaluate((case,),()) is EvaluationOutcome.UNKNOWN
    result=EvaluationResult("1",EvaluationOutcome.PASS,("ok",),"abc")
    assert EvaluationSuite().evaluate((case,),(result,)) is EvaluationOutcome.PASS

def test_m11_tenant_boundary():
    TenantBoundary().ensure("t","t")
    with pytest.raises(PermissionError): TenantBoundary().ensure("t","other")

def test_m12_redacts_secrets():
    assert "secret=[REDACTED]" in redact("secret=abc")

def test_m13_readiness_contracts():
    assert HealthStatus("fdse",Readiness.READY,"ok").readiness is Readiness.READY
    assert IdempotencyRecord("t","k","d").tenant_id=="t"

def test_m14_certification_fail_closed_and_certified():
    phases=tuple((f"M{i}",CertificationStatus.CERTIFIED) for i in range(15))
    evidence=digest(sorted(phases))
    bundle=CertificationBundle("abc",phases,evidence)
    assert CertificationValidator().validate(bundle) is CertificationStatus.CERTIFIED
    incomplete=CertificationBundle("abc",phases[:-1],evidence)
    assert CertificationValidator().validate(incomplete) is CertificationStatus.UNKNOWN
