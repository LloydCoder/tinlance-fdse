# Changelog

## 1.9.0 — E6 Enterprise Validation, Certification & GA

- Added the complete 28-layer enterprise validation taxonomy.
- Added exact M0–M18 and E1–E6 phase coverage requirements.
- Added fail-closed validation evidence, deterministic certification digests, and GA gate semantics.
- Kept external production health, customer readiness, and deployment authority outside FDSE.

# Changelog

## 1.8.0 — E5 Production Integration & System-of-Systems Validation

- Added versioned cross-system integration contracts covering FDSE, FDE Mastery, Agent Platform, Tinlance, providers, CI/CD, provenance, deployment, observability, and customer environments.
- Added deterministic integration/evidence graph semantics and fail-closed verification requirements.
- Kept external execution, authentication, approval, deployment, storage, and observability authority outside FDSE.
- Added E5 contract and verification regression coverage.

# Changelog

## 1.7.0 — E4 Evidence Spine, Lineage, Incident & Resilience

- Added an end-to-end evidence spine semantic chain.
- Added mandatory lineage metadata for actor/agent, timestamp, payload digest, provenance, authority, and causal relationship.
- Added typed incident and resilience semantics.
- Added fail-closed lineage coverage, scope, timestamp, digest, and self-reference invariants.
- Preserved external ownership of incident execution, evidence storage, approvals, certification authority, and operational recovery.


## 1.6.0 — E3 Assurance, Agentic Security & Supply-Chain Intelligence

- Added typed assurance chains and configuration-driven framework mappings.
- Added canonical agentic-security asset/risk relationships.
- Added end-to-end software supply-chain semantic lineage.
- Added fail-closed scope, collision, and self-reference invariants.
- Preserved external ownership of authentication, authorization, signing, builders, registries, runtime enforcement, and deployment infrastructure.


## 1.5.0 — E2 Engineering Intelligence & Cross-System Semantics

- Added canonical risk, policy, change, and operational semantic chains.
- Added tenant/repository/revision-scoped semantic references and deterministic graph serialization.
- Added fail-closed semantic collision, scope, and self-reference invariants.
- Added a cross-system engineering-intelligence contract without duplicating FDE Mastery execution or Agent Platform authority.


## 1.4.1 — E1 Baseline Closure

- Reconciled distribution/runtime version to the M18 release line and added a version invariant.
- Expanded the documented public API through M15–M18 without exporting permissive reference/test doubles.
- Removed production-side allow-all/no-op workflow helpers and the time-window-only identity verifier; tests now own their explicit doubles.
- Reconciled repository structure, README source maps, audit references, and the enterprise closure track.
- Added E1 contract and public-API regression coverage.


## 1.4.0 — M18 Agent Ecosystem Runtime

- Added governed skills, applications, extensions, connectors, and packages with versioned manifests and provenance.
- Added deterministic dependency constraints, verified-before-enable lifecycle, quarantine, disable, rollback, and manifest integrity digests.
- Added explicit external capability-grant and signature-verification boundaries; extensions cannot self-acquire authority.
- Extended final certification requirements from M0–M14 to complete M0–M18 coverage.
- Added M18 adversarial ecosystem and certification regression tests.


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


