"""Tenant/revision-scoped trusted-memory contracts (M15).

Trusted memory is integrity/provenance-bearing context. It is never an authority
source: it cannot grant identity, approval, capabilities, or execution rights.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from .context import (
    ContextItem,
    ContextKind,
    ContextQuality,
    ContextSnapshot,
    ContextSource,
    filter_secret_like,
)
from .evidence import digest


class MemoryTrust(StrEnum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"


@dataclass(frozen=True, slots=True)
class MemoryProvenance:
    source_id: str
    source_revision: str
    evidence_digest: str

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.source_id,
                self.source_revision,
                self.evidence_digest,
            )
        ):
            raise ValueError("memory provenance is required")
        if len(self.evidence_digest) != 64 or any(
            char not in "0123456789abcdef" for char in self.evidence_digest.lower()
        ):
            raise ValueError("memory evidence digest must be SHA-256 hex")


@dataclass(frozen=True, slots=True)
class TrustedMemory:
    memory_id: str
    tenant_id: str
    repository_id: str
    revision: str
    namespace: str
    key: str
    value: str
    provenance: MemoryProvenance
    content_digest: str
    created_at: datetime
    expires_at: datetime | None = None
    trust: MemoryTrust = MemoryTrust.UNVERIFIED

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.memory_id,
                self.tenant_id,
                self.repository_id,
                self.revision,
                self.namespace,
                self.key,
                self.value,
                self.content_digest,
            )
        ):
            raise ValueError("memory scope and content are required")
        if "\x00" in self.value:
            raise ValueError("memory value contains NUL")
        if self.expires_at is not None and self.expires_at <= self.created_at:
            raise ValueError("memory expiry must be after creation")
        if self.content_digest != digest(self.value):
            raise ValueError("memory content digest does not match value")
        if self.provenance.source_revision != self.revision:
            raise ValueError("memory provenance revision must match memory revision")


class TrustedMemoryStore:
    """Append-only, scope-enforcing memory registry for deterministic domain use."""

    def __init__(self) -> None:
        self._items: dict[str, TrustedMemory] = {}

    def put(self, memory: TrustedMemory) -> TrustedMemory:
        existing = self._items.get(memory.memory_id)
        if existing is not None and existing != memory:
            raise ValueError("memory identifier is already bound to another record")
        self._items[memory.memory_id] = memory
        return memory

    def get(
        self,
        tenant_id: str,
        repository_id: str,
        revision: str,
        memory_id: str,
        *,
        now: datetime | None = None,
    ) -> TrustedMemory | None:
        memory = self._items.get(memory_id)
        if memory is None:
            return None
        if (
            memory.tenant_id != tenant_id.strip()
            or memory.repository_id != repository_id.strip()
            or memory.revision != revision.strip()
        ):
            raise PermissionError("memory scope violation")
        current = now or datetime.now(UTC)
        if memory.expires_at is not None and current >= memory.expires_at:
            return None
        return memory

    def list_active(
        self,
        tenant_id: str,
        repository_id: str,
        revision: str,
        *,
        now: datetime | None = None,
    ) -> tuple[TrustedMemory, ...]:
        current = now or datetime.now(UTC)
        scope = (tenant_id.strip(), repository_id.strip(), revision.strip())
        items = [
            memory
            for memory in self._items.values()
            if (memory.tenant_id, memory.repository_id, memory.revision) == scope
            and (memory.expires_at is None or current < memory.expires_at)
        ]
        return tuple(
            sorted(
                items,
                key=lambda item: (item.namespace, item.key, item.memory_id),
            )
        )

    def snapshot_digest(
        self,
        tenant_id: str,
        repository_id: str,
        revision: str,
        *,
        now: datetime | None = None,
    ) -> str:
        return digest(
            [
                (
                    item.memory_id,
                    item.namespace,
                    item.key,
                    item.value,
                    item.content_digest,
                    item.provenance.source_id,
                    item.provenance.source_revision,
                    item.provenance.evidence_digest,
                    item.trust.value,
                )
                for item in self.list_active(
                    tenant_id,
                    repository_id,
                    revision,
                    now=now,
                )
            ]
        )


@dataclass(frozen=True, slots=True)
class ContextMemoryEnvelope:
    """Deterministic view combining revision-bound context and memory."""

    context: ContextSnapshot
    memories: tuple[TrustedMemory, ...]
    envelope_digest: str

    @classmethod
    def build(
        cls,
        context: ContextSnapshot,
        memories: tuple[TrustedMemory, ...],
    ) -> ContextMemoryEnvelope:
        ordered = tuple(
            sorted(
                memories,
                key=lambda item: (item.namespace, item.key, item.memory_id),
            )
        )
        if any(
            item.tenant_id != context.tenant_id
            or item.repository_id != context.repository_id
            or item.revision != context.revision
            for item in ordered
        ):
            raise ValueError("memory does not match context scope or revision")
        envelope_digest = digest(
            {
                "context": context.snapshot_digest,
                "memory": [
                    (
                        item.memory_id,
                        item.content_digest,
                        item.provenance.evidence_digest,
                    )
                    for item in ordered
                ],
            }
        )
        return cls(context, ordered, envelope_digest)

    def as_context_items(self) -> tuple[ContextItem, ...]:
        return self.context.items + tuple(
            ContextItem(
                kind=ContextKind.CONSTRAINT,
                key=f"{item.namespace}:{item.key}",
                value=filter_secret_like(item.value),
                source=_memory_source(item),
            )
            for item in self.memories
        )


def _memory_source(memory: TrustedMemory) -> ContextSource:
    return ContextSource(
        source_id=f"memory:{memory.memory_id}",
        revision=memory.revision,
        provenance=memory.provenance.source_id,
        observed_at=memory.created_at,
        tenant_id=memory.tenant_id,
        repository_id=memory.repository_id,
        freshness_seconds=0,
        confidence=(
            ContextQuality.HIGH if memory.trust is MemoryTrust.VERIFIED else ContextQuality.UNKNOWN
        ),
    )
