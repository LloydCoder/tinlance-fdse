"""Canonical assurance, agentic-security, and supply-chain semantics (E3)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .engineering_intelligence import IntelligenceRelation, SemanticRef
from .evidence import digest


class AssuranceRelation(StrEnum):
    CONTROLS = "controls"
    TESTS = "tests"
    SUPPORTED_BY = "supported_by"
    RESULTS_IN = "results_in"
    ASSURES = "assures"
    MAPS_TO = "maps_to"
    DEPENDS_ON = "depends_on"
    BUILT_BY = "built_by"
    PRODUCES = "produces"
    PROVENANCE_FOR = "provenance_for"
    ATTESTS = "attests"
    VERIFIED_BY = "verified_by"
    RELEASED_AS = "released_as"


class AgenticSecurityRisk(StrEnum):
    PRIVILEGE_ESCALATION = "privilege_escalation"
    CAPABILITY_EXPANSION = "capability_expansion"
    DELEGATION_ABUSE = "delegation_abuse"
    CONTEXT_POISONING = "context_poisoning"
    MEMORY_POISONING = "memory_poisoning"
    TOOL_POISONING = "tool_poisoning"
    MALICIOUS_SKILL = "malicious_skill"
    MCP_RISK = "mcp_risk"
    CREDENTIAL_EXPOSURE = "credential_exposure"
    SUPPLY_CHAIN_TAMPERING = "supply_chain_tampering"
    UNEXPECTED_EXECUTION = "unexpected_execution"
    INTER_AGENT_TRUST = "inter_agent_trust"


class AgenticAssetKind(StrEnum):
    AGENT = "agent"
    CAPABILITY = "capability"
    SKILL = "skill"
    TOOL = "tool"
    CONNECTOR = "connector"
    MEMORY = "memory"
    CONTEXT = "context"
    DELEGATION = "delegation"
    MESSAGE = "message"
    EXTENSION = "extension"
    PACKAGE = "package"
    ARTIFACT = "artifact"
    PROVENANCE = "provenance"
    TRUST_RELATIONSHIP = "trust_relationship"


@dataclass(frozen=True, slots=True)
class AssuranceChain:
    requirement: SemanticRef
    control: SemanticRef
    test: SemanticRef
    evidence: SemanticRef
    result: SemanticRef
    assurance: SemanticRef

    def __post_init__(self) -> None:
        _same_scope(
            (
                self.requirement,
                self.control,
                self.test,
                self.evidence,
                self.result,
                self.assurance,
            )
        )


@dataclass(frozen=True, slots=True)
class FrameworkMapping:
    framework_id: str
    framework_version: str
    external_requirement_id: str
    semantic_requirement: SemanticRef

    def __post_init__(self) -> None:
        if any(
            not value.strip()
            for value in (
                self.framework_id,
                self.framework_version,
                self.external_requirement_id,
            )
        ):
            raise ValueError("framework mapping fields are required")


@dataclass(frozen=True, slots=True)
class FrameworkDefinition:
    framework_id: str
    framework_version: str
    mappings: tuple[FrameworkMapping, ...]

    def __post_init__(self) -> None:
        if not self.framework_id.strip() or not self.framework_version.strip():
            raise ValueError("framework definition identity is required")
        if not self.mappings:
            raise ValueError("framework definition requires mappings")
        if any(
            mapping.framework_id != self.framework_id
            or mapping.framework_version != self.framework_version
            for mapping in self.mappings
        ):
            raise ValueError("framework mapping identity must match definition")


@dataclass(frozen=True, slots=True)
class AgenticSecurityRelation:
    source: SemanticRef
    risk: AgenticSecurityRisk
    target: SemanticRef

    def __post_init__(self) -> None:
        _same_scope((self.source, self.target))
        if self.source == self.target:
            raise ValueError("agentic security relation cannot be self-referential")


@dataclass(frozen=True, slots=True)
class SupplyChainChain:
    source: SemanticRef
    revision: SemanticRef
    dependency: SemanticRef
    build: SemanticRef
    artifact: SemanticRef
    provenance: SemanticRef
    attestation: SemanticRef
    verification: SemanticRef
    release: SemanticRef

    def __post_init__(self) -> None:
        _same_scope(
            (
                self.source,
                self.revision,
                self.dependency,
                self.build,
                self.artifact,
                self.provenance,
                self.attestation,
                self.verification,
                self.release,
            )
        )


class AssuranceSecurityGraph:
    """Deterministic E3 semantics; verification authority remains external."""

    def __init__(self) -> None:
        self._refs: dict[tuple[str, str], SemanticRef] = {}
        self._relations: set[tuple[SemanticRef, str, SemanticRef]] = set()

    def add_ref(self, ref: SemanticRef) -> None:
        key = (ref.kind, ref.identifier)
        existing = self._refs.get(key)
        if existing is not None and existing != ref:
            raise ValueError("E3 semantic identifier collision")
        self._refs[key] = ref

    def add_relation(
        self,
        source: SemanticRef,
        relation: str,
        target: SemanticRef,
    ) -> None:
        _same_scope((source, target))
        if source == target:
            raise ValueError("E3 relation cannot be self-referential")
        self.add_ref(source)
        self.add_ref(target)
        self._relations.add((source, relation, target))

    def add_assurance(self, chain: AssuranceChain) -> None:
        for source, relation, target in (
            (chain.requirement, AssuranceRelation.CONTROLS, chain.control),
            (chain.control, AssuranceRelation.TESTS, chain.test),
            (chain.test, AssuranceRelation.SUPPORTED_BY, chain.evidence),
            (chain.evidence, AssuranceRelation.RESULTS_IN, chain.result),
            (chain.result, AssuranceRelation.ASSURES, chain.assurance),
        ):
            self.add_relation(source, relation.value, target)

    def add_framework(self, framework: FrameworkDefinition) -> None:
        for mapping in framework.mappings:
            self.add_relation(
                SemanticRef(
                    "framework",
                    framework.framework_id,
                    mapping.semantic_requirement.tenant_id,
                    mapping.semantic_requirement.repository_id,
                    mapping.semantic_requirement.revision,
                ),
                AssuranceRelation.MAPS_TO.value,
                mapping.semantic_requirement,
            )

    def add_agentic_security(self, relation: AgenticSecurityRelation) -> None:
        self.add_relation(relation.source, relation.risk.value, relation.target)

    def add_supply_chain(self, chain: SupplyChainChain) -> None:
        for source, relation, target in (
            (chain.source, "produces_revision", chain.revision),
            (chain.revision, "depends_on", chain.dependency),
            (chain.dependency, "input_to", chain.build),
            (chain.build, "produces_artifact", chain.artifact),
            (chain.artifact, "provenance_for", chain.provenance),
            (chain.provenance, "attests", chain.attestation),
            (chain.attestation, "verified_by", chain.verification),
            (chain.verification, "released_as", chain.release),
        ):
            self.add_relation(source, relation, target)

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
                source.kind,
                source.identifier,
                relation,
                target.kind,
                target.identifier,
            )
            for source, relation, target in self._relations
        )
        return digest({"refs": refs, "relations": relations})

    @property
    def relations(self) -> tuple[tuple[SemanticRef, str, SemanticRef], ...]:
        return tuple(
            sorted(
                self._relations,
                key=lambda item: (
                    item[0].kind,
                    item[0].identifier,
                    item[1],
                    item[2].kind,
                    item[2].identifier,
                ),
            )
        )


def _same_scope(refs: tuple[SemanticRef, ...]) -> None:
    if not refs:
        raise ValueError("E3 semantics require references")
    scope = (refs[0].tenant_id, refs[0].repository_id, refs[0].revision)
    if any((ref.tenant_id, ref.repository_id, ref.revision) != scope for ref in refs):
        raise ValueError("E3 semantics cross engineering scope")
