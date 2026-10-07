# fmt: off
# ruff: noqa: E501
"""Measured starting-state contracts."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from fdse.contracts import EvidenceRef

from ._common import enum_required, finite_number, required, unique_ids, validate_evidence_ref


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
        for value, name in (
            (self.metric_id, "metric_id"), (self.unit, "metric unit"),
            (self.window, "measurement window"), (self.population, "population"),
            (self.source, "metric source"), (self.confidence, "confidence"),
        ):
            required(value, name)
        for name in ("metric_id", "unit", "window", "population", "source", "confidence"):
            object.__setattr__(self, name, required(getattr(self, name), name))
        object.__setattr__(self, "method", enum_required(self.method, MeasurementMethod, "method"))
        object.__setattr__(self, "value", finite_number(self.value, "metric value"))
        object.__setattr__(self, "evidence", validate_evidence_ref(self.evidence))
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
        for value, name in (
            (self.baseline_id, "baseline_id"), (self.tenant_id, "tenant_id"),
            (self.revision, "revision"), (self.version, "version"),
        ):
            required(value, name)
        for name in ("baseline_id", "tenant_id", "revision", "version"):
            object.__setattr__(self, name, required(getattr(self, name), name))
        if not self.observations:
            raise ValueError("baseline requires at least one observation")
        unique_ids(tuple(o.metric_id for o in self.observations), "metric_id")
        object.__setattr__(self, "assumptions", tuple(required(v, "baseline assumption") for v in self.assumptions))
