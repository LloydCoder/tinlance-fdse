# fmt: off
# ruff: noqa: E501, I001
# ruff: noqa: E501, I001
"""Measured starting-state contracts."""
from __future__ import annotations

from dataclasses import dataclass
import math
from enum import StrEnum

from fdse.contracts import EvidenceRef

from ._common import required, unique_ids

# fmt: off
class MeasurementMethod(StrEnum):
    OBSERVED = "observed"
    SYSTEM_REPORT = "system_report"
    SAMPLE = "sample"
    INTERVIEW = "interview"
    CALCULATED = "calculated"

@dataclass(frozen=True, slots=True)
class MetricObservation:
    metric_id: str
    value: float
    unit: str
    window: str
    population: str
    method: MeasurementMethod
    source: str
    evidence: EvidenceRef
    confidence: str = "unspecified"
    currency: str | None = None
    period: str | None = None
    assumptions: tuple[str, ...] = ()
    derivation: str | None = None
    def __post_init__(self) -> None:
        object.__setattr__(self, "metric_id", required(self.metric_id, "metric_id"))
        object.__setattr__(self, "unit", required(self.unit, "metric unit"))
        object.__setattr__(self, "window", required(self.window, "measurement window"))
        object.__setattr__(self, "population", required(self.population, "population"))
        object.__setattr__(self, "source", required(self.source, "metric source"))
        object.__setattr__(self, "confidence", required(self.confidence, "confidence"))
        if not math.isfinite(self.value):
            raise ValueError("metric value must be finite")
        if self.currency is not None:
            object.__setattr__(self, "currency", required(self.currency, "metric currency"))
            if self.period is None or self.derivation is None:
                raise ValueError("economic metric requires period and derivation")
        if self.period is not None:
            object.__setattr__(self, "period", required(self.period, "metric period"))
        object.__setattr__(self, "assumptions", tuple(required(v, "metric assumption") for v in self.assumptions))
        if self.derivation is not None:
            object.__setattr__(self, "derivation", required(self.derivation, "metric derivation"))

@dataclass(frozen=True, slots=True)
class Baseline:
    baseline_id: str
    tenant_id: str
    revision: str
    version: str
    observations: tuple[MetricObservation, ...]
    assumptions: tuple[str, ...] = ()
    def __post_init__(self) -> None:
        for value, name in ((self.baseline_id, "baseline_id"), (self.tenant_id, "tenant_id"), (self.revision, "revision"), (self.version, "version")):
            required(value, name)
        object.__setattr__(self, "baseline_id", required(self.baseline_id, "baseline_id"))
        object.__setattr__(self, "tenant_id", required(self.tenant_id, "tenant_id"))
        object.__setattr__(self, "revision", required(self.revision, "revision"))
        object.__setattr__(self, "version", required(self.version, "version"))
        if not self.observations:
            raise ValueError("baseline requires at least one observation")
        unique_ids(tuple(o.metric_id for o in self.observations), "metric_id")
        object.__setattr__(self, "assumptions", tuple(required(v, "baseline assumption") for v in self.assumptions))
