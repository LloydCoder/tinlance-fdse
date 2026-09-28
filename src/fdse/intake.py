"""Validated engineering intake at the FDSE domain boundary."""
from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID
from .contracts import ExecutionRisk, TenantScope
from .errors import BoundaryViolation

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
        _required(self.tenant_id, "tenant_id")
        _required(self.repository_id, "repository_id")
        _required(self.revision, "revision")
        _bounded(self.objective, "objective", 4096)
        _bounded(self.idempotency_key, "idempotency_key", 256)

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
            idempotency_key=_normalized(request.idempotency_key, "idempotency_key"),
            status=IntakeStatus.ACCEPTED,
        )

def _normalized(value: str, field_name: str) -> str:
    value = value.strip()
    if not value:
        raise BoundaryViolation(f"{field_name} is required")
    if "\x00" in value:
        raise BoundaryViolation(f"{field_name} contains a NUL byte")
    return value

def _required(value: str, field_name: str) -> None:
    _normalized(value, field_name)

def _bounded(value: str, field_name: str, maximum: int) -> None:
    value = _normalized(value, field_name)
    if len(value) > maximum:
        raise BoundaryViolation(f"{field_name} exceeds maximum length")

def _required_uuid(value: str, field_name: str) -> UUID:
    value = _normalized(value, field_name)
    try:
        return UUID(value)
    except ValueError as exc:
        raise BoundaryViolation(f"{field_name} must be a valid UUID") from exc
