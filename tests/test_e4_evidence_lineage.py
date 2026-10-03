from datetime import UTC, datetime
from unittest import TestCase

from fdse import (
    EvidenceSpineChain,
    EvidenceSpineGraph,
    IncidentChain,
    IncidentRelation,
    LineageRecord,
    LineageRelation,
    ResilienceSemantics,
    SemanticRef,
)

NOW = datetime(2026, 10, 3, tzinfo=UTC)


def ref(kind: str, identifier: str) -> SemanticRef:
    return SemanticRef(kind, identifier, "t", "repo", "sha")


def metadata(
    pairs: tuple[tuple[SemanticRef, str, SemanticRef], ...],
) -> tuple[LineageRecord, ...]:
    return tuple(
        LineageRecord(
            source,
            relation,
            target,
            ref("actor", "agent"),
            NOW,
            "a" * 64,
            ref("provenance", f"prov-{index}"),
            ref("authority", "authority"),
        )
        for index, (source, relation, target) in enumerate(pairs)
    )


def test_spine_incident_and_resilience_are_deterministic() -> None:
    chain = EvidenceSpineChain(
        ref("customer-request", "request"),
        ref("context", "context"),
        ref("plan", "plan"),
        ref("risk", "risk"),
        ref("policy", "policy"),
        ref("agent-workflow", "agent"),
        ref("change", "change"),
        ref("execution", "execution"),
        ref("observation", "observation"),
        ref("evidence", "evidence"),
        ref("finding", "finding"),
        ref("evaluation", "evaluation"),
        ref("assurance", "assurance"),
        ref("certification", "certification"),
        ref("release", "release"),
        ref("incident-feedback", "feedback"),
    )
    spine_refs = (
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
    spine_pairs = tuple(
        (source, LineageRelation.FEEDS.value, target)
        for source, target in zip(spine_refs[:-1], spine_refs[1:], strict=True)
    )
    incident = IncidentChain(
        ref("signal", "signal"),
        ref("incident", "incident"),
        ref("detection", "detection"),
        ref("triage", "triage"),
        ref("containment", "containment"),
        ref("investigation", "investigation"),
        ref("remediation", "remediation"),
        ref("verification", "verification"),
        ref("closure", "closure"),
    )
    incident_pairs = (
        (incident.signal, IncidentRelation.SIGNALS.value, incident.incident),
        (incident.incident, IncidentRelation.DETECTED_BY.value, incident.detection),
        (incident.incident, IncidentRelation.TRIAGED_BY.value, incident.triage),
        (incident.incident, IncidentRelation.CONTAINED_BY.value, incident.containment),
        (incident.incident, IncidentRelation.INVESTIGATED_BY.value, incident.investigation),
        (incident.incident, IncidentRelation.REMEDIATED_BY.value, incident.remediation),
        (incident.incident, IncidentRelation.VERIFIED_BY.value, incident.verification),
        (incident.incident, IncidentRelation.CLOSED_BY.value, incident.closure),
    )
    resilience = ResilienceSemantics(
        ref("objective", "objective"),
        ref("dependency", "dependency"),
        ref("failure-mode", "failure"),
        ref("recovery-objective", "recovery"),
        ref("validation", "validation"),
    )
    resilience_pairs = (
        (resilience.objective, "depends_on", resilience.dependency),
        (resilience.objective, "fails_as", resilience.failure_mode),
        (resilience.objective, "recovers_by", resilience.recovery_objective),
        (resilience.recovery_objective, "validated_by", resilience.validation),
    )

    graph = EvidenceSpineGraph()
    graph.add_spine(chain, metadata(spine_pairs))
    graph.add_incident(incident, metadata(incident_pairs))
    graph.add_resilience(resilience, metadata(resilience_pairs))
    first = graph.snapshot_digest()

    reverse = EvidenceSpineGraph()
    reverse.add_resilience(resilience, metadata(resilience_pairs))
    reverse.add_incident(incident, metadata(incident_pairs))
    reverse.add_spine(chain, metadata(spine_pairs))
    assert reverse.snapshot_digest() == first
    assert len(graph.lineage) == 27


def test_lineage_metadata_and_scope_fail_closed() -> None:
    with TestCase().assertRaises(ValueError):
        LineageRecord(
            ref("a", "a"),
            "caused_by",
            ref("b", "b"),
            ref("actor", "actor"),
            datetime(2026, 10, 3),
            "a" * 64,
            ref("provenance", "p"),
            ref("authority", "auth"),
        )
    with TestCase().assertRaises(ValueError):
        LineageRecord(
            ref("a", "a"),
            "caused_by",
            SemanticRef("b", "b", "other", "repo", "sha"),
            ref("actor", "actor"),
            NOW,
            "a" * 64,
            ref("provenance", "p"),
            ref("authority", "auth"),
        )
    with TestCase().assertRaises(ValueError):
        LineageRecord(
            ref("a", "a"),
            "caused_by",
            ref("b", "b"),
            ref("actor", "actor"),
            NOW,
            "not-a-digest",
            ref("provenance", "p"),
            ref("authority", "auth"),
        )
