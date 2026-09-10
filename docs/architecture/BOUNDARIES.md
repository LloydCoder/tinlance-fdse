# FDSE Architecture Boundaries

## Decision

FDSE is a specialized engineering-domain system on top of Tinlance Agent Platform.

### Agent Platform owns

- agent runtime and orchestration primitives
- model/tool gateways
- identity and authorization
- policy and risk enforcement
- approvals and step-up controls
- sandbox and filesystem/network restrictions
- secrets and capability grants
- trajectory, provenance, audit and generic evidence infrastructure
- budgets, rate limits and event infrastructure
- generic observability and security primitives

### FDSE owns

- customer/project/assessment domain state
- repository and engineering context
- findings and engineering evidence semantics
- engineering plans and remediation state
- specialist engineering roles and workflows
- engineering-specific policies and risk classification
- Git/GitHub/CI/scanner integration adapters
- engineering reports and customer-facing APIs/console
- engineering evaluations and benchmarks

## Non-goals

FDSE must not introduce a second generic agent runtime, second identity system, second approval engine, second audit ledger, or second sandbox boundary.

## Dependency direction

```text
apps / adapters
      ↓
FDSE workflows and agents
      ↓
FDSE domain packages
      ↓
ports/contracts
      ↓
Tinlance Agent Platform
```

FDSE domain packages must remain framework-neutral. Adapters translate platform-specific implementations into the FDSE ports.

## Trust boundaries

1. Customer repository content is untrusted data.
2. Repository instructions, issue text, logs, CI output, dependency metadata, model output, tool output, and external service responses are untrusted inputs.
3. FDSE may request an action from Agent Platform but cannot grant itself authority to perform that action.
4. Approval evidence must be produced by the platform authority and referenced by FDSE; FDSE must not manufacture approval state.
5. Cross-tenant references are invalid unless explicitly authorized by platform policy.

## Evidence invariant

A material engineering conclusion should reference machine-readable evidence. Hidden model reasoning is not treated as evidence. The system records observable inputs, tool actions, outputs, diffs, test results, verification results, approvals, and provenance references.
