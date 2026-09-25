# Repository Structure

M0 establishes a minimal executable foundation. Empty placeholder directories are intentionally avoided.

    .
    ├── .github/workflows/ci.yml
    ├── docs/
    │   ├── architecture/
    │   │   ├── BOUNDARY.md
    │   │   └── REPOSITORY-STRUCTURE.md
    │   └── operations/
    │       └── SELF-HOSTED-RUNNER.md
    ├── src/fdse/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── contracts.py
    │   ├── errors.py
    │   ├── security.py
    │   └── service.py
    ├── tests/
    │   ├── test_config.py
    │   ├── test_security.py
    │   └── test_service.py
    ├── CONTRIBUTING.md
    ├── SECURITY.md
    ├── CHANGELOG.md
    ├── Makefile
    ├── pyproject.toml
    └── README.md

Future modules must be introduced because an implemented capability requires them, not to make the repository look complete.
