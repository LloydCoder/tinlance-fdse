# fmt: off
"""End-to-end Transformation lifecycle consistency contract."""
from __future__ import annotations

from dataclasses import dataclass

from ._common import unique_ids
from .baseline import Baseline
from .binding import AgentSystemBinding
from .execution import GovernedExecutionReceipt
from .handoff import Handoff
from .measurement import Measurement, MeasurementStage
from .outcome import Outcome
from .realization import EngineeringRealization
from .replication import ReplicationProfile
from .transformation import Transformation


@dataclass(frozen=True, slots=True)
class TransformationLifecycle:
    """Correlate the complete FDSE transformation lifecycle without executing it."""

    transformation: Transformation
    baseline: Baseline
    realization: EngineeringRealization
    binding: AgentSystemBinding | None = None
    execution_receipts: tuple[GovernedExecutionReceipt, ...] = ()
    measurements: tuple[Measurement, ...] = ()
    outcome: Outcome | None = None
    handoff: Handoff | None = None
    replications: tuple[ReplicationProfile, ...] = ()

    def validate_internal_consistency(self) -> None:
        """Fail closed on cross-object scope and identity mismatches."""
        transformation = self.transformation
        if self.baseline.tenant_id != transformation.tenant_id:
            raise ValueError("baseline tenant does not match transformation")
        if self.baseline.revision != transformation.revision:
            raise ValueError("baseline revision does not match transformation")
        if self.baseline.version != transformation.version:
            raise ValueError("baseline version does not match transformation")
        if self.realization.transformation_id != transformation.transformation_id:
            raise ValueError("realization transformation does not match")
        if self.realization.transformation_version != transformation.version:
            raise ValueError("realization version does not match")
        if self.realization.target_process_id != transformation.process.process_id:
            raise ValueError("realization process does not match")

        if self.binding is None and self.execution_receipts:
            raise ValueError("execution receipts require an Agent System binding")
        if self.binding is not None:
            if self.binding.transformation_id != transformation.transformation_id:
                raise ValueError("binding transformation does not match")
            if self.binding.transformation_version != transformation.version:
                raise ValueError("binding version does not match")
            if self.binding.tenant_id != transformation.tenant_id:
                raise ValueError("binding tenant does not match")

        if self.execution_receipts:
            unique_ids(
                tuple(receipt.receipt_id for receipt in self.execution_receipts),
                "receipt_id",
            )
        receipt_run_refs = {receipt.run_ref for receipt in self.execution_receipts}
        for receipt in self.execution_receipts:
            if receipt.transformation_id != transformation.transformation_id:
                raise ValueError("execution receipt transformation does not match")
            if receipt.tenant_id != transformation.tenant_id:
                raise ValueError("execution receipt tenant does not match")
            if self.binding is None or receipt.binding_id != self.binding.binding_id:
                raise ValueError("execution receipt binding does not match")
        if self.binding is not None and self.binding.execution_ref is not None:
            if self.binding.execution_ref not in receipt_run_refs:
                raise ValueError("binding execution reference has no matching receipt")
        measurement_ids = {measurement.measurement_id for measurement in self.measurements}
        if self.binding is not None and not set(self.binding.measurement_refs).issubset(measurement_ids):
            raise ValueError("binding measurement references do not resolve")

        if self.measurements:
            unique_ids(
                tuple(measurement.measurement_id for measurement in self.measurements),
                "measurement_id",
            )
        for measurement in self.measurements:
            if measurement.transformation_id != transformation.transformation_id:
                raise ValueError("measurement transformation does not match")
            if measurement.tenant_id != transformation.tenant_id:
                raise ValueError("measurement tenant does not match")
            if measurement.revision != transformation.revision:
                raise ValueError("measurement revision does not match")

        if self.outcome is not None:
            if self.outcome.transformation_id != transformation.transformation_id:
                raise ValueError("outcome transformation does not match")
            if self.outcome.tenant_id != transformation.tenant_id:
                raise ValueError("outcome tenant does not match")
            if self.outcome.version != transformation.version:
                raise ValueError("outcome version does not match")
            if self.binding is not None and self.binding.outcome_ref is not None and self.binding.outcome_ref != self.outcome.outcome_id:
                raise ValueError("binding outcome reference does not match outcome")
            if not any(
                measurement.stage
                in {MeasurementStage.POST_DEPLOYMENT, MeasurementStage.FOLLOW_UP}
                for measurement in self.measurements
            ):
                raise ValueError("outcome requires a post-deployment or follow-up measurement")

        if self.handoff is not None:
            if self.handoff.transformation_id != transformation.transformation_id:
                raise ValueError("handoff transformation does not match")
            if self.handoff.tenant_id != transformation.tenant_id:
                raise ValueError("handoff tenant does not match")

        if self.replications:
            unique_ids(tuple(rep.replication_id for rep in self.replications), "replication_id")
        for replication in self.replications:
            if replication.source_transformation_id != transformation.transformation_id:
                raise ValueError("replication source transformation does not match")
            if replication.source_tenant_id != transformation.tenant_id:
                raise ValueError("replication source tenant does not match")

    def require_ga_contract(self) -> None:
        """Require the repository-level lifecycle objects without claiming external success."""
        self.validate_internal_consistency()
        if self.binding is None:
            raise ValueError("GA contract requires an Agent System binding")
        if not self.execution_receipts:
            raise ValueError("GA contract requires execution receipt contracts")
        if not self.measurements:
            raise ValueError("GA contract requires measurement contracts")
        if self.outcome is None:
            raise ValueError("GA contract requires an outcome contract")
        if self.handoff is None:
            raise ValueError("GA contract requires a handoff contract")


__all__ = ["TransformationLifecycle"]
