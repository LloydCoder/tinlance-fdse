# ruff: noqa: E501, I001
"""Transformation measurement contracts."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from fdse.contracts import EvidenceRef

from ._common import required

# fmt: off
class MeasurementStage(StrEnum):
    BASELINE = "BASELINE"
    TARGET = "TARGET"
    POST_DEPLOYMENT = "POST_DEPLOYMENT"
    FOLLOW_UP = "FOLLOW_UP"

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
    def __post_init__(self) -> None:
        for value, name in ((self.measurement_id, "measurement_id"), (self.transformation_id, "transformation_id"), (self.tenant_id, "tenant_id"), (self.revision, "revision"), (self.metric_id, "metric_id"), (self.unit, "unit"), (self.window, "window"), (self.method, "method")):
            required(value, name)
        object.__setattr__(self, "measurement_id", required(self.measurement_id, "measurement_id"))
        object.__setattr__(self, "transformation_id", required(self.transformation_id, "transformation_id"))
        object.__setattr__(self, "tenant_id", required(self.tenant_id, "tenant_id"))
        object.__setattr__(self, "revision", required(self.revision, "revision"))
        object.__setattr__(self, "metric_id", required(self.metric_id, "metric_id"))
        object.__setattr__(self, "unit", required(self.unit, "unit"))
        object.__setattr__(self, "window", required(self.window, "window"))
        object.__setattr__(self, "method", required(self.method, "method"))
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
