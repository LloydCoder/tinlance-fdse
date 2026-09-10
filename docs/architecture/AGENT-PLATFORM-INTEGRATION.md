# Agent Platform Integration Contract

FDSE depends on `LloydCoder/tinlance-agent-platform` as an external/private platform dependency. At the time of the M0 audit, that repository contains its architecture README but no executable implementation yet; therefore FDSE defines a domain-side port without pretending that the platform API already exists.

## Required platform capabilities

FDSE will require platform-backed capabilities for:

- tenant-bound agent identity
- capability grants
- risk classification and policy decisions
- human approval references
- sandboxed execution
- command/filesystem/network controls
- secrets isolation
- bounded execution budgets/timeouts
- trajectory and provenance references
- audit/event correlation
- cancellation and recovery

## Call pattern

```text
FDSE workflow
   ↓
ExecutionRequest
   ↓
AgentPlatformPort
   ↓
Agent Platform authorization/policy/approval/sandbox
   ↓
controlled execution
   ↓
ExecutionHandle + trajectory/evidence references
   ↓
FDSE workflow
```

FDSE must never accept a model response as proof that an action was authorized.

## Versioning requirement

The integration must use a versioned, contract-tested platform API/SDK before M4. Until that exists, the FDSE port remains intentionally minimal and provider-neutral.

## Failure behavior

- Missing platform authorization: fail closed.
- Missing required approval: pause/escalate; never auto-promote.
- Expired execution handle: stop and request a new governed execution.
- Platform unavailable: do not silently fall back to unrestricted local execution.
- Tenant mismatch: reject the request.
- Unknown capability: reject the request.
