# M11 — Customer Product

## Purpose

M11 defines tenant-safe customer-domain contracts.

## Scope

Customer project and request records bind engineering work to:

- tenant;
- repository;
- revision;
- objective or project identity.

## Boundary

FDSE owns the domain contract. Customer-facing API, UI, billing, identity, authentication, and persistence infrastructure remain external.

## Invariant

Tenant boundaries must be checked before domain records are accessed or used for customer-facing operations. Cross-tenant mixing is rejected.

## Integration note

M11 does not define a customer application. It defines the semantics that a customer application must preserve.
