"""Tinlance FDSE engineering-domain layer."""

from .agents import SpecialistRegistry, SpecialistRole, SpecialistSpec
from .certification import (
    CertificationBundle,
    CertificationStatus,
    CertificationValidator,
)
from .context import (
    ContextBuilder,
    ContextItem,
    ContextKind,
    ContextQuality,
    ContextSnapshot,
    ContextSource,
    ContextStore,
)
from .domain import (
    Assessment,
    ChangeSet,
    ChangeStatus,
    EngineeringContext,
    EngineeringPlan,
    EngineeringReport,
    Evidence,
    Finding,
    FindingStatus,
    PlanStatus,
    Project,
    RepositoryRef,
    VerificationResult,
    VerificationStatus,
)
from .evaluation import (
    EvaluationCase,
    EvaluationOutcome,
    EvaluationResult,
    EvaluationSuite,
)
from .governance import ApprovalStatus, GovernanceBoundary, GovernanceReference
from .intake import (
    IntakeRecord,
    IntakeRegistry,
    IntakeRequest,
    IntakeStatus,
    IntakeValidator,
)
from .platform import (
    AgentPlatformAdapter,
    GovernedPlatformAdapter,
    PlatformCapabilities,
    PlatformCompatibility,
    PlatformExecution,
    PlatformIntent,
)
from .product import CustomerProject, CustomerRequest, TenantBoundary
from .production import (
    HealthProbe,
    HealthStatus,
    IdempotencyRecord,
    Readiness,
    ReadinessGate,
)
from .security_hardening import ControlClass, SecurityControl, redact
from .transitions import transition_change, transition_finding, transition_plan
from .workflows import WorkflowInstance, WorkflowState, transition

__all__ = [
    "Assessment",
    "ChangeSet",
    "ChangeStatus",
    "EngineeringContext",
    "EngineeringPlan",
    "EngineeringReport",
    "Evidence",
    "Finding",
    "FindingStatus",
    "PlanStatus",
    "Project",
    "RepositoryRef",
    "VerificationResult",
    "VerificationStatus",
    "transition_change",
    "transition_finding",
    "transition_plan",
    "IntakeRecord",
    "IntakeRegistry",
    "IntakeRequest",
    "IntakeStatus",
    "IntakeValidator",
    "SpecialistRegistry",
    "SpecialistRole",
    "SpecialistSpec",
    "CertificationBundle",
    "CertificationStatus",
    "CertificationValidator",
    "ContextBuilder",
    "ContextItem",
    "ContextKind",
    "ContextQuality",
    "ContextSnapshot",
    "ContextSource",
    "ContextStore",
    "EvaluationCase",
    "EvaluationOutcome",
    "EvaluationResult",
    "EvaluationSuite",
    "ApprovalStatus",
    "GovernanceBoundary",
    "GovernanceReference",
    "AgentPlatformAdapter",
    "GovernedPlatformAdapter",
    "PlatformCapabilities",
    "PlatformCompatibility",
    "PlatformExecution",
    "PlatformIntent",
    "CustomerProject",
    "CustomerRequest",
    "TenantBoundary",
    "HealthProbe",
    "HealthStatus",
    "IdempotencyRecord",
    "Readiness",
    "ReadinessGate",
    "ControlClass",
    "SecurityControl",
    "redact",
    "WorkflowInstance",
    "WorkflowState",
    "transition",
    "__version__",
]

__version__ = "1.0.0"
