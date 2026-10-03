# E6 — Enterprise Validation, Certification & GA

E6 defines the final fail-closed validation and certification semantics for FDSE.

## Validation layers

The contract covers 28 layers:

Unit, Contract, Cross-Repository Contract, Integration, Security, Adversarial, Property/Invariant, Failure Injection, Workflow Recovery, Memory/Context Security, Multi-Agent, MCP/Tool Security, Supply Chain, Provenance, E2E, Performance, Load, Concurrency, Tenant Isolation, Migration, Disaster Recovery, Observability, Documentation, API Compatibility, Dependency Security, CI/CD, Release Certification, and Production Readiness.

## Phase coverage

The required phase set is exactly M0–M18 plus E1–E6. No M19 exists.

## Fail-closed certification

The validation graph requires exactly one evidence record for every phase/layer pair. Missing evidence, duplicate identity, non-SHA-256 digests, FAIL status, or UNKNOWN status prevents the enterprise gate from passing.

Passing repository validation is not equivalent to production certification. External production evidence must be supplied by the relevant Agent Platform, FDE Mastery, Tinlance, provider, deployment, observability, and customer systems.

## Definition of done

- all 28 validation layers are represented;
- M0–M18 and E1–E6 coverage is exact;
- evidence is immutable and digest-bound;
- validation is deterministic and insertion-order independent;
- failure and missing-evidence paths are fail-closed;
- public API, tests, README, roadmap, changelog, and repository structure are reconciled;
- external GA claims remain impossible without explicit production evidence.
