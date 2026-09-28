# Repository Structure

The repository is capability-driven.

- M0: contracts.py, security.py, config.py, service.py
- M1: domain.py, evidence.py, integrity.py, transitions.py, ports.py, store.py, policy.py, execution.py
- M2: intake.py
- M3: context.py
- M4: platform.py
- M5: agents.py
- M6: workflows.py
- M7: git_ci.py
- M8: evidence_graph.py
- M9: governance.py
- M10: evaluation.py
- M11: product.py
- M12: security_hardening.py
- M13: production.py
- M14: certification.py

Every phase preserves explicit tenant/repository/revision scope and deterministic/fail-closed semantics. FDSE must not add a competing runtime, authorization kernel, sandbox, model gateway, or generic tool authority.
