"""Evidence spine, causal lineage, incident, and resilience semantics (E4)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from .engineering_intelligence import SemanticRef
from .evidence import digest


class LineageRelation(StrEnum):
    DERIVED_FROM = "derived_from"
    CAUSED_BY = "caused_by"
    OBSERVED_AS = "observed_as"
    SUPPORTED_BY = "supported_by"
    VERIFIED_BY = "verified_by"
    FEEDS = "feeds"
    FEEDBACK_TO = "feedback_to"


class IncidentRelation(StrEnum):
    SIGNALS = "signals"
    DETECTED_BY = "detected_by"
    TRIAGED_BY = "triaged_by"
    CONTAINED_BY = "contained_by"
    INVESTIGATED_BY = "investigated_by"
    REMEDIATED_BY = "remediated_by"
    VERIFIED_BY = "verified_by"
    CLOSED_BY = "closed_by"


@dataclass(frozen=True, slots=True)
class LineageRecord:
    source: SemanticRef
    relation: str
    target: SemanticRef
    actor: SemanticRef
    occurred_at: datetime
    payload_digest: str
    provenance: SemanticRef
    authority: SemanticRef

    def __post_init__(self) -> None:
        _same_scope(
            (
                self.source,
                self.target,
                self.actor,
                self.provenance,
                self.authority,
            )
        )
        if self.occurred_at.tzinfo is None or self.occurred_at.utcoffset() is None:
            raise ValueError("lineage timestamp must be timezone-aware")
        if not _sha256(self.payload_digest):
            raise ValueError("lineage payload digest must be SHA-256")


@dataclass(frozen=True, slots=True)
class EvidenceSpineChain:
    customer_request: SemanticRef
    context: SemanticRef
    plan: SemanticRef
    risk: SemanticRef
    policy: SemanticRef
    agent_or_workflow: SemanticRef
    change: SemanticRef
    execution: SemanticRef
    observation: SemanticRef
    evidence: SemanticRef
    finding: SemanticRef
    evaluation: SemanticRef
    assurance: SemanticRef
    certification: SemanticRef
    release: SemanticRef
    incident_or_feedback: SemanticRef

    def __post_init__(self) -> None:
        _same_scope(
            (
                self.customer_request,
                self.context,
                self.plan,
                self.risk,
                self.policy,
                self.agent_or_workflow,
                self.change,
                self.execution,
                self.observation,
                self.evidence,
                self.finding,
                self.evaluation,
                self.assurance,
                self.certification,
                self.release,
                self.incident_or_feedback,
            )
        )


@dataclass(frozen=True, slots=True)
class IncidentChain:
    signal: SemanticRef
    incident: SemanticRef
    detection: SemanticRef
    triage: SemanticRef
    containment: SemanticRef
    investigation: SemanticRef
    remediation: SemanticRef
    verification: SemanticRef
    closure: SemanticRef

    def __post_init__(self) -> None:
        _same_scope(
            (
                self.signal,
                self.incident,
                self.detection,
                self.triage,
                self.containment,
                self.investigation,
                self.remediation,
                self.verification,
                self.closure,
            )
        )


@dataclass(frozen=True, slots=True)
class ResilienceSemantics:
    objective: SemanticRef
    dependency: SemanticRef
    failure_mode: SemanticRef
    recovery_objective: SemanticRef
    validation: SemanticRef

    def __post_init__(self) -> None:
        _same_scope(
            (
                self.objective,
                self.dependency,
                self.failure_mode,
                self.recovery_objective,
                self.validation,
            )
        )


class EvidenceSpineGraph:
    """Deterministic lineage semantics; it does not store authority or execute incidents."""

    def __init__(self) -> None:
        self._refs: dict[tuple[str, str], SemanticRef] = {}
        self._lineage: set[LineageRecord] = set()

    def add_ref(self, ref: SemanticRef) -> None:
        key = (ref.kind, ref.identifier)
        existing = self._refs.get(key)
        if existing is not None and existing != ref:
            raise ValueError("E4 semantic identifier collision")
        self._refs[key] = ref

    def add_lineage(self, record: LineageRecord) -> None:
        if record.source == record.target:
            raise ValueError("lineage cannot be self-referential")
        self.add_ref(record.source)
        self.add_ref(record.target)
        self.add_ref(record.actor)
        self.add_ref(record.provenance)
        self.add_ref(record.authority)
        self._lineage.add(record)

    def add_spine(
        self,
        chain: EvidenceSpineChain,
        metadata: tuple[LineageRecord, ...],
    ) -> None:
        refs = (
            chain.customer_request,
            chain.context,
            chain.plan,
            chain.risk,
            chain.policy,
            chain.agent_or_workflow,
            chain.change,
            chain.execution,
            chain.observation,
            chain.evidence,
            chain.finding,
            chain.evaluation,
            chain.assurance,
            chain.certification,
            chain.release,
            chain.incident_or_feedback,
        )
        for ref in refs:
            self.add_ref(ref)
        self._add_expected(
            tuple(
                (source, LineageRelation.FEEDS.value, target)
                for source, target in zip(refs[:-1], refs[1:], strict=True)
            ),
            metadata,
        )

    def add_incident(
        self,
        chain: IncidentChain,
        metadata: tuple[LineageRecord, ...],
    ) -> None:
        refs = (
            chain.signal,
            chain.incident,
            chain.detection,
            chain.triage,
            chain.containment,
            chain.investigation,
            chain.remediation,
            chain.verification,
            chain.closure,
        )
        for ref in refs:
            self.add_ref(ref)
        self._add_expected(
            (
                (chain.signal, IncidentRelation.SIGNALS.value, chain.incident),
                (chain.incident, IncidentRelation.DETECTED_BY.value, chain.detection),
                (chain.incident, IncidentRelation.TRIAGED_BY.value, chain.triage),
                (
                    chain.incident,
                    IncidentRelation.CONTAINED_BY.value,
                    chain.containment,
                ),
                (
                    chain.incident,
                    IncidentRelation.INVESTIGATED_BY.value,
                    chain.investigation,
                ),
                (
                    chain.incident,
                    IncidentRelation.REMEDIATED_BY.value,
                    chain.remediation,
                ),
                (
                    chain.incident,
                    IncidentRelation.VERIFIED_BY.value,
                    chain.verification,
                ),
                (chain.incident, IncidentRelation.CLOSED_BY.value, chain.closure),
            ),
            metadata,
        )

    def add_resilience(
        self,
        semantics: ResilienceSemantics,
        metadata: tuple[LineageRecord, ...],
    ) -> None:
        refs = (
            semantics.objective,
            semantics.dependency,
            semantics.failure_mode,
            semantics.recovery_objective,
            semantics.validation,
        )
        for ref in refs:
            self.add_ref(ref)
        self._add_expected(
            (
                (semantics.objective, "depends_on", semantics.dependency),
                (semantics.objective, "fails_as", semantics.failure_mode),
                (semantics.objective, "recovers_by", semantics.recovery_objective),
                (semantics.recovery_objective, "validated_by", semantics.validation),
            ),
            metadata,
        )

    def _add_expected(
        self,
        expected: tuple[tuple[SemanticRef, str, SemanticRef], ...],
        metadata: tuple[LineageRecord, ...],
    ) -> None:
        expected_relations = set(expected)
        actual_relations = {
            (record.source, record.relation, record.target) for record in metadata
        }
        if actual_relations != expected_relations:
            raise ValueError("lineage metadata must cover every required relationship")
        for record in metadata:
            self.add_lineage(record)

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
        lineage = sorted(
            (
                record.source.kind,
                record.source.identifier,
                record.relation,
                record.target.kind,
                record.target.identifier,
                record.actor.identifier,
                record.occurred_at.isoformat(),
                record.payload_digest,
                record.provenance.identifier,
                record.authority.identifier,
            )
            for record in self._lineage
        )
        return digest({"refs": refs, "lineage": lineage})

    @property
    def lineage(self) -> tuple[LineageRecord, ...]:
        return tuple(
            sorted(
                self._lineage,
                key=lambda record: (
                    record.source.kind,
                    record.source.identifier,
                    record.relation,
                    record.target.kind,
                    record.target.identifier,
                    record.occurred_at.isoformat(),
                ),
            )
        )


def _same_scope(refs: tuple[SemanticRef, ...]) -> None:
    if not refs:
        raise ValueError("E4 semantics require references")
    scope = (refs[0].tenant_id, refs[0].repository_id, refs[0].revision)
    if any((ref.tenant_id, ref.repository_id, ref.revision) != scope for ref in refs):
        raise ValueError("E4 semantics cross engineering scope")


def _sha256(value: str):
    return len(value) == 64 and all(
        character in "0123456789abcdef" for character in value
    )

