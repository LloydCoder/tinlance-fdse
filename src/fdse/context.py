"""Deterministic, tenant-scoped engineering context assembly (M3)."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4
from .evidence import digest
from .security import validate_workspace_relative_path

_MAX_TEXT=4096
_MAX_ITEMS=256

class ContextKind(StrEnum):
    REPOSITORY="repository"; ARCHITECTURE="architecture"; DEPENDENCY="dependency"; BUILD="build"
    TEST="test"; CI="ci"; SECURITY="security"; DEPLOYMENT="deployment"; OWNERSHIP="ownership"
    RECENT_CHANGE="recent_change"; CONSTRAINT="constraint"

class ContextQuality(StrEnum):
    UNKNOWN="unknown"; LOW="low"; MEDIUM="medium"; HIGH="high"

@dataclass(frozen=True, slots=True)
class ContextSource:
    source_id: str
    revision: str
    provenance: str
    observed_at: datetime
    scope: str
    freshness_seconds: int
    confidence: ContextQuality=ContextQuality.UNKNOWN
    def __post_init__(self)->None:
        if not self.source_id.strip() or not self.revision.strip() or not self.provenance.strip():
            raise ValueError("context source identifiers are required")
        if self.freshness_seconds < 0: raise ValueError("freshness cannot be negative")
        if not self.scope.strip(): raise ValueError("context scope is required")

@dataclass(frozen=True, slots=True)
class ContextItem:
    kind: ContextKind
    key: str
    value: str
    source: ContextSource
    def __post_init__(self)->None:
        if not self.key.strip() or not self.value.strip(): raise ValueError("context item is required")
        if len(self.value)>_MAX_TEXT: raise ValueError("context item exceeds maximum length")
        if "\x00" in self.value: raise ValueError("context item contains NUL")

@dataclass(frozen=True, slots=True)
class ContextSnapshot:
    snapshot_id: UUID
    tenant_id: str
    repository_id: str
    revision: str
    items: tuple[ContextItem,...]
    created_at: datetime
    snapshot_digest: str
    def __post_init__(self)->None:
        if not self.tenant_id.strip() or not self.repository_id.strip() or not self.revision.strip():
            raise ValueError("context scope is required")
        if len(self.items)>_MAX_ITEMS: raise ValueError("context snapshot is too large")

class ContextBuilder:
    def build(self, tenant_id:str, repository_id:str, revision:str, items:tuple[ContextItem,...])->ContextSnapshot:
        tenant_id=tenant_id.strip(); repository_id=repository_id.strip(); revision=revision.strip()
        if not tenant_id or not repository_id or not revision: raise ValueError("context scope is required")
        ordered=tuple(sorted(items,key=lambda x:(x.kind.value,x.key,x.source.source_id,x.source.revision)))
        if len(ordered)>_MAX_ITEMS: raise ValueError("context snapshot is too large")
        payload=[{"kind":x.kind.value,"key":x.key,"value":x.value,"source":x.source.source_id,
                  "revision":x.source.revision,"provenance":x.source.provenance} for x in ordered]
        return ContextSnapshot(uuid4(),tenant_id,repository_id,revision,ordered,datetime.now(UTC),digest(payload))

class ContextStore:
    def __init__(self)->None: self._items:dict[tuple[str,str,str],ContextSnapshot]={}
    def put(self,snapshot:ContextSnapshot)->ContextSnapshot:
        key=(snapshot.tenant_id,snapshot.repository_id,snapshot.revision)
        self._items[key]=snapshot; return snapshot
    def get(self,tenant_id:str,repository_id:str,revision:str)->ContextSnapshot|None:
        return self._items.get((tenant_id.strip(),repository_id.strip(),revision.strip()))

def filter_secret_like(value:str)->str:
    lowered=value.lower()
    markers=("password=","passwd=","secret=","token=","api_key=","authorization:")
    if any(marker in lowered for marker in markers): return "[REDACTED]"
    return value

def validate_context_path(path:str)->str: return validate_workspace_relative_path(path)
