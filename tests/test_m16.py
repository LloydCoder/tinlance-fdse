from datetime import UTC, datetime

import pytest

from fdse.workflow_runtime import (
    FixedClock,
    InMemoryWorkflowStateStore,
    NodeKind,
    PermanentFailure,
    RetryableFailure,
    RetryPolicy,
    WorkflowDefinition,
    WorkflowEdge,
    WorkflowNode,
    WorkflowRunStatus,
    WorkflowRuntime,
)


class Executor:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def execute(self, run, node):
        self.calls.append(node.node_id)
        if node.node_id == "retry" and self.calls.count("retry") == 1:
            raise RetryableFailure
        if node.node_id == "fail":
            raise PermanentFailure
        return "ok"


class Approval:
    def __init__(self, allowed: bool) -> None:
        self.allowed_value = allowed

    def allowed(self, run, node) -> bool:
        return self.allowed_value


class Platform:
    def start(self, run):
        return "platform-run"

    def cancel(self, run):
        return None


def definition(*nodes: WorkflowNode, edges: tuple[WorkflowEdge, ...] = ()) -> WorkflowDefinition:
    return WorkflowDefinition("wf", "rev-1", nodes, edges, nodes[0].node_id)


def test_workflow_definition_rejects_cycles() -> None:
    with pytest.raises(ValueError):
        definition(
            WorkflowNode("a", NodeKind.TASK),
            WorkflowNode("b", NodeKind.TASK),
            edges=(WorkflowEdge("a", "b"), WorkflowEdge("b", "a")),
        )


def test_retry_is_bounded_and_deterministic() -> None:
    executor = Executor()
    runtime = WorkflowRuntime(
        InMemoryWorkflowStateStore(),
        executor,
        approval_gate=Approval(True),
        platform_mapper=Platform(),
        clock=FixedClock(datetime(2026, 10, 1, tzinfo=UTC)),
    )
    run = runtime.create(
        "r1",
        "t",
        "repo",
        "sha",
        definition(
            WorkflowNode(
                "retry",
                NodeKind.TASK,
                RetryPolicy(max_attempts=2, backoff_seconds=3),
            )
        ),
    )
    runtime.start(run)
    runtime.tick(run)
    assert run.status is WorkflowRunStatus.RUNNING
    assert run.attempts["retry"] == 1
    runtime.tick(run)
    assert run.status is WorkflowRunStatus.SUCCEEDED
    assert run.attempts["retry"] == 2
    assert [event.event_type for event in runtime.events["r1"]] == [
        "started",
        "node_started",
        "retry_scheduled",
        "node_started",
        "node_completed",
    ]


def test_checkpoint_and_idempotency_are_scope_bound() -> None:
    store = InMemoryWorkflowStateStore()
    runtime = WorkflowRuntime(
        store,
        Executor(),
        approval_gate=Approval(True),
        platform_mapper=Platform(),
        clock=FixedClock(datetime(2026, 10, 1, tzinfo=UTC)),
    )
    d = definition(WorkflowNode("a", NodeKind.TASK))
    run = runtime.create("r1", "t", "repo", "sha", d)
    assert runtime.create("r1", "t", "repo", "sha", d) is run
    with pytest.raises(ValueError):
        runtime.create("r1", "other", "repo", "sha", d)


def test_approval_gate_is_fail_closed() -> None:
    runtime = WorkflowRuntime(
        InMemoryWorkflowStateStore(),
        Executor(),
        approval_gate=Approval(False),
        platform_mapper=Platform(),
        clock=FixedClock(datetime(2026, 10, 1, tzinfo=UTC)),
    )
    run = runtime.create(
        "r1",
        "t",
        "repo",
        "sha",
        definition(WorkflowNode("approve", NodeKind.APPROVAL)),
    )
    runtime.start(run)
    runtime.tick(run)
    assert run.status is WorkflowRunStatus.WAITING


def test_deadline_and_cancellation_are_terminal() -> None:
    clock = FixedClock(datetime(2026, 10, 1, tzinfo=UTC))
    runtime = WorkflowRuntime(
        InMemoryWorkflowStateStore(),
        Executor(),
        approval_gate=Approval(True),
        platform_mapper=Platform(),
        clock=clock,
    )
    d = WorkflowDefinition(
        "wf", "rev-1", (WorkflowNode("a", NodeKind.TASK),), (), "a", deadline_seconds=1
    )
    run = runtime.create("r1", "t", "repo", "sha", d)
    runtime.start(run)
    clock.current = datetime(2026, 10, 1, 0, 0, 2, tzinfo=UTC)
    runtime.tick(run)
    assert run.status is WorkflowRunStatus.FAILED

    run2 = runtime.create("r2", "t", "repo", "sha", definition(WorkflowNode("a", NodeKind.TASK)))
    runtime.start(run2)
    runtime.request_cancel(run2)
    runtime.tick(run2)
    assert run2.status is WorkflowRunStatus.CANCELLED
