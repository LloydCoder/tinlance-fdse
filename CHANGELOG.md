## Post-P15 forensic remediation

- Hardened TransformationLifecycle runtime boundaries so malformed aggregate, container, and nested-object inputs fail closed with structured TypeError results.
- Hardened lifecycle transition helpers to canonicalize enum inputs and reject invalid transition values with domain errors rather than leaking mapping errors.
- Added regression coverage for malformed lifecycle containers and binding types.
- PR #49 passed Python 3.12/3.13 compatibility and quality CI before squash merge; merged-main CI also passed.

# Changelog

All notable changes to Tinlance FDSE are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses semantic versioning for package releases.

## [Unreleased]

### Added
- P1–P10 Transformation capability: process/baseline semantics, DELETE/CODE/AGENT/HUMAN classification, target-state design, Agent-System binding, engineering realization, governed execution receipts, measurement/outcome qualification, handoff, replication qualification, and lifecycle GA consistency.
- Final Transformation forensic audit and explicit repository-level GA non-certification boundary.
- P11–P15 enterprise hardening, AP/invoice reference, replication kit, Agent Platform integration proof, final certification, and authoritative lifecycle transition validation.

### Changed
- Reconciled README, roadmap, architecture, and public Transformation API documentation.

## [1.9.0] — 2026-10-04

### Added
- E6 enterprise validation, certification, and GA-gate contracts.
- Full M0–M18 and E1–E6 validation semantics.
- Deterministic validation evidence and certification digest requirements.

### Changed
- Reconciled repository metadata and documentation around the Apache-2.0 package license.
- Clarified that E5/E6 external production evidence remains a separate gate.

## [1.8.0] — 2026-10-03

### Added
- E5 production-integration and system-of-systems validation contracts.
- Deterministic integration/evidence graph semantics.

## [1.7.0] — 2026-10-03

### Added
- E4 evidence spine, causal lineage, incident, and resilience semantics.

## [1.6.0] — 2026-10-03

### Added
- E3 assurance, agentic-security, framework-mapping, and supply-chain semantics.

## [1.5.0] — 2026-10-03

### Added
- E2 engineering-intelligence and cross-system semantic chains.

## [1.4.1] — 2026-10-03

### Changed
- Reconciled public API, packaging, helper boundaries, and M15–M18 documentation.
- Removed permissive production-side helpers that could be mistaken for authority implementations.

## [1.4.0] — 2026-10-03

### Added
- M18 governed skills, applications, extensions, connectors, and packages.
- Manifest integrity, dependency constraints, quarantine, disable, rollback, and provenance semantics.

## [1.3.0] — 2026-10-03

### Added
- M17 agent identity, authenticated messaging, bounded delegation, shared context, aggregation, and escalation semantics.

## [1.2.0] — 2026-10-03

### Added
- M16 deterministic workflow DAGs, retry/backoff, deadlines, cancellation, approval gates, checkpoints, recovery, and idempotency semantics.

## [1.1.0] — 2026-10-03

### Added
- M15 revision-scoped trusted-memory and context semantics.

## [1.0.0] — 2026-10-02

### Added
- M0–M14 FDSE domain capability baseline.
- Revision-bound context, evidence/provenance graph primitives, deterministic evaluation, security redaction, readiness contracts, and fail-closed certification verification.

## [0.2.0] — 2026-09-12

### Added
- M1 immutable engineering-domain entities, lifecycle states, evidence hashing, integrity chains, provider ports, and Agent Platform execution boundaries.

## [0.1.0] — 2026-09-10

### Added
- M0 domain package, configuration/path validation, approval-gated service boundary, documentation checks, and CI foundation.

[1.9.0]: https://github.com/LloydCoder/tinlance-fdse/tree/main
