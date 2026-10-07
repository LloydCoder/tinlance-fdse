# fmt: off
# ruff: noqa: E501
"""Canonical AP/invoice Transformation reference fixture.

The fixture is deterministic and explicitly synthetic. It is a contract-level
golden case for tests, documentation, and integration proofs; its measurements
are not customer results and must never be presented as such.
"""
from __future__ import annotations

from dataclasses import dataclass

from fdse.contracts import EvidenceRef, ProvenanceRef

from .baseline import Baseline, MeasurementMethod, MetricObservation
from .binding import AgentSystemBinding
from .classification import (
    Action,
    Classification,
    DecisionBasis,
    DecisionConfidence,
    Reversibility,
    RiskLevel,
)
from .execution import ExecutionReceiptState, GovernedExecutionReceipt
from .handoff import Handoff, OwnershipTransferStatus
from .lifecycle import TransformationLifecycle
from .measurement import Measurement, MeasurementDirection, MeasurementStage
from .outcome import Outcome, OutcomeAcceptance
from .process import Process, ProcessStep
from .realization import EngineeringRealization
from .transformation import TargetState, Transformation


@dataclass(frozen=True, slots=True)
class ReferenceAPInvoiceTransformation:
    """A reproducible, non-customer AP/invoice transformation golden case."""

    lifecycle: TransformationLifecycle
    synthetic: bool = True

    def __post_init__(self) -> None:
        if not self.synthetic:
            raise ValueError("the AP/invoice reference fixture must remain explicitly synthetic")

    def validate(self) -> None:
        self.lifecycle.require_ga_contract()


def _evidence(evidence_id: str) -> EvidenceRef:
    return EvidenceRef(
        evidence_id,
        "test_result",
        ProvenanceRef("reference-ap-invoice-fixture", "fixture-v1"),
        f"fixture-digest-{evidence_id}",
    )


def build_reference_ap_invoice_transformation() -> ReferenceAPInvoiceTransformation:
    """Build the canonical synthetic AP/invoice lifecycle fixture."""
    tenant_id = "reference-tenant"
    revision = "ap-invoice-v1"
    version = "1.0"

    process = Process(
        "ap-invoice",
        tenant_id,
        revision,
        version,
        "process supplier invoices from receipt through approval",
        (
            ProcessStep("receive", "receive invoice", "AP clerk", "ERP"),
            ProcessStep("validate", "validate invoice", "AP clerk", "ERP", ("receive",)),
            ProcessStep("code", "code invoice", "AP analyst", "ERP", ("validate",)),
            ProcessStep("approve", "approve invoice", "finance manager", "ERP", ("code",)),
        ),
        actors=("AP clerk", "AP analyst", "finance manager"),
        systems=("ERP",),
        boundaries=("supplier intake", "accounts payable", "approved posting"),
        volume=100.0,
        frequency="synthetic batch",
        evidence_ids=("fixture-process",),
    )

    classifications = (
        Classification(
            "class-receive",
            tenant_id,
            revision,
            "receive",
            Action.CODE,
            "standardize intake metadata",
            "finance",
            expected_effect="normalized invoice intake",
            evidence=(_evidence("ev-class-receive"),),
            decision_basis=DecisionBasis.OBSERVED,
            risk_level=RiskLevel.LOW,
            reversibility=Reversibility.REVERSIBLE,
            confidence=DecisionConfidence.HIGH,
        ),
        Classification(
            "class-validate",
            tenant_id,
            revision,
            "validate",
            Action.AGENT,
            "automate deterministic validation with exception routing",
            "finance",
            expected_effect="validated invoices with explicit exceptions",
            evidence=(_evidence("ev-class-validate"),),
            decision_basis=DecisionBasis.ANALYSIS,
            risk_level=RiskLevel.HIGH,
            reversibility=Reversibility.REVERSIBLE,
            confidence=DecisionConfidence.MEDIUM,
        ),
        Classification(
            "class-code",
            tenant_id,
            revision,
            "code",
            Action.AGENT,
            "propose accounting codes from governed mappings",
            "finance",
            expected_effect="consistent coding proposals",
            evidence=(_evidence("ev-class-code"),),
            decision_basis=DecisionBasis.DOCUMENTED,
            risk_level=RiskLevel.HIGH,
            reversibility=Reversibility.REVERSIBLE,
            confidence=DecisionConfidence.MEDIUM,
            transition_conditions=("low-confidence proposals require review",),
        ),
        Classification(
            "class-approve",
            tenant_id,
            revision,
            "approve",
            Action.HUMAN,
            "retain financial approval authority with a named human owner",
            "finance manager",
            expected_effect="approved posting with accountable ownership",
            evidence=(_evidence("ev-class-approve"),),
            decision_basis=DecisionBasis.POLICY,
            risk_level=RiskLevel.CRITICAL,
            reversibility=Reversibility.IRREVERSIBLE,
            confidence=DecisionConfidence.HIGH,
        ),
    )

    target_state = TargetState(
        "ap-invoice",
        ("receive -> validate -> code -> approve",),
        classifications,
        ("resolve exceptions", "approve posting"),
        ("validate invoices", "propose accounting codes"),
        integration_requirements=("ERP invoice API",),
        governance_requirements=("approval policy", "exception threshold"),
        acceptance_criteria=(
            "all four process steps are represented",
            "exception path is explicit",
        ),
        exception_handling=("route validation failures to AP analyst",),
        human_decision_rights=("finance manager approves posting",),
        recovery_requirements=("restore prior coding mapping",),
        observability_requirements=("record validation and coding outcomes",),
    )

    transformation = Transformation(
        "tr-ap-invoice",
        tenant_id,
        revision,
        version,
        process,
        target_state,
    )

    baseline = Baseline(
        "baseline-ap-invoice",
        tenant_id,
        revision,
        version,
        (
            MetricObservation(
                "cycle_time",
                20.0,
                "minutes",
                "synthetic-window",
                "100 synthetic invoices",
                MeasurementMethod.OBSERVED,
                "reference fixture",
                _evidence("ev-baseline-cycle"),
            ),
            MetricObservation(
                "exception_rate",
                0.10,
                "ratio",
                "synthetic-window",
                "100 synthetic invoices",
                MeasurementMethod.CALCULATED,
                "reference fixture",
                _evidence("ev-baseline-exception"),
            ),
        ),
    )

    realization = EngineeringRealization(
        "real-ap-invoice",
        "tr-ap-invoice",
        version,
        "ap-invoice",
        "reference-engineering-owner",
        ("validate invoice fields", "propose coding", "route exceptions"),
        repository_refs=("reference-repo",),
        integration_refs=("erp-invoice-api",),
        agent_refs=("reference-ap-agent",),
        evaluation_refs=("reference-ap-golden-suite",),
        verification_refs=("reference-ci-gate",),
        acceptance_criteria=("golden fixture invariants pass",),
    )

    binding = AgentSystemBinding(
        "binding-ap-invoice",
        "tr-ap-invoice",
        version,
        "agent-transformation-ap-invoice",
        1,
        tenant_id,
        "reference-ap-agent",
        "1.0",
        "reference-workspace",
        "reference-task",
        ("invoice.validate", "invoice.code"),
        execution_ref="reference-run-1",
        evidence_refs=("ev-run-ap-invoice",),
        measurement_refs=("m-baseline-cycle", "m-target-cycle", "m-post-cycle"),
        outcome_ref="outcome-ap-invoice",
    )

    receipt = GovernedExecutionReceipt(
        "receipt-ap-invoice",
        "tr-ap-invoice",
        "binding-ap-invoice",
        tenant_id,
        "reference-run-1",
        ExecutionReceiptState.SUCCEEDED,
        ("reference-policy",),
        approval_refs=("reference-approval",),
        evidence_refs=("ev-run-ap-invoice",),
        output_refs=("reference-output",),
    )

    baseline_measurement = Measurement(
        "m-baseline-cycle",
        "tr-ap-invoice",
        tenant_id,
        revision,
        "cycle_time",
        MeasurementStage.BASELINE,
        20.0,
        "minutes",
        "synthetic-window",
        "reference fixture",
        _evidence("ev-measure-baseline"),
    )
    target_measurement = Measurement(
        "m-target-cycle",
        "tr-ap-invoice",
        tenant_id,
        revision,
        "cycle_time",
        MeasurementStage.TARGET,
        15.0,
        "minutes",
        "design-window",
        "reference target",
    )
    post_measurement = Measurement(
        "m-post-cycle",
        "tr-ap-invoice",
        tenant_id,
        revision,
        "cycle_time",
        MeasurementStage.POST_DEPLOYMENT,
        14.0,
        "minutes",
        "synthetic-post-window",
        "reference fixture",
        _evidence("ev-measure-post"),
        20.0,
        15.0,
        "lower is better",
        "illustrative improvement",
        direction=MeasurementDirection.LOWER_IS_BETTER,
    )

    outcome = Outcome(
        "outcome-ap-invoice",
        "tr-ap-invoice",
        tenant_id,
        version,
        "synthetic-post-window",
        ("m-baseline-cycle",),
        ("m-target-cycle",),
        (("cycle_time", 14.0),),
        (("cycle_time", -6.0),),
        OutcomeAcceptance.INCONCLUSIVE,
        (_evidence("ev-outcome"),),
        limitations=("synthetic fixture; not a customer result",),
    )

    handoff = Handoff(
        "handoff-ap-invoice",
        "tr-ap-invoice",
        tenant_id,
        "reference-technical-owner",
        "reference-operational-owner",
        ("reference-artifact",),
        ("reference-training",),
        ("reference-runbook",),
        ("reference-escalation",),
        ("reference-rollback",),
        "reference acceptance",
        OwnershipTransferStatus.PENDING,
    )

    lifecycle = TransformationLifecycle(
        transformation,
        baseline,
        realization,
        binding,
        (receipt,),
        (baseline_measurement, target_measurement, post_measurement),
        outcome,
        handoff,
    )
    fixture = ReferenceAPInvoiceTransformation(lifecycle)
    fixture.validate()
    return fixture


__all__ = [
    "ReferenceAPInvoiceTransformation",
    "build_reference_ap_invoice_transformation",
]
