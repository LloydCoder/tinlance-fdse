# Repository Structure

The repository is capability-driven. This map describes the current implementation and intentionally does not list files that do not exist.

## Source

- M0/M1 foundation: `src/fdse/contracts.py`, `errors.py`, `config.py`, `service.py`, `security.py`, `domain.py`, `evidence.py`, `integrity.py`
- M2: `src/fdse/intake.py`
- M3: `src/fdse/context.py`
- M4: `src/fdse/platform.py`
- M5: `src/fdse/agents.py`
- M6: `src/fdse/workflows.py`
- M7: `src/fdse/git_ci.py`
- M8: `src/fdse/evidence_graph.py`
- M9: `src/fdse/governance.py`
- M10: `src/fdse/evaluation.py`
- M11: `src/fdse/product.py`
- M12: `src/fdse/security_hardening.py`
- M13: `src/fdse/production.py`
- M14: `src/fdse/certification.py`
- M15: `src/fdse/trusted_memory.py`
- M16: `src/fdse/workflow_runtime.py`
- M17: `src/fdse/multi_agent_runtime.py`
- M18: `src/fdse/ecosystem_runtime.py`

The package public API is defined in `src/fdse/__init__.py`.

## Tests

- Existing phase-specific tests cover the M0/M1 foundation and M2 intake.
- `tests/test_m3_m14.py` contains cross-phase regression coverage for the M1 lifecycle through M14 contracts.
- `tests/test_m15.py`, `tests/test_m16.py`, `tests/test_m17.py`, and `tests/test_m18.py` provide phase-specific regression coverage through the final roadmap phase.

- `docs/architecture/M15-CONTEXT-TRUSTED-MEMORY.md`, `M16-WORKFLOW-RUNTIME.md`, `M17-MULTI-AGENT-RUNTIME.md`, and `M18-AGENT-ECOSYSTEM-RUNTIME.md` define the post-M14 capabilities.

## Documentation

- `docs/architecture/ROADMAP.md` is the canonical M0–M18 capability map.
- `docs/architecture/M2-INTAKE.md` defines the M2 intake boundary.
- `docs/operations/SELF-HOSTED-RUNNER.md` is historical/decommissioning guidance; the current CI workflow uses GitHub-hosted runners.

## Boundary invariant

Every phase must preserve explicit tenant/repository/revision scope where the data represents customer engineering work, deterministic integrity, and fail-closed behavior.

FDSE must not add a competing runtime, authorization kernel, sandbox, model gateway, generic tool authority, or deployment platform. Those are external platform/infrastructure responsibilities.
