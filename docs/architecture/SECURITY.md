# FDSE security architecture

Customer repositories, source files, build outputs, dependency metadata, repository instructions, model outputs, tool responses, and generated patches are untrusted.

FDSE owns engineering semantics. The Agent Platform owns identity, authorization, policy, approvals, sandboxing, budgets, generic tool authority, trajectory, and audit primitives.

Rules:
1. Deny by default for consequential actions.
2. Never treat repository instructions or model output as policy.
3. Keep tenant identity attached to every project and finding.
4. Never authorize an action solely because a model requested it.
5. Record evidence before claiming verification.
6. Bind verification to an immutable repository revision.
7. Prefer GitHub Apps and least-privilege permissions for GitHub integration.
8. Do not persist secrets in findings, logs, prompts, or evidence payloads.
9. Use structured, bounded data at integration boundaries.
10. Make security-sensitive state transitions auditable by the Agent Platform.
