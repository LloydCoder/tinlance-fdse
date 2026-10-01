# Changelog

## 1.3.0 — M17 Multi-Agent Runtime

- Added authenticated agent identity attestations and fail-closed message verification.
- Added bounded parent/child delegation, read-only shared context, deterministic aggregation, and explicit escalation.
- Bound inter-agent messaging to registered tenant/repository/revision scope and monotonic conversation sequences.
- Added M17 adversarial regression tests and architecture documentation.


## 1.2.0 — M16 Real Workflow Runtime

- Added deterministic DAG validation and cycle rejection.
- Added bounded retry/backoff, deadlines, cancellation, approval gates, checkpoints, recovery/resume, conditions, idempotency, and Agent Platform run mapping.
- Added M16 regression tests and architecture documentation.


## 1.1.0 — M15 Context + Trusted Memory

- Added tenant/repository/revision-scoped trusted-memory semantics.
- Added immutable memory identifiers, content digests, provenance, expiry, and deterministic memory snapshots.
- Added deterministic context-memory envelopes without granting memory execution or authorization authority.
- Added M15 regression and boundary tests.
- Reconciled the roadmap from M0–M14 to M0–M18.

## 1.0.0 — M0–M14 domain capability baseline

- Established the M0–M14 FDSE domain capability sequence.
- Added deterministic engineering context with provenance, freshness, confidence, bounded snapshots, and secret filtering.
- Added a versioned Agent Platform boundary without duplicating platform authority.
- Added specialist role contracts and explicit workflow transitions.
- Added Git/GitHub/CI provider contracts bound to repository revisions.
- Added evidence/provenance graph primitives and deterministic graph integrity digests.
- Added external governance references, deterministic evaluation, tenant-safe product contracts, security redaction, production-readiness contracts, and fail-closed E2E certification verification.
- Added cross-phase regression coverage.
- Reconciled repository documentation with the actual implementation and made external production dependencies explicit.
- Hardened public CI around GitHub-hosted runners, immutable action references, merge-queue validation, and build provenance attestation.

## 0.2.0 — M1

- Added immutable core engineering-domain entities and lifecycle states.
- Added canonical evidence hashing, integrity chains, lifecycle rules, persistence/provider ports, and Agent Platform execution boundaries.

## 0.1.0 — M0

- Established the FDSE domain package, configuration/path validation, approval-gated service boundary, documentation checks, and CI foundation.
