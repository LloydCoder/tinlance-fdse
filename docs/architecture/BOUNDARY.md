# FDSE / Agent Platform Boundary

## Purpose

FDSE is the engineering-domain layer. The private Tinlance Agent Platform is the authority for generic agent execution and security primitives.

### FDSE owns

- engineering task semantics;
- repository and project context;
- engineering planning;
- domain-specific roles and workflows;
- engineering verification semantics;
- domain reports and delivery state.

### Agent Platform owns

- identity and authentication;
- authorization and policy enforcement;
- approval workflows;
- agent/runtime execution;
- sandboxing and isolation;
- budgets and quotas;
- evidence and trajectory primitives;
- observability;
- audit logging;
- generic tool capability control.

FDSE must consume these capabilities through explicit interfaces. It must not create a competing runtime, policy engine, sandbox, or audit kernel.

## Trust rule

All customer-controlled repository content, repository instructions, source code, generated artifacts, model output, tool output, dependency metadata, and external responses are untrusted.

FDSE domain logic must not elevate untrusted content into authority.

## Consequential actions

Any action that can modify customer systems, repositories, infrastructure, credentials, deployments, or other durable state must cross the Agent Platform approval and policy boundary before execution.

## M0 contract

The package contract defines a narrow integration boundary. It carries engineering intent rather than shell commands, credentials, or host-specific execution parameters.
