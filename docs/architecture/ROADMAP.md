# FDSE M0–M18 Capability Roadmap

This document is the canonical capability map for the repository. README and
phase documents must remain consistent with it.

## Completion vocabulary

A phase is **FDSE-implemented** when its domain semantics, invariants, public
contracts, regression tests, and documentation exist and conform to the
FDSE/Agent Platform boundary.

A phase is **production-integrated** only when the external service/runtime it
depends on exists, is connected through a versioned adapter, is exercised by
integration/E2E tests, and its operational controls are verified.

FDSE-implemented must never be represented as proof that external dependencies
are deployed or healthy.

| Phase | FDSE ownership | External dependency |
|---|---|---|
| M0 | Domain boundary, security/config, CI/documentation foundation | GitHub Actions |
| M1 | Engineering entities, lifecycle, evidence/integrity | Durable infrastructure |
| M2 | Validation, normalization, scope, idempotency semantics | Durable intake store |
| M3 | Context-source/item/snapshot semantics and deterministic digest | Repository/context collectors |
| M4 | Versioned Agent Platform adapter/capability contract | Tinlance Agent Platform |
| M5 | Specialist role/evidence specifications | Agent runtime, models, tooling |
| M6 | Explicit workflow state machine | Workflow persistence/orchestration |
| M7 | Provider-neutral repository/check ports | Git/GitHub and CI services |
| M8 | Evidence graph and integrity relations | Durable evidence/event store |
| M9 | External governance references | Agent Platform governance |
| M10 | Deterministic evaluation semantics | Concrete evaluator/test engines |
| M11 | Tenant-safe customer domain contracts | Customer API/UI/billing infrastructure |
| M12 | Domain validation, tenant, secret, integrity and authority controls | IAM, secret manager, sandbox, network controls |
| M13 | Health/readiness/idempotency semantics | Deployment, monitoring, alerting, SLO infrastructure |
| M14 | Fail-closed certification-bundle verifier | Real E2E execution and external attestation |
| M15 | Context + trusted memory semantics | Durable memory, KMS/encryption, access control |
| M16 | Real workflow runtime: durable DAG, controls, recovery | Durable workflow store/scheduler/orchestrator |
| M17 | Multi-agent runtime: delegation, supervision, messaging, isolation | Agent Platform identity/runtime |
| M18 | Agent ecosystem runtime: skills/apps/extensions/connectors/packages | Signature/provenance and capability-grant infrastructure |

## Phase status

| Phase | Status |
|---|---|
| M0–M14 | Implemented at FDSE contract/domain level |
| M15 | Implemented |
| M16 | Implemented |
| M17 | Implemented |
| M18 | Implemented |

## M15 — Context + Trusted Memory

M15 adds revision-scoped, provenance-bearing memory that can be composed with
deterministic engineering context. Memory never becomes an authority source.

## M16 — Real Workflow Runtime

M16 adds a framework-neutral workflow runtime contract for durable DAG execution,
parallel branches, conditions, bounded retry/backoff, deadlines/timeouts,
cancellation, approval/human gates, compensation, checkpoints, recovery/resume,
event/schedule triggers, idempotency, and Agent Platform Run mapping.

## M17 — Multi-Agent Runtime

M17 adds explicit supervision/delegation, child tasks, authenticated messaging,
aggregation, shared context, isolation, propagation/escalation, tenant
isolation, anti-spoofing, provenance, and capability boundaries.

## M18 — Agent Ecosystem Runtime

M18 adds governed skills, applications, extensions, connectors, and packages
with manifests, versions, dependency constraints, grants, hashes/signatures,
provenance, lifecycle, rollback, and quarantine. Untrusted extensions cannot
self-acquire capabilities.

## Architectural boundary

FDSE does not own identity, authentication, authorization, approvals, generic
agent authority, model access, sandboxing, durable infrastructure, or deployment
infrastructure. M16–M18 define domain/runtime contracts and deterministic
reference semantics; production authority remains with the Agent Platform and
external infrastructure.

## Enterprise closure track E1–E6

The core capability roadmap ends at M18. Enterprise completion is tracked separately so there is deliberately no M19.

| Track | Scope |
|---|---|
| E1 | Baseline closure: package/runtime version, public API, helper boundaries, tests, packaging, provenance, and documentation reconciliation |
| E2 | Engineering intelligence and canonical cross-system risk, policy, change, and operational semantics | Implemented on enterprise branch |
| E3 | Assurance, agentic-security semantics, framework mappings, and software supply-chain intelligence |
| E4 | Evidence spine, causal lineage, incident semantics, and resilience intelligence | Implemented on enterprise branch |
| E5 | Production integration across FDSE, FDE Mastery, Agent Platform, Tinlance, providers, CI/CD, registries, provenance, deployment, observability, and customer systems | Contract/validation layer implemented; external production evidence remains required |
| E6 | Cross-repository, security, adversarial, performance, recovery, tenant-isolation, migration, disaster-recovery, documentation, compatibility, CI/CD, and release certification gates | Validation/certification contract implemented; external GA evidence remains required |

An enterprise track is complete only when its repository changes, contracts, tests, documentation, and applicable external integration evidence satisfy its definition of done. E1–E4 are implemented at the FDSE semantic/contract level. E5 provides the versioned system-of-systems contract and validation substrate; actual production evidence remains an external gate. E6 provides the deterministic enterprise validation/certification matrix; GA remains fail-closed until external production evidence is supplied.

## Security references

- OWASP ASVS 5.0.0 for application-security verification and positive input validation.
- NIST SP 800-218 (SSDF 1.1) as the finalized SSDF baseline.
- GitHub Actions secure-use guidance for least-privilege permissions and immutable action references.
- OpenTelemetry semantic conventions for interoperable telemetry naming.
- OWASP Top 10 for Agentic Applications 2026 for agentic security and trust-boundary risk context.
- SLSA v1.2 for software supply-chain provenance and verification semantics.
- A2A for agent interoperability; interoperability does not imply authority.
