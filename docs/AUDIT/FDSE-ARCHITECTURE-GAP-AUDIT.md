# FDSE Architecture & Gap Audit

**Audit date:** 2026-09-10  
**Scope:** `tinlance-fdse`, `tinlance-agent-platform`, `fde-mastery`, `Tinlance`, `tinlance-threatfade`, `tinlance-threatfade-web`; `fusionops` was checked and was not accessible under `LloydCoder/fusionops`.

## Executive finding

`LloydCoder/tinlance-fdse` was empty before M0 bootstrap. `LloydCoder/tinlance-agent-platform` currently contains an architectural README but no executable platform implementation. This means FDSE must **not** pretend that a runtime integration already exists.

The strongest reusable source is `fde-mastery`, which already contains a production-oriented platform kernel, trust/security controls, durable workflow concepts, FDE engagement lifecycle decisions, evaluation, observability and deployment gates. However, its architecture also shows why the new separation is necessary: the generic platform concerns belong in Agent Platform, while FDSE should own only software-engineering domain semantics.

## Repository findings

### `tinlance-fdse`

- Empty repository at audit start.
- No existing application, domain model, workflow, integration, security control, CI or deployment implementation.
- M0 therefore establishes the first executable domain boundary rather than migrating legacy code blindly.

### `tinlance-agent-platform`

- Contains a detailed architectural README.
- Declares identity, authorization, policy, approvals, budgets, registries, orchestration, agent runtime, model/tool adapters, sandboxing, events, trajectory, provenance, audit, evaluation and observability as platform responsibilities.
- Explicitly states that FDSE and other products must consume the platform instead of duplicating the kernel.
- No executable subsystem was found in the repository at audit time.
- **Critical dependency:** FDSE M4 cannot be honestly completed until the platform exposes a versioned, tested integration contract.

### `fde-mastery`

- Mature enterprise monorepo with `packages/platform-core` as its production platform distribution.
- Explicit control/data/trust-plane architecture and architecture tests.
- Existing durable workflow, policy, approval, tenant, security, evaluation, observability and deployment concepts are valuable design inputs.
- ADR-0015 defines an FDE engagement lifecycle above durable workflow execution and explicitly keeps execution/authorization outside the engagement layer.
- ADR-0018 defines a fail-closed agent security gate before tool execution and treats model/retrieval/tool/peer-agent outputs as untrusted.
- **Do not copy `platform-core` into FDSE.** Its generic capabilities are candidates for migration/consumption by Agent Platform, not FDSE domain code.

### `Tinlance`

- Existing FDE API boundary is authenticated, tenant-aware and explicitly separated from the public application.
- M9 runtime, M7 security gateway and M8 evaluation platform are documented as distinct control layers.
- Existing FDE integration contract uses authenticated service-to-service execution, correlation and idempotency.
- This is a useful upstream/customer integration reference, but FDSE must not recreate M7/M8/M9 inside itself.

### `tinlance-threatfade`

- Strong evidence-first engineering patterns: structured evidence, tenant-scoped persistence, audit, provenance, bounded transport, reproducible benchmarks and explicit distinction between repository evidence and external assurance.
- Security posture includes bounded inputs, non-root execution, dropped capabilities, `no-new-privileges`, supply-chain controls and signed evidence artifacts.
- These patterns should inform FDSE evidence and engineering verification, but ThreatFade remains a product/integration boundary rather than an FDSE dependency.

### `tinlance-threatfade-web`

- Exists as a separate ThreatFade web application repository.
- It should remain an external product surface; FDSE may later integrate through stable APIs/events, not shared domain internals.

### `fusionops`

- `LloydCoder/fusionops` was not found through the connected GitHub repository endpoint during this audit.
- No implementation assumptions are made from its absence.

## Reuse decisions

### Reuse conceptually / through contracts

- FDE engagement lifecycle and promotion-gate ideas from `fde-mastery`.
- Existing tenant/correlation/idempotency conventions from Tinlance.
- Evidence/provenance discipline from ThreatFade.
- Existing security architecture patterns and evaluation methodology from `fde-mastery`.

### Reuse through Agent Platform once implemented

- Identity and tenant binding.
- Authorization and capability grants.
- Policy/risk decisions.
- Approval state.
- Sandbox and execution controls.
- Generic agent/model/tool runtime.
- Trajectory/provenance/audit infrastructure.
- Budgets, events and observability.

### Must not be duplicated in FDSE

- Generic agent runtime.
- Generic model gateway.
- Generic tool gateway.
- Generic identity/authentication.
- Generic policy decision point.
- Generic approval engine.
- Generic secrets manager.
- Generic sandbox.
- Generic trajectory/audit ledger.
- Generic memory/retrieval subsystem.

## Principal gaps

1. Agent Platform has no executable implementation yet.
2. FDSE has no persistent domain schema.
3. FDSE has no repository intake implementation.
4. FDSE has no engineering-context extraction pipeline.
5. FDSE has no specialist agent implementations.
6. FDSE has no engineering workflow engine.
7. FDSE has no Git/GitHub/CI adapters.
8. FDSE has no structured finding/evidence/report lifecycle implementation beyond M0 contracts.
9. FDSE has no engineering-specific approval/policy integration beyond the port boundary.
10. FDSE has no evaluation benchmark suite.
11. FDSE has no customer API/console.
12. FDSE has no production deployment path.
13. End-to-end tenant isolation is not yet executable in FDSE.
14. No safe customer-code execution boundary exists yet; this must be provided by Agent Platform before code-executing workflows are enabled.

## Architectural risks

### R1 — Platform duplication

**Risk:** FDSE grows its own runtime/security primitives because Agent Platform is not yet implemented.  
**Control:** keep FDSE ports minimal; reject local fallbacks that bypass platform policy.

### R2 — Repository prompt/tool injection

Customer-controlled repository instructions, source files, CI output and logs can attempt to manipulate agents.  
**Control:** treat all repository-derived text as untrusted data; platform-controlled tool authorization remains authoritative.

### R3 — Customer-code execution

Build/test/debug tasks can execute arbitrary code.  
**Control:** no host execution; require Agent Platform sandbox policy with resource limits, filesystem isolation, network egress controls and disposable workspaces.

### R4 — Credential overreach

GitHub and cloud credentials can create high-impact external side effects.  
**Control:** GitHub App/fine-grained scoped permissions, per-operation capabilities, approval gates and short-lived credentials.

### R5 — Evidence inflation

An agent can assert a fix without proving it.  
**Control:** findings require observable evidence references, diffs, test results and verification records.

### R6 — Cross-tenant leakage

Repository context and evidence are highly sensitive.  
**Control:** tenant/project/repository ancestry must be enforced at the platform boundary and repeated in FDSE domain invariants.

## Production blockers

The following are blockers for customer-facing autonomous engineering execution:

- executable Agent Platform integration with fail-closed authorization and sandboxing;
- durable tenant-scoped FDSE persistence;
- safe repository workspace lifecycle;
- Git/GitHub least-privilege integration;
- evidence/provenance persistence;
- human approval enforcement;
- reproducible verification pipeline;
- security and supply-chain testing;
- end-to-end CI and deployment validation;
- customer acceptance tests against representative repositories.

## M0 conclusion

M0 is correctly scoped to establish boundaries, contracts, domain primitives, tests and architecture documentation. It must not prematurely implement agent execution, code execution or external side effects.
