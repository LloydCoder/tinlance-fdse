"""Deterministic evaluation contracts (M10)."""
from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum

class EvaluationOutcome(StrEnum):
    PASS="pass"; FAIL="fail"; UNKNOWN="unknown"

@dataclass(frozen=True,slots=True)
class EvaluationCase:
    case_id:str; objective:str; expected_invariants:tuple[str,...]
    def __post_init__(self)->None:
        if not self.case_id.strip() or not self.objective.strip() or not self.expected_invariants: raise ValueError("invalid evaluation case")

@dataclass(frozen=True,slots=True)
class EvaluationResult:
    case_id:str; outcome:EvaluationOutcome; observations:tuple[str,...]; revision:str
    def __post_init__(self)->None:
        if not self.case_id.strip() or not self.revision.strip(): raise ValueError("invalid evaluation result")

class EvaluationSuite:
    def evaluate(self,cases:tuple[EvaluationCase,...],results:tuple[EvaluationResult,...])->EvaluationOutcome:
        by_id={r.case_id:r for r in results}
        if any(c.case_id not in by_id for c in cases): return EvaluationOutcome.UNKNOWN
        if any(by_id[c.case_id].outcome is EvaluationOutcome.FAIL for c in cases): return EvaluationOutcome.FAIL
        if any(by_id[c.case_id].outcome is EvaluationOutcome.UNKNOWN for c in cases): return EvaluationOutcome.UNKNOWN
        return EvaluationOutcome.PASS
