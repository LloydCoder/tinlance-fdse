"""Evidence/provenance graph primitives (M8)."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

from .evidence import digest


class EvidenceRelation(StrEnum):
    SUPPORTS = "supports"
    DERIVED_FROM = "derived_from"
    CONTRADICTS = "contradicts"
    VERIFIES = "verifies"


@dataclass(frozen=True, slots=True)
class EvidenceNode:
    evidence_id: UUID
    kind: str
    revision: str
    payload_digest: str
    source: str

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (self.kind, self.revision, self.payload_digest, self.source)
        ):
            raise ValueError("evidence node fields are required")


@dataclass(frozen=True, slots=True)
class EvidenceEdge:
    source_id: UUID
    target_id: UUID
    relation: EvidenceRelation


class EvidenceGraph:
    def __init__(self) -> None:
        self._nodes: dict[UUID, EvidenceNode] = {}
        self._edges: set[EvidenceEdge] = set()

    def add_node(self, node: EvidenceNode) -> None:
        self._nodes[node.evidence_id] = node

    def add_edge(self, edge: EvidenceEdge) -> None:
        if edge.source_id not in self._nodes or edge.target_id not in self._nodes:
            raise ValueError("evidence edge references unknown node")
        if edge.source_id == edge.target_id:
            raise ValueError("self-referential evidence edge")
        self._edges.add(edge)

    def snapshot_digest(self) -> str:
        nodes = sorted(
            (
                str(node.evidence_id),
                node.kind,
                node.revision,
                node.payload_digest,
                node.source,
            )
            for node in self._nodes.values()
        )
        edges = sorted(
            (str(edge.source_id), str(edge.target_id), edge.relation.value)
            for edge in self._edges
        )
        return digest({"nodes": nodes, "edges": edges})
