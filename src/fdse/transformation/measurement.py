# fmt: off
# ruff: noqa: E501
"""Transformation measurement contracts."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from fdse.contracts import EvidenceRef

from ._common import enum_required, finite_number, required, validate_evidence_ref


class MeasurementStage(StrEnum):
    BASELINE = "BASELINE"
    TARGET = "TARGET"
    POST_DEPLOYMENT = "POST_DEPLOYMENT"
    FOLLOW_UP = "FOLLOW_UP"


class MeasurementDirection(StrEnum):
    UNSPECIFIED = "UNSPECIFIED"
    LOWER_IS_BETTER = "LOWER_IS_BETTER"
    HIGHER_IS_BETTER = "HIGHER_IS_BETTER"
    TARGET_BAND = "TARGET_BAND"
    EQUALS = "EQUALS"


@dataclass(frozen=True, slots=True)
class Measurement:
    measurement_id: str
    transformation_id: str
    tenant_id: str
    revision: str
    metric_id: str
    stage: MeasurementStage
    value: float
    unit: str
    window: str
    method: str
    evidence: EvidenceRef | None = None
    baseline_value: float | None = None
    target_value: float | None = None
    comparison: str | None = None
    result_status: str | None = None
    direction: MeasurementDirection = MeasurementDirection.UNSPECIFIED
    acceptance_threshold: float | None = None

    def __post_init__(self) -> None:
        for value, name in (
            (self.measurement_id, "measurement_id"), (self.transformation_id, "transformation_id"),
            (self.tenant_id, "tenant_id"), (self.revision, "revision"), (self.metric_id, "metric_id"),
            (self.unit, "unit"), (self.window, "window"), (self.method, "method"),
        ):
            required(value, name)
        for name in (
            "measurement_id", "transformation_id", "tenant_id", "revision",
            "metric_id", "unit", "window", "method",
        ):
            object.__setattr__(self, name, required(getattr(self, name), name))
        object.__setattr__(self, "stage", enum_required(self.stage, MeasurementStage, "stage"))
        object.__setattr__(self, "direction", enum_required(self.direction, MeasurementDirection, "direction"))
        object.__setattr__(self, "value", finite_number(self.value, "measurement value"))
        for candidate, name in (
            (self.baseline_value, "baseline_value"),
            (self.target_value, "target_value"),
            (self.acceptance_threshold, "acceptance_threshold"),
        ):
            if candidate is not None:
                object.__setattr__(self, name, finite_number(candidate, name))
        if self.evidence is not None:
            object.__setattr__(self, "evidence", validate_evidence_ref(self.evidence))
        if self.stage != MeasurementStage.TARGET and self.evidence is None:
            raise ValueError("non-target measurement requires evidence")
        if self.stage == MeasurementStage.BASELINE and self.baseline_value is None:
            object.__setattr__(self, "baseline_value", self.value)
        if self.stage == MeasurementStage.TARGET and self.target_value is None:
            object.__setattr__(self, "target_value", self.value)
        if self.comparison is not None:
            object.__setattr__(self, "comparison", required(self.comparison, "comparison"))
        if self.result_status is not None:
            object.__setattr__(self, "result_status", required(self.result_status, "result_status"))
        if self.stage in {MeasurementStage.POST_DEPLOYMENT, MeasurementStage.FOLLOW_UP}:
            if self.baseline_value is None or self.target_value is None:
                raise ValueError("observed measurement requires baseline and target values")
            if self.comparison is None or self.result_status is None:
                raise ValueError("observed measurement requires comparison and result status")
