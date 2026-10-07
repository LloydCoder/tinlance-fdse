# fmt: off
# ruff: noqa: E501
"""Enterprise replication kit semantics.

The kit separates reusable methodology from customer-specific adaptation and
learned material. It qualifies replication from evidence; it never self-certifies
business success.
"""
from __future__ import annotations

from dataclasses import dataclass

from ._common import enum_required, required, unique_ids
from .replication import ReplicationProfile, ReplicationStage


@dataclass(frozen=True, slots=True)
class EnterpriseReplicationKit:
    """A reusable, auditable package for repeating a validated transformation."""

    kit_id: str
    source_transformation_id: str
    source_tenant_id: str
    target_tenant_id: str
    methodology: tuple[str, ...]
    discovery_template: tuple[str, ...]
    classification_taxonomy: tuple[str, ...]
    governance_templates: tuple[str, ...]
    evaluation_suite_refs: tuple[str, ...]
    golden_dataset_refs: tuple[str, ...]
    kpi_refs: tuple[str, ...]
    measurement_refs: tuple[str, ...]
    deployment_plan: tuple[str, ...]
    rollback_plan: tuple[str, ...]
    handoff_artifacts: tuple[str, ...]
    training_artifacts: tuple[str, ...]
    customer_specific: tuple[str, ...] = ()
    learned_adaptations: tuple[str, ...] = ()
    adaptation_parameters: tuple[tuple[str, str], ...] = ()
    source_outcome_ref: str | None = None
    target_transformation_id: str | None = None
    target_outcome_ref: str | None = None
    evidence_refs: tuple[str, ...] = ()
    stage: ReplicationStage = ReplicationStage.PLANNED

    def __post_init__(self) -> None:
        for value, name in (
            (self.kit_id, "kit_id"),
            (self.source_transformation_id, "source_transformation_id"),
            (self.source_tenant_id, "source_tenant_id"),
            (self.target_tenant_id, "target_tenant_id"),
        ):
            required(value, name)
        for name in (
            "kit_id",
            "source_transformation_id",
            "source_tenant_id",
            "target_tenant_id",
        ):
            object.__setattr__(self, name, required(getattr(self, name), name))
        if self.source_tenant_id == self.target_tenant_id:
            raise ValueError("replication kit source and target tenants must differ")
        object.__setattr__(self, "stage", enum_required(self.stage, ReplicationStage, "stage"))
        for name in (
            "methodology",
            "discovery_template",
            "classification_taxonomy",
            "governance_templates",
            "evaluation_suite_refs",
            "golden_dataset_refs",
            "kpi_refs",
            "measurement_refs",
            "deployment_plan",
            "rollback_plan",
            "handoff_artifacts",
            "training_artifacts",
            "customer_specific",
            "learned_adaptations",
        ):
            object.__setattr__(
                self,
                name,
                tuple(required(value, name) for value in getattr(self, name)),
            )
        if not self.methodology:
            raise ValueError("replication kit requires reusable methodology")
        if not self.discovery_template or not self.classification_taxonomy:
            raise ValueError("replication kit requires discovery and classification contracts")
        if not self.governance_templates or not self.evaluation_suite_refs:
            raise ValueError("replication kit requires governance and evaluation contracts")
        if not self.golden_dataset_refs or not self.kpi_refs or not self.measurement_refs:
            raise ValueError("replication kit requires golden datasets, KPIs, and measurements")
        if not self.deployment_plan or not self.rollback_plan:
            raise ValueError("replication kit requires deployment and rollback plans")
        if not self.handoff_artifacts or not self.training_artifacts:
            raise ValueError("replication kit requires handoff and training artifacts")
        object.__setattr__(
            self,
            "adaptation_parameters",
            tuple(
                (required(key, "adaptation key"), required(value, "adaptation value"))
                for key, value in self.adaptation_parameters
            ),
        )
        for name in (
            "source_outcome_ref",
            "target_transformation_id",
            "target_outcome_ref",
        ):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, required(value, name))
        object.__setattr__(
            self,
            "evidence_refs",
            unique_ids(self.evidence_refs, "evidence_ref"),
        )
        if self.stage in {
            ReplicationStage.DEPLOYED,
            ReplicationStage.MEASURED,
            ReplicationStage.ACCEPTED,
            ReplicationStage.FAILED,
        } and self.target_transformation_id is None:
            raise ValueError("deployed or terminal kit requires target transformation")
        if self.stage in {ReplicationStage.MEASURED, ReplicationStage.ACCEPTED}:
            if self.source_outcome_ref is None or self.target_outcome_ref is None:
                raise ValueError("qualified kit requires source and target outcomes")
            if not self.evidence_refs:
                raise ValueError("qualified kit requires evidence references")

    def validate(self) -> None:
        """Validate the kit without making a business-success claim."""
        self.to_replication_profile()

    def to_replication_profile(self) -> ReplicationProfile:
        """Project the kit into the canonical replication domain contract."""
        return ReplicationProfile(
            replication_id=self.kit_id,
            source_transformation_id=self.source_transformation_id,
            source_tenant_id=self.source_tenant_id,
            target_tenant_id=self.target_tenant_id,
            methodology=self.methodology,
            customer_specific=self.customer_specific,
            learned_adaptations=self.learned_adaptations,
            adaptation_parameters=self.adaptation_parameters,
            stage=self.stage,
            source_outcome_ref=self.source_outcome_ref,
            target_transformation_id=self.target_transformation_id,
            target_outcome_ref=self.target_outcome_ref,
            evidence_refs=self.evidence_refs,
        )


__all__ = ["EnterpriseReplicationKit"]
