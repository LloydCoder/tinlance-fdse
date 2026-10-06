# M10 — Evaluation

## Purpose

M10 defines deterministic, revision-bound evaluation semantics.

## Rules

- Every evaluation case identifies the revision it evaluates.
- Every expected invariant must be explicitly represented.
- Missing cases or results produce an UNKNOWN outcome.
- A failing result produces FAIL.
- Unknown or incomplete evidence cannot silently become PASS.
- Model output is not the authority for pass/fail.

## Boundary

FDSE defines evaluation semantics. Concrete test engines, scanners, deployment checks, and external evidence collectors remain integration dependencies.

## Invariant

Evaluation must be reproducible from its case, result, revision, and satisfied-invariant set.
