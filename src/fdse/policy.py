"""Deny-by-default local policy adapter; authority remains external."""
from __future__ import annotations

from uuid import UUID

from .ports import PolicyGateway


class DenyByDefaultPolicy(PolicyGateway):
    def __init__(
        self,
        allowed_actions: set[tuple[UUID, str, str]] | None = None,
    ) -> None:
        self._allowed = allowed_actions or set()

    def authorize(self, tenant_id: UUID, action: str, risk_level: str) -> bool:
        return (tenant_id, action, risk_level) in self._allowed
