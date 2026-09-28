"""Deterministic evaluation contracts (M10)."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class EvaluationOutcome(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class EvaluationCase:
    case_id: str
    objective: str
    revision: str
    expected_invariants: tuple[str, ...]

    def __post_init__(self) -> None:
        if (
            not self.case_id.strip()
            or not self.objective.strip()
            or not self.revision.strip()
            or not self.expected_invariants
            or any(not invariant.strip() for invariant in self.expected_invariants)
        ):
            raise ValueError("invalid evaluation case")


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    case_id: str
    outcome: EvaluationOutcome
    observations: tuple[str, ...]
    revision: str
    satisfied_invariants: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if (
            not self.case_id.strip()
            or not self.revision.strip()
            or any(not observation.strip() for observation in self.observations)
            or any(not invariant.strip() for invariant in self.satisfied_invariants)
        ):
            raise ValueError("invalid evaluation result")


class EvaluationSuite:
    def evaluate(
        self,
        cases: tuple[EvaluationCase, ...],
        results: tuple[EvaluationResult, ...],
    ) -> EvaluationOutcome:
        by_id = {result.case_id: result for result in results}
        if len(by_id) != len(results):
            return EvaluationOutcome.UNKNOWN
        if any(case.case_id not in by_id for case in cases):
            return EvaluationOutcome.UNKNOWN
        for case in cases:
            result = by_id[case.case_id]
            if result.revision != case.revision:
                return EvaluationOutcome.UNKNOWN
            if result.outcome is EvaluationOutcome.FAIL:
                return EvaluationOutcome.FAIL
            if result.outcome is EvaluationOutcome.UNKNOWN:
                return EvaluationOutcome.UNKNOWN
            if set(case.expected_invariants) - set(result.satisfied_invariants):
                return EvaluationOutcome.UNKNOWN
        return EvaluationOutcome.PASS
