# M18 — Agent Ecosystem Runtime

M18 completes the FDSE domain/runtime roadmap with governed ecosystem semantics
for skills, applications, extensions, connectors, and packages.

## Capabilities

- versioned extension manifests;
- artifact and signature digests;
- publisher/source/build/attestation provenance;
- dependency constraints and deterministic compatibility checks;
- explicit capability requests;
- externally authorized capability grants;
- verified-before-enable lifecycle;
- disable, quarantine, and rollback semantics;
- deterministic manifest integrity digests.

## Security boundary

FDSE does not verify cryptographic signatures itself, issue capability grants,
execute extension code, provide sandboxing, expose network credentials, or
replace Agent Platform authorization.

An extension can request capabilities in its manifest, but it cannot grant
those capabilities to itself. A grant is accepted only from the configured
external authority and only for capabilities already declared by the manifest.

Quarantined extensions cannot be enabled. Rollback selects the newest prior
registered version deterministically.

## Enterprise ecosystem model

The intended production chain is:

    manifest
      -> artifact/provenance verification
      -> external signature verification
      -> external capability grant
      -> FDSE dependency/lifecycle checks
      -> Agent Platform sandbox/policy
      -> execution

This separation follows modern agent interoperability patterns: protocols can
describe agents and capabilities, but interoperability does not itself confer
authorization.
