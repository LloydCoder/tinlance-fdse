"""Tenant-safe customer product contracts (M11)."""
from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True,slots=True)
class CustomerProject:
    project_id:UUID; tenant_id:UUID; repository_id:str; revision:str; name:str
    def __post_init__(self)->None:
        if not self.repository_id.strip() or not self.revision.strip() or not self.name.strip(): raise ValueError("customer project fields are required")

@dataclass(frozen=True,slots=True)
class CustomerRequest:
    request_id:str; tenant_id:str; repository_id:str; objective:str; revision:str
    def __post_init__(self)->None:
        if not all(x.strip() for x in (self.request_id,self.tenant_id,self.repository_id,self.objective,self.revision)):
            raise ValueError("customer request fields are required")

class TenantBoundary:
    def ensure(self,tenant_id:str,requested_tenant_id:str)->None:
        if tenant_id.strip()!=requested_tenant_id.strip(): raise PermissionError("tenant boundary violation")
