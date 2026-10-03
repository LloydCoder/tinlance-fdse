import pytest

from fdse.engineering_intelligence import (
    ChangeChain,
    EngineeringIntelligenceGraph,
    IntelligenceRelation,
    OperationalSemantics,
    PolicyChain,
    RiskChain,
    SemanticRef,
    SemanticRelation,
)


def ref(
    kind: str,
    identifier: str,
    scope: tuple[str, str, str] = ("t", "repo", "sha"),
) -> SemanticRef:
    return SemanticRef(kind, identifier, *scope)


def test_all_canonical_chains_are_scope_safe_and_deterministic() -> None:
    risk = RiskChain(
        ref("asset", "a"),
        ref("threat", "t1"),
        ref("scenario", "s"),
        ref("control", "c"),
        ref("evidence", "e"),
        ref("finding", "f"),
        ref("risk", "r"),
        ref("treatment", "tr"),
        ref("residual-risk", "rr"),
    )
    policy = PolicyChain(
        ref("policy", "p"),
        ref("requirement", "req"),
        ref("constraint", "con"),
        ref("guardrail", "g"),
        ref("approval-requirement", "ar"),
    )
    change = ChangeChain(
        ref("change", "ch"),
        ref("impact", "i"),
        ref("risk", "cr"),
        (ref("evidence", "ce"),),
        (ref("evaluation", "ev"),),
        ref("approval-requirement", "ca"),
        ref("verification", "v"),
        ref("release", "rel"),
    )
    operational = OperationalSemantics(
        ref("objective", "o"),
        ref("slo", "slo"),
        ref("customer-impact-threshold", "threshold"),
        ref("recovery-objective", "rto"),
        ref("assurance-requirement", "assure"),
    )

    graph = EngineeringIntelligenceGraph()
    graph.add_risk_chain(risk)
    graph.add_policy_chain(policy)
    graph.add_change_chain(change)
    graph.add_operational_semantics(operational)
    digest_a = graph.snapshot_digest()

    reverse = EngineeringIntelligenceGraph()
    reverse.add_operational_semantics(operational)
    reverse.add_change_chain(change)
    reverse.add_policy_chain(policy)
    reverse.add_risk_chain(risk)
    assert reverse.snapshot_digest() == digest_a
    assert len(graph.relations) == 21


def test_scope_escape_and_reference_collision_fail_closed() -> None:
    graph = EngineeringIntelligenceGraph()
    graph.add_ref(ref("asset", "a"))
    with pytest.raises(ValueError):
        graph.add_relation(
            SemanticRelation(
                ref("asset", "a"),
                IntelligenceRelation.THREATENS,
                ref("threat", "x", ("other", "repo", "sha")),
            )
        )

    with pytest.raises(ValueError):
        graph.add_ref(ref("asset", "a", ("t", "other-repo", "sha")))


def test_required_change_semantics_are_enforced() -> None:
    with pytest.raises(ValueError):
        ChangeChain(
            ref("change", "c"),
            ref("impact", "i"),
            ref("risk", "r"),
            (),
            (ref("evaluation", "e"),),
            ref("approval-requirement", "a"),
            ref("verification", "v"),
            ref("release", "rel"),
        )
    with pytest.raises(ValueError):
        ChangeChain(
            ref("change", "c"),
            ref("impact", "i"),
            ref("risk", "r"),
            (ref("evidence", "e"),),
            (),
            ref("approval-requirement", "a"),
            ref("verification", "v"),
            ref("release", "rel"),
        )


def test_empty_or_self_referential_semantics_are_rejected() -> None:
    with pytest.raises(ValueError):
        SemanticRef("", "id", "t", "repo", "sha")
    with pytest.raises(ValueError):
        SemanticRelation(
            ref("asset", "a"),
            IntelligenceRelation.THREATENS,
            ref("asset", "a"),
        )
