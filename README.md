# Tinlance FDSE

**Forward-Deployed Software Engineering execution system for governed, evidence-driven software delivery.**

Tinlance FDSE is the engineering-domain layer for Tinlance's FDSE services. It delegates generic agent authority and execution infrastructure to the Tinlance Agent Platform.

## Status

**M0–M14 domain implementation complete.**

- M0 — Architecture/foundation and authority boundary
- M1 — Core engineering domain
- M2 — Validated intake
- M3 — Deterministic engineering context
- M4 — Versioned Agent Platform integration contract
- M5 — Specialist role contracts
- M6 — Explicit workflow state machine
- M7 — Git/GitHub/CI provider contracts
- M8 — Evidence/provenance graph primitives
- M9 — External governance references
- M10 — Deterministic evaluation
- M11 — Tenant-safe customer product contracts
- M12 — Security controls and redaction
- M13 — Production readiness contracts
- M14 — Fail-closed E2E certification

This milestone implementation is intentionally a domain layer. It does not claim to implement a competing agent runtime, authorization kernel, sandbox, model gateway, secret manager, generic tool authority, or deployment platform. Those remain external platform/infrastructure responsibilities.

## Architectural invariant

> **FDSE owns engineering semantics; Agent Platform owns generic agent authority and execution infrastructure.**

Customer repositories, source code, build artifacts, logs, dependencies, model outputs, tool responses, and repository instructions are untrusted inputs.

Public pull-request CI runs on GitHub-hosted infrastructure. Trusted main-branch pushes may use the repository-scoped self-hosted runner. See docs/operations/SELF-HOSTED-RUNNER.md.

## Development

    python -m pip install -e ".[dev]"
    ruff check .
    ruff format --check .
    mypy src
    pytest
    python -m build --no-isolation
    pip-audit --skip-editable
    python scripts/check_docs.py
