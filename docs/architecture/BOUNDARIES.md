# FDSE Architecture Boundaries

## Decision

FDSE is a specialized engineering-domain system on top of Tinlance Agent Platform.

### Agent Platform owns

- agent runtime and orchestration
- model/tool gateways
- identity and authentication/authorization
- policy and risk enforcement
- approvals
- sandboxing and filesystem/network restrictions
- secrets and capability grants
- budgets and resource limits
- generic trajectory, provenance and audit
- generic observability and memory/retrieval

### FDSE owns

- tenant-scoped customer/project/assessment engineering state
- repositories and engineering context
- findings and engineering evidence semantics
- investigation/remediation/verification semantics
- engineering workflows and specialist roles
- engineering-specific policies/evaluations
- Git/GitHub/CI engineering adapters
- engineering reports and customer-facing engineering API/console

FDSE must not recreate generic Agent Platform infrastructure.

## Dependency direction

```text
apps / adapters
      ↓
FDSE workflows
      ↓
FDSE domain
      ↓
ports / contracts
      ↓
Agent Platform
```

Framework and provider dependencies belong in adapters/infrastructure, not in the domain package.

## Trust boundary

All customer-controlled or externally produced content is untrusted: source code, documentation, issues, pull requests, commits, CI/build output, dependency metadata, generated artifacts, model output, tool output, scanner output and external API responses.

Untrusted content is data only. It cannot grant capability, approval, authorization or policy exceptions.

Human authority remains explicit: a model/finding/tool response cannot manufacture approval.

## Execution boundary

FDSE requests execution → Agent Platform authorizes/policies/approves → Agent Platform provisions controls → execution occurs → Agent Platform returns structured result/provenance → FDSE consumes the result.

FDSE has no local customer-code execution path in M0.
