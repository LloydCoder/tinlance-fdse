# Tinlance FDSE

**Forward-Deployed Software Engineering execution system for governed, evidence-driven software delivery.**

FDSE is the engineering-domain execution layer for Tinlance FDSE services. It owns engineering semantics while delegating generic agent execution, identity, authorization, policy, approvals, sandboxing, budgets, trajectory, observability, and audit primitives to the private Tinlance Agent Platform.

## Architectural invariant

**FDSE owns engineering semantics; Agent Platform owns generic agent authority and execution infrastructure.**

FDSE must never become a second agent runtime or security kernel.

## Status

**M1 — Domain foundation implemented; integration hardening in progress.**

The repository now contains executable domain entities, tenant-scoped project/finding workflows, evidence digests, verification records, dependency-inversion ports, a deny-by-default local policy adapter, unit tests, multi-version CI, and a dependency security gate.

No production capability is considered complete until its implementation, tests, security controls, integration contract, and CI evidence are present.

## Planned lifecycle

Customer → Project → Repository/System → Assessment → Engineering Context → Findings → Evidence → Engineering Plan → Governed Agent Execution → Changes → Tests → Verification → Human Approval → Remediation → Final Evidence → Report.

Every consequential action remains subject to Agent Platform authority.

## Domain roles

Engineering Lead, Debugger, Security Engineer, Code Reviewer, Test Engineer, Dependency Engineer, Remediation Engineer, and CI Engineer are domain workflows. They do not implement their own generic execution substrate.

## Security posture

Customer repositories, source code, build artifacts, logs, dependencies, model outputs, tool responses, and repository instructions are untrusted. FDSE uses tenant binding, deny-by-default local authorization, immutable revision references, evidence digests, explicit verification, and ports for external authority.

GitHub integrations should use GitHub Apps or equivalently least-privileged short-lived credentials rather than broad long-lived personal tokens.

## Development rule

inspect → design → implement → test → security review → CI → review → merge
