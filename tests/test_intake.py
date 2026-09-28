from uuid import uuid4

import pytest

from fdse.errors import BoundaryViolation
from fdse.intake import IntakeRequest, IntakeStatus, IntakeValidator


def request(**overrides: object) -> IntakeRequest:
    values: dict[str, object] = {
        "request_id": str(uuid4()),
        "tenant_id": " tenant-1 ",
        "repository_id": " repo-1 ",
        "revision": "abc123",
        "objective": " Fix the failing test ",
        "risk": "medium",
        "idempotency_key": " idem-1 ",
    }
    values.update(overrides)
    return IntakeRequest(**values)  # type: ignore[arg-type]


def test_intake_normalizes_and_accepts() -> None:
    record = IntakeValidator().validate(request())
    assert record.status is IntakeStatus.ACCEPTED
    assert record.scope.tenant_id == "tenant-1"
    assert record.objective == "Fix the failing test"
    assert record.idempotency_key == "idem-1"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("request_id", "not-a-uuid"),
        ("tenant_id", ""),
        ("repository_id", ""),
        ("revision", ""),
        ("objective", ""),
        ("idempotency_key", ""),
    ],
)
def test_intake_rejects_invalid_boundary_values(field: str, value: str) -> None:
    with pytest.raises(BoundaryViolation):
        request(**{field: value})


def test_intake_rejects_nul() -> None:
    with pytest.raises(BoundaryViolation):
        request(objective="safe\x00unsafe")


def test_intake_rejects_oversized_objective() -> None:
    with pytest.raises(BoundaryViolation):
        request(objective="x" * 4097)
