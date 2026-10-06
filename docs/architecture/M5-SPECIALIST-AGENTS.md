# M5 — Specialist Agents

## Purpose

M5 defines specialist roles as domain contracts rather than autonomous runtime implementations.

A specialist specification identifies the role, engineering scope, expected evidence, and output requirements needed for governed engineering work.

## Boundary

FDSE owns:

- specialist role definitions;
- evidence requirements;
- domain input/output contracts;
- scope and revision binding.

The Agent Platform owns:

- agent identity;
- model invocation;
- tool authority;
- execution isolation;
- delegation runtime;
- approvals.

## Invariant

A specialist's output is untrusted until evaluated under the applicable FDSE contracts. A model or agent cannot self-authorize consequential work.
