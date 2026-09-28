# M1 — Core Domain

M1 turns the M0 boundary into an executable engineering-domain model.

## Implemented

- tenant-owned projects bound to an immutable repository revision;
- assessments and engineering context;
- evidence records with canonical SHA-256 payload digests;
- findings with evidence references;
- verification results explicitly bound to a revision;
- engineering plans, change sets, and reports;
- explicit plan, change-set, and finding lifecycle transition rules, including approval state;
- dependency-inversion ports for persistence, repository providers, policy, and Agent Platform execution;
- deny-by-default local policy adapter;
- Agent Platform execution gateway that always requires approval and carries repository revision;
- deterministic in-memory stores conforming to the persistence ports for tests.

## Authority boundary

M1 does not authorize customer actions, issue credentials, execute shell commands, implement a sandbox, implement a model gateway, or replace Agent Platform policy/approval/audit infrastructure.

The Agent Platform remains authoritative for consequential execution. FDSE validates domain invariants and passes structured intent across the boundary.
