"""Validated engineering intake at the FDSE domain boundary."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

from .contracts import ExecutionRisk, TenantScope
from .errors import BoundaryViolation

_MAX_SCOPE = 256
_MAX_REVISION = 512
_MAX_OBJECTIVE = 4096
_MAX_IDEMPOTENCY_KEY = 256
_ALLOWED_RISKS = {"low", "medium", "high", "critical"}


class IntakeStatus(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class IntakeRequest:
    request_id: str
    tenant_id: str
    repository_id: str
    revision: str
    objective: str
    risk: ExecutionRisk
    idempotency_key: str

    def __post_init__(self) -> None:
        _required_uuid(self.request_id, "request_id")
        _bounded(self.tenant_id, "tenant_id", _MAX_SCOPE)
        _bounded(self.repository_id, "repository_id", _MAX_SCOPE)
        _bounded(self.revision, "revision", _MAX_REVISION)
        _bounded(self.objective, "objective", _MAX_OBJECTIVE)
        _bounded(self.idempotency_key, "idempotency_key", _MAX_IDEMPOTENCY_KEY)
        if self.risk not in _ALLOWED_RISKS:
            raise BoundaryViolation("risk is invalid")


@dataclass(frozen=True, slots=True)
class IntakeRecord:
    request_id: UUID
    scope: TenantScope
    revision: str
    objective: str
    risk: ExecutionRisk
    idempotency_key: str
    status: IntakeStatus


class IntakeValidator:
    """Pure validation/normalization; it never authorizes or executes."""

    def validate(self, request: IntakeRequest) -> IntakeRecord:
        return IntakeRecord(
            request_id=_required_uuid(request.request_id, "request_id"),
            scope=TenantScope(
                tenant_id=_normalized(request.tenant_id, "tenant_id"),
                repository_id=_normalized(request.repository_id, "repository_id"),
            ),
            revision=_normalized(request.revision, "revision"),
            objective=_normalized(request.objective, "objective"),
            risk=request.risk,
            idempotency_key=_normalized(
                request.idempotency_key,
                "idempotency_key",
            ),
            status=IntakeStatus.ACCEPTED,
        )


class IntakeRegistry:
    """Deterministic idempotency registry; it has no execution authority."""

    def __init__(self) -> None:
        self._records: dict[tuple[str, str], IntakeRecord] = {}

    def put(self, record: IntakeRecord) -> IntakeRecord:
        key = (record.scope.tenant_id, record.idempotency_key)
        existing = self._records.get(key)
        if existing is not None and existing != record:
            raise BoundaryViolation(
                "idempotency key is already bound to another request"
            )
        self._records[key] = record
        return record

    def get(
        self,
        tenant_id: str,
        idempotency_key: str,
    ) -> IntakeRecord | None:
        key = (
            _normalized(tenant_id, "tenant_id"),
            _normalized(idempotency_key, "idempotency_key"),
        )
        return self._records.get(key)


def _normalized(value: str, field_name: str) -> str:
    value = value.strip()
    if not value:
        raise BoundaryViolation(f"{field_name} is required")
    if "\x00" in value:
        raise BoundaryViolation(f"{field_name} contains a NUL byte")
    return value


def _bounded(value: str, field_name: str, maximum: int) -> None:
    value = _normalized(value, field_name)
    if len(value) > maximum:
        raise BoundaryViolation(f"{field_name} exceeds maximum length")


def _required_uuid(value: str, field_name: str) -> UUID:
    value = _normalized(value, field_name)
    try:
        return UUID(value)
    except ValueError as exc:
        raise BoundaryViolation(
            f"{field_name} must be a valid UUID"
        ) from exc
