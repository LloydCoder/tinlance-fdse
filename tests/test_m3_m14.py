from datetime import UTC, datetime
from uuid import uuid4

import pytest

from fdse.agents import SpecialistRegistry, SpecialistRole, SpecialistSpec
from fdse.certification import (
    CertificationBundle,
    CertificationStatus,
    CertificationValidator,
)
from fdse.context import (
    ContextBuilder,
    ContextItem,
    ContextKind,
    ContextQuality,
    ContextSource,
    ContextStore,
    filter_secret_like,
)
from fdse.evaluation import (
    EvaluationCase,
    EvaluationOutcome,
    EvaluationResult,
    EvaluationSuite,
)
from fdse.evidence import digest
from fdse.evidence_graph import (
    EvidenceEdge,
    EvidenceGraph,
    EvidenceNode,
    EvidenceRelation,
)
from fdse.git_ci import CheckResult, RepositorySnapshot
from fdse.governance import (
    ApprovalStatus,
    GovernanceBoundary,
    GovernanceReference,
)
from fdse.platform import PlatformCapabilities, PlatformCompatibility
from fdse.product import TenantBoundary
from fdse.production import HealthStatus, IdempotencyRecord, Readiness, ReadinessGate
from fdse.security_hardening import redact
from fdse.workflows import WorkflowInstance, WorkflowState


def source() -> ContextSource:
    return ContextSource(
        "git",
        "abc",
        "repository",
        datetime.now(UTC),
        "tenant/repo",
        0,
        ContextQuality.HIGH,
    )


def test_m3_snapshot_is_deterministic_and_scoped() -> None:
    first = ContextItem(ContextKind.REPOSITORY, "language", "python", source())
    second = ContextItem(ContextKind.TEST, "runner", "pytest", source())
    one = ContextBuilder().build("t", "r", "abc", (second, first))
    two = ContextBuilder().build("t", "r", "abc", (first, second))
    assert one.snapshot_digest == two.snapshot_digest
    store = ContextStore()
    store.put(one)
    assert store.get("t", "r", "abc") == one


def test_m3_secret_filter() -> None:
    assert filter_secret_like("token=abc") == "[REDACTED]"


def test_m4_requires_platform_authority_capabilities() -> None:
    PlatformCompatibility().validate(
        PlatformCapabilities("1.0", True, True, True, True, True)
    )
    with pytest.raises(ValueError):
        PlatformCompatibility().validate(
            PlatformCapabilities("1.0", True, False, True, True, True)
        )


def test_m5_registry_rejects_duplicates() -> None:
    spec = SpecialistSpec(
        SpecialistRole.TEST,
        "test changes",
        True,
        ("test-result",),
    )
    SpecialistRegistry((spec,)).get(SpecialistRole.TEST)
    with pytest.raises(ValueError):
        SpecialistRegistry((spec, spec))


def test_m6_invalid_workflow_transition() -> None:
    workflow = WorkflowInstance("w", "t", "r", "abc")
    assert workflow.advance(WorkflowState.CONTEXT).state is WorkflowState.CONTEXT
    with pytest.raises(ValueError):
        workflow.advance(WorkflowState.EXECUTION)


def test_m7_revision_bound_contracts() -> None:
    assert RepositorySnapshot("t", "github", "r", "abc", "main").revision == "abc"
    assert CheckResult("t", "ci", "completed", "success", "abc").revision == "abc"


def test_m8_graph_is_integrity_digestable() -> None:
    first = EvidenceNode(uuid4(), "t", "r", "test", "abc", "d1", "ci")
    second = EvidenceNode(uuid4(), "t", "r", "report", "abc", "d2", "report")
    graph = EvidenceGraph()
    graph.add_node(first)
    graph.add_node(second)
    graph.add_edge(
        EvidenceEdge(first.evidence_id, second.evidence_id, EvidenceRelation.SUPPORTS)
    )
    assert len(graph.snapshot_digest()) == 64


def test_m9_authority_is_external() -> None:
    reference = GovernanceReference("a", "p", ApprovalStatus.APPROVED)
    GovernanceBoundary().validate(reference)
    with pytest.raises(ValueError):
        GovernanceReference("a", "p", ApprovalStatus.APPROVED, "fdse")


def test_m10_evaluation_is_fail_closed() -> None:
    case = EvaluationCase("1", "objective", "abc", ("invariant",))
    assert EvaluationSuite().evaluate((case,), ()) is EvaluationOutcome.UNKNOWN
    result = EvaluationResult("1", EvaluationOutcome.PASS, ("ok",), "abc")
    assert EvaluationSuite().evaluate((case,), (result,)) is EvaluationOutcome.PASS


def test_m11_tenant_boundary() -> None:
    TenantBoundary().ensure("t", "t")
    with pytest.raises(PermissionError):
        TenantBoundary().ensure("t", "other")


def test_m12_redacts_secrets() -> None:
    assert "secret=[REDACTED]" in redact("secret=abc")


def test_m13_readiness_contracts() -> None:
    assert HealthStatus("fdse", Readiness.READY, "ok").readiness is Readiness.READY
    assert IdempotencyRecord("t", "k", "d").tenant_id == "t"


def test_m14_certification_fail_closed_and_certified() -> None:
    phases = tuple(
        (f"M{i}", CertificationStatus.CERTIFIED)
        for i in range(15)
    )
    evidence = digest(sorted(phases))
    bundle = CertificationBundle("abc", phases, evidence, "att-1", "github", "run-1", "abc")
    assert CertificationValidator().validate(bundle) is CertificationStatus.CERTIFIED
    incomplete = CertificationBundle("abc", phases[:-1], evidence, "att-1", "github", "run-1", "abc")
    assert CertificationValidator().validate(incomplete) is CertificationStatus.UNKNOWN
