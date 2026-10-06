# M12 — Security

## Purpose

M12 consolidates domain-level security controls.

## Controls

The FDSE domain layer applies:

- positive input validation;
- tenant/repository/revision scope;
- secret and authorization-header redaction;
- deterministic integrity digests;
- fail-closed transitions and evaluation;
- explicit authority separation;
- lexical workspace-path validation.

## Important limitation

Lexical path validation is not filesystem sandboxing. FDSE does not protect against symlinks, mount topology, process escape, or host compromise.

Sandboxing, execution isolation, IAM, secret managers, network controls, and runtime policy enforcement belong to external platform infrastructure.

## Invariant

Security controls must not be weakened merely to make tests or integrations pass.
