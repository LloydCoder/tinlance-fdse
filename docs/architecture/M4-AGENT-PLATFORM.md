# M4 — Agent Platform Integration

## Purpose

M4 defines the versioned contract between FDSE engineering semantics and the Tinlance Agent Platform.

## FDSE responsibility

FDSE constructs explicit engineering intent. The intent is scoped to the customer engineering context and must not contain host-specific execution authority, credentials, or shell commands.

## Platform responsibility

The Agent Platform remains authoritative for:

- identity and authentication;
- authorization and policy;
- human approvals;
- runtime execution;
- sandboxing and isolation;
- model and tool access;
- budgets and quotas;
- audit and observability.

## Invariant

FDSE must never interpret an approval-required flag as an approval grant. Consequential actions cross the platform governance boundary.

## Evidence boundary

A successful FDSE contract test proves the adapter semantics. It does not prove that a production Agent Platform endpoint is deployed or healthy.
