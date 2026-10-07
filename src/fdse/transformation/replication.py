# fmt: off
# ruff: noqa: E501
"""Replication and adaptation contracts."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ._common import enum_required, required, unique_ids


class ReplicationStage(StrEnum):
    PLANNED = "PLANNED"
    CONFIGURED = "CONFIGURED"
    DEPLOYED = "DEPLOYED"
    MEASURED = "MEASURED"
    ACCEPTED = "ACCEPTED"
    FAILED = "FAILED"


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
    stage: ReplicationStage = ReplicationStage.PLANNED
    source_outcome_ref: str | None = None
    target_transformation_id: str | None = None
    target_outcome_ref: str | None = None
    target_transformation_tenant_id: str | None = None
    target_transformation_version: str | None = None
    target_outcome_tenant_id: str | None = None
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for value, name in (
            (self.replication_id, "replication_id"),
            (self.source_transformation_id, "source_transformation_id"),
            (self.source_tenant_id, "source_tenant_id"),
            (self.target_tenant_id, "target_tenant_id"),
        ):
            required(value, name)
        for name in ("replication_id", "source_transformation_id", "source_tenant_id", "target_tenant_id"):
            object.__setattr__(self, name, required(getattr(self, name), name))
        if self.source_tenant_id == self.target_tenant_id:
            raise ValueError("replication source and target tenants must differ")
        if not isinstance(self.success_claimed, bool):
            raise TypeError("success_claimed must be bool")
        object.__setattr__(self, "stage", enum_required(self.stage, ReplicationStage, "stage"))
        if self.success_claimed:
            raise ValueError("replication profiles cannot self-certify success")
        object.__setattr__(self, "methodology", tuple(required(v, "methodology item") for v in self.methodology))
        object.__setattr__(self, "customer_specific", tuple(required(v, "customer-specific item") for v in self.customer_specific))
        object.__setattr__(self, "learned_adaptations", tuple(required(v, "learned adaptation") for v in self.learned_adaptations))
        object.__setattr__(self, "adaptation_parameters", tuple((required(k, "parameter key"), required(v, "parameter value")) for k, v in self.adaptation_parameters))
        if not self.methodology:
            raise ValueError("replication profile requires reusable methodology")
        for name in (
            "source_outcome_ref",
            "target_transformation_id",
            "target_transformation_tenant_id",
            "target_transformation_version",
            "target_outcome_ref",
            "target_outcome_tenant_id",
        ):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, required(value, name))
        object.__setattr__(self, "evidence_refs", unique_ids(self.evidence_refs, "evidence_ref"))
        if self.stage in {ReplicationStage.MEASURED, ReplicationStage.ACCEPTED, ReplicationStage.FAILED} and not self.evidence_refs:
            raise ValueError("measured or terminal replication stage requires evidence references")
        if self.stage in {ReplicationStage.MEASURED, ReplicationStage.ACCEPTED}:
            if self.target_outcome_ref is None or self.source_outcome_ref is None:
                raise ValueError("qualified replication requires source and target outcome references")
            if self.target_transformation_tenant_id != self.target_tenant_id:
                raise ValueError("target transformation tenant must match target tenant")
            if self.target_transformation_version is None:
                raise ValueError("qualified replication requires target transformation version")
            if self.target_outcome_tenant_id != self.target_tenant_id:
                raise ValueError("target outcome tenant must match target tenant")
        if self.stage in {
            ReplicationStage.DEPLOYED, ReplicationStage.MEASURED,
            ReplicationStage.ACCEPTED, ReplicationStage.FAILED,
        } and self.target_transformation_id is None:
            raise ValueError("deployed or terminal replication requires target transformation reference")
