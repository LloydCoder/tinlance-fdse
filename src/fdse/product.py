"""Tenant-safe customer product contracts (M11)."""
from __future__ import annotations

from dataclasses import dataclass


def _required(value: str, field_name: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError(f"{field_name} is required")
    if "\x00" in value:
        raise ValueError(f"{field_name} contains a NUL byte")
    return value


@dataclass(frozen=True, slots=True)
class CustomerProject:
    project_id: str
    tenant_id: str
    repository_id: str
    revision: str
    name: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.project_id, "project_id"),
            (self.tenant_id, "tenant_id"),
            (self.repository_id, "repository_id"),
            (self.revision, "revision"),
            (self.name, "name"),
        ):
            _required(value, name)


@dataclass(frozen=True, slots=True)
class CustomerRequest:
    request_id: str
    tenant_id: str
    repository_id: str
    objective: str
    revision: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.request_id, "request_id"),
            (self.tenant_id, "tenant_id"),
            (self.repository_id, "repository_id"),
            (self.objective, "objective"),
            (self.revision, "revision"),
        ):
            _required(value, name)


class TenantBoundary:
    def ensure(self, tenant_id: str, requested_tenant_id: str) -> None:
        if _required(tenant_id, "tenant_id") != _required(
            requested_tenant_id,
            "requested_tenant_id",
        ):
            raise PermissionError("tenant boundary violation")
