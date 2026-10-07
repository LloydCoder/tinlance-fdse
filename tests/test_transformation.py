# fmt: off
# ruff: noqa: E501, E701, I001
from __future__ import annotations
import pytest
from fdse.contracts import EvidenceRef, ProvenanceRef
from fdse.transformation import (
    Action, Baseline, Classification, DecisionBasis, DecisionConfidence, Handoff,
    Measurement, MeasurementMethod, MeasurementStage, MetricObservation, Outcome,
    OwnershipTransferStatus, Process, ProcessStep, ReplicationProfile, Reversibility,
    RiskLevel, TargetState, Transformation, digest_value, serialize,
)
def evidence(eid: str = "ev-1") -> EvidenceRef:
    return EvidenceRef(eid, "observation", ProvenanceRef("source-1", "rev-1"), "digest-1")
def process() -> Process:
    return Process("proc-1","tenant-1","rev-1","v1","invoice processing",(ProcessStep("s1","receive","AP clerk","ERP"),ProcessStep("s2","approve","manager","ERP")),actors=("AP clerk","manager"),systems=("ERP",))
def classifications() -> tuple[Classification, ...]:
    return (Classification("c1","tenant-1","rev-1","s1",Action.CODE,"parse invoice","finance",expected_effect="extract invoice",evidence=(evidence("ev-1"),),decision_basis=DecisionBasis.ANALYSIS,risk_level=RiskLevel.MEDIUM,reversibility=Reversibility.REVERSIBLE,confidence=DecisionConfidence.HIGH),Classification("c2","tenant-1","rev-1","s2",Action.HUMAN,"approve exceptions","finance",expected_effect="approve exception",evidence=(evidence("ev-2"),),decision_basis=DecisionBasis.POLICY,risk_level=RiskLevel.HIGH,reversibility=Reversibility.REVERSIBLE,confidence=DecisionConfidence.HIGH))
def target() -> TargetState:
    return TargetState("proc-1",("receive -> approve",),classifications(),("manager approval",),("invoice extraction",))
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
    bad=TargetState("proc-1",("x",),(Classification("c","tenant-1","rev-2","s1",Action.CODE,"x","owner",expected_effect="code",evidence=(evidence(),)),Classification("c2","tenant-1","rev-1","s2",Action.HUMAN,"x","owner",expected_effect="human",evidence=(evidence("ev-2"),))),("human",),("system",))
    with pytest.raises(ValueError): Transformation("tr","tenant-1","rev-1","v1",p,bad)
    with pytest.raises(ValueError): TargetState("proc-1",("x",),(classifications()[0],classifications()[0]),("human",),("system",))
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
