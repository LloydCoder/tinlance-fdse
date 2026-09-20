# FDSE Implementation Roadmap

Milestones are evidence gates, not file-count targets.

| Milestone | Outcome | Completion gate |
|---|---|---|
| M0 | Architecture & repository foundation | boundaries, contracts, invariant tests, security baseline and CI green |
| M1 | FDSE core domain | executable domain persistence + migrations + invariant tests |
| M2 | Project & repository intake | safe repository registration + deterministic intake evidence |
| M3 | Engineering context | reproducible stack/architecture/test/dependency context |
| M4 | Agent Platform integration | versioned platform API + fail-closed contract tests |
| M5 | Specialist engineering agents | bounded domain roles + evaluations |
| M6 | Engineering workflows | governed engineering lifecycle |
| M7 | Git/GitHub/CI integrations | least-privilege engineering adapters |
| M8 | Evidence & provenance | durable evidence lineage and verification |
| M9 | Human approval & policy | enforced risk-tier approval gates |
| M10 | Evaluation framework | reproducible benchmarks and regression gates |
| M11 | Customer API & console | tenant-safe customer/operator surfaces |
| M12 | Security hardening | threat model, abuse testing and supply-chain/sandbox validation |
| M13 | Production deployment | reproducible deployment, health, observability and rollback |
| M14 | End-to-end validation | representative governed engineering loop |

## State vocabulary

**Planned** = described but not implemented.  
**In progress** = implementation exists but acceptance gate is not satisfied.  
**Implemented** = code exists.  
**Tested** = relevant automated tests pass.  
**Verified** = acceptance evidence has been reviewed against the actual repository state.  
**Merged** = GitHub reports the PR as merged.  
**Production-ready** = all project-defined production gates are satisfied.

These states are deliberately not interchangeable.

## Current status

M0 is **in progress** on `feat/m0-architecture-foundation` and PR #1. M1 is not part of M0 and must not be inferred from the separate `feat/fdse-foundation` work.

M0 must not claim CI green or merged until GitHub confirms the final commit's checks and merge state.
