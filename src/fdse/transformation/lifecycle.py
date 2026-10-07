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
from .replication import ReplicationProfile, ReplicationStage
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
        """Fail closed on cross-object scope, identity, and reference mismatches."""
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

        unique_ids(
            tuple(receipt.receipt_id for receipt in self.execution_receipts),
            "receipt_id",
        )
        receipt_run_refs = {receipt.run_ref for receipt in self.execution_receipts}
        if len(receipt_run_refs) != len(self.execution_receipts):
            raise ValueError("execution receipts contain duplicate run references")
        terminal_states = {
            receipt.run_ref: receipt.state
            for receipt in self.execution_receipts
            if receipt.state.value in {"SUCCEEDED", "FAILED", "CANCELLED", "PARTIAL"}
        }
        if len(terminal_states) != sum(
            receipt.state.value in {"SUCCEEDED", "FAILED", "CANCELLED", "PARTIAL"}
            for receipt in self.execution_receipts
        ):
            raise ValueError("execution run has contradictory terminal receipts")
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
        unique_ids(tuple(measurement_ids), "measurement_id")
        for measurement in self.measurements:
            if measurement.transformation_id != transformation.transformation_id:
                raise ValueError("measurement transformation does not match")
            if measurement.tenant_id != transformation.tenant_id:
                raise ValueError("measurement tenant does not match")
            if measurement.revision != transformation.revision:
                raise ValueError("measurement revision does not match")

        evidence_ids = {
            observation.evidence.evidence_id
            for observation in self.baseline.observations
        }
        evidence_ids.update(
            evidence.evidence_id
            for classification in transformation.target_state.classifications
            for evidence in classification.evidence
        )
        evidence_ids.update(
            evidence_ref
            for receipt in self.execution_receipts
            for evidence_ref in receipt.evidence_refs
        )
        evidence_ids.update(
            measurement.evidence.evidence_id
            for measurement in self.measurements
            if measurement.evidence is not None
        )
        if self.outcome is not None:
            evidence_ids.update(evidence.evidence_id for evidence in self.outcome.evidence)

        if self.binding is not None:
            if not set(self.binding.measurement_refs).issubset(measurement_ids):
                raise ValueError("binding measurement references do not resolve")
            if not set(self.binding.evidence_refs).issubset(evidence_ids):
                raise ValueError("binding evidence references do not resolve")

        if self.outcome is not None:
            if self.outcome.transformation_id != transformation.transformation_id:
                raise ValueError("outcome transformation does not match")
            if self.outcome.tenant_id != transformation.tenant_id:
                raise ValueError("outcome tenant does not match")
            if self.outcome.version != transformation.version:
                raise ValueError("outcome version does not match")
            if (
                self.binding is not None
                and self.binding.outcome_ref is not None
                and self.binding.outcome_ref != self.outcome.outcome_id
            ):
                raise ValueError("binding outcome reference does not match outcome")
            baseline_refs = set(self.outcome.baseline_refs)
            target_refs = set(self.outcome.target_refs)
            if not baseline_refs.issubset(measurement_ids):
                raise ValueError("outcome baseline references do not resolve")
            if not target_refs.issubset(measurement_ids):
                raise ValueError("outcome target references do not resolve")
            baseline_measurements = {
                measurement.measurement_id: measurement
                for measurement in self.measurements
                if measurement.measurement_id in baseline_refs
            }
            target_measurements = {
                measurement.measurement_id: measurement
                for measurement in self.measurements
                if measurement.measurement_id in target_refs
            }
            for measurement in baseline_measurements.values():
                if measurement.stage is not MeasurementStage.BASELINE:
                    raise ValueError("outcome baseline reference is not a baseline measurement")
            for measurement in target_measurements.values():
                if measurement.stage is not MeasurementStage.TARGET:
                    raise ValueError("outcome target reference is not a target measurement")
            referenced_measurements = list(
                baseline_measurements.values()
            ) + list(target_measurements.values())
            referenced_metric_ids = {
                measurement.metric_id for measurement in referenced_measurements
            }
            observed_metric_ids = {
                metric_id for metric_id, _ in self.outcome.observed_values
            }
            if referenced_metric_ids != observed_metric_ids:
                raise ValueError("outcome observed values must exactly match referenced metrics")
            observed_by_metric = dict(self.outcome.observed_values)
            variance_by_metric = dict(self.outcome.variance)
            for metric_id in referenced_metric_ids:
                baselines = [
                    measurement for measurement in baseline_measurements.values()
                    if measurement.metric_id == metric_id
                ]
                if len(baselines) != 1:
                    raise ValueError("outcome requires exactly one baseline measurement per metric")
                candidates = [
                    measurement for measurement in self.measurements
                    if measurement.metric_id == metric_id
                    and measurement.stage
                    in {MeasurementStage.POST_DEPLOYMENT, MeasurementStage.FOLLOW_UP}
                    and measurement.window == self.outcome.measurement_period
                ]
                if len(candidates) != 1:
                    raise ValueError(
                        "outcome requires exactly one observed measurement per metric "
                        "and period"
                    )
                observed = candidates[0]
                baseline = baselines[0]
                if observed.unit != baseline.unit:
                    raise ValueError("outcome measurement unit does not match baseline unit")
                if observed_by_metric[metric_id] != observed.value:
                    raise ValueError("outcome observed value does not match measurement")
                expected_variance = observed.value - baseline.value
                if variance_by_metric[metric_id] != expected_variance:
                    raise ValueError("outcome variance does not match observed minus baseline")
            if not any(
                measurement.stage in {
                    MeasurementStage.POST_DEPLOYMENT,
                    MeasurementStage.FOLLOW_UP,
                }
                for measurement in self.measurements
            ):
                raise ValueError(
                    "outcome requires a post-deployment or follow-up measurement"
                )

        if self.handoff is not None:
            if self.handoff.transformation_id != transformation.transformation_id:
                raise ValueError("handoff transformation does not match")
            if self.handoff.tenant_id != transformation.tenant_id:
                raise ValueError("handoff tenant does not match")
            if self.handoff.ownership_status.value == "TRANSFERRED":
                if not set(self.handoff.acceptance_evidence).issubset(evidence_ids):
                    raise ValueError("transferred handoff acceptance evidence does not resolve")

        unique_ids(
            tuple(replication.replication_id for replication in self.replications),
            "replication_id",
        )
        for replication in self.replications:
            if replication.source_transformation_id != transformation.transformation_id:
                raise ValueError("replication source transformation does not match")
            if replication.source_tenant_id != transformation.tenant_id:
                raise ValueError("replication source tenant does not match")
            if replication.target_tenant_id == transformation.tenant_id:
                raise ValueError("replication target tenant must differ from source")
            if replication.source_outcome_ref is not None:
                if (
                    self.outcome is None
                    or replication.source_outcome_ref != self.outcome.outcome_id
                ):
                    raise ValueError("replication source outcome reference does not resolve")
            if replication.stage in {ReplicationStage.MEASURED, ReplicationStage.ACCEPTED}:
                if (
                    replication.target_transformation_tenant_id
                    != replication.target_tenant_id
                ):
                    raise ValueError(
                        "replication target transformation tenant does not match target"
                    )
                if replication.target_transformation_version is None:
                    raise ValueError(
                        "qualified replication target transformation version is required"
                    )
                if replication.target_outcome_tenant_id != replication.target_tenant_id:
                    raise ValueError("replication target outcome tenant does not match target")
            if (
                replication.stage
                in {
                    ReplicationStage.DEPLOYED,
                    ReplicationStage.MEASURED,
                    ReplicationStage.ACCEPTED,
                    ReplicationStage.FAILED,
                }
                and replication.target_transformation_id is None
            ):
                raise ValueError(
                    "deployed or terminal replication requires target transformation reference"
                )
            if replication.stage in {
                ReplicationStage.DEPLOYED,
                ReplicationStage.MEASURED,
                ReplicationStage.ACCEPTED,
                ReplicationStage.FAILED,
            }:
                if (
                    replication.target_transformation_tenant_id
                    != replication.target_tenant_id
                ):
                    raise ValueError(
                        "replication target transformation tenant does not match target"
                    )
                if replication.target_transformation_version is None:
                    raise ValueError(
                        "deployed or terminal replication requires target transformation "
                        "version"
                    )
            if (
                replication.stage
                in {
                    ReplicationStage.MEASURED,
                    ReplicationStage.ACCEPTED,
                    ReplicationStage.FAILED,
                }
                and not set(replication.evidence_refs).issubset(evidence_ids)
            ):
                raise ValueError("replication evidence references do not resolve")

    def require_ga_contract(self) -> None:
        """Require repository-level lifecycle objects without claiming external success."""
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
