"""Evidence/provenance graph primitives (M8)."""
from __future__ import annotations

from dataclasses import dataclass
import re
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
    tenant_id: str
    repository_id: str
    kind: str
    revision: str
    payload_digest: str
    source: str

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.tenant_id,
                self.repository_id,
                self.kind,
                self.revision,
                self.payload_digest,
                self.source,
            )
        ):
            raise ValueError("evidence node fields are required")
        if not re.fullmatch(r"[0-9a-f]{64}", self.payload_digest):
            raise ValueError("evidence payload digest must be a SHA-256 hex digest")


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
        existing = self._nodes.get(node.evidence_id)
        if existing is not None and existing != node:
            raise ValueError("evidence identifier is already bound to another node")
        self._nodes[node.evidence_id] = node

    def add_edge(self, edge: EvidenceEdge) -> None:
        source = self._nodes.get(edge.source_id)
        target = self._nodes.get(edge.target_id)
        if source is None or target is None:
            raise ValueError("evidence edge references unknown node")
        if (
            source.tenant_id != target.tenant_id
            or source.repository_id != target.repository_id
            or source.revision != target.revision
        ):
            raise ValueError("evidence edge crosses scope or repository revision")
        if edge.source_id == edge.target_id:
            raise ValueError("self-referential evidence edge")
        self._edges.add(edge)

    def snapshot_digest(self) -> str:
        nodes = sorted(
            (
                str(node.evidence_id),
                node.tenant_id,
                node.repository_id,
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
