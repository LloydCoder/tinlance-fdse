# fmt: off
# ruff: noqa: E501, I001
# ruff: noqa: E501, I001
"""Observed transformation outcomes."""
from __future__ import annotations

from dataclasses import dataclass
import math
from enum import StrEnum

from fdse.contracts import EvidenceRef

from ._common import required, unique_ids

class OutcomeAcceptance(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    INCONCLUSIVE = "inconclusive"

# fmt: off
@dataclass(frozen=True, slots=True)
class Outcome:
    outcome_id: str
    transformation_id: str
    tenant_id: str
    version: str
    measurement_period: str
    baseline_refs: tuple[str, ...]
    target_refs: tuple[str, ...]
    observed_values: tuple[tuple[str, float], ...]
    variance: tuple[tuple[str, float], ...]
    acceptance_state: str
    evidence: tuple[EvidenceRef, ...]
    limitations: tuple[str, ...] = ()
    def __post_init__(self) -> None:
        for value, name in ((self.outcome_id, "outcome_id"), (self.transformation_id, "transformation_id"), (self.tenant_id, "tenant_id"), (self.version, "version"), (self.measurement_period, "measurement_period"), (self.acceptance_state, "acceptance_state")):
            required(value, name)
        object.__setattr__(self, "outcome_id", required(self.outcome_id, "outcome_id"))
        object.__setattr__(self, "transformation_id", required(self.transformation_id, "transformation_id"))
        object.__setattr__(self, "tenant_id", required(self.tenant_id, "tenant_id"))
        object.__setattr__(self, "version", required(self.version, "version"))
        object.__setattr__(self, "measurement_period", required(self.measurement_period, "measurement_period"))
        object.__setattr__(self, "acceptance_state", OutcomeAcceptance(required(self.acceptance_state, "acceptance_state")))
        if not self.baseline_refs or not self.target_refs:
            raise ValueError("outcome requires baseline and target references")
        unique_ids(self.baseline_refs, "baseline_ref")
        unique_ids(self.target_refs, "target_ref")
        if not self.observed_values:
            raise ValueError("outcome requires observed values")
        observed_ids = unique_ids(tuple(metric_id for metric_id, _ in self.observed_values), "observed metric_id")
        variance_ids = unique_ids(tuple(metric_id for metric_id, _ in self.variance), "variance metric_id")
        if set(observed_ids) != set(variance_ids):
            raise ValueError("outcome variance must match observed metric identifiers")
        if any(not math.isfinite(value) for _, value in self.observed_values + self.variance):
            raise ValueError("outcome values must be finite")
        if not self.evidence:
            raise ValueError("outcome requires supporting evidence")
        object.__setattr__(self, "limitations", tuple(required(v, "limitation") for v in self.limitations))
