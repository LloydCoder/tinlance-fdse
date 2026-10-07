# ruff: noqa: E501
"""Canonical DELETE/CODE/AGENT/HUMAN semantics."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from fdse.contracts import EvidenceRef

from ._common import required

# fmt: off
class Action(StrEnum):
    DELETE = "DELETE"
    CODE = "CODE"
    AGENT = "AGENT"
    HUMAN = "HUMAN"

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
    def __post_init__(self) -> None:
        for value, name in ((self.classification_id, "classification_id"), (self.tenant_id, "tenant_id"), (self.revision, "revision"), (self.step_id, "step_id"), (self.rationale, "rationale"), (self.decision_owner, "decision_owner")):
            required(value, name)
        object.__setattr__(self, "classification_id", required(self.classification_id, "classification_id"))
        object.__setattr__(self, "tenant_id", required(self.tenant_id, "tenant_id"))
        object.__setattr__(self, "revision", required(self.revision, "revision"))
        object.__setattr__(self, "step_id", required(self.step_id, "step_id"))
        object.__setattr__(self, "rationale", required(self.rationale, "rationale"))
        object.__setattr__(self, "decision_owner", required(self.decision_owner, "decision_owner"))
        object.__setattr__(self, "constraints", tuple(required(v, "constraint") for v in self.constraints))
        object.__setattr__(self, "expected_effect", required(self.expected_effect, "expected_effect"))
        object.__setattr__(self, "risk_considerations", tuple(required(v, "risk consideration") for v in self.risk_considerations))
        if not self.evidence:
            raise ValueError("classification requires supporting evidence")
