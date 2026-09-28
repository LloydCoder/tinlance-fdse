# FDSE M0–M14 Roadmap

| Phase | Capability | Domain completion |
| --- | --- | --- |
| M0 | Foundation | Architecture, contracts, security/config validation, CI boundary |
| M1 | Core Domain | Engineering entities, lifecycle, evidence/integrity, ports and stores |
| M2 | Intake | Validated, normalized, idempotent engineering intake |
| M3 | Context | Revision-scoped deterministic engineering context |
| M4 | Agent Platform | Versioned authority-boundary integration contract |
| M5 | Specialist Agents | Explicit specialist roles and evidence requirements |
| M6 | Workflows | Fail-closed workflow state machine |
| M7 | Git/GitHub/CI | Revision-bound repository and CI provider contracts |
| M8 | Evidence | Evidence/provenance graph and deterministic graph integrity |
| M9 | Governance | External approval/policy references; no duplicate authority |
| M10 | Evaluation | Deterministic, revision-bound, fail-closed evaluation |
| M11 | Customer Product | Tenant-scoped customer domain contracts |
| M12 | Security | Input, tenant, secret, integrity and authority controls |
| M13 | Production | Health, readiness and idempotency contracts |
| M14 | E2E Certification | Explicit M0–M14 certification bundle and fail-closed validator |

## Completion invariant

A phase is complete only when its domain capability is implemented, tested, documented, and compatible with the Agent Platform boundary.

FDSE owns engineering semantics. The Tinlance Agent Platform owns generic identity, authorization, approval, sandboxing, tools, model access, audit, and consequential execution.

## Security baseline

The implementation uses positive validation, explicit scope, deterministic integrity, and fail-closed semantics consistent with OWASP ASVS 5.0 input-validation guidance and NIST SSDF practices. NIST's current SSDF 1.2 material remains a draft; the finalized SP 800-218 v1.1 remains the finalized SSDF reference until v1.2 is finalized.
