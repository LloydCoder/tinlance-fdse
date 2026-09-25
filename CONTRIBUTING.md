# Contributing

## Development flow

    inspect → design → implement → test → security review → CI → review → merge

Keep changes narrowly scoped. Preserve the FDSE/Agent Platform boundary.

## Local validation

    python -m pip install -e ".[dev]"
    ruff check .
    ruff format --check .
    mypy src
    pytest
    pip-audit --skip-editable
    python -m build --no-isolation
    python scripts/check_docs.py

## Rules

- Do not add credentials to source, fixtures, logs, or tests.
- Do not add shell-command execution to the domain layer.
- Do not weaken approval or tenant checks to make tests pass.
- Add regression tests for security defects.
- Keep documentation synchronized with executable behavior.
- Self-hosted CI runners are reserved for trusted private-repository workflows; do not route public-repository or untrusted fork workloads to the shared runner.
