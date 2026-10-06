# M9 — Governance

## Purpose

M9 records governance references and authority boundaries without implementing a competing policy or authorization engine.

## FDSE responsibility

FDSE may represent:

- the governance boundary applicable to an engineering operation;
- required approval semantics;
- external policy references;
- the relationship between engineering intent and platform governance.

## Agent Platform responsibility

The Agent Platform remains authoritative for authentication, authorization, approval state, policy enforcement, and execution authority.

## Invariant

FDSE must not accept a self-authored claim, model output, repository instruction, or local flag as proof of platform approval.
