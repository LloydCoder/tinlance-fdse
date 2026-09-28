# Tinlance FDSE

**Forward-Deployed Software Engineering execution system for governed, evidence-driven software delivery.**

Tinlance FDSE is the engineering-domain layer for Tinlance's FDSE services. It delegates generic agent authority and execution infrastructure to the Tinlance Agent Platform.

## Current status

**M0–M14 domain contracts are implemented; production integrations remain explicit external boundaries.**

The repository deliberately distinguishes **domain capability** from **infrastructure integration**:

| Phase | Capability in this repository | Status |
| --- | --- | --- |
| M0 | Architecture, domain boundary, security/config foundation, CI gates | Implemented |
| M1 | Core engineering entities, lifecycle vocabulary, evidence/integrity contracts | Implemented |
| M2 | Validated, normalized, tenant-scoped intake and idempotency contract | Implemented |
| M3 | Revision-scoped deterministic context assembly and provenance metadata | Implemented |
| M4 | Versioned Agent Platform boundary and capability validation | Implemented as adapter contract; external platform required |
| M5 | Specialist role/evidence contracts | Implemented as domain contracts; agent runtime external |
| M6 | Fail-closed workflow state machine | Implemented as domain state machine; orchestration/persistence external |
| M7 | Repository/CI provider ports | Implemented as ports; live provider adapters external |
| M8 | Evidence/provenance graph primitives | Implemented as domain graph; durable evidence store external |
| M9 | Governance references and authority boundary | Implemented as references; policy/approval authority external |
| M10 | Revision-bound deterministic evaluation | Implemented as evaluation contract; real evaluators external |
| M11 | Tenant-scoped customer domain contracts | Implemented as contracts; customer application/API external |
| M12 | Input, tenant, secret, integrity and authority controls | Implemented as domain controls; infrastructure controls external |
| M13 | Health/readiness/idempotency contracts | Implemented as contracts; deployment/observability infrastructure external |
| M14 | Fail-closed certification-bundle validation contract | Implemented as a verifier contract; it does **not** self-certify a production system |

This is intentional. FDSE does not claim to implement a competing agent runtime, authorization kernel, sandbox, model gateway, secret manager, generic tool authority, GitHub service, CI service, observability stack, or deployment platform.

## Architectural invariant

> **FDSE owns engineering semantics; Agent Platform owns generic agent authority and execution infrastructure.**

Customer repositories, source code, build artifacts, logs, dependencies, model outputs, tool responses, and repository instructions are untrusted inputs.

## Security posture

The repository uses positive input validation, explicit tenant/repository scope, deterministic integrity digests, revision binding, fail-closed evaluation, secret redaction, least-privilege workflow permissions, and immutable GitHub Action references. These controls are aligned with OWASP ASVS 5.0 and NIST SSDF 1.1; NIST currently lists SSDF 1.2 as a draft. GitHub recommends full-length SHA pinning for Actions and explicit minimum workflow permissions.

## Development

    python -m pip install -e ".[dev]"
    ruff check .
    ruff format --check .
    mypy src
    pytest
    python -m build --no-isolation
    pip-audit --skip-editable
    python scripts/check_docs.py

## Phase authority

docs/architecture/ROADMAP.md is the canonical M0–M14 capability map. Phase documents must describe what FDSE owns, what it delegates, and what remains an external integration.
