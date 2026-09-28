"""End-to-end certification bundle and fail-closed validation (M14)."""
from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum
from .evidence import digest

class CertificationStatus(StrEnum):
    CERTIFIED="certified"; FAILED="failed"; UNKNOWN="unknown"

@dataclass(frozen=True,slots=True)
class CertificationBundle:
    revision:str
    phase_results:tuple[tuple[str,CertificationStatus],...]
    evidence_digest:str
    def __post_init__(self)->None:
        if not self.revision.strip() or not self.phase_results or not self.evidence_digest.strip():
            raise ValueError("incomplete certification bundle")

class CertificationValidator:
    REQUIRED=tuple(f"M{i}" for i in range(15))
    def validate(self,bundle:CertificationBundle)->CertificationStatus:
        results=dict(bundle.phase_results)
        if any(phase not in results for phase in self.REQUIRED): return CertificationStatus.UNKNOWN
        if any(results[p] is not CertificationStatus.CERTIFIED for p in self.REQUIRED): return CertificationStatus.FAILED
        expected=digest(sorted(bundle.phase_results))
        if expected!=bundle.evidence_digest: return CertificationStatus.FAILED
        return CertificationStatus.CERTIFIED
