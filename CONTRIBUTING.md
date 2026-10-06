# Contributing to Tinlance FDSE

Thank you for contributing. FDSE is security-sensitive domain infrastructure, so correctness and boundary preservation matter more than change volume.

## Before you start

1. Read [README.md](README.md).
2. Read [docs/architecture/BOUNDARY.md](docs/architecture/BOUNDARY.md).
3. Read [SECURITY.md](SECURITY.md) for vulnerability handling.
4. Search existing issues and pull requests before opening new work.

## Development flow

~~~text
fork → branch → implement → test → security review → CI → review → merge
~~~

Keep pull requests focused. Do not combine unrelated refactors with behavioral changes.

## Local setup

~~~bash
python -m pip install -e ".[dev]"
make check
~~~

The full check includes:

- Ruff linting and formatting;
- strict mypy type checking;
- pytest;
- pip-audit;
- package build;
- documentation-link validation.

## Coding standards

- Python 3.12+.
- Prefer explicit, typed domain contracts.
- Preserve tenant, repository, and revision scope.
- Fail closed on malformed, stale, conflicting, or insufficient input.
- Keep observations, evidence, findings, evaluations, and certification distinct.
- Never add credentials, secrets, or customer data to source, tests, fixtures, logs, or documentation.
- Do not introduce shell execution, sandboxing, authorization, model credentials, or generic agent authority into FDSE.
- Add regression tests for security-sensitive behavior.
- Update architecture documentation when contracts or invariants change.

## Commits

Use Conventional Commit-style messages where practical, for example:

~~~text
feat(intake): add revision-bound validation
fix(security): reject cross-tenant evidence
docs(architecture): reconcile M18 boundary
test(certification): cover duplicate phase evidence
~~~

## Pull requests

A pull request should explain:

- what changed and why;
- affected contracts or invariants;
- tests run locally;
- security implications;
- documentation changes;
- any external integration evidence required.

Do not claim production integration, certification, or GA readiness from unit/CI results alone.

## Security-sensitive changes

If you discover a vulnerability, do not open a public issue. Follow [SECURITY.md](SECURITY.md).

## License

By contributing, you agree that your contributions are submitted under the repository's Apache-2.0 license unless a separate written agreement states otherwise.
