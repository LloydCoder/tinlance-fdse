"""Enterprise end-to-end certification bundle and fail-closed validation (M18)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .evidence import digest


class CertificationStatus(StrEnum):
    CERTIFIED = "certified"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class CertificationBundle:
    revision: str
    phase_results: tuple[tuple[str, CertificationStatus], ...]
    evidence_digest: str
    attestation_id: str
    attestation_issuer: str
    workflow_run_id: str
    commit_sha: str

    def __post_init__(self) -> None:
        if not self.revision.strip() or not self.phase_results:
            raise ValueError("incomplete certification bundle")
        if not self.evidence_digest.strip():
            raise ValueError("certification evidence digest is required")
        if not all(
            value.strip()
            for value in (
                self.attestation_id,
                self.attestation_issuer,
                self.workflow_run_id,
                self.commit_sha,
            )
        ):
            raise ValueError("external attestation metadata is required")


class CertificationValidator:
    REQUIRED = tuple(f"M{i}" for i in range(19))

    def validate(
        self,
        bundle: CertificationBundle,
        expected_revision: str | None = None,
        expected_commit_sha: str | None = None,
    ) -> CertificationStatus:
        results = dict(bundle.phase_results)
        if len(results) != len(bundle.phase_results):
            return CertificationStatus.FAILED
        if any(phase not in results for phase in self.REQUIRED):
            return CertificationStatus.UNKNOWN
        if expected_revision is not None and bundle.revision != expected_revision:
            return CertificationStatus.FAILED
        if expected_commit_sha is not None and bundle.commit_sha != expected_commit_sha:
            return CertificationStatus.FAILED
        if any(results[phase] is not CertificationStatus.CERTIFIED for phase in self.REQUIRED):
            return CertificationStatus.FAILED
        expected_evidence_digest = digest(sorted(bundle.phase_results))
        if bundle.evidence_digest != expected_evidence_digest:
            return CertificationStatus.FAILED
        return CertificationStatus.CERTIFIED
