# ruff: noqa: E501, I001
"""Replication and adaptation contracts."""
from __future__ import annotations

from dataclasses import dataclass

from ._common import required

# fmt: off
@dataclass(frozen=True, slots=True)
class ReplicationProfile:
    replication_id: str
    source_transformation_id: str
    source_tenant_id: str
    target_tenant_id: str
    methodology: tuple[str, ...]
    customer_specific: tuple[str, ...]
    learned_adaptations: tuple[str, ...]
    adaptation_parameters: tuple[tuple[str, str], ...] = ()
    success_claimed: bool = False
    def __post_init__(self) -> None:
        for value, name in ((self.replication_id, "replication_id"), (self.source_transformation_id, "source_transformation_id"), (self.source_tenant_id, "source_tenant_id"), (self.target_tenant_id, "target_tenant_id")):
            required(value, name)
        object.__setattr__(self, "replication_id", required(self.replication_id, "replication_id"))
        object.__setattr__(self, "source_transformation_id", required(self.source_transformation_id, "source_transformation_id"))
        object.__setattr__(self, "source_tenant_id", required(self.source_tenant_id, "source_tenant_id"))
        object.__setattr__(self, "target_tenant_id", required(self.target_tenant_id, "target_tenant_id"))
        object.__setattr__(self, "methodology", tuple(required(v, "methodology item") for v in self.methodology))
        object.__setattr__(self, "customer_specific", tuple(required(v, "customer-specific item") for v in self.customer_specific))
        object.__setattr__(self, "learned_adaptations", tuple(required(v, "learned adaptation") for v in self.learned_adaptations))
        object.__setattr__(self, "adaptation_parameters", tuple((required(k, "parameter key"), required(v, "parameter value")) for k, v in self.adaptation_parameters))
        if self.success_claimed:
            raise ValueError("replication profiles cannot self-certify success")
