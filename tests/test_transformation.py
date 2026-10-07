# fmt: off
# ruff: noqa: E501, E701, I001
from __future__ import annotations
import pytest
from fdse.contracts import EvidenceRef, ProvenanceRef
from fdse.transformation import (
    AgentSystemBinding,
    EngineeringRealization,
    ExecutionReceiptState, GovernedExecutionReceipt,
    MeasurementDirection, OutcomeAcceptance,
    Action, Baseline, Classification, DecisionBasis, DecisionConfidence, Handoff,
    Measurement, MeasurementMethod, MeasurementStage, MetricObservation, Outcome,
    OwnershipTransferStatus, Process, ProcessStep, ReplicationProfile, Reversibility,
    ReplicationStage, RiskLevel, TargetState, Transformation, TransformationLifecycle, digest_value, serialize,
)
def evidence(eid: str = "ev-1") -> EvidenceRef:
    return EvidenceRef(eid, "observation", ProvenanceRef("source-1", "rev-1"), "digest-1")
def process() -> Process:
    return Process("proc-1","tenant-1","rev-1","v1","invoice processing",(ProcessStep("s1","receive","AP clerk","ERP"),ProcessStep("s2","approve","manager","ERP")),actors=("AP clerk","manager"),systems=("ERP",))
def classifications() -> tuple[Classification, ...]:
    return (Classification("c1","tenant-1","rev-1","s1",Action.CODE,"parse invoice","finance",expected_effect="extract invoice",evidence=(evidence("ev-1"),),decision_basis=DecisionBasis.ANALYSIS,risk_level=RiskLevel.MEDIUM,reversibility=Reversibility.REVERSIBLE,confidence=DecisionConfidence.HIGH),Classification("c2","tenant-1","rev-1","s2",Action.HUMAN,"approve exceptions","finance",expected_effect="approve exception",evidence=(evidence("ev-2"),),decision_basis=DecisionBasis.POLICY,risk_level=RiskLevel.HIGH,reversibility=Reversibility.REVERSIBLE,confidence=DecisionConfidence.HIGH))
def target() -> TargetState:
    return TargetState("proc-1",("receive -> approve",),classifications(),("manager approval",),("invoice extraction",),acceptance_criteria=("cycle time <= target",),human_decision_rights=("manager approves exceptions",))
def test_valid_construction_every_canonical_object() -> None:
    p=process()
    baseline=Baseline("base-1","tenant-1","rev-1","v1",(MetricObservation("cycle_time",12.0,"minutes","2026-Q3","all invoices",MeasurementMethod.OBSERVED,"ERP",evidence()),))
    transformation=Transformation("tr-1","tenant-1","rev-1","v1",p,target())
    measurement=Measurement("m-1","tr-1","tenant-1","rev-1","cycle_time",MeasurementStage.POST_DEPLOYMENT,8.0,"minutes","2026-Q4","ERP",evidence(),12.0,10.0,"lower is better","improved")
    outcome=Outcome("out-1","tr-1","tenant-1","v1","2026-Q4",("m-base",),("m-target",),(("cycle_time",8.0),),(("cycle_time",-4.0),),"accepted",(evidence("ev-3"),))
    replication=ReplicationProfile("rep-1","tr-1","tenant-1","tenant-2",("discovery",),("ERP mapping",),("exception lesson",))
    handoff=Handoff("h-1","tr-1","tenant-1","tech-owner","ops-owner",("runbook.pdf",),("training",),("runbook",),("support",),("rollback",),"accepted",OwnershipTransferStatus.ACCEPTED)
    assert all((baseline,transformation,measurement,outcome,replication,handoff))
def test_classification_taxonomy_is_closed_and_explicit() -> None:
    assert tuple(Action)==(Action.DELETE,Action.CODE,Action.AGENT,Action.HUMAN)
    c=classifications()[0]
    assert c.decision_basis is DecisionBasis.ANALYSIS
    assert c.risk_level is RiskLevel.MEDIUM
    assert c.reversibility is Reversibility.REVERSIBLE
    assert c.confidence is DecisionConfidence.HIGH
def test_classification_taxonomy_requires_evidence() -> None:
    with pytest.raises(ValueError): Classification("c","t","r","s",Action.CODE,"x","owner")
def test_classification_rejects_noncanonical_action() -> None:
    with pytest.raises(ValueError): Classification("c","t","r","s","NOT_AN_ACTION","x","owner",evidence=(evidence(),))
def test_classification_rejects_invalid_decision_basis() -> None:
    with pytest.raises(ValueError): Classification("c","t","r","s",Action.AGENT,"x","owner",evidence=(evidence(),),decision_basis="BAD")
def test_blank_and_nul_rejection() -> None:
    with pytest.raises(ValueError): Process("","tenant-1","rev-1","v1","purpose",(ProcessStep("s1","x","a","sys"),))
    with pytest.raises(ValueError): Process("p","tenant-1","rev-1","v1","bad\x00purpose",(ProcessStep("s1","x","a","sys"),))
def test_scope_revision_and_classification_rejection() -> None:
    p=process()
    with pytest.raises(ValueError): Transformation("tr","tenant-2","rev-1","v1",p,target())
    bad=TargetState("proc-1",("x",),(Classification("c","tenant-1","rev-2","s1",Action.CODE,"x","owner",expected_effect="code",evidence=(evidence(),)),Classification("c2","tenant-1","rev-1","s2",Action.HUMAN,"x","owner",expected_effect="human",evidence=(evidence("ev-2"),))),("human",),("system",),acceptance_criteria=("accepted",),human_decision_rights=("owner",))
    with pytest.raises(ValueError): Transformation("tr","tenant-1","rev-1","v1",p,bad)
    with pytest.raises(ValueError): TargetState("proc-1",("x",),(classifications()[0],classifications()[0]),("human",),("system",),acceptance_criteria=("accepted",),human_decision_rights=("owner",))
def test_deterministic_serialization_and_digest() -> None:
    p=process()
    assert serialize(p)==serialize(p)
    assert digest_value(p)==digest_value(p)
    assert b'"tenant_id":"tenant-1"' in serialize(p)
def test_baseline_evidence_and_identifier_collision() -> None:
    with pytest.raises(ValueError): Baseline("b","t","r","v",(MetricObservation("m",1.0,"count","w","all",MeasurementMethod.OBSERVED,"sys",evidence()),MetricObservation("m",2.0,"count","w","all",MeasurementMethod.OBSERVED,"sys",evidence("e2"))))
def test_measurement_stage_semantics() -> None:
    with pytest.raises(ValueError): Measurement("m","tr","t","r","metric",MeasurementStage.POST_DEPLOYMENT,1.0,"count","w","system")
    baseline=Measurement("b","tr","t","r","metric",MeasurementStage.BASELINE,10.0,"count","w","system",evidence())
    target_m=Measurement("t","tr","t","r","metric",MeasurementStage.TARGET,5.0,"count","w","design")
    assert baseline.baseline_value==10.0 and target_m.target_value==5.0
def test_outcome_and_replication_qualification() -> None:
    with pytest.raises(ValueError): Outcome("o","tr","t","v","period",("b",),("t",),(("m",1.0),),(("m",0.0),),"accepted",())
    with pytest.raises(ValueError): ReplicationProfile("r","tr","source","target",("method",),("mapping",),("lesson",),success_claimed=True)
def test_handoff_acceptance_invariants() -> None:
    with pytest.raises(ValueError): Handoff("h","tr","t","tech","ops",(),("training",),("runbook",),("support",),("rollback",),"accepted",OwnershipTransferStatus.ACCEPTED)


def test_process_rejects_unknown_internal_dependency() -> None:
    with pytest.raises(ValueError):
        Process(
            "proc-dep",
            "tenant-1",
            "rev-1",
            "v1",
            "invoice processing",
            (
                ProcessStep("s1", "receive", "AP clerk", "ERP", dependencies=("missing",)),
            ),
        )


def test_process_allows_explicit_external_dependency() -> None:
    p = Process(
        "proc-ext",
        "tenant-1",
        "rev-1",
        "v1",
        "invoice processing",
        (
            ProcessStep(
                "s1",
                "receive",
                "AP clerk",
                "ERP",
                dependencies=("external:bank-api",),
            ),
        ),
    )
    assert p.steps[0].dependencies == ("external:bank-api",)


def test_baseline_economic_metric_requires_explicit_derivation() -> None:
    with pytest.raises(ValueError):
        MetricObservation(
            "annual_cost",
            1000.0,
            "currency",
            "2026",
            "all invoices",
            MeasurementMethod.CALCULATED,
            "finance model",
            evidence(),
            currency="USD",
        )
    economic = MetricObservation(
        "annual_cost",
        1000.0,
        "currency",
        "2026",
        "all invoices",
        MeasurementMethod.CALCULATED,
        "finance model",
        evidence(),
        currency="USD",
        period="2026",
        assumptions=("loaded labor cost",),
        derivation="hours * loaded hourly cost",
    )
    assert economic.currency == "USD"


def test_baseline_rejects_non_finite_metric() -> None:
    with pytest.raises(ValueError):
        MetricObservation(
            "bad",
            float("inf"),
            "count",
            "2026",
            "all",
            MeasurementMethod.OBSERVED,
            "ERP",
            evidence(),
        )


def test_target_state_requires_acceptance_and_human_decision_rights() -> None:
    cs = classifications()
    with pytest.raises(ValueError):
        TargetState("proc-1", ("receive -> approve",), cs, (), ("invoice extraction",))
    target_state = TargetState(
        "proc-1",
        ("receive -> approve",),
        cs,
        ("manager approval",),
        ("invoice extraction",),
        acceptance_criteria=("cycle time <= target",),
        human_decision_rights=("manager approves exceptions",),
        exception_handling=("route low-confidence invoices to manager",),
        recovery_requirements=("restore previous mapping",),
        observability_requirements=("record extraction confidence",),
    )
    assert target_state.human_decision_rights == ("manager approves exceptions",)


def test_agent_system_binding_is_authority_neutral_and_traceable() -> None:
    binding = AgentSystemBinding(
        "bind-1",
        "tr-1",
        "v1",
        "agent-tr-1",
        1,
        "tenant-1",
        "invoice-agent",
        "2026.10",
        "workspace-1",
        "task-1",
        ("invoice.extract",),
        execution_ref="run-1",
        evidence_refs=("ev-1",),
        measurement_refs=("m-1",),
        outcome_ref="out-1",
    )
    assert binding.execution_ref == "run-1"
    assert binding.capability_refs == ("invoice.extract",)


def test_agent_system_binding_requires_capability_and_valid_version() -> None:
    with pytest.raises(ValueError):
        AgentSystemBinding(
            "bind-1",
            "tr-1",
            "v1",
            "agent-tr-1",
            0,
            "tenant-1",
            "invoice-agent",
            "2026.10",
            "workspace-1",
            "task-1",
            (),
        )


def test_engineering_realization_is_explicit_and_non_executable() -> None:
    realization = EngineeringRealization(
        "real-1",
        "tr-1",
        "v1",
        "proc-1",
        "fdse-engineer",
        ("extract invoice fields", "route exceptions"),
        repository_refs=("repo-invoice",),
        integration_refs=("erp-api",),
        agent_refs=("invoice-agent",),
        evaluation_refs=("eval-invoice",),
        verification_refs=("ci-green",),
        acceptance_criteria=("golden dataset threshold met",),
    )
    assert realization.agent_refs == ("invoice-agent",)


def test_engineering_realization_requires_requirements_and_acceptance() -> None:
    with pytest.raises(ValueError):
        EngineeringRealization(
            "real-1",
            "tr-1",
            "v1",
            "proc-1",
            "fdse-engineer",
            (),
            acceptance_criteria=("accepted",),
        )
    with pytest.raises(ValueError):
        EngineeringRealization(
            "real-1",
            "tr-1",
            "v1",
            "proc-1",
            "fdse-engineer",
            ("requirement",),
        )


def test_governed_execution_receipt_requires_policy_and_terminal_evidence() -> None:
    receipt = GovernedExecutionReceipt(
        "receipt-1",
        "tr-1",
        "bind-1",
        "tenant-1",
        "run-1",
        ExecutionReceiptState.SUCCEEDED,
        ("policy-agent-execution",),
        approval_refs=("approval-1",),
        evidence_refs=("ev-run-1",),
        output_refs=("artifact-1",),
    )
    assert receipt.state is ExecutionReceiptState.SUCCEEDED


def test_governed_execution_receipt_rejects_unevidenced_terminal_state() -> None:
    with pytest.raises(ValueError):
        GovernedExecutionReceipt(
            "receipt-1",
            "tr-1",
            "bind-1",
            "tenant-1",
            "run-1",
            ExecutionReceiptState.SUCCEEDED,
            ("policy-agent-execution",),
        )


def test_measurement_requires_complete_post_deployment_comparison() -> None:
    with pytest.raises(ValueError):
        Measurement(
            "m-incomplete",
            "tr",
            "t",
            "r",
            "metric",
            MeasurementStage.POST_DEPLOYMENT,
            8.0,
            "minutes",
            "2026-Q4",
            "ERP",
            evidence(),
            12.0,
            10.0,
        )
    measurement = Measurement(
        "m-complete",
        "tr",
        "t",
        "r",
        "metric",
        MeasurementStage.POST_DEPLOYMENT,
        8.0,
        "minutes",
        "2026-Q4",
        "ERP",
        evidence(),
        12.0,
        10.0,
        "lower is better",
        "improved",
        direction=MeasurementDirection.LOWER_IS_BETTER,
        acceptance_threshold=10.0,
    )
    assert measurement.direction is MeasurementDirection.LOWER_IS_BETTER


def test_outcome_requires_matching_variance_metrics() -> None:
    with pytest.raises(ValueError):
        Outcome(
            "out-mismatch",
            "tr",
            "t",
            "v",
            "period",
            ("b",),
            ("t",),
            (("cycle_time", 8.0),),
            (("error_rate", -1.0),),
            "accepted",
            (evidence(),),
        )


def test_outcome_acceptance_state_is_canonical() -> None:
    outcome = Outcome(
        "out-state",
        "tr",
        "t",
        "v",
        "period",
        ("b",),
        ("t",),
        (("cycle_time", 8.0),),
        (("cycle_time", -4.0),),
        "accepted",
        (evidence(),),
    )
    assert outcome.acceptance_state is OutcomeAcceptance.ACCEPTED


def test_replication_requires_evidence_and_target_outcome_when_qualified() -> None:
    with pytest.raises(ValueError):
        ReplicationProfile(
            "rep-qualified",
            "tr-1",
            "tenant-1",
            "tenant-2",
            ("discovery",),
            ("ERP mapping",),
            ("lesson",),
            stage=ReplicationStage.ACCEPTED,
            evidence_refs=("ev-rep",),
        )
    qualified = ReplicationProfile(
        "rep-qualified",
        "tr-1",
        "tenant-1",
        "tenant-2",
        ("discovery",),
        ("ERP mapping",),
        ("lesson",),
        stage=ReplicationStage.ACCEPTED,
        source_outcome_ref="out-1",
        target_transformation_id="tr-2",
        target_outcome_ref="out-2",
        target_transformation_tenant_id="tenant-2",
        target_transformation_version="1.0",
        target_outcome_tenant_id="tenant-2",
        evidence_refs=("ev-rep",),
    )
    assert qualified.stage is ReplicationStage.ACCEPTED


def test_transferred_handoff_requires_acceptance_evidence() -> None:
    with pytest.raises(ValueError):
        Handoff(
            "h-transfer",
            "tr",
            "tenant",
            "tech",
            "ops",
            ("artifact",),
            ("training",),
            ("runbook",),
            ("support",),
            ("recovery",),
            "accepted",
            OwnershipTransferStatus.TRANSFERRED,
        )


def test_process_rejects_dependency_cycles_and_non_finite_volume() -> None:
    with pytest.raises(ValueError):
        Process(
            "cycle",
            "tenant",
            "rev",
            "v1",
            "cyclic process",
            (
                ProcessStep("a", "a", "actor", "system", dependencies=("b",)),
                ProcessStep("b", "b", "actor", "system", dependencies=("a",)),
            ),
        )
    with pytest.raises(ValueError):
        Process(
            "nan-volume",
            "tenant",
            "rev",
            "v1",
            "bad volume",
            (ProcessStep("a", "a", "actor", "system"),),
            volume=float("nan"),
        )


def test_target_state_rejects_duplicate_classification_ids() -> None:
    c1, c2 = classifications()
    duplicate = Classification(
        c1.classification_id,
        c2.tenant_id,
        c2.revision,
        c2.step_id,
        c2.action,
        c2.rationale,
        c2.decision_owner,
        expected_effect=c2.expected_effect,
        evidence=c2.evidence,
    )
    with pytest.raises(ValueError):
        TargetState(
            "proc-1",
            ("receive -> approve",),
            (c1, duplicate),
            ("manager approval",),
            ("invoice extraction",),
            acceptance_criteria=("accepted",),
            human_decision_rights=("manager",),
        )


def test_transformation_lifecycle_ga_contract_is_cross_scope_consistent() -> None:
    p = process()
    tr = Transformation("tr-ga", "tenant-1", "rev-1", "v1", p, target())
    baseline = Baseline(
        "base-ga",
        "tenant-1",
        "rev-1",
        "v1",
        (
            MetricObservation(
                "cycle_time",
                12.0,
                "minutes",
                "2026-Q3",
                "all invoices",
                MeasurementMethod.OBSERVED,
                "ERP",
                evidence("ev-base-ga"),
            ),
        ),
    )
    realization = EngineeringRealization(
        "real-ga",
        "tr-ga",
        "v1",
        "proc-1",
        "fdse-engineer",
        ("extract invoice fields",),
        acceptance_criteria=("golden dataset threshold met",),
    )
    binding = AgentSystemBinding(
        "bind-ga",
        "tr-ga",
        "v1",
        "agent-tr-ga",
        1,
        "tenant-1",
        "invoice-agent",
        "2026.10",
        "workspace-ga",
        "task-ga",
        ("invoice.extract",),
        execution_ref="run-ga",
    )
    receipt = GovernedExecutionReceipt(
        "receipt-ga",
        "tr-ga",
        "bind-ga",
        "tenant-1",
        "run-ga",
        ExecutionReceiptState.SUCCEEDED,
        ("policy-agent-execution",),
        evidence_refs=("ev-run-ga",),
    )
    baseline_measurement = Measurement(
        "m-base",
        "tr-ga",
        "tenant-1",
        "rev-1",
        "cycle_time",
        MeasurementStage.BASELINE,
        12.0,
        "minutes",
        "2026-Q3",
        "ERP",
        evidence("ev-measure-base-ga"),
    )
    target_measurement = Measurement(
        "m-target",
        "tr-ga",
        "tenant-1",
        "rev-1",
        "cycle_time",
        MeasurementStage.TARGET,
        10.0,
        "minutes",
        "design",
        "target-state",
    )
    measurement = Measurement(
        "m-ga",
        "tr-ga",
        "tenant-1",
        "rev-1",
        "cycle_time",
        MeasurementStage.POST_DEPLOYMENT,
        8.0,
        "minutes",
        "2026-Q4",
        "ERP",
        evidence("ev-measure-ga"),
        12.0,
        10.0,
        "lower is better",
        "improved",
        direction=MeasurementDirection.LOWER_IS_BETTER,
    )
    outcome = Outcome(
        "out-ga",
        "tr-ga",
        "tenant-1",
        "v1",
        "2026-Q4",
        ("m-base",),
        ("m-target",),
        (("cycle_time", 8.0),),
        (("cycle_time", -4.0),),
        "accepted",
        (evidence("ev-out-ga"),),
    )
    handoff = Handoff(
        "handoff-ga",
        "tr-ga",
        "tenant-1",
        "tech-owner",
        "ops-owner",
        ("artifact",),
        ("training",),
        ("runbook",),
        ("support",),
        ("recovery",),
        "accepted",
        OwnershipTransferStatus.ACCEPTED,
    )
    lifecycle = TransformationLifecycle(
        tr,
        baseline,
        realization,
        binding,
        (receipt,),
        (baseline_measurement, target_measurement, measurement),
        outcome,
        handoff,
    )
    lifecycle.require_ga_contract()


def test_transformation_lifecycle_rejects_cross_tenant_binding() -> None:
    tr = Transformation("tr-ga", "tenant-1", "rev-1", "v1", process(), target())
    baseline = Baseline(
        "base-ga",
        "tenant-1",
        "rev-1",
        "v1",
        (
            MetricObservation(
                "cycle_time",
                12.0,
                "minutes",
                "2026-Q3",
                "all invoices",
                MeasurementMethod.OBSERVED,
                "ERP",
                evidence("ev-base-ga"),
            ),
        ),
    )
    realization = EngineeringRealization(
        "real-ga",
        "tr-ga",
        "v1",
        "proc-1",
        "fdse-engineer",
        ("extract invoice fields",),
        acceptance_criteria=("accepted",),
    )
    binding = AgentSystemBinding(
        "bind-ga",
        "tr-ga",
        "v1",
        "agent-tr-ga",
        1,
        "tenant-2",
        "invoice-agent",
        "2026.10",
        "workspace-ga",
        "task-ga",
        ("invoice.extract",),
    )
    lifecycle = TransformationLifecycle(tr, baseline, realization, binding)
    with pytest.raises(ValueError):
        lifecycle.validate_internal_consistency()


def test_transformation_lifecycle_rejects_unresolved_execution_reference() -> None:
    tr = Transformation("tr-ref", "tenant-1", "rev-1", "v1", process(), target())
    baseline = Baseline(
        "base-ref",
        "tenant-1",
        "rev-1",
        "v1",
        (
            MetricObservation(
                "cycle_time",
                12.0,
                "minutes",
                "2026-Q3",
                "all invoices",
                MeasurementMethod.OBSERVED,
                "ERP",
                evidence("ev-base-ref"),
            ),
        ),
    )
    realization = EngineeringRealization(
        "real-ref",
        "tr-ref",
        "v1",
        "proc-1",
        "fdse-engineer",
        ("extract",),
        acceptance_criteria=("accepted",),
    )
    binding = AgentSystemBinding(
        "bind-ref",
        "tr-ref",
        "v1",
        "agent-tr-ref",
        1,
        "tenant-1",
        "invoice-agent",
        "2026.10",
        "workspace-ref",
        "task-ref",
        ("invoice.extract",),
        execution_ref="missing-run",
    )
    lifecycle = TransformationLifecycle(tr, baseline, realization, binding)
    with pytest.raises(ValueError):
        lifecycle.validate_internal_consistency()


def test_enterprise_runtime_type_hardening_rejects_malformed_states() -> None:
    with pytest.raises(TypeError):
        Measurement("m", "tr", "t", "r", "metric", 1, 1.0, "count", "w", "system", evidence())
    with pytest.raises(TypeError):
        AgentSystemBinding("b", "tr", "v1", "agent-tr", True, "t", "agent", "1", "ws", "task", ("cap",))
    with pytest.raises(TypeError):
        ReplicationProfile("r", "tr", "t1", "t2", ("method",), ("specific",), ("lesson",), success_claimed=1)
    with pytest.raises(TypeError):
        Outcome("o", "tr", "t", "v1", "period", ("b",), ("t",), (("m", True),), (("m", 0.0),), "accepted", (evidence(),))


def test_enterprise_enum_values_are_canonicalized_or_rejected() -> None:
    measurement = Measurement(
        "m-enum", "tr", "t", "r", "metric", "POST_DEPLOYMENT", 1.0,
        "count", "window", "system", evidence(), 2.0, 1.0, "lower", "improved",
        direction="LOWER_IS_BETTER",
    )
    assert measurement.stage is MeasurementStage.POST_DEPLOYMENT
    assert measurement.direction is MeasurementDirection.LOWER_IS_BETTER
    with pytest.raises(ValueError):
        Measurement(
            "m-bad-enum", "tr", "t", "r", "metric", "UNKNOWN", 1.0,
            "count", "window", "system", evidence(), 2.0, 1.0, "lower", "improved",
        )


def test_enterprise_evidence_reference_is_strict() -> None:
    with pytest.raises(TypeError):
        MetricObservation(
            "metric", 1.0, "count", "window", "all", MeasurementMethod.OBSERVED,
            "system", "not-an-evidence-ref",
        )
    with pytest.raises(ValueError):
        MetricObservation(
            "metric", 1.0, "count", "window", "all", MeasurementMethod.OBSERVED,
            "system", EvidenceRef("ev", "not-a-kind", ProvenanceRef("src", "rev"), "digest"),
        )


def test_enterprise_replication_requires_distinct_source_and_target() -> None:
    with pytest.raises(ValueError):
        ReplicationProfile(
            "rep", "tr", "tenant-1", "tenant-1", ("method",), ("mapping",), ("lesson",)
        )
    with pytest.raises(ValueError):
        ReplicationProfile(
            "rep", "tr", "tenant-1", "tenant-2", ("method",), ("mapping",), ("lesson",),
            stage=ReplicationStage.DEPLOYED,
        )


def test_enterprise_lifecycle_rejects_dangling_outcome_references() -> None:
    tr = Transformation("tr-ref2", "tenant-1", "rev-1", "v1", process(), target())
    baseline = Baseline(
        "base-ref2", "tenant-1", "rev-1", "v1",
        (MetricObservation(
            "cycle_time", 12.0, "minutes", "2026-Q3", "all",
            MeasurementMethod.OBSERVED, "ERP", evidence("ev-base-ref2"),
        ),),
    )
    realization = EngineeringRealization(
        "real-ref2", "tr-ref2", "v1", "proc-1", "fdse-engineer", ("extract",),
        acceptance_criteria=("accepted",),
    )
    measurement = Measurement(
        "m-post-ref2", "tr-ref2", "tenant-1", "rev-1", "cycle_time",
        MeasurementStage.POST_DEPLOYMENT, 8.0, "minutes", "2026-Q4", "ERP",
        evidence("ev-measure-ref2"), 12.0, 10.0, "lower is better", "improved",
    )
    outcome = Outcome(
        "out-ref2", "tr-ref2", "tenant-1", "v1", "2026-Q4",
        ("missing-baseline",), ("missing-target",),
        (("cycle_time", 8.0),), (("cycle_time", -4.0),), "accepted",
        (evidence("ev-out-ref2"),),
    )
    lifecycle = TransformationLifecycle(tr, baseline, realization, measurements=(measurement,), outcome=outcome)
    with pytest.raises(ValueError):
        lifecycle.validate_internal_consistency()


def test_enterprise_serialization_rejects_non_finite_values() -> None:
    with pytest.raises(ValueError):
        serialize({"value": float("nan")})
    with pytest.raises(ValueError):
        digest_value({"value": float("inf")})
    with pytest.raises(TypeError):
        serialize({1: "not-a-canonical-key"})


def test_enterprise_objects_remain_immutable() -> None:
    p = process()
    with pytest.raises((AttributeError, TypeError)):
        p.process_id = "changed"  # type: ignore[misc]


def test_reference_ap_invoice_transformation_is_deterministic_and_synthetic() -> None:
    from fdse.transformation import build_reference_ap_invoice_transformation

    first = build_reference_ap_invoice_transformation()
    second = build_reference_ap_invoice_transformation()
    assert first.synthetic is True
    assert serialize(first.lifecycle.transformation) == serialize(second.lifecycle.transformation)
    assert digest_value(first.lifecycle.transformation) == digest_value(second.lifecycle.transformation)
    assert first.lifecycle.outcome is not None
    assert first.lifecycle.outcome.acceptance_state is OutcomeAcceptance.INCONCLUSIVE
    first.validate()


def test_enterprise_replication_kit_requires_lineage_and_projects_to_profile() -> None:
    from fdse.transformation import EnterpriseReplicationKit

    kit = EnterpriseReplicationKit(
        "kit-1",
        "tr-source",
        "tenant-source",
        "tenant-target",
        ("reuse discovery",),
        ("process boundary",),
        ("DELETE/CODE/AGENT/HUMAN",),
        ("approval matrix",),
        ("eval-suite",),
        ("golden-dataset",),
        ("cycle-time",),
        ("measurement-contract",),
        ("deploy",),
        ("rollback",),
        ("runbook",),
        ("training",),
        customer_specific=("ERP mapping",),
        learned_adaptations=("exception routing",),
    )
    kit.validate()
    profile = kit.to_replication_profile()
    assert profile.source_transformation_id == "tr-source"
    assert profile.target_tenant_id == "tenant-target"

    with pytest.raises(ValueError):
        EnterpriseReplicationKit(
            "kit-bad",
            "tr-source",
            "tenant-source",
            "tenant-source",
            ("reuse",),
            ("boundary",),
            ("taxonomy",),
            ("governance",),
            ("eval",),
            ("golden",),
            ("kpi",),
            ("measurement",),
            ("deploy",),
            ("rollback",),
            ("handoff",),
            ("training",),
        )


def test_agent_platform_integration_proof_is_authority_neutral() -> None:
    from fdse.transformation import AgentPlatformIntegrationProof

    proof = AgentPlatformIntegrationProof(
        "proof-1",
        "tr-ap-invoice",
        "1.0",
        "agent-transformation-ap-invoice",
        1,
        "workspace-1",
        "task-1",
        "sdk-v1",
        "platform-run-1",
        ("policy-1",),
        ("approval-1",),
        "receipt-1",
        ("evidence-1",),
        ("measurement-1",),
        "outcome-1",
    )
    proof.validate()
    assert proof.authority_owner == "agent-platform"
    assert proof.production_verified is False

    with pytest.raises(ValueError):
        AgentPlatformIntegrationProof(
            "proof-bad",
            "tr",
            "1",
            "agent-tr",
            1,
            "ws",
            "task",
            "sdk",
            "run",
            ("policy",),
            ("approval",),
            "receipt",
            ("evidence",),
            ("measurement",),
            "outcome",
            authority_owner="fdse",
        )


def test_enterprise_lifecycle_rejects_dangling_handoff_and_replication_evidence() -> None:
    from dataclasses import replace

    from fdse.transformation import (
        OwnershipTransferStatus,
        ReplicationProfile,
        ReplicationStage,
        build_reference_ap_invoice_transformation,
    )

    reference = build_reference_ap_invoice_transformation()
    bad_handoff = replace(
        reference.lifecycle.handoff,
        ownership_status=OwnershipTransferStatus.TRANSFERRED,
        acceptance_evidence=("missing-acceptance-evidence",),
    )
    with pytest.raises(ValueError):
        replace(reference.lifecycle, handoff=bad_handoff).require_ga_contract()

    bad_replication = ReplicationProfile(
        "rep-bad-evidence",
        "tr-ap-invoice",
        "reference-tenant",
        "target-tenant",
        ("methodology",),
        ("adaptation",),
        ("lesson",),
        stage=ReplicationStage.MEASURED,
        source_outcome_ref="outcome-ap-invoice",
        target_transformation_id="target-tr",
        target_outcome_ref="target-outcome",
        target_transformation_tenant_id="target-tenant",
        target_transformation_version="1.0",
        target_outcome_tenant_id="target-tenant",
        evidence_refs=("missing-replication-evidence",),
    )
    with pytest.raises(ValueError):
        replace(reference.lifecycle, replications=(bad_replication,)).validate_internal_consistency()

    good_replication = ReplicationProfile(
        "rep-good",
        "tr-ap-invoice",
        "reference-tenant",
        "target-tenant",
        ("methodology",),
        ("adaptation",),
        ("lesson",),
        stage=ReplicationStage.MEASURED,
        source_outcome_ref="outcome-ap-invoice",
        target_transformation_id="target-tr",
        target_outcome_ref="target-outcome",
        target_transformation_tenant_id="target-tenant",
        target_transformation_version="1.0",
        target_outcome_tenant_id="target-tenant",
        evidence_refs=("ev-outcome",),
    )
    replace(reference.lifecycle, replications=(good_replication,)).validate_internal_consistency()

    with pytest.raises(ValueError):
        replace(
            reference.lifecycle,
            outcome=replace(
                reference.lifecycle.outcome,
                observed_values=(("cycle_time", 13.0),),
            ),
        ).validate_internal_consistency()

    duplicate_run = replace(reference.lifecycle.execution_receipts[0], receipt_id="receipt-duplicate")
    with pytest.raises(ValueError):
        replace(
            reference.lifecycle,
            execution_receipts=(reference.lifecycle.execution_receipts[0], duplicate_run),
        ).validate_internal_consistency()



def test_transformation_lifecycle_transitions_fail_closed() -> None:
    from fdse.transformation import (
        ExecutionReceiptState,
        OwnershipTransferStatus,
        ReplicationStage,
        transition_execution,
        transition_handoff,
        transition_replication,
    )

    assert (
        transition_execution(
            ExecutionReceiptState.PLANNED, ExecutionReceiptState.RUNNING
        )
        is ExecutionReceiptState.RUNNING
    )
    assert (
        transition_replication(
            ReplicationStage.MEASURED, ReplicationStage.ACCEPTED
        )
        is ReplicationStage.ACCEPTED
    )
    assert (
        transition_handoff(
            OwnershipTransferStatus.ACCEPTED, OwnershipTransferStatus.TRANSFERRED
        )
        is OwnershipTransferStatus.TRANSFERRED
    )

    with pytest.raises(ValueError):
        transition_execution(ExecutionReceiptState.PLANNED, ExecutionReceiptState.SUCCEEDED)
    with pytest.raises(ValueError):
        transition_replication(ReplicationStage.PLANNED, ReplicationStage.ACCEPTED)
    with pytest.raises(ValueError):
        transition_handoff(OwnershipTransferStatus.PENDING, OwnershipTransferStatus.TRANSFERRED)


def test_enterprise_lifecycle_rejects_malformed_container_and_object_types() -> None:
    reference = __import__("fdse.transformation", fromlist=["build_reference_ap_invoice_transformation"]).build_reference_ap_invoice_transformation()
    with pytest.raises(TypeError):
        TransformationLifecycle(
            reference.lifecycle.transformation,
            reference.lifecycle.baseline,
            reference.lifecycle.realization,
            reference.lifecycle.binding,
            execution_receipts=[reference.lifecycle.execution_receipts[0]],  # type: ignore[arg-type]
        ).validate_internal_consistency()
    with pytest.raises(TypeError):
        TransformationLifecycle(
            reference.lifecycle.transformation,
            reference.lifecycle.baseline,
            reference.lifecycle.realization,
            binding="not-a-binding",  # type: ignore[arg-type]
        ).validate_internal_consistency()
