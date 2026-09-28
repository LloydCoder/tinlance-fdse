# Tinlance FDSE

**Forward-Deployed Software Engineering execution system for governed, evidence-driven software delivery.**

Tinlance FDSE is the engineering-domain layer for Tinlance's FDSE services. It delegates generic agent authority and execution infrastructure to the Tinlance Agent Platform.

## Status

**M0 — Architecture & repository foundation: merged to main.**

M0 establishes the FDSE/Agent Platform boundary, typed tenant/repository scope, minimal evidence/provenance/integrity/verification vocabulary, non-secret configuration validation, lexical workspace-path invariants, approval-gated execution intent, deterministic tests, and CI quality gates.

M0 does not claim a customer workflow, production execution engine, generic authorization system, sandbox, persistence layer, or autonomous agent runtime.

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
