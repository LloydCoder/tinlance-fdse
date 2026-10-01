# M17 — Multi-Agent Runtime

M17 defines FDSE-side semantics for supervised multi-agent engineering work.

## Capabilities

- authenticated agent identity attestations;
- bounded parent/child delegation;
- tenant/repository/revision-scoped child tasks;
- read-only shared context references;
- explicit capability requests without capability granting;
- authenticated, revision-scoped messages;
- monotonic conversation sequencing and idempotent message identifiers;
- deterministic child-result aggregation;
- explicit escalation and provenance;
- terminal task/result semantics.

## Security boundary

Identity verification, authentication, authorization, capability grants, model
access, process isolation, sandboxing, network policy, quotas, and consequential
execution remain Agent Platform authority.

FDSE never treats a delegation request, message, capability request, or model
result as an authorization grant.

## Anti-spoofing

A message is accepted only when its attestation identifies the exact sender,
the external verifier accepts the attestation, its payload digest matches, and
its conversation sequence is the next expected sequence.

Delegated tasks preserve the parent's tenant, repository, and revision scope.
Shared context is explicitly read-only.
