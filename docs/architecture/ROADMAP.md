# FDSE M0–M14 Capability Roadmap

This document is the canonical capability map for the repository.

## Definition of completion

A phase is **implemented in FDSE** when its domain semantics, invariants, public contracts, tests, and documentation exist and are compatible with the architecture boundary.

A phase is **production-integrated** only when the external service/runtime it depends on exists, is connected through a versioned adapter, is exercised by integration/E2E tests, and its operational controls are verified.

FDSE must never convert a contract into a claim that an external system exists.

| Phase | Capability | FDSE ownership | External dependency |
| --- | --- | --- | --- |
| M0 | Foundation | Domain boundary, security invariants, CI/documentation foundation | GitHub Actions/runner |
| M1 | Core Domain | Engineering entities, lifecycle vocabulary, evidence/integrity | Durable infrastructure |
| M2 | Intake | Validation, normalization, scope, idempotency semantics | Durable intake store |
| M3 | Context | Context source/item/snapshot semantics, deterministic digest | Repository/context collectors |
| M4 | Agent Platform | Versioned adapter and capability compatibility | Tinlance Agent Platform |
| M5 | Specialist Agents | Specialist role/evidence specifications | Agent runtime/model/tooling |
| M6 | Workflows | Explicit transition graph and fail-closed transitions | Workflow persistence/orchestration |
| M7 | Git/GitHub/CI | Provider-neutral repository/check ports | GitHub/Git provider and CI APIs |
| M8 | Evidence | Evidence graph and integrity relations | Durable evidence/event store |
| M9 | Governance | References to approvals/policies owned externally | Agent Platform governance |
| M10 | Evaluation | Deterministic evaluation semantics | Concrete test/evaluator engines |
| M11 | Customer Product | Tenant-safe customer domain contracts | API/UI/billing/product infrastructure |
| M12 | Security | Domain security controls and redaction | IAM, secret manager, sandbox, network controls |
| M13 | Production | Readiness and idempotency semantics | Deployment, monitoring, alerting, SLO infrastructure |
| M14 | E2E Certification | Fail-closed certification verification contract | Real E2E execution and external attestation |

## Architectural boundary

FDSE does not own identity, authorization, approvals, sandboxing, model access, generic tools, consequential execution, or audit infrastructure. Those capabilities belong to the Tinlance Agent Platform.

## Certification rule

M14 may return CERTIFIED only for a supplied bundle whose required phase results, revision, evidence digest, and external attestation fields validate. A constructed in-memory bundle is not evidence that production FDSE has been certified.

## Security references

- OWASP ASVS 5.0.0 for application security verification and positive input validation.
- NIST SP 800-218 (SSDF 1.1) as the finalized SSDF baseline.
- NIST SP 800-218 Rev. 1 (SSDF 1.2) is currently a draft.
- GitHub Actions secure-use guidance for least-privilege permissions and immutable action references.
