# M2 — Intake

M2 defines the trusted FDSE intake boundary for externally supplied engineering work.

## Responsibilities

- require a valid request identifier and explicit tenant/repository scope;
- require a repository revision and bounded engineering objective;
- normalize surrounding whitespace exactly once at the domain boundary;
- reject NUL bytes and oversized objective/idempotency fields;
- require an idempotency key for repeatable submission semantics;
- produce an immutable, typed IntakeRecord.

## Non-responsibilities

Intake does not authenticate a caller, authorize an action, execute customer code, create a sandbox, invoke a model, or approve consequential work. Those concerns remain outside the FDSE domain boundary and, where generic authority is required, belong to the Tinlance Agent Platform.

## Security invariants

1. Untrusted input is positively validated before it reaches domain services.
2. Tenant and repository scope remain explicit and inseparable.
3. Validation failure is fail-closed.
4. Input normalization is deterministic and occurs before downstream processing.
5. The intake layer has no network, filesystem, subprocess, model, or repository-provider side effects.

These controls align with trusted service-layer validation in OWASP ASVS 5.0 and secure-development practices in NIST SSDF. They are domain controls, not a substitute for platform authorization or sandbox isolation.

## Acceptance criteria

- valid intake becomes an immutable IntakeRecord;
- malformed UUIDs, blank scope/revision/objective/idempotency values, NUL bytes, and oversized objectives are rejected;
- tests cover the rejection paths;
- M0/M1 architectural boundaries remain unchanged.
