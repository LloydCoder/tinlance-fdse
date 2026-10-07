"""Observed transformation outcomes."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from fdse.contracts import EvidenceRef

from ._common import enum_required, finite_number, required, unique_ids, validate_evidence_ref


class OutcomeAcceptance(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    INCONCLUSIVE = "inconclusive"


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
    acceptance_state: OutcomeAcceptance
    evidence: tuple[EvidenceRef, ...]
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for value, name in (
            (self.outcome_id, "outcome_id"), (self.transformation_id, "transformation_id"),
            (self.tenant_id, "tenant_id"), (self.version, "version"),
            (self.measurement_period, "measurement_period"),
        ):
            required(value, name)
        for name in ("outcome_id", "transformation_id", "tenant_id", "version", "measurement_period"):
            object.__setattr__(self, name, required(getattr(self, name), name))
        object.__setattr__(self, "acceptance_state", enum_required(self.acceptance_state, OutcomeAcceptance, "acceptance_state"))
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
        object.__setattr__(
            self,
            "observed_values",
            tuple((required(metric_id, "observed metric_id"), finite_number(value, "observed value")) for metric_id, value in self.observed_values),
        )
        object.__setattr__(
            self,
            "variance",
            tuple((required(metric_id, "variance metric_id"), finite_number(value, "variance value")) for metric_id, value in self.variance),
        )
        if not self.evidence:
            raise ValueError("outcome requires supporting evidence")
        object.__setattr__(
            self, "evidence",
            tuple(validate_evidence_ref(value, "outcome evidence") for value in self.evidence),
        )
        object.__setattr__(self, "limitations", tuple(required(v, "limitation") for v in self.limitations))
