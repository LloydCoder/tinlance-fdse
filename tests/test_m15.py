from datetime import UTC, datetime, timedelta

import pytest

from fdse.context import ContextBuilder, ContextItem, ContextKind, ContextQuality, ContextSource
from fdse.evidence import digest
from fdse.trusted_memory import (
    ContextMemoryEnvelope,
    MemoryProvenance,
    MemoryTrust,
    TrustedMemory,
    TrustedMemoryStore,
)


def memory(
    *,
    memory_id: str = "m1",
    tenant: str = "t",
    repo: str = "r",
    revision: str = "abc",
    trust: MemoryTrust = MemoryTrust.UNVERIFIED,
    expires_at: datetime | None = None,
) -> TrustedMemory:
    value = "deployments use immutable revisions"
    return TrustedMemory(
        memory_id, tenant, repo, revision, "engineering", "deployment", value,
        MemoryProvenance("source-1", revision, "a" * 64), digest(value),
        datetime(2026, 10, 1, tzinfo=UTC), expires_at, trust,
    )


def context():
    source = ContextSource(
        "git", "abc", "repository", datetime(2026, 10, 1, tzinfo=UTC),
        "t", "r", 0, ContextQuality.HIGH,
    )
    item = ContextItem(ContextKind.REPOSITORY, "language", "python", source)
    return ContextBuilder().build("t", "r", "abc", (item,))


def test_memory_is_immutable_and_digest_bound() -> None:
    item = memory(trust=MemoryTrust.VERIFIED)
    assert item.content_digest == digest(item.value)
    with pytest.raises(ValueError):
        TrustedMemory(
            item.memory_id, item.tenant_id, item.repository_id, item.revision,
            item.namespace, item.key, "tampered", item.provenance,
            item.content_digest, item.created_at,
        )


def test_store_is_append_only_and_scope_enforcing() -> None:
    store = TrustedMemoryStore()
    item = memory()
    assert store.put(item) == item
    assert store.put(item) == item
    with pytest.raises(ValueError):
        store.put(memory(memory_id="m1", revision="def"))
    with pytest.raises(PermissionError):
        store.get("other", "r", "abc", "m1")


def test_expired_memory_is_not_returned() -> None:
    created = datetime(2026, 10, 1, tzinfo=UTC)
    item = memory(expires_at=created + timedelta(minutes=1))
    store = TrustedMemoryStore()
    store.put(item)
    assert store.get("t", "r", "abc", "m1", now=created + timedelta(minutes=2)) is None


def test_memory_snapshot_is_deterministic_and_scoped() -> None:
    store = TrustedMemoryStore()
    store.put(memory(memory_id="m2"))
    store.put(memory(memory_id="m1"))
    assert store.snapshot_digest("t", "r", "abc") == store.snapshot_digest("t", "r", "abc")


def test_context_memory_envelope_is_revision_bound() -> None:
    envelope = ContextMemoryEnvelope.build(context(), (memory(trust=MemoryTrust.VERIFIED),))
    assert len(envelope.envelope_digest) == 64
    assert envelope.memories[0].trust is MemoryTrust.VERIFIED


def test_context_memory_envelope_rejects_foreign_revision() -> None:
    with pytest.raises(ValueError):
        ContextMemoryEnvelope.build(context(), (memory(revision="def"),))
