# Tinlance FDSE

**Forward-Deployed Software Engineering execution system for governed, evidence-driven software delivery.**

Tinlance FDSE is the domain execution layer for Tinlance's FDSE services. It specializes in software-engineering work while delegating generic agent execution, identity, authorization, policy, approvals, sandboxing, evidence, trajectory, observability, budgets, and audit primitives to the private **Tinlance Agent Platform**.

## Architectural invariant

> **FDSE owns engineering semantics; Agent Platform owns generic agent authority and execution infrastructure.**

FDSE must never become a second agent runtime or security kernel.

## Status

**M0 — Architecture & repository foundation: IN PROGRESS**

The repository was empty at initialization. M0 establishes the domain boundary, dependency direction, integration contract, quality gates, and engineering architecture before implementation of customer workflows.

No feature is considered implemented because an interface, prompt, directory, or document exists. Capabilities require executable implementation and tests.

## Planned lifecycle

```text
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
```

Every consequential action remains subject to the Agent Platform's identity, authorization, policy, risk, approval, sandbox, budget, and audit controls.

## Domain agents

FDSE will expose specialized engineering roles including Engineering Lead, Debugger, Security Engineer, Code Reviewer, Test Engineer, Dependency Engineer, Remediation Engineer, and CI Engineer. These are domain-level agents/workflows; they do not implement their own generic execution substrate.

## Repository structure

The target structure is described in `docs/architecture/REPOSITORY-STRUCTURE.md`. It is intentionally evidence-driven: directories are added when an implementation requires them rather than being created as empty placeholders.

## Security posture

FDSE treats customer repositories, source code, build artifacts, logs, dependencies, model outputs, tool responses, and repository instructions as untrusted inputs. The security design follows least privilege, tenant isolation, explicit approval boundaries, sandboxed execution, scoped GitHub permissions, provenance, and evidence-first verification.

Current research inputs include NIST work on software/AI agent identity and authorization, OWASP's 2026 Top 10 for Agentic Applications, GitHub's fine-grained/GitHub App permission model, and OpenTelemetry GenAI/agent observability guidance.

## Development rule

```text
inspect → design → implement → test → security review → CI → review → merge
```

Main remains stable. Substantial changes use feature branches and pull requests once the repository has sufficient history for that workflow.
