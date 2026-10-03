from datetime import UTC, datetime

import pytest

from fdse.engineering_intelligence import SemanticRef
from fdse.evidence_lineage import (
    EvidenceSpineChain,
    EvidenceSpineGraph,
    IncidentChain,
    LineageRecord,
    ResilienceSemantics,
)


def ref(kind: str, identifier: str) -> SemanticRef:
    return SemanticRef(kind, identifier, "t", "repo", "sha")


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
    actor = ref("actor", "agent")
    provenance = ref("provenance", "prov")
    authority = ref("authority", "authority")
    lineage = LineageRecord(
        chain.context,
        "derived_from",
        chain.plan,
        actor,
        datetime(2026, 10, 3, tzinfo=UTC),
        "a" * 64,
        provenance,
        authority,
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
    resilience = ResilienceSemantics(
        ref("objective", "objective"),
        ref("dependency", "dependency"),
        ref("failure-mode", "failure"),
        ref("recovery-objective", "recovery"),
        ref("validation", "validation"),
    )

    graph = EvidenceSpineGraph()
    graph.add_spine(chain, (lineage,))
    graph.add_incident(incident)
    graph.add_resilience(resilience)
    first = graph.snapshot_digest()

    reverse = EvidenceSpineGraph()
    reverse.add_spine(chain, (lineage,))
    reverse.add_resilience(resilience)
    reverse.add_incident(incident)
    assert reverse.snapshot_digest() == first
    assert len(graph.lineage) == 9


def test_lineage_metadata_and_scope_fail_closed() -> None:
    with pytest.raises(ValueError):
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
    with pytest.raises(ValueError):
        LineageRecord(
            ref("a", "a"),
            "caused_by",
            SemanticRef("b", "b", "other", "repo", "sha"),
            ref("actor", "actor"),
            datetime(2026, 10, 3, tzinfo=UTC),
            "a" * 64,
            ref("provenance", "p"),
            ref("authority", "auth"),
        )
    with pytest.raises(ValueError):
        LineageRecord(
            ref("a", "a"),
            "caused_by",
            ref("b", "b"),
            ref("actor", "actor"),
            datetime(2026, 10, 3, tzinfo=UTC),
            "not-a-digest",
            ref("provenance", "p"),
            ref("authority", "auth"),
        )
