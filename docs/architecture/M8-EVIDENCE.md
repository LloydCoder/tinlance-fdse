# M8 — Evidence

## Purpose

M8 provides domain primitives for representing evidence and provenance relationships.

## Semantics

Evidence is distinct from:

1. observations;
2. findings;
3. evaluations;
4. certification.

Evidence records are revision- and project-scoped and support deterministic integrity representation.

## Graph model

Evidence graph primitives represent typed nodes and relationships. Graph serialization and integrity digests are deterministic so equivalent domain state can be compared reliably.

## Boundary

FDSE defines evidence semantics. Durable evidence storage, event retention, trajectory infrastructure, and production observability remain external platform responsibilities.

## Invariant

Evidence cannot manufacture authority. A piece of evidence can support an evaluation or certification decision only when it satisfies the applicable contract.
