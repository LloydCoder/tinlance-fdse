# FDSE Repository Structure

The repository uses domain-driven boundaries. A directory is created when executable code or a maintained artifact requires it; empty placeholder trees are not considered architecture.

```text
apps/
  api/                 customer/project/assessment API boundary
  worker/              asynchronous FDSE workflow boundary
  console/             operator/customer UI boundary

packages/
  fdse_core/           domain model and stable ports
  projects/            project/repository lifecycle
  assessments/         assessment orchestration and state
  findings/            finding lifecycle and severity/confidence
  evidence/            engineering evidence semantics
  reports/             evidence-backed report generation
  remediation/         approved change plans and remediation state
  engineering_context/ repository-derived context
  repository_intelligence/ stack/architecture/test/dependency analysis
  workflow_engine/     FDSE-specific workflow definitions
  integrations/        external engineering adapters
  common/              only FDSE-specific shared primitives

agents/                specialized engineering roles
skills/                engineering-specific skills
workflows/             customer engineering workflows
evals/                 reproducible engineering evaluations
tests/                 unit, integration, security and architecture tests
database/              migrations and schema ownership
infrastructure/        deployment/runtime configuration
security/              FDSE threat models and security tests
docs/                  architecture, operations and evidence
research/               maintained research notes and benchmarks
.github/                CI and repository governance
```

The structure deliberately avoids a local `runtime`, `sandbox`, `identity`, `policy`, `approval`, `audit`, `memory`, or `model_gateway` package because those are Agent Platform responsibilities.
