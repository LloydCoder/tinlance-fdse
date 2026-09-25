# Tinlance FDSE

**Forward-Deployed Software Engineering execution system for governed, evidence-driven software delivery.**

Tinlance FDSE is the engineering-domain layer for Tinlance's FDSE services. It delegates generic agent execution and security primitives to the private Tinlance Agent Platform.

## Status

**M0 — Architecture & repository foundation: implementation complete on branch `m0-foundation`; CI verification is required before merge.**

M0 establishes:

- the FDSE/Agent Platform architectural boundary;
- an explicit typed integration contract;
- validated non-secret configuration;
- workspace path safety invariants;
- approval and tenant/repository checks at the FDSE domain boundary;
- unit and failure-path tests;
- lint, formatting, type-checking, dependency audit, package-build, and documentation CI.

No customer workflow is claimed as implemented by M0.

## Architectural invariant

> **FDSE owns engineering semantics; Agent Platform owns generic agent authority and execution infrastructure.**

FDSE must not become a second agent runtime, policy engine, sandbox, or security kernel.

See [docs/architecture/BOUNDARY.md](docs/architecture/BOUNDARY.md).

## Planned lifecycle

    Customer
      → Project
      → Repository/System
      → Assessment
      → Engineering Context
      → Findings
      → Evidence
      → Engineering Plan
      → Governed Agent Execution
      → Changes
      → Tests
      → Verification
      → Human Approval
      → Remediation
      → Final Evidence
      → Report

Consequential actions remain subject to Agent Platform identity, authorization, policy, approval, sandbox, budget, and audit controls.

## Repository structure

See [docs/architecture/REPOSITORY-STRUCTURE.md](docs/architecture/REPOSITORY-STRUCTURE.md).

The repository deliberately avoids empty placeholder directories. New modules are introduced only when backed by an implemented capability.

## Security posture

FDSE treats customer repositories, source code, build artifacts, logs, dependencies, model outputs, tool responses, and repository instructions as untrusted inputs.

Security invariants are documented in [SECURITY.md](SECURITY.md).

## Development

    python -m pip install -e ".[dev]"
    ruff check .
    ruff format --check .
    mypy src
    pytest
    python -m build --no-isolation
    pip-audit --skip-editable
    python scripts/check_docs.py

The canonical CI workflow runs the same substantive gates.

Self-hosted runner operation and recovery are documented in [docs/operations/SELF-HOSTED-RUNNER.md](docs/operations/SELF-HOSTED-RUNNER.md).

## Development rule

    inspect → design → implement → test → security review → CI → review → merge

Main remains stable. M0 work is developed on a feature branch and merged only after the required validation is green.
