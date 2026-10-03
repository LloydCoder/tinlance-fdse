"""Canonical engineering-intelligence semantics (E2).

FDSE owns the meaning and relationships of engineering risk, policy, change,
and operational objectives. It does not calculate authoritative risk scores,
grant approvals, execute changes, or replace external governance/runtime
systems.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .evidence import digest


class IntelligenceRelation(StrEnum):
    THREATENS = "threatens"
    SCENARIO_OF = "scenario_of"
    CONTROL_FOR = "control_for"
    SUPPORTED_BY = "supported_by"
    FINDING_FROM = "finding_from"
    RISK_OF = "risk_of"
    TREATED_BY = "treated_by"
    RESIDUAL_OF = "residual_of"
    REQUIRES = "requires"
    CONSTRAINS = "constrains"
    GUARDS = "guards"
    APPROVAL_REQUIRED_BY = "approval_required_by"
    EXCEPTED_BY = "excepted_by"
    IMPACTS = "impacts"
    EVALUATED_BY = "evaluated_by"
    VERIFIED_BY = "verified_by"
    RELEASED_AS = "released_as"
    MEASURED_BY = "measured_by"
    THRESHOLD_FOR = "threshold_for"
    RECOVERED_BY = "recovered_by"
    ASSURED_BY = "assured_by"


@dataclass(frozen=True, slots=True)
class SemanticRef:
    kind: str
    identifier: str
    tenant_id: str
    repository_id: str
    revision: str

    def __post_init__(self) -> None:
        values = (
            self.kind,
            self.identifier,
            self.tenant_id,
            self.repository_id,
            self.revision,
        )
        if any(not value.strip() for value in values):
            raise ValueError("semantic reference fields are required")
        if any("\x00" in value for value in values):
            raise ValueError("semantic reference fields cannot contain NUL bytes")


@dataclass(frozen=True, slots=True)
class SemanticRelation:
    source: SemanticRef
    relation: IntelligenceRelation
    target: SemanticRef

    def __post_init__(self) -> None:
        if (
            self.source.tenant_id,
            self.source.repository_id,
            self.source.revision,
        ) != (
            self.target.tenant_id,
            self.target.repository_id,
            self.target.revision,
        ):
            raise ValueError("semantic relation crosses engineering scope")
        if self.source == self.target:
            raise ValueError("semantic relation cannot be self-referential")


@dataclass(frozen=True, slots=True)
class RiskChain:
    asset: SemanticRef
    threat: SemanticRef
    scenario: SemanticRef
    control: SemanticRef
    evidence: SemanticRef
    finding: SemanticRef
    risk: SemanticRef
    treatment: SemanticRef
    residual_risk: SemanticRef

    def __post_init__(self) -> None:
        refs = (
            self.asset,
            self.threat,
            self.scenario,
            self.control,
            self.evidence,
            self.finding,
            self.risk,
            self.treatment,
            self.residual_risk,
        )
        _validate_same_scope(refs)
        if len({(ref.kind, ref.identifier) for ref in refs}) != len(refs):
            raise ValueError("risk chain references must be unique")


@dataclass(frozen=True, slots=True)
class PolicyChain:
    policy: SemanticRef
    requirement: SemanticRef
    constraint: SemanticRef
    guardrail: SemanticRef
    approval_requirement: SemanticRef
    exception: SemanticRef | None = None

    def __post_init__(self) -> None:
        refs = (
            self.policy,
            self.requirement,
            self.constraint,
            self.guardrail,
            self.approval_requirement,
            self.exception,
        )
        _validate_same_scope(tuple(ref for ref in refs if ref is not None))


@dataclass(frozen=True, slots=True)
class ChangeChain:
    change: SemanticRef
    impact: SemanticRef
    risk: SemanticRef
    required_evidence: tuple[SemanticRef, ...]
    required_evaluation: tuple[SemanticRef, ...]
    approval_requirement: SemanticRef
    verification: SemanticRef
    release: SemanticRef

    def __post_init__(self) -> None:
        refs = (
            self.change,
            self.impact,
            self.risk,
            *self.required_evidence,
            *self.required_evaluation,
            self.approval_requirement,
            self.verification,
            self.release,
        )
        _validate_same_scope(refs)
        if not self.required_evidence:
            raise ValueError("change semantics require evidence requirements")
        if not self.required_evaluation:
            raise ValueError("change semantics require evaluation requirements")


@dataclass(frozen=True, slots=True)
class OperationalSemantics:
    objective: SemanticRef
    slo: SemanticRef
    customer_impact_threshold: SemanticRef
    recovery_objective: SemanticRef
    assurance_requirement: SemanticRef

    def __post_init__(self) -> None:
        _validate_same_scope(
            (
                self.objective,
                self.slo,
                self.customer_impact_threshold,
                self.recovery_objective,
                self.assurance_requirement,
            )
        )


class EngineeringIntelligenceGraph:
    """Deterministic semantic graph; it has no authority or execution powers."""

    def __init__(self) -> None:
        self._refs: dict[tuple[str, str], SemanticRef] = {}
        self._relations: set[SemanticRelation] = set()

    def add_ref(self, ref: SemanticRef) -> None:
        key = (ref.kind, ref.identifier)
        existing = self._refs.get(key)
        if existing is not None and existing != ref:
            raise ValueError("semantic identifier is already bound to another reference")
        self._refs[key] = ref

    def add_relation(self, relation: SemanticRelation) -> None:
        self.add_ref(relation.source)
        self.add_ref(relation.target)
        self._relations.add(relation)

    def add_risk_chain(self, chain: RiskChain) -> None:
        self._add_pairs(
            (
                (chain.asset, IntelligenceRelation.THREATENS, chain.threat),
                (chain.threat, IntelligenceRelation.SCENARIO_OF, chain.scenario),
                (chain.scenario, IntelligenceRelation.CONTROL_FOR, chain.control),
                (chain.control, IntelligenceRelation.SUPPORTED_BY, chain.evidence),
                (chain.evidence, IntelligenceRelation.FINDING_FROM, chain.finding),
                (chain.finding, IntelligenceRelation.RISK_OF, chain.risk),
                (chain.risk, IntelligenceRelation.TREATED_BY, chain.treatment),
                (
                    chain.treatment,
                    IntelligenceRelation.RESIDUAL_OF,
                    chain.residual_risk,
                ),
            )
        )

    def add_policy_chain(self, chain: PolicyChain) -> None:
        pairs: tuple[tuple[SemanticRef, IntelligenceRelation, SemanticRef], ...] = (
            (chain.policy, IntelligenceRelation.REQUIRES, chain.requirement),
            (chain.requirement, IntelligenceRelation.CONSTRAINS, chain.constraint),
            (chain.constraint, IntelligenceRelation.GUARDS, chain.guardrail),
            (
                chain.guardrail,
                IntelligenceRelation.APPROVAL_REQUIRED_BY,
                chain.approval_requirement,
            ),
        )
        if chain.exception is not None:
            pairs += (
                (
                    chain.constraint,
                    IntelligenceRelation.EXCEPTED_BY,
                    chain.exception,
                ),
            )
        self._add_pairs(pairs)

    def add_change_chain(self, chain: ChangeChain) -> None:
        pairs = [
            (chain.change, IntelligenceRelation.IMPACTS, chain.impact),
            (chain.impact, IntelligenceRelation.RISK_OF, chain.risk),
            (chain.change, IntelligenceRelation.REQUIRES, chain.approval_requirement),
            (chain.change, IntelligenceRelation.VERIFIED_BY, chain.verification),
            (chain.change, IntelligenceRelation.RELEASED_AS, chain.release),
        ]
        pairs.extend(
            (chain.change, IntelligenceRelation.REQUIRES, ref) for ref in chain.required_evidence
        )
        pairs.extend(
            (chain.change, IntelligenceRelation.EVALUATED_BY, ref)
            for ref in chain.required_evaluation
        )
        self._add_pairs(tuple(pairs))

    def add_operational_semantics(self, semantics: OperationalSemantics) -> None:
        self._add_pairs(
            (
                (semantics.objective, IntelligenceRelation.MEASURED_BY, semantics.slo),
                (
                    semantics.objective,
                    IntelligenceRelation.THRESHOLD_FOR,
                    semantics.customer_impact_threshold,
                ),
                (
                    semantics.objective,
                    IntelligenceRelation.RECOVERED_BY,
                    semantics.recovery_objective,
                ),
                (
                    semantics.objective,
                    IntelligenceRelation.ASSURED_BY,
                    semantics.assurance_requirement,
                ),
            )
        )

    def snapshot_digest(self) -> str:
        refs = sorted(
            (
                ref.kind,
                ref.identifier,
                ref.tenant_id,
                ref.repository_id,
                ref.revision,
            )
            for ref in self._refs.values()
        )
        relations = sorted(
            (
                relation.source.kind,
                relation.source.identifier,
                relation.relation.value,
                relation.target.kind,
                relation.target.identifier,
            )
            for relation in self._relations
        )
        return digest({"refs": refs, "relations": relations})

    @property
    def references(self) -> tuple[SemanticRef, ...]:
        return tuple(self._refs[key] for key in sorted(self._refs))

    @property
    def relations(self) -> tuple[SemanticRelation, ...]:
        return tuple(
            sorted(
                self._relations,
                key=lambda item: (
                    item.source.kind,
                    item.source.identifier,
                    item.relation.value,
                    item.target.kind,
                    item.target.identifier,
                ),
            )
        )

    def _add_pairs(
        self,
        pairs: tuple[tuple[SemanticRef, IntelligenceRelation, SemanticRef], ...],
    ) -> None:
        for source, relation, target in pairs:
            self.add_relation(SemanticRelation(source, relation, target))


def _validate_same_scope(refs: tuple[SemanticRef, ...]) -> None:
    if not refs:
        raise ValueError("semantic chain requires references")
    scope = (refs[0].tenant_id, refs[0].repository_id, refs[0].revision)
    if any((ref.tenant_id, ref.repository_id, ref.revision) != scope for ref in refs):
        raise ValueError("semantic chain crosses engineering scope")
