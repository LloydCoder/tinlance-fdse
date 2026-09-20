# FDSE repository structure

FDSE is organized around domain semantics, application workflows, infrastructure adapters, and verification. Generic agent authority is not implemented here.

- src/fdse/domain.py: immutable domain entities and lifecycle states.
- src/fdse/ports.py: dependency-inversion ports for persistence, policy, execution, and repository providers.
- src/fdse/service.py: application orchestration.
- src/fdse/evidence.py: canonicalization and evidence digests.
- src/fdse/store.py: deterministic local adapters for tests.
- src/fdse/policy.py: deny-by-default local policy adapter.
- tests/: executable acceptance and unit tests.
- .github/workflows/ci.yml: test, lint, compile, and dependency security gates.

Production adapters must be added behind the ports. FDSE must not acquire its own model gateway, token issuer, sandbox, approval engine, or generic tool authority.
