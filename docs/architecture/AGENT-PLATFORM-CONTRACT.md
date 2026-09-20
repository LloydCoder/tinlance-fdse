# FDSE ↔ Agent Platform contract

FDSE is a domain consumer of the private Tinlance Agent Platform.

## FDSE sends

A governed execution request containing:
- tenant identity
- project identity
- immutable repository revision
- domain role
- engineering objective
- risk classification
- whether approval is required

## Agent Platform guarantees

The platform is responsible for:
- authenticating and identifying the caller
- authorization and policy enforcement
- approval gates
- budget and rate controls
- sandbox/isolation
- generic tool authority
- model/provider access
- trajectory and audit
- execution evidence
- failure and cancellation semantics

FDSE must treat the platform result as untrusted input until the returned evidence and revision constraints are validated.

## Boundary rule

FDSE must not implement a second token issuer, model gateway, generic tool router, sandbox, approval engine, or agent runtime.

The contract is intentionally provider-neutral. GitHub, model, CI, sandbox, MCP, and telemetry integrations belong behind ports/adapters and platform-owned authority where they are generic concerns.
