# M13 — Production

## Purpose

M13 defines domain contracts for health, readiness, and idempotency.

## Semantics

Readiness and health contracts distinguish domain state from deployment health. Idempotency records prevent repeated requests from being treated as new work when the same scoped key is reused.

## External responsibilities

Deployment, monitoring, alerting, SLOs, durable storage, infrastructure health, and production incident response remain external.

## Invariant

A green FDSE readiness contract is not evidence that the complete production system is healthy.

## Relationship to later phases

M13 establishes the domain contract. E5 and E6 add cross-system validation and certification semantics without absorbing external infrastructure into FDSE.
