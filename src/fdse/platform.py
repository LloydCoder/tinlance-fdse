"""Versioned Agent Platform integration contract (M4)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

PLATFORM_API_VERSION = "1.0"


@dataclass(frozen=True, slots=True)
class PlatformCapabilities:
    api_version: str
    execution: bool
    approvals: bool
    sandbox: bool
    identity: bool
    audit: bool


@dataclass(frozen=True, slots=True)
class PlatformIntent:
    tenant_id: UUID
    project_id: UUID
    revision: str
    role: str
    objective: str
    risk: str
    approval_required: bool = True

    def __post_init__(self) -> None:
        if not self.revision.strip() or not self.role.strip() or not self.objective.strip():
            raise ValueError("platform intent fields are required")
        if not self.approval_required:
            raise ValueError("FDSE consequential intents must require approval")


@dataclass(frozen=True, slots=True)
class PlatformExecution:
    execution_id: UUID
    status: str
    evidence_ids: tuple[UUID, ...] = ()


class AgentPlatformAdapter(Protocol):
    def capabilities(self) -> PlatformCapabilities: ...
    def submit(self, intent: PlatformIntent) -> PlatformExecution: ...


class PlatformCompatibility:
    def validate(self, caps: PlatformCapabilities) -> None:
        if caps.api_version != PLATFORM_API_VERSION:
            raise ValueError("unsupported Agent Platform API version")
        if not (
            caps.execution
            and caps.approvals
            and caps.sandbox
            and caps.identity
            and caps.audit
        ):
            raise ValueError("Agent Platform lacks required authority capabilities")
