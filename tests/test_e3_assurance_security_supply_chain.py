import pytest

from fdse.assurance_security_supply_chain import (
    AgenticAssetKind,
    AgenticSecurityRelation,
    AgenticSecurityRisk,
    AssuranceChain,
    AssuranceSecurityGraph,
    FrameworkDefinition,
    FrameworkMapping,
    SupplyChainChain,
)
from fdse.engineering_intelligence import SemanticRef


def ref(kind: str, identifier: str) -> SemanticRef:
    return SemanticRef(kind, identifier, "t", "repo", "sha")


def test_assurance_framework_agentic_and_supply_chain_semantics() -> None:
    assurance = AssuranceChain(
        ref("requirement", "req"),
        ref("control", "control"),
        ref("test", "test"),
        ref("evidence", "evidence"),
        ref("result", "result"),
        ref("assurance", "assurance"),
    )
    framework = FrameworkDefinition(
        "owasp-asvs",
        "5.0",
        (FrameworkMapping("owasp-asvs", "5.0", "V1", ref("requirement", "req")),),
    )
    agentic = AgenticSecurityRelation(
        ref(AgenticAssetKind.AGENT.value, "agent"),
        AgenticSecurityRisk.TOOL_POISONING,
        ref(AgenticAssetKind.TOOL.value, "tool"),
    )
    supply = SupplyChainChain(
        ref("source", "source"),
        ref("revision", "revision"),
        ref("dependency", "dependency"),
        ref("build", "build"),
        ref("artifact", "artifact"),
        ref("provenance", "provenance"),
        ref("attestation", "attestation"),
        ref("verification", "verification"),
        ref("release", "release"),
    )
    graph = AssuranceSecurityGraph()
    graph.add_assurance(assurance)
    graph.add_framework(framework)
    graph.add_agentic_security(agentic)
    graph.add_supply_chain(supply)
    assert len(graph.relations) == 15
    assert graph.snapshot_digest() == AssuranceSecurityGraphDigest(graph)


def AssuranceSecurityGraphDigest(graph: AssuranceSecurityGraph) -> str:
    reverse = AssuranceSecurityGraph()
    for source, relation, target in reversed(graph.relations):
        reverse.add_relation(source, relation, target)
    return reverse.snapshot_digest()


def test_frameworks_are_data_not_hardcoded_business_logic() -> None:
    mapping = FrameworkMapping("customer-framework", "2026.1", "REQ-7", ref("requirement", "r"))
    definition = FrameworkDefinition("customer-framework", "2026.1", (mapping,))
    graph = AssuranceSecurityGraph()
    graph.add_framework(definition)
    assert graph.relations[0][1] == "maps_to"


def test_scope_escape_and_self_reference_fail_closed() -> None:
    graph = AssuranceSecurityGraph()
    with pytest.raises(ValueError):
        graph.add_relation(
            ref("agent", "a"),
            AgenticSecurityRisk.PRIVILEGE_ESCALATION.value,
            SemanticRef("tool", "t", "other", "repo", "sha"),
        )
    with pytest.raises(ValueError):
        graph.add_agentic_security(
            AgenticSecurityRelation(
                ref("agent", "a"),
                AgenticSecurityRisk.CREDENTIAL_EXPOSURE,
                ref("agent", "a"),
            )
        )
