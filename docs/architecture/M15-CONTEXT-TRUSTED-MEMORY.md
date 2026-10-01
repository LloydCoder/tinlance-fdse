# M15 — Context + Trusted Memory

M15 extends M3 context with bounded, revision-scoped memory. Memory is a
provenance-bearing context source, never an authority source.

## Invariants

- Every memory is bound to exactly one tenant, repository, and revision.
- Memory content is content-addressed by SHA-256.
- Provenance revision must match the memory revision.
- Records are append-only by immutable memory identifier.
- Expired memory is unavailable to active reads.
- Cross-scope reads fail closed.
- Deterministic ordering produces reproducible memory and envelope digests.
- Secret-like values are redacted when converted back into context.
- VERIFIED means provenance/integrity verification only; it does not grant
  authorization, approval, capabilities, identity, or execution authority.

## Boundary

FDSE owns memory semantics and deterministic context composition. Durable memory
storage, identity, authorization, encryption/KMS, retention enforcement, and
production access control remain infrastructure/Agent Platform responsibilities.

## Enterprise alignment

M15 uses explicit provenance and integrity rather than treating model output or
repository content as trusted authority. This follows the repository's existing
fail-closed trust model and NIST SSDF's emphasis on secure development practices
throughout the lifecycle.
