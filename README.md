# Tinlance FDSE

**A Python domain layer for governed, evidence-driven forward-deployed software engineering.**

[![CI](https://github.com/LloydCoder/tinlance-fdse/actions/workflows/ci.yml/badge.svg)](https://github.com/LloydCoder/tinlance-fdse/actions/workflows/ci.yml) [![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

~~~mermaid
flowchart TD
    A[Customer engineering work] --> B[Tinlance FDSE]
    B --> B1[Intake + scope]
    B1 --> B2[Context + planning]
    B2 --> T

    subgraph T[Transformation domain]
        T1[Baseline current state] --> T2[Classify target intent]
        T2 --> T3[Define target state]
        T3 --> T4[Transformation plan + realization]
        T4 --> T5[Governed execution binding]
        T5 --> T6[Measure baseline vs target]
        T6 --> T7[Outcome + evidence]
        T7 --> T8[Handoff + acceptance]
        T8 --> T9[Replication kit]
    end

    T --> B3[Evidence + evaluation]
    B3 --> B4[Workflow + certification]
    B4 --> C[Versioned governed intent]
    C --> D[Tinlance Agent Platform]
    D --> D1[Identity + authorization]
    D --> D2[Approvals + policy]
    D --> D3[Runtime + sandbox]
    D --> D4[Tools + budgets + audit]

    T5 -. execution authority .-> D
    D --> T6
    D --> T7
~~~

> [!NOTE]
> FDSE is the engineering-domain layer, not the generic agent authority layer. Identity, authorization, approvals, sandboxing, model access, budgets, and runtime authority belong to the Tinlance Agent Platform. The Transformation domain defines the engineering transformation lifecycle and evidence contracts; it does not become the execution authority.

## Why FDSE

FDSE turns untrusted engineering inputs into explicit, tenant- and revision-scoped domain objects, evidence, evaluations, workflow intent, and certification semantics.

| FDSE provides | FDSE deliberately does not provide |
|---|---|
| Engineering entities and lifecycle contracts | Authentication or authorization |
| Revision-bound context and evidence | Generic agent execution |
| Fail-closed workflow semantics | Filesystem/process sandboxing |
| Git/CI provider contracts | Model gateway or model credentials |
| Evidence and provenance primitives | Durable platform infrastructure |
| Deterministic evaluation and certification | Deployment, billing, or production monitoring |

**Core boundary:** FDSE owns engineering semantics; the Tinlance Agent Platform owns generic agent authority and execution infrastructure.

## Quick Start

Requires Python 3.12+.

~~~bash
git clone https://github.com/LloydCoder/tinlance-fdse.git
cd tinlance-fdse
python -m pip install -e ".[dev]"
python -c "import fdse; print(fdse.__version__)"
~~~

Expected result: `1.9.0`.

## Installation

### Development install

~~~bash
python -m pip install -e ".[dev]"
~~~

### Runtime/package install

Build a distribution with:

~~~bash
python -m build --no-isolation
~~~

Then install the generated wheel from `dist/`.

### Requirements

- Python 3.12 or newer.
- No runtime third-party dependencies are required by the package.
- Development tooling is declared in `pyproject.toml`.

## Usage

The public API is exported from `fdse`.

### Basic: create a revision-bound project

~~~python
from uuid import uuid4

from fdse import Project, RepositoryRef

project = Project.create(
    tenant_id=uuid4(),
    name="customer-api",
    repository=RepositoryRef(
        provider="github",
        owner="example",
        name="customer-api",
        revision="a" * 40,
    ),
)

print(project.project_id)
~~~

### Advanced: evaluate evidence-bound work

~~~python
from fdse import (
    EvaluationCase,
    EvaluationOutcome,
    EvaluationResult,
    EvaluationSuite,
)

case = EvaluationCase(
    case_id="tests-pass",
    objective="verify the pinned revision",
    revision="a" * 40,
    expected_invariants=("tests_pass",),
)

result = EvaluationResult(
    case_id="tests-pass",
    outcome=EvaluationOutcome.PASS,
    observations=("pytest completed successfully",),
    revision="a" * 40,
    satisfied_invariants=("tests_pass",),
)

assert EvaluationSuite().evaluate((case,), (result,)) is EvaluationOutcome.PASS
~~~

FDSE objects are contracts and domain semantics. Consequential actions must cross the Agent Platform governance boundary.

## Configuration and limits

| Area | Default / requirement |
|---|---|
| Python | >= 3.12 |
| Package version | 1.9.0 |
| Runtime dependencies | None |
| Ruff line length | 100 |
| Mypy | Strict |
| Tests | `tests/` |
| Documentation validation | `scripts/check_docs.py` |
| CI runners | GitHub-hosted |
| Action references | Full commit SHA |
| Execution authority | External Agent Platform |

## Features

| Capability | Status |
|---|---|
| M0–M14 FDSE domain contracts | Implemented |
| M15 trusted memory semantics | Implemented |
| M16 workflow runtime semantics | Implemented |
| M17 multi-agent semantics | Implemented |
| M18 governed ecosystem semantics | Implemented |
| E2 engineering intelligence | Implemented |
| E3 assurance/security/supply-chain semantics | Implemented |
| E4 evidence lineage/incident/resilience semantics | Implemented |
| E5 production-integration contracts | Implemented; external production evidence required |
| E6 validation/certification contracts | Implemented; external GA evidence required |
| Transformation P1–P15 enterprise capability | Implemented at repository/domain level; external production, customer outcome, and replication evidence remain required |

> [!WARNING]
> “Implemented” means the FDSE-side contracts, invariants, tests, and documentation exist. It does not mean external production infrastructure, customer integrations, or the Agent Platform are deployed or healthy.

## Security model

Customer repositories, source code, configuration, generated artifacts, dependency metadata, model output, tool output, external responses, and build/test output are untrusted.

FDSE is fail-closed by design:

1. scope remains bound to tenant, repository, and revision;
2. mutable branch state is not a substitute for a concrete revision;
3. evidence, findings, evaluation, and certification remain distinct;
4. untrusted content cannot grant authority;
5. consequential execution requires the Agent Platform governance path.

See [SECURITY.md](SECURITY.md) and [docs/architecture/BOUNDARY.md](docs/architecture/BOUNDARY.md).

## Documentation

| Guide | Purpose |
|---|---|
| [Architecture roadmap](docs/architecture/ROADMAP.md) | Canonical M0–M18 and E1–E6 capability map |
| [Boundary](docs/architecture/BOUNDARY.md) | FDSE ↔ Agent Platform authority boundary |
| [Repository structure](docs/architecture/REPOSITORY-STRUCTURE.md) | Source, tests, and documentation map |
| [M15–M18 architecture](docs/architecture/) | Runtime and ecosystem contracts |
| [Enterprise validation](docs/architecture/E6-VALIDATION-CERTIFICATION-GA.md) | Validation and GA semantics |
| [Transformation Domain](docs/architecture/TRANSFORMATION-DOMAIN.md) | P1–P15 transformation lifecycle, Agent-System binding, measurement, handoff, and replication contracts |
| [Classification Taxonomy](docs/architecture/CLASSIFICATION-TAXONOMY.md) | Canonical DELETE/CODE/AGENT/HUMAN decision semantics |
| [Operations](docs/operations/SELF-HOSTED-RUNNER.md) | Historical runner decommissioning guidance |
| [Changelog](CHANGELOG.md) | Release history |

The documentation is organized primarily as architecture/reference material. Executable behavior remains the source of truth for contracts and tests.

## Development

~~~bash
python -m pip install -e ".[dev]"
make check
~~~

The CI quality gate runs linting, formatting checks, strict typing, tests, dependency auditing, packaging, documentation-link validation, and artifact inspection. Pull requests and merge queues additionally test Python 3.12 and 3.13.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Security-sensitive changes must preserve the FDSE/Agent Platform boundary and include regression coverage.

## License

Tinlance FDSE is licensed under the [Apache License 2.0](LICENSE).

Copyright © 2026 Tinlance Limited.

## Support

For usage and contribution questions, see [SUPPORT.md](SUPPORT.md). Report security vulnerabilities privately according to [SECURITY.md](SECURITY.md).

<details>
<summary>Roadmap and release semantics</summary>

The core roadmap ends at M18. Enterprise closure is tracked separately as E1–E6; there is intentionally no M19.

E5 and E6 remain fail-closed on external production evidence. A green repository CI run is not an external production certification.

</details>
