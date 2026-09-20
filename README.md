# Tinlance FDSE

**Forward-Deployed Software Engineering execution system for governed, evidence-driven software delivery.**

FDSE is Tinlance's engineering-domain execution layer. It owns engineering semantics while consuming generic execution authority and infrastructure from the private Tinlance Agent Platform.

## M0 status

**M0 — Architecture & Repository Foundation: IN PROGRESS**

M0 establishes the repository structure, framework-neutral contracts, trust boundary, tenant-safety primitives, evidence-integrity primitives, CI/security gates and documentation. It does **not** implement a local agent runtime, sandbox, generic policy engine, approval engine, unrestricted customer-code execution, or production Agent Platform.

The separate `feat/fdse-foundation` branch/PR #2 contains work beyond M0's architectural scope. It is not evidence that M0 is complete.

## Architectural invariant

> **FDSE owns engineering semantics; Agent Platform owns generic authority and execution infrastructure.**

Customer-controlled source, documentation, issue/PR text, CI output, dependency metadata, model output and tool output are untrusted data. They cannot grant authority.

## Execution boundary

```text
FDSE request
  → Agent Platform authorization/policy/approval
  → controlled execution
  → structured result + provenance/evidence references
  → FDSE verification
```

FDSE never executes customer code directly on its application host.

## M0 development loop

```text
inspect → design → implement → test → security review → CI → review → merge
```

See `docs/architecture/BOUNDARIES.md`, `docs/architecture/AGENT-PLATFORM-INTEGRATION.md` and `docs/ROADMAP.md`.

M0 release state is authoritative only after the final branch commit has a successful GitHub Actions run and PR #1 is merged; until then it remains in progress.
