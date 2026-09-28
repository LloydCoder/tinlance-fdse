# Tinlance FDSE

**Forward-Deployed Software Engineering execution system for governed, evidence-driven software delivery.**

Tinlance FDSE is the engineering-domain layer for Tinlance's FDSE services. It delegates generic agent authority and execution infrastructure to the Tinlance Agent Platform.

## Status

**M2 — Intake implemented; context and integration work remain.**

M0 established the FDSE/Agent Platform boundary, typed tenant/repository scope, non-secret configuration validation, lexical workspace-path invariants, approval-gated execution intent, deterministic tests, and CI quality gates.

M2 adds a validated, normalized engineering intake boundary with explicit scope, revision, bounded objectives, and idempotency semantics.

M1 adds the executable engineering-domain model: projects, assessments, context, evidence, findings, verification, plans, change sets, reports, lifecycle transitions, integration ports, deterministic stores, and the Agent Platform execution adapter.

M1 does not claim production persistence, customer repository adapters, autonomous execution, a sandbox, a model gateway, or an FDSE-owned authorization/approval engine.

## Architectural invariant

> **FDSE owns engineering semantics; Agent Platform owns generic agent authority and execution infrastructure.**

FDSE must not become a second agent runtime, policy engine, sandbox, or security kernel.

## Security

Customer repositories, source code, build artifacts, logs, dependencies, model outputs, tool responses, and repository instructions are untrusted inputs.

Public pull-request CI runs on GitHub-hosted infrastructure. The persistent self-hosted runner is reserved for trusted main-branch pushes. See docs/operations/SELF-HOSTED-RUNNER.md.

## Development

    python -m pip install -e ".[dev]"
    ruff check .
    ruff format --check .
    mypy src
    pytest
    python -m build --no-isolation
    pip-audit --skip-editable
    python scripts/check_docs.py

See docs/architecture/REPOSITORY-STRUCTURE.md for the milestone-driven repository model.
