# Changelog

## 0.2.0 — M1

- Added immutable core engineering-domain entities and lifecycle states.
- Bound projects, evidence, findings, verification, plans, changes, and reports to project/repository revisions.
- Added canonical evidence hashing and integrity-chain helpers.
- Added explicit lifecycle transition rules with invalid-transition rejection.
- Added dependency-inversion ports for persistence, repository providers, policy, and Agent Platform execution.
- Added deny-by-default local policy and approval-preserving execution adapter.
- Added deterministic in-memory stores and M1 regression tests.

## 0.1.0 — M0

- Established the FDSE domain package.
- Established the FDSE/Agent Platform boundary contract.
- Added configuration validation and workspace path validation.
- Added approval, task, and tenant/repository invariants at the domain service boundary.
- Added gateway contract validation and failure-path regression tests.
- Added documentation link validation.
- Hardened self-hosted CI workflow routing and action pinning.
- Added the self-hosted runner recovery and security runbook.
- Added unit and failure-path tests.
- Added CI quality and dependency-security gates.
