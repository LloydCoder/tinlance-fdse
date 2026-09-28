# Repository Structure

The repository is capability-driven.

- `src/fdse/contracts.py`: M0 boundary contracts.
- `src/fdse/security.py`: M0 lexical path invariants.
- `src/fdse/config.py`: M0 non-secret configuration validation.
- `src/fdse/domain.py`: M1 engineering-domain entities.
- `src/fdse/evidence.py`: canonical evidence serialization and digests.
- `src/fdse/integrity.py`: record and chain digests.
- `src/fdse/transitions.py`: explicit lifecycle transitions.
- `src/fdse/ports.py`: dependency-inversion integration ports.
- `src/fdse/store.py`: deterministic test adapters.
- `src/fdse/policy.py`: deny-by-default local policy adapter.
- `src/fdse/execution.py`: Agent Platform boundary adapter.
- `src/fdse/service.py`: M0 boundary service.

Future modules must be justified by implemented capabilities. FDSE must not add a competing runtime, authorization kernel, sandbox, model gateway, or generic tool authority.
