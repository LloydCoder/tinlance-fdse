# Agent Platform Integration Contract

**Contract version:** FDSE-AP-0.1 (M0 design contract; not a production API)

FDSE depends on `LloydCoder/tinlance-agent-platform` as an external/private platform dependency. At the M0 audit, that repository had architecture documentation but no executable implementation. FDSE therefore defines only a provider-neutral port.

## Ownership

FDSE owns engineering semantics. Agent Platform owns generic execution authority and infrastructure: identity, authentication/authorization, policy, approvals, sandboxing, secrets, budgets, trajectory, generic provenance/audit and generic observability.

FDSE cannot grant itself authority by calling this port.

## Request contract

Required: tenant_id, actor_id, project_id, assessment_id, workflow_id, requested task, risk tier, correlation_id, idempotency_key.

Optional: requested_capabilities.

The tenant/project/assessment ancestry must be checked by FDSE before submission and independently enforced by Agent Platform.

## Response contract

Required: execution_id, execution status, provenance reference, evidence references.

A failed response must include a non-sensitive error code. Malformed or unknown responses are rejected; they are never treated as success.

## Semantics

- correlation_id links the request across FDSE and Agent Platform.
- idempotency_key prevents accidental duplicate submission where the platform supports idempotency.
- execution_id identifies a platform execution; it is not a request ID.
- evidence references point to observable evidence and do not by themselves establish truth.
- provenance identifies how an execution/result was produced; it is not an authorization grant.
- approval is authoritative only when issued by Agent Platform.

## Fail-closed behavior

- missing authority context → deny
- tenant mismatch → deny
- unknown capability → deny
- unavailable authority provider → no consequential execution
- missing approval → no consequential execution
- malformed response → reject
- unknown execution state → reject
- platform output or model output → never treated as authority

FDSE must never fall back to local unrestricted execution when the platform is unavailable.

## Compatibility

M4 must replace this design contract with a versioned, contract-tested platform API/SDK and explicit compatibility policy. No undocumented Agent Platform internals may become an FDSE dependency.
