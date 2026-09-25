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

## Approval semantics

ExecutionRequest.approval_required=True means that the requested consequential operation requires the Agent Platform approval/governance path. It is not an approval grant, approval attestation, or evidence that a human or policy engine has already approved the operation.

FDSE does not create, verify, or substitute for Agent Platform approval evidence. The Agent Platform remains authoritative for authorization and approval state. M0 therefore rejects requests that disable the approval requirement and otherwise delegates the request to the platform boundary.

## M0 gateway lifecycle boundary

M0 defines only a submit() integration boundary returning an opaque ExecutionHandle. The handle identifies a platform-owned execution lifecycle.

M0 intentionally does not define APIs for polling or querying execution state, retrieving evidence or trajectories, cancelling execution, changing execution policy, or controlling runtime resources. Those lifecycle capabilities belong to later FDSE/Agent Platform integration work.

The status values on the M0 handle describe platform lifecycle states that may be returned by the boundary; they do not imply that submit() is a terminal-state operation.

## Workspace-path boundary

FDSE's workspace-path validator performs lexical validation only: relative-path syntax, POSIX separators, NUL rejection, and lexical .. traversal rejection.

It is not a filesystem sandbox. It does not resolve filesystem objects or protect against symlinks, mount points, bind mounts, or other filesystem topology. Filesystem isolation and execution containment are Agent Platform responsibilities.

## M0 contract

The package contract defines a narrow integration boundary. It carries engineering intent rather than shell commands, credentials, or host-specific execution parameters.
