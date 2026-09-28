# FDSE M0–M14 Capability Roadmap

This document is the **canonical capability map** for the repository. README and phase documents must remain consistent with it.

## Completion vocabulary

A phase is **FDSE-implemented** when its domain semantics, invariants, public contracts, regression tests, and documentation exist and conform to the FDSE/Agent Platform boundary.

A phase is **production-integrated** only when the external service/runtime it depends on exists, is connected through a versioned adapter, is exercised by integration/E2E tests, and its operational controls are verified.

A phase being FDSE-implemented must never be represented as proof that its external dependencies are deployed or healthy.

| Phase | FDSE ownership | External dependency |
|---|---|---|
| M0 | Domain boundary, security/config, CI/documentation foundation | GitHub Actions |
| M1 | Engineering entities, lifecycle, evidence/integrity | Durable infrastructure |
| M2 | Validation, normalization, scope, idempotency semantics | Durable intake store |
| M3 | Context-source/item/snapshot semantics and deterministic digest | Repository/context collectors |
| M4 | Versioned Agent Platform adapter/capability contract | Tinlance Agent Platform |
| M5 | Specialist role/evidence specifications | Agent runtime, models, tooling |
| M6 | Explicit fail-closed workflow state machine | Workflow persistence/orchestration |
| M7 | Provider-neutral repository/check ports | Git/GitHub and CI services |
| M8 | Evidence graph and integrity relations | Durable evidence/event store |
| M9 | External governance references | Agent Platform governance |
| M10 | Deterministic evaluation semantics | Concrete evaluator/test engines |
| M11 | Tenant-safe customer domain contracts | Customer API/UI/billing infrastructure |
| M12 | Domain validation, tenant, secret, integrity and authority controls | IAM, secret manager, sandbox, network controls |
| M13 | Health/readiness/idempotency semantics | Deployment, monitoring, alerting, SLO infrastructure |
| M14 | Fail-closed certification-bundle verifier | Real E2E execution and external attestation |

## Phase status

| Phase | FDSE status |
|---|---|
| M0 | Implemented |
| M1 | Implemented |
| M2 | Implemented |
| M3 | Implemented |
| M4 | Implemented as an adapter contract |
| M5 | Implemented as domain contracts |
| M6 | Implemented as a domain state machine |
| M7 | Implemented as provider ports |
| M8 | Implemented as domain graph primitives |
| M9 | Implemented as governance references |
| M10 | Implemented as deterministic evaluation semantics |
| M11 | Implemented as tenant-scoped contracts |
| M12 | Implemented as domain security controls |
| M13 | Implemented as readiness/idempotency contracts |
| M14 | Implemented as a fail-closed verifier |

## Architectural boundary

FDSE does not own identity, authentication, authorization, approvals, sandboxing, model access, generic tools, consequential execution, durable audit infrastructure, or deployment infrastructure. Those capabilities belong to the Tinlance Agent Platform or other explicit infrastructure services.

## Certification rule

M14 may return CERTIFIED only for a supplied bundle whose required phase results, revision/commit constraints, deterministic evidence digest, and external attestation metadata validate.

A constructed in-memory bundle is not proof that production FDSE has been certified.

## Security references

- OWASP ASVS 5.0.0 for application-security verification and positive input validation.
- NIST SP 800-218 (SSDF 1.1) as the finalized SSDF baseline.
- GitHub Actions secure-use guidance for least-privilege permissions and immutable action references.
- GitHub artifact attestations for signed build provenance and independent verification.
