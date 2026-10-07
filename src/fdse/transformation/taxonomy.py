"""Canonical classification taxonomy and fail-closed decision semantics."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from fdse.contracts import EvidenceRef

from ._common import required


class RiskLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Reversibility(StrEnum):
    REVERSIBLE = "REVERSIBLE"
    PARTIALLY_REVERSIBLE = "PARTIALLY_REVERSIBLE"
    IRREVERSIBLE = "IRREVERSIBLE"


class DecisionBasis(StrEnum):
    OBSERVED = "OBSERVED"
    CALCULATED = "CALCULATED"
    INTERVIEW = "INTERVIEW"
    POLICY = "POLICY"
    DESIGN = "DESIGN"


@dataclass(frozen=True, slots=True)
class ClassificationDecision:
    """Evidence-backed metadata surrounding one canonical action decision.

    This object does not execute or authorize the action. It records why a
    classification was selected and what constraints apply.
    """

    action: Action
    risk: RiskLevel
    reversibility: Reversibility
    decision_basis: DecisionBasis
    confidence: str
    rationale: str
    decision_owner: str
    constraints: tuple[str, ...] = ()
    evidence: tuple[EvidenceRef, ...] = ()

    def __post_init__(self) -> None:
        for value, name in (
            (self.confidence, "confidence"),
            (self.rationale, "rationale"),
            (self.decision_owner, "decision_owner"),
        ):
            required(value, name)
        object.__setattr__(
            self,
            "constraints",
            tuple(required(value, "constraint") for value in self.constraints),
        )
        if not self.evidence:
            raise ValueError("classification decision requires supporting evidence")


@dataclass(frozen=True, slots=True)
class ClassificationPolicy:
    """Non-executable policy metadata for reviewing canonical actions."""

    action: Action
    minimum_risk: RiskLevel
    requires_human_decision: bool
    requires_rollback: bool
    requires_evidence: bool = True

    def __post_init__(self) -> None:
        if self.requires_evidence is False:
            raise ValueError("classification decisions always require evidence")


def default_policy(action: Action) -> ClassificationPolicy:
    """Return the conservative review policy for a canonical action."""
    if action is Action.DELETE:
        return ClassificationPolicy(action, RiskLevel.HIGH, True, True)
    if action is Action.CODE:
        return ClassificationPolicy(action, RiskLevel.MEDIUM, True, True)
    if action is Action.AGENT:
        return ClassificationPolicy(action, RiskLevel.HIGH, True, True)
    return ClassificationPolicy(action, RiskLevel.MEDIUM, True, False)


# Import after declarations to keep the module dependency acyclic.
from .classification import Action  # noqa: E402

__all__ = [
    "ClassificationDecision",
    "ClassificationPolicy",
    "DecisionBasis",
    "Reversibility",
    "RiskLevel",
    "default_policy",
]
