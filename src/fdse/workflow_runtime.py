"""Deterministic FDSE workflow runtime semantics (M16).

The reference runtime owns workflow semantics and recovery state transitions.
Durability, scheduling, approval authority, and agent execution remain explicit
ports owned by infrastructure or the Tinlance Agent Platform.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import StrEnum
from typing import Protocol

from .evidence import digest


class WorkflowRunStatus(StrEnum):
    CREATED = "created"
    RUNNING = "running"
    WAITING = "waiting"
    PAUSED = "paused"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"
    FAILED = "failed"
    SUCCEEDED = "succeeded"


class NodeKind(StrEnum):
    TASK = "task"
    CONDITION = "condition"
    APPROVAL = "approval"
    COMPENSATION = "compensation"


class RetryableFailure(Exception):
    """Executor failure that may be retried within the node retry budget."""


class PermanentFailure(Exception):
    """Executor failure that must fail the workflow."""


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    max_attempts: int = 1
    backoff_seconds: int = 0
    multiplier: int = 2
    max_backoff_seconds: int = 300

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be positive")
        if self.backoff_seconds < 0 or self.max_backoff_seconds < 0:
            raise ValueError("retry delays cannot be negative")
        if self.multiplier < 1:
            raise ValueError("retry multiplier must be positive")

    def delay_for(self, attempt: int) -> int:
        if attempt < 1:
            raise ValueError("attempt must be positive")
        delay = self.backoff_seconds * (self.multiplier ** (attempt - 1))
        return min(delay, self.max_backoff_seconds)


@dataclass(frozen=True, slots=True)
class WorkflowNode:
    node_id: str
    kind: NodeKind
    retry: RetryPolicy = field(default_factory=RetryPolicy)
    timeout_seconds: int | None = None
    compensation_node_id: str | None = None

    def __post_init__(self) -> None:
        if not self.node_id.strip():
            raise ValueError("node_id is required")
        if self.timeout_seconds is not None and self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")


@dataclass(frozen=True, slots=True)
class WorkflowEdge:
    source: str
    target: str
    condition: str | None = None


@dataclass(frozen=True, slots=True)
class WorkflowDefinition:
    workflow_id: str
    revision: str
    nodes: tuple[WorkflowNode, ...]
    edges: tuple[WorkflowEdge, ...]
    entry_node_id: str
    deadline_seconds: int | None = None

    def __post_init__(self) -> None:
        ids = [node.node_id for node in self.nodes]
        if len(ids) != len(set(ids)):
            raise ValueError("workflow node identifiers must be unique")
        if self.entry_node_id not in ids:
            raise ValueError("entry node must exist")
        if self.deadline_seconds is not None and self.deadline_seconds <= 0:
            raise ValueError("workflow deadline must be positive")
        node_ids = set(ids)
        for edge in self.edges:
            if edge.source not in node_ids or edge.target not in node_ids:
                raise ValueError("workflow edge references an unknown node")
            if edge.source == edge.target:
                raise ValueError("workflow graph cannot contain self-loops")
        _assert_acyclic(ids, self.edges)

    def node(self, node_id: str) -> WorkflowNode:
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        raise KeyError(node_id)

    def predecessors(self, node_id: str) -> tuple[WorkflowEdge, ...]:
        return tuple(edge for edge in self.edges if edge.target == node_id)

    def successors(self, node_id: str) -> tuple[WorkflowEdge, ...]:
        return tuple(edge for edge in self.edges if edge.source == node_id)


@dataclass(frozen=True, slots=True)
class WorkflowEvent:
    sequence: int
    run_id: str
    event_type: str
    node_id: str | None
    attempt: int
    occurred_at: datetime
    payload_digest: str


@dataclass(frozen=True, slots=True)
class WorkflowCheckpoint:
    run_id: str
    definition_revision: str
    completed_nodes: tuple[str, ...]
    failed_nodes: tuple[str, ...]
    active_node: str | None
    result_keys: tuple[str, ...]
    event_sequence: int
    state_digest: str


@dataclass(slots=True)
class WorkflowRun:
    run_id: str
    tenant_id: str
    repository_id: str
    revision: str
    definition: WorkflowDefinition
    status: WorkflowRunStatus = WorkflowRunStatus.CREATED
    completed_nodes: set[str] = field(default_factory=set)
    failed_nodes: set[str] = field(default_factory=set)
    results: dict[str, str] = field(default_factory=dict)
    attempts: dict[str, int] = field(default_factory=dict)
    active_node: str | None = None
    platform_run_id: str | None = None
    event_sequence: int = 0
    started_at: datetime | None = None
    deadline_at: datetime | None = None
    cancel_requested: bool = False


class WorkflowStateStore(Protocol):
    def save(self, run: WorkflowRun, checkpoint: WorkflowCheckpoint) -> None: ...

    def load(self, run_id: str) -> WorkflowRun | None: ...


class WorkflowExecutor(Protocol):
    def execute(self, run: WorkflowRun, node: WorkflowNode) -> str: ...


class ApprovalGate(Protocol):
    def allowed(self, run: WorkflowRun, node: WorkflowNode) -> bool: ...


class PlatformRunMapper(Protocol):
    def start(self, run: WorkflowRun) -> str: ...

    def cancel(self, run: WorkflowRun) -> None: ...


class Clock(Protocol):
    def now(self) -> datetime: ...


class InMemoryWorkflowStateStore:
    def __init__(self) -> None:
        self.runs: dict[str, WorkflowRun] = {}
        self.checkpoints: dict[str, WorkflowCheckpoint] = {}

    def save(self, run: WorkflowRun, checkpoint: WorkflowCheckpoint) -> None:
        self.runs[run.run_id] = run
        self.checkpoints[run.run_id] = checkpoint

    def load(self, run_id: str) -> WorkflowRun | None:
        return self.runs.get(run_id)


class FixedClock:
    def __init__(self, current: datetime) -> None:
        self.current = current

    def now(self) -> datetime:
        return self.current


class AllowAllApprovalGate:
    def allowed(self, run: WorkflowRun, node: WorkflowNode) -> bool:
        return False if node.kind is NodeKind.APPROVAL else True


class NoopPlatformRunMapper:
    def start(self, run: WorkflowRun) -> str:
        return f"platform:{run.run_id}"

    def cancel(self, run: WorkflowRun) -> None:
        return None


class WorkflowRuntime:
    """Fail-closed reference runtime with checkpoints after every state mutation."""

    def __init__(
        self,
        state_store: WorkflowStateStore,
        executor: WorkflowExecutor,
        *,
        approval_gate: ApprovalGate,
        platform_mapper: PlatformRunMapper,
        clock: Clock,
    ) -> None:
        self.state_store = state_store
        self.executor = executor
        self.approval_gate = approval_gate
        self.platform_mapper = platform_mapper
        self.clock = clock
        self.events: dict[str, tuple[WorkflowEvent, ...]] = {}

    def create(
        self,
        run_id: str,
        tenant_id: str,
        repository_id: str,
        revision: str,
        definition: WorkflowDefinition,
    ) -> WorkflowRun:
        existing = self.state_store.load(run_id)
        if existing is not None:
            if (
                existing.tenant_id,
                existing.repository_id,
                existing.revision,
                existing.definition.revision,
            ) != (tenant_id, repository_id, revision, definition.revision):
                raise ValueError("idempotency key is bound to different workflow scope")
            return existing
        run = WorkflowRun(run_id, tenant_id, repository_id, revision, definition)
        self._checkpoint(run)
        return run

    def start(self, run: WorkflowRun) -> WorkflowRun:
        if run.status not in {WorkflowRunStatus.CREATED, WorkflowRunStatus.PAUSED}:
            return run
        now = self.clock.now()
        run.started_at = run.started_at or now
        if run.definition.deadline_seconds is not None:
            run.deadline_at = run.started_at + timedelta(
                seconds=run.definition.deadline_seconds
            )
        run.platform_run_id = run.platform_run_id or self.platform_mapper.start(run)
        run.status = WorkflowRunStatus.RUNNING
        self._emit(run, "started", None, 0)
        self._checkpoint(run)
        return run

    def resume(self, run_id: str) -> WorkflowRun:
        run = self.state_store.load(run_id)
        if run is None:
            raise KeyError(run_id)
        if run.status is not WorkflowRunStatus.PAUSED:
            raise ValueError("only paused workflows may be resumed")
        return self.start(run)

    def request_cancel(self, run: WorkflowRun) -> WorkflowRun:
        if run.status in {
            WorkflowRunStatus.SUCCEEDED,
            WorkflowRunStatus.FAILED,
            WorkflowRunStatus.CANCELLED,
        }:
            return run
        run.cancel_requested = True
        run.status = WorkflowRunStatus.CANCELLING
        self.platform_mapper.cancel(run)
        self._emit(run, "cancel_requested", run.active_node, 0)
        self._checkpoint(run)
        return run

    def tick(self, run: WorkflowRun) -> WorkflowRun:
        if run.status is not WorkflowRunStatus.RUNNING:
            return run
        if run.cancel_requested:
            run.status = WorkflowRunStatus.CANCELLED
            self._emit(run, "cancelled", run.active_node, 0)
            self._checkpoint(run)
            return run
        if run.deadline_at is not None and self.clock.now() >= run.deadline_at:
            run.status = WorkflowRunStatus.FAILED
            self._emit(run, "deadline_exceeded", run.active_node, 0)
            self._checkpoint(run)
            return run

        ready = self._ready_nodes(run)
        if not ready:
            if len(run.completed_nodes) == len(run.definition.nodes):
                run.status = WorkflowRunStatus.SUCCEEDED
                self._emit(run, "succeeded", None, 0)
                self._checkpoint(run)
                return run
            run.status = WorkflowRunStatus.FAILED
            self._emit(run, "blocked", run.active_node, 0)
            self._checkpoint(run)
            return run

        node = ready[0]
        run.active_node = node.node_id
        if node.kind is NodeKind.APPROVAL and not self.approval_gate.allowed(run, node):
            run.status = WorkflowRunStatus.WAITING
            self._emit(run, "approval_required", node.node_id, 0)
            self._checkpoint(run)
            return run

        attempt = run.attempts.get(node.node_id, 0) + 1
        run.attempts[node.node_id] = attempt
        self._emit(run, "node_started", node.node_id, attempt)
        try:
            result = self.executor.execute(run, node)
        except RetryableFailure:
            if attempt >= node.retry.max_attempts:
                run.failed_nodes.add(node.node_id)
                run.status = WorkflowRunStatus.FAILED
                self._emit(run, "retry_budget_exhausted", node.node_id, attempt)
            else:
                self._emit(
                    run,
                    "retry_scheduled",
                    node.node_id,
                    attempt,
                    {"delay_seconds": node.retry.delay_for(attempt)},
                )
            self._checkpoint(run)
            return run
        except PermanentFailure:
            run.failed_nodes.add(node.node_id)
            run.status = WorkflowRunStatus.FAILED
            self._emit(run, "node_failed", node.node_id, attempt)
            self._checkpoint(run)
            return run

        run.results[node.node_id] = result
        run.completed_nodes.add(node.node_id)
        run.active_node = None
        self._emit(run, "node_completed", node.node_id, attempt, {"result": result})
        self._checkpoint(run)
        return run

    def _ready_nodes(self, run: WorkflowRun) -> tuple[WorkflowNode, ...]:
        candidates: list[WorkflowNode] = []
        for node in run.definition.nodes:
            if node.node_id in run.completed_nodes or node.node_id in run.failed_nodes:
                continue
            incoming = run.definition.predecessors(node.node_id)
            if not incoming:
                if node.node_id == run.definition.entry_node_id:
                    candidates.append(node)
                continue
            if not all(edge.source in run.completed_nodes for edge in incoming):
                continue
            if not _conditions_allow(incoming, run.results):
                continue
            candidates.append(node)
        return tuple(sorted(candidates, key=lambda node: node.node_id))

    def _emit(
        self,
        run: WorkflowRun,
        event_type: str,
        node_id: str | None,
        attempt: int,
        payload: object = None,
    ) -> None:
        run.event_sequence += 1
        event = WorkflowEvent(
            run.event_sequence,
            run.run_id,
            event_type,
            node_id,
            attempt,
            self.clock.now(),
            digest(payload if payload is not None else {}),
        )
        self.events[run.run_id] = (*self.events.get(run.run_id, ()), event)

    def _checkpoint(self, run: WorkflowRun) -> None:
        checkpoint = WorkflowCheckpoint(
            run_id=run.run_id,
            definition_revision=run.definition.revision,
            completed_nodes=tuple(sorted(run.completed_nodes)),
            failed_nodes=tuple(sorted(run.failed_nodes)),
            active_node=run.active_node,
            result_keys=tuple(sorted(run.results)),
            event_sequence=run.event_sequence,
            state_digest=digest(
                {
                    "status": run.status.value,
                    "completed": sorted(run.completed_nodes),
                    "failed": sorted(run.failed_nodes),
                    "results": sorted(run.results.items()),
                    "attempts": sorted(run.attempts.items()),
                    "active": run.active_node,
                    "platform_run": run.platform_run_id,
                }
            ),
        )
        self.state_store.save(run, checkpoint)


def _conditions_allow(
    edges: tuple[WorkflowEdge, ...],
    results: dict[str, str],
) -> bool:
    for edge in edges:
        if edge.condition is None:
            continue
        if results.get(edge.source) != edge.condition:
            return False
    return True


def _assert_acyclic(
    node_ids: list[str],
    edges: tuple[WorkflowEdge, ...],
) -> None:
    graph: dict[str, tuple[str, ...]] = {node_id: () for node_id in node_ids}
    for edge in edges:
        graph[edge.source] = (*graph[edge.source], edge.target)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visiting:
            raise ValueError("workflow graph must be acyclic")
        if node_id in visited:
            return
        visiting.add(node_id)
        for target in graph[node_id]:
            visit(target)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in node_ids:
        visit(node_id)
