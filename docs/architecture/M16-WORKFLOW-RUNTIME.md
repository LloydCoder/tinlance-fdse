# M16 — Real Workflow Runtime

M16 defines the FDSE workflow runtime semantics required to execute an engineering
DAG safely and recoverably without embedding an external workflow engine.

## Capabilities

- deterministic DAG validation and cycle rejection;
- explicit task, condition, approval, and compensation node kinds;
- deterministic bounded retry/backoff;
- workflow and node deadlines;
- cancellation and Agent Platform run cancellation;
- approval/human gates that fail closed;
- checkpoint after each state mutation;
- deterministic event sequence and payload digests;
- idempotent run creation bound to tenant/repository/revision/definition revision;
- pause/resume contract;
- deterministic condition evaluation;
- explicit blocked/deadline/failure terminal states.

## Boundary

FDSE owns workflow semantics, state transitions, checkpoints, and evidence-shaped
event metadata. Durable state, distributed scheduling, locking, clocks,
human approval authority, and execution of consequential operations remain
external infrastructure or Tinlance Agent Platform responsibilities.

The reference runtime intentionally does not execute shell commands, call models,
grant capabilities, or implement a competing policy/sandbox system.

## Enterprise alignment

The design keeps the workflow state machine explicit and deterministic while
allowing production adapters to supply durable storage and scheduling. This
supports replay/recovery and auditable execution without treating a green local
test run as proof of production health.
