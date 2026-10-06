# M6 — Workflows

## Purpose

M6 defines the FDSE lifecycle state machine.

## Semantics

Workflow transitions are:

- explicit;
- finite;
- fail-closed;
- revision-aware;
- validated before state change.

Invalid transitions must be rejected rather than coerced into a nearby state.

## Boundary

M6 defines domain transition semantics. Durable scheduling, persistence, retries, recovery, and execution orchestration are external runtime responsibilities and are expanded by M16.

## Invariant

A workflow state must not silently cross tenant, repository, or revision scope, and a transition must not grant execution authority.
