"""Production-readiness contracts without owning infrastructure (M13)."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class Readiness(StrEnum):
    READY = "ready"
    NOT_READY = "not_ready"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class HealthStatus:
    component: str
    readiness: Readiness
    detail: str

    def __post_init__(self) -> None:
        if not self.component.strip():
            raise ValueError("component is required")


class HealthProbe(Protocol):
    def check(self) -> HealthStatus: ...


@dataclass(frozen=True, slots=True)
class IdempotencyRecord:
    tenant_id: str
    key: str
    request_digest: str

    def __post_init__(self) -> None:
        if not all(
            value.strip() for value in (self.tenant_id, self.key, self.request_digest)
        ):
            raise ValueError("idempotency record is required")


class ReadinessGate:
    def evaluate(self, probes: tuple[HealthProbe, ...]) -> Readiness:
        if not probes:
            return Readiness.UNKNOWN
        statuses = tuple(probe.check() for probe in probes)
        if any(status.readiness is Readiness.NOT_READY for status in statuses):
            return Readiness.NOT_READY
        if any(status.readiness is Readiness.UNKNOWN for status in statuses):
            return Readiness.UNKNOWN
        return Readiness.READY
