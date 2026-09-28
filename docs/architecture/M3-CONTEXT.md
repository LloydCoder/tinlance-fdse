# M3 — Engineering Context

M3 provides deterministic, tenant/repository/revision-scoped engineering context. Context is source-linked, bounded, freshness-aware, confidence-aware, immutable once snapshotted, and digestable for reproducibility.

It covers repository, architecture, dependencies, build/test/CI, security, deployment, ownership, recent changes, and explicit constraints. It does not execute repository code, fetch networks, store secrets, authorize actions, or replace evidence/provenance authority.

Secret-like values are redacted before downstream use. Snapshots are invalidated by revision identity rather than mutable branch state.
