"""E6 enterprise validation, certification, and GA gate semantics.

E6 defines a deterministic, fail-closed validation model for repository,
cross-system, security, recovery, compatibility, and release evidence. It
does not mint evidence, grant production authority, or declare external
systems healthy without explicit external evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .evidence import digest


CORE_PHASES = tuple(f"M{index}" for index in range(19))
ENTERPRISE_PHASES = tuple(f"E{index}" for index in range(1, 7))
ALL_PHASES = CORE_PHASES + ENTERPRISE_PHASES


class ValidationLayer(StrEnum):
    UNIT = "unit"
    CONTRACT = "contract"
    CROSS_REPOSITORY = "cross_repository"
    INTEGRATION = "integration"
    SECURITY = "security"
    ADVERSARIAL = "adversarial"
    PROPERTY = "property"
    FAILURE_INJECTION = "failure_injection"
    WORKFLOW_RECOVERY = "workflow_recovery"
    MEMORY_CONTEXT_SECURITY = "memory_context_security"
    MULTI_AGENT = "multi_agent"
    MCP_TOOL_SECURITY = "mcp_tool_security"
    SUPPLY_CHAIN = "supply_chain"
    PROVENANCE = "provenance"
    END_TO_END = "e2e"
    PERFORMANCE = "performance"
    LOAD = "load"
    CONCURRENCY = "concurrency"
    TENANT_ISOLATION = "tenant_isolation"
    MIGRATION = "migration"
    DISASTER_RECOVERY = "disaster_recovery"
    OBSERVABILITY = "observability"
    DOCUMENTATION = "documentation"
    API_COMPATIBILITY = "api_compatibility"
    DEPENDENCY_SECURITY = "dependency_security"
    CICD = "ci_cd"
    RELEASE_CERTIFICATION = "release_certification"
    PRODUCTION_READINESS = "production_readiness"


class ValidationStatus(StrEnum):
    PASS = "pass"  # noqa: S105
    FAIL = "fail"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class ValidationEvidence:
    phase: str
    layer: ValidationLayer
    status: ValidationStatus
    evidence_id: str
    revision: str
    payload_digest: str

    def __post_init__(self) -> None:
        if self.phase not in ALL_PHASES:
            raise ValueError("validation evidence references an unknown phase")
        if any(not value.strip() for value in (self.evidence_id, self.revision)):
            raise ValueError("validation evidence identity is required")
        if len(self.payload_digest) != 64 or any(
            character not in "0123456789abcdef" for character in self.payload_digest
        ):
            raise ValueError("validation evidence digest must be SHA-256")


@dataclass(frozen=True, slots=True)
class EnterpriseValidationPlan:
    required_phases: tuple[str, ...] = ALL_PHASES
    required_layers: tuple[ValidationLayer, ...] = tuple(ValidationLayer)

    def __post_init__(self) -> None:
        if set(self.required_phases) != set(ALL_PHASES):
            raise ValueError(
                "enterprise validation must cover M0-M18 and E1-E6 exactly"
            )
        if len(self.required_layers) != len(set(self.required_layers)):
            raise ValueError("validation layers must be unique")


class EnterpriseValidationGraph:
    """Deterministic fail-closed validation graph; no external authority is minted."""

    def __init__(self, plan: EnterpriseValidationPlan | None = None) -> None:
        self.plan = plan or EnterpriseValidationPlan()
        self._evidence: dict[tuple[str, ValidationLayer], ValidationEvidence] = {}

    def add_evidence(self, evidence: ValidationEvidence) -> None:
        key = (evidence.phase, evidence.layer)
        existing = self._evidence.get(key)
        if existing is not None and existing != evidence:
            raise ValueError("validation evidence identity collision")
        self._evidence[key] = evidence

    def gate(self) -> None:
        expected = {
            (phase, layer)
            for phase in self.plan.required_phases
            for layer in self.plan.required_layers
        }
        actual = set(self._evidence)
        if actual != expected:
            raise ValueError("enterprise validation evidence coverage is incomplete")
        if any(
            item.status is not ValidationStatus.PASS for item in self._evidence.values()
        ):
            raise ValueError("enterprise validation is not fully passing")

    def snapshot_digest(self) -> str:
        values = sorted(
            (
                item.phase,
                item.layer.value,
                item.status.value,
                item.evidence_id,
                item.revision,
                item.payload_digest,
            )
            for item in self._evidence.values()
        )
        return digest({"evidence": values})

    @property
    def evidence(self) -> tuple[ValidationEvidence, ...]:
        return tuple(
            sorted(
                self._evidence.values(),
                key=lambda item: (item.phase, item.layer.value),
            )
        )
