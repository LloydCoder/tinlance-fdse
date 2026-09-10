# FDSE Implementation Roadmap

Milestones are evidence gates, not file-count targets.

| Milestone | Outcome | Completion gate |
|---|---|---|
| M0 | Architecture and repository foundation | contracts, boundaries, tests, CI and audit are green |
| M1 | FDSE core domain | durable domain model + migrations + invariant tests |
| M2 | Project/repository intake | safe repository registration and deterministic intake evidence |
| M3 | Engineering context | reproducible stack/architecture/test/dependency context |
| M4 | Agent Platform integration | versioned platform contract + fail-closed integration tests |
| M5 | Specialist agents | role-specific agents with bounded capabilities and evals |
| M6 | Engineering workflows | intake/assessment/investigation/remediation/verification/reporting |
| M7 | Git/GitHub/CI | least-privilege adapters and end-to-end repository change flow |
| M8 | Evidence/provenance | durable evidence graph and verification lineage |
| M9 | Human approvals/policies | enforced risk-tier approval gates with negative tests |
| M10 | Evaluation | reproducible engineering benchmarks and regression gates |
| M11 | Customer API/console | tenant-safe operator/customer experience |
| M12 | Security hardening | threat model, abuse tests, supply-chain and sandbox validation |
| M13 | Production deployment | reproducible deployment, health, observability and rollback |
| M14 | End-to-end validation | representative customer repositories pass the complete governed loop |

## Immediate next order

1. Complete M0 CI and architecture verification.
2. Build Agent Platform's executable foundation in its own repository; FDSE must not duplicate it.
3. Implement M1 FDSE domain persistence and tenancy ancestry.
4. Implement M2 repository intake using read-only access first.
5. Add M3 engineering context extraction before enabling autonomous remediation.

Autonomous code modification is intentionally downstream of safe intake, context, platform authorization and sandboxing.
