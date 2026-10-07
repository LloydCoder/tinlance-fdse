# fmt: off
# ruff: noqa: E501
"""Canonical DELETE/CODE/AGENT/HUMAN classification semantics and taxonomy."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from fdse.contracts import EvidenceRef

from ._common import enum_required, required, validate_evidence_ref


class Action(StrEnum):
    DELETE = "DELETE"
    CODE = "CODE"
    AGENT = "AGENT"
    HUMAN = "HUMAN"


class DecisionBasis(StrEnum):
    OBSERVED = "OBSERVED"
    DOCUMENTED = "DOCUMENTED"
    INTERVIEW = "INTERVIEW"
    ANALYSIS = "ANALYSIS"
    POLICY = "POLICY"


class RiskLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Reversibility(StrEnum):
    REVERSIBLE = "REVERSIBLE"
    PARTIAL = "PARTIAL"
    IRREVERSIBLE = "IRREVERSIBLE"


class DecisionConfidence(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass(frozen=True, slots=True)
class Classification:
    classification_id: str
    tenant_id: str
    revision: str
    step_id: str
    action: Action
    rationale: str
    decision_owner: str
    constraints: tuple[str, ...] = ()
    expected_effect: str = ""
    risk_considerations: tuple[str, ...] = ()
    evidence: tuple[EvidenceRef, ...] = ()
    decision_basis: DecisionBasis = DecisionBasis.ANALYSIS
    risk_level: RiskLevel = RiskLevel.MEDIUM
    reversibility: Reversibility = Reversibility.REVERSIBLE
    confidence: DecisionConfidence = DecisionConfidence.MEDIUM
    transition_conditions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for value, name in (
            (self.classification_id, "classification_id"),
            (self.tenant_id, "tenant_id"),
            (self.revision, "revision"),
            (self.step_id, "step_id"),
            (self.rationale, "rationale"),
            (self.decision_owner, "decision_owner"),
        ):
            required(value, name)
        for name in (
            "classification_id", "tenant_id", "revision", "step_id",
            "rationale", "decision_owner",
        ):
            object.__setattr__(self, name, required(getattr(self, name), name))
        object.__setattr__(self, "constraints", tuple(required(v, "constraint") for v in self.constraints))
        object.__setattr__(self, "expected_effect", required(self.expected_effect, "expected_effect"))
        object.__setattr__(
            self, "risk_considerations",
            tuple(required(v, "risk consideration") for v in self.risk_considerations),
        )
        object.__setattr__(
            self, "transition_conditions",
            tuple(required(v, "transition condition") for v in self.transition_conditions),
        )
        object.__setattr__(self, "action", enum_required(self.action, Action, "action"))
        object.__setattr__(self, "decision_basis", enum_required(self.decision_basis, DecisionBasis, "decision_basis"))
        object.__setattr__(self, "risk_level", enum_required(self.risk_level, RiskLevel, "risk_level"))
        object.__setattr__(self, "reversibility", enum_required(self.reversibility, Reversibility, "reversibility"))
        object.__setattr__(self, "confidence", enum_required(self.confidence, DecisionConfidence, "confidence"))
        if not self.evidence:
            raise ValueError("classification requires supporting evidence")
        object.__setattr__(
            self, "evidence",
            tuple(validate_evidence_ref(value, "classification evidence") for value in self.evidence),
        )
