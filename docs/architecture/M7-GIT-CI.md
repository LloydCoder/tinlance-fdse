# M7 — Git/GitHub/CI

## Purpose

M7 defines provider-neutral contracts for repository and CI systems.

## Contract requirements

Provider adapters should expose revision-bound information such as:

- repository identity;
- concrete commit/revision;
- changed state;
- check results;
- provider metadata required by the domain contract.

## Security boundary

Repository contents and CI output are untrusted. Provider adapters do not become generic command runners or execution authorities.

## Determinism

Engineering state should be tied to a concrete revision rather than a mutable branch name. CI evidence must remain attributable to the revision it evaluates.

## External dependency

GitHub, other Git providers, and CI services remain external systems. M7 does not implement them.
