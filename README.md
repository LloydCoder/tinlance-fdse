# Tinlance FDSE

**Forward-Deployed Software Engineering (FDSE) domain layer for governed, evidence-driven software delivery.**

Tinlance FDSE defines the engineering semantics, contracts, invariants, evidence model, workflow state, evaluation rules, and certification semantics required to operate FDSE safely.

It is intentionally **not** an autonomous agent runtime. Generic agent authority and execution infrastructure are supplied by the **Tinlance Agent Platform**.

[![CI](https://github.com/LloydCoder/tinlance-fdse/actions/workflows/ci.yml/badge.svg)](https://github.com/LloydCoder/tinlance-fdse/actions/workflows/ci.yml)

---

## What FDSE is

FDSE is the engineering-domain substrate between customer engineering work and the generic Tinlance Agent Platform.

It turns untrusted engineering inputs into explicit, bounded, revision-aware domain objects and sends consequential execution intent across a governed platform boundary.

~~~text
Customer engineering work
        │
        ▼
┌───────────────────────────────┐
│ Tinlance FDSE                 │
│                               │
│ Intake → Context → Planning   │
│ → Specialists → Workflows     │
│ → Git/CI → Evidence           │
│ → Evaluation → Product        │
│ → Security → Readiness        │
│ → Certification               │
└───────────────┬───────────────┘
                │ versioned intent
                ▼
┌───────────────────────────────┐
│ Tinlance Agent Platform       │
│                               │
│ Identity / Authorization      │
│ Approvals / Policy            │
│ Runtime / Sandbox             │
│ Models / Tools / Budgets      │
│ Audit / Observability         │
└───────────────────────────────┘
~~~

**Architectural invariant:**

> **FDSE owns engineering semantics; Agent Platform owns generic agent authority and execution infrastructure.**

This boundary is deliberate. FDSE must not become a second agent runtime, authorization kernel, sandbox, model gateway, generic tool authority, or deployment platform.

## What FDSE owns

- tenant- and repository-scoped engineering work;
- immutable revision binding;
- validated and normalized intake;
- deterministic engineering context;
- specialist role and evidence requirements;
- fail-closed workflow transitions;
- repository and CI provider contracts;
- evidence and provenance graph primitives;
- deterministic evaluation semantics;
- customer-domain contracts;
- domain security controls and secret redaction;
- health, readiness, and idempotency contracts;
- fail-closed certification verification.

## What FDSE deliberately does not own

- identity and authentication;
- authorization and policy enforcement;
- human approval authority;
- autonomous agent/runtime execution;
- filesystem/process sandboxing;
- model gateway and model credentials;
- generic tool authority;
- budgets and quotas;
- durable evidence/trajectory infrastructure;
- GitHub itself and other provider services;
- workflow orchestration and durable workflow state;
- customer API/UI/billing infrastructure;
- deployment infrastructure;
- production monitoring, alerting, and SLO systems.

Those capabilities must be connected through explicit, versioned interfaces rather than reimplemented inside FDSE.

---

## Trust model

FDSE treats the following as **untrusted input**:

- customer repository contents;
- repository instructions and configuration;
- source code and generated artifacts;
- dependency metadata;
- model output;
- tool output;
- external service responses;
- build and test output.

Untrusted content cannot grant itself authority.

Consequential actions that can change customer repositories, infrastructure, credentials, deployments, or other durable state must cross the Agent Platform approval and policy boundary.

The FDSE approval flag means an operation must enter the platform governance path. It is not an approval grant and is not evidence that approval has already occurred.

---

## Core invariants

1. **Explicit scope** — tenant, repository, and revision remain bound wherever customer engineering state is represented.
2. **Revision determinism** — engineering context, checks, evaluation, and certification are tied to a concrete revision rather than mutable branch state.
3. **Evidence before authority** — observations, evidence, findings, evaluations, and certification are distinct concepts.
4. **Fail closed** — malformed, missing, conflicting, stale, or insufficient information does not silently become success.
5. **No self-authority** — model output, repository content, or self-authored claims cannot authorize consequential execution or certify production.
6. **Deterministic integrity** — canonical hashes/digests make relevant state reproducible and tamper-evident.
7. **Tenant isolation** — cross-tenant, cross-repository, and cross-revision mixing is rejected.
8. **Approval separation** — FDSE emits governed intent; the Agent Platform remains authoritative for authorization and approval.
9. **Lexical safety is not sandboxing** — FDSE path validation is lexical; filesystem and execution isolation remain platform responsibilities.
10. **External certification evidence** — M14 requires externally supplied attestation metadata and matching evidence rather than accepting an in-memory declaration as proof.

---

## M0–M18 capability map

The canonical phase definition is [docs/architecture/ROADMAP.md](docs/architecture/ROADMAP.md).

| Phase | FDSE capability | Repository status |
|---|---|---|
| M0 | Architecture, boundary, security/config and CI foundation | Implemented |
| M1 | Core engineering entities, lifecycle, evidence/integrity contracts | Implemented |
| M2 | Validated, normalized, tenant-scoped intake and idempotency semantics | Implemented |
| M3 | Revision-scoped deterministic context and provenance metadata | Implemented |
| M4 | Versioned Agent Platform adapter/capability contract | Implemented; platform external |
| M5 | Specialist role and evidence contracts | Implemented; runtime external |
| M6 | Fail-closed workflow state machine | Implemented; orchestration/persistence external |
| M7 | Repository and CI provider ports | Implemented; provider services external |
| M8 | Evidence/provenance graph primitives | Implemented; durable store external |
| M9 | Governance references and authority boundary | Implemented; authority external |
| M10 | Revision-bound deterministic evaluation | Implemented; concrete evaluators external |
| M11 | Tenant-scoped customer domain contracts | Implemented; customer application external |
| M12 | Input, tenant, secret, integrity and authority controls | Implemented; infrastructure controls external |
| M13 | Health/readiness/idempotency contracts | Implemented; deployment/observability external |
| M14 | Fail-closed certification-bundle verifier | Implemented; real E2E evidence/attestation external |
| M15 | Context + trusted memory semantics | Implemented; durable memory/KMS/access control external |
| M16 | Real workflow runtime: durable DAG and recovery semantics | Implemented; durable scheduling/store external |
| M17 | Multi-agent runtime: supervision, delegation, messaging, isolation | Implemented; Agent Platform identity/runtime external |
| M18 | Agent ecosystem runtime: governed skills, apps, extensions, connectors, packages | Implemented; signature/grant/execution infrastructure external |

**Important:** “Implemented” means the FDSE-side domain semantics, invariants, tests, and documentation exist. It does **not** mean every external production dependency is deployed or healthy.

---

## Repository layout

~~~text
src/fdse/
├── contracts.py            # M0/M1 foundational contracts
├── errors.py               # Domain errors
├── config.py               # Configuration/path validation
├── service.py              # Domain service boundary
├── security.py             # Core security contracts
├── domain.py               # Core engineering entities
├── evidence.py             # Evidence records
├── integrity.py            # Canonical integrity helpers
├── transitions.py          # Single lifecycle transition authority
├── intake.py               # M2 intake
├── context.py              # M3 context
├── platform.py             # M4 Agent Platform boundary
├── agents.py               # M5 specialist contracts
├── workflows.py            # M6 workflows
├── git_ci.py               # M7 repository/CI ports
├── evidence_graph.py       # M8 evidence graph
├── governance.py           # M9 governance references
├── evaluation.py           # M10 evaluation
├── product.py              # M11 customer contracts
├── security_hardening.py   # M12 hardening/redaction
├── production.py           # M13 readiness/idempotency
├── certification.py        # M14 certification verification
├── trusted_memory.py       # M15 trusted context/memory semantics
├── workflow_runtime.py     # M16 workflow runtime semantics
├── multi_agent_runtime.py  # M17 multi-agent runtime semantics
├── ecosystem_runtime.py    # M18 agent ecosystem semantics
├── engineering_intelligence.py # E2 engineering intelligence
├── assurance_security_supply_chain.py # E3 assurance/security/supply chain
├── evidence_lineage.py     # E4 evidence/lineage/incident/resilience
├── integration.py          # E5 production integration contracts
└── enterprise_validation.py # E6 validation/certification/GA gates
~~~

The package public API is exported from [src/fdse/__init__.py](src/fdse/__init__.py), including the M15–M18 and E2–E6 enterprise contracts.

See [docs/architecture/REPOSITORY-STRUCTURE.md](docs/architecture/REPOSITORY-STRUCTURE.md) for the authoritative structure map.
---

## Documentation

| Document | Purpose |
|---|---|
| [ROADMAP.md](docs/architecture/ROADMAP.md) | Canonical M0–M18 capability and completion definitions |
| [M15-CONTEXT-TRUSTED-MEMORY.md](docs/architecture/M15-CONTEXT-TRUSTED-MEMORY.md) | Context + trusted memory semantics |
| [M16-WORKFLOW-RUNTIME.md](docs/architecture/M16-WORKFLOW-RUNTIME.md) | Workflow runtime semantics |
| [M17-MULTI-AGENT-RUNTIME.md](docs/architecture/M17-MULTI-AGENT-RUNTIME.md) | Multi-agent runtime semantics |
| [M18-AGENT-ECOSYSTEM-RUNTIME.md](docs/architecture/M18-AGENT-ECOSYSTEM-RUNTIME.md) | Agent ecosystem runtime semantics |
| [E2-ENGINEERING-INTELLIGENCE.md](docs/architecture/E2-ENGINEERING-INTELLIGENCE.md) | Canonical engineering intelligence semantics |
| [E3-ASSURANCE-SECURITY-SUPPLY-CHAIN.md](docs/architecture/E3-ASSURANCE-SECURITY-SUPPLY-CHAIN.md) | Assurance, agentic security, and supply-chain semantics |
| [E4-EVIDENCE-LINEAGE-INCIDENT-RESILIENCE.md](docs/architecture/E4-EVIDENCE-LINEAGE-INCIDENT-RESILIENCE.md) | Evidence spine, causal lineage, incident, and resilience semantics |
| [E5-PRODUCTION-INTEGRATION.md](docs/architecture/E5-PRODUCTION-INTEGRATION.md) | Versioned production-integration and system-of-systems validation contracts |
| [E6-VALIDATION-CERTIFICATION-GA.md](docs/architecture/E6-VALIDATION-CERTIFICATION-GA.md) | Enterprise validation, certification, and GA gate semantics |
| [BOUNDARY.md](docs/architecture/BOUNDARY.md) | FDSE ↔ Agent Platform authority boundary |
| [REPOSITORY-STRUCTURE.md](docs/architecture/REPOSITORY-STRUCTURE.md) | Current source/documentation map |
| [AUDIT-2026-10-03.md](docs/architecture/AUDIT-2026-10-03.md) | Latest architecture/reconciliation audit |
| [M1-CORE-DOMAIN.md](docs/architecture/M1-CORE-DOMAIN.md) | Core engineering domain |
| [M2-INTAKE.md](docs/architecture/M2-INTAKE.md) | Trusted intake boundary |
| [M3-CONTEXT.md](docs/architecture/M3-CONTEXT.md) | Deterministic engineering context |
| [M4-AGENT-PLATFORM.md](docs/architecture/M4-AGENT-PLATFORM.md) | Agent Platform integration contract |
| [M5-SPECIALIST-AGENTS.md](docs/architecture/M5-SPECIALIST-AGENTS.md) | Specialist contracts |
| [M6-WORKFLOWS.md](docs/architecture/M6-WORKFLOWS.md) | Workflow semantics |
| [M7-GIT-CI.md](docs/architecture/M7-GIT-CI.md) | Git/CI provider contracts |
| [M8-EVIDENCE.md](docs/architecture/M8-EVIDENCE.md) | Evidence graph |
| [M9-GOVERNANCE.md](docs/architecture/M9-GOVERNANCE.md) | Governance boundary |
| [M10-EVALUATION.md](docs/architecture/M10-EVALUATION.md) | Deterministic evaluation |
| [M11-CUSTOMER-PRODUCT.md](docs/architecture/M11-CUSTOMER-PRODUCT.md) | Customer domain contracts |
| [M12-SECURITY.md](docs/architecture/M12-SECURITY.md) | Security controls |
| [M13-PRODUCTION.md](docs/architecture/M13-PRODUCTION.md) | Production-readiness contracts |
| [M14-CERTIFICATION.md](docs/architecture/M14-CERTIFICATION.md) | E2E certification verification |
| [SELF-HOSTED-RUNNER.md](docs/operations/SELF-HOSTED-RUNNER.md) | Historical runner decommissioning guidance |

---

## Enterprise closure track

The M0–M18 capability roadmap is complete. Enterprise completion is tracked separately as E1–E6 so that the domain roadmap is not extended with an M19:

| Track | Purpose | Status |
|---|---|---|
| E1 | Baseline closure and contract integrity | Implemented |
| E2 | Engineering intelligence and cross-system semantics | Implemented |
| E3 | Assurance, agentic security and supply-chain intelligence | Implemented |
| E4 | Evidence spine, lineage, incident and resilience intelligence | Implemented |
| E5 | Production integration and system-of-systems validation | Contract/validation layer implemented; external production evidence required |
| E6 | Enterprise validation, certification and GA | Validation/certification contract implemented; external GA evidence required |

These tracks extend verification and integration; they do not authorize FDSE to absorb Agent Platform authority or external infrastructure responsibilities.

## Security posture

FDSE uses:

- positive input validation;
- explicit tenant/repository/revision scope;
- deterministic integrity digests;
- fail-closed state transitions and evaluation;
- secret and authorization-header redaction;
- explicit authority separation;
- least-privilege GitHub workflow permissions;
- immutable full-commit-SHA GitHub Action references;
- merge-queue workflow coverage;
- build artifact provenance attestation on main-branch builds.

GitHub documents least-privilege workflow permissions and full-SHA action pinning as security practices for GitHub Actions. Artifact attestations provide signed build provenance that can be independently verified; an attestation is provenance evidence, not a guarantee that an artifact is secure.

The repository's application-security framing references OWASP ASVS 5.0.0, NIST SP 800-218 (SSDF 1.1), OWASP Top 10 for Agentic Applications 2026, and SLSA v1.2. These references inform FDSE semantics; they do not constitute external certification or deployment evidence.

---

## Development

Requirements:

- Python 3.12+;
- a clean virtual environment is recommended.

Install development dependencies:

~~~bash
python -m pip install -e ".[dev]"
~~~

Run the full local quality gate:

~~~bash
ruff check .
ruff format --check .
mypy src
pytest
pip-audit --skip-editable
python -m build --no-isolation
python scripts/check_docs.py
~~~

Or:

~~~bash
make check
~~~

The CI workflow runs the quality gate on GitHub-hosted runners and additionally tests Python 3.12 and 3.13 on pull requests and merge queues.

---

## CI and supply-chain controls

.github/workflows/ci.yml:

- runs on GitHub-hosted infrastructure;
- explicitly declares workflow permissions;
- uses immutable full-length commit SHAs for actions;
- validates lint, formatting, typing, tests, dependency audit, package build, and documentation links;
- runs compatibility tests on Python 3.12 and 3.13 for pull requests and merge queues;
- generates build provenance attestations for main-branch distributions.

The historical persistent self-hosted runner is **not** part of the current FDSE CI path. See [docs/operations/SELF-HOSTED-RUNNER.md](docs/operations/SELF-HOSTED-RUNNER.md) only for decommissioning and incident-response history.

---

## Certification semantics

M14 is a verifier, not a self-certification mechanism.

A certification bundle must satisfy its configured revision/commit constraints, contain exactly the required M0–M18 phase coverage without duplicates, contain certified phase results, match its deterministic evidence digest, and carry the required external attestation metadata.

This distinction matters:

~~~text
green FDSE CI
     ≠
healthy Agent Platform
     ≠
production deployment readiness
     ≠
E2E certification
~~~

A repository workflow can establish confidence in the FDSE codebase without proving that external runtime, infrastructure, customer integrations, or production controls are healthy.

---

## Versioning

The package currently reports version 1.9.0. The changelog records the M15–M18 capability evolution and the M0–M14 baseline.

Phase implementation status is governed by docs/architecture/ROADMAP.md; documentation must not claim external production integration unless the relevant integration has actually been deployed and verified.

---

## License

Tinlance FDSE is released under the Apache License 2.0. See [LICENSE](LICENSE) for the governing terms.

---

## Project governance

Changes should preserve the FDSE/Agent Platform boundary, add regression coverage for security-sensitive defects, keep documentation synchronized with executable behavior, and avoid introducing credentials or generic execution authority into the domain layer.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).
