import pytest

from fdse import (
    ALL_PHASES,
    EnterpriseValidationGraph,
    EnterpriseValidationPlan,
    ValidationEvidence,
    ValidationLayer,
    ValidationStatus,
)


def evidence(
    phase: str, layer: ValidationLayer, status: ValidationStatus
) -> ValidationEvidence:
    return ValidationEvidence(
        phase,
        layer,
        status,
        f"{phase}-{layer.value}",
        "revision",
        "a" * 64,
    )


def test_enterprise_validation_requires_complete_passing_matrix() -> None:
    graph = EnterpriseValidationGraph()
    for phase in ALL_PHASES:
        for layer in ValidationLayer:
            graph.add_evidence(evidence(phase, layer, ValidationStatus.PASS))
    graph.gate()
    assert len(graph.evidence) == len(ALL_PHASES) * len(ValidationLayer)


def test_enterprise_validation_fails_closed_on_missing_or_failed_evidence() -> None:
    graph = EnterpriseValidationGraph()
    for phase in ALL_PHASES:
        for layer in ValidationLayer:
            if phase == "E6" and layer is ValidationLayer.PRODUCTION_READINESS:
                continue
            graph.add_evidence(evidence(phase, layer, ValidationStatus.PASS))
    with pytest.raises(ValueError):
        graph.gate()

    graph.add_evidence(
        evidence("E6", ValidationLayer.PRODUCTION_READINESS, ValidationStatus.FAIL)
    )
    with pytest.raises(ValueError):
        graph.gate()


def test_validation_plan_rejects_incomplete_phase_coverage() -> None:
    with pytest.raises(ValueError):
        EnterpriseValidationPlan(required_phases=ALL_PHASES[:-1])


def test_validation_digest_is_order_independent() -> None:
    first = EnterpriseValidationGraph()
    second = EnterpriseValidationGraph()
    for phase in ALL_PHASES:
        for layer in ValidationLayer:
            item = evidence(phase, layer, ValidationStatus.PASS)
            first.add_evidence(item)
    for phase in reversed(ALL_PHASES):
        for layer in reversed(tuple(ValidationLayer)):
            second.add_evidence(evidence(phase, layer, ValidationStatus.PASS))
    assert first.snapshot_digest() == second.snapshot_digest()
