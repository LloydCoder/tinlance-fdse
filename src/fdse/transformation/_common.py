"""Private validation and deterministic serialization helpers.

These helpers are deliberately strict because transformation objects are
security- and business-critical contracts.  Dataclass annotations alone do
not validate runtime inputs.
"""
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum, StrEnum
import math
from typing import Any, cast
from uuid import UUID

from fdse.contracts import EvidenceRef, ProvenanceRef
from fdse.evidence import canonical_json, digest

_EVIDENCE_KINDS = frozenset({"observation", "artifact", "test_result", "tool_result", "report"})


def required(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    value = value.strip()
    if not value:
        raise ValueError(f"{field_name} is required")
    if "\x00" in value:
        raise ValueError(f"{field_name} contains a NUL byte")
    return value


def unique_ids(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    values = tuple(required(v, field_name) for v in values)
    if len(set(values)) != len(values):
        raise ValueError(f"{field_name} contains duplicate identifiers")
    return values


def enum_required(value: Any, enum_type: type[Enum], field_name: str) -> Any:
    if isinstance(value, enum_type):
        return value
    if isinstance(value, str):
        try:
            return enum_type(value)
        except ValueError as exc:
            raise ValueError(f"{field_name} is not a valid {enum_type.__name__}") from exc
    raise TypeError(f"{field_name} must be {enum_type.__name__} or its canonical string value")


def finite_number(value: Any, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{field_name} must be finite")
    return result


def validate_evidence_ref(value: EvidenceRef, field_name: str = "evidence") -> EvidenceRef:
    if not isinstance(value, EvidenceRef):
        raise TypeError(f"{field_name} must be EvidenceRef")
    if not isinstance(value.provenance, ProvenanceRef):
        raise TypeError(f"{field_name}.provenance must be ProvenanceRef")
    required(value.evidence_id, f"{field_name}.evidence_id")
    required(value.integrity_digest, f"{field_name}.integrity_digest")
    required(value.provenance.source_id, f"{field_name}.provenance.source_id")
    required(value.provenance.revision, f"{field_name}.provenance.revision")
    if not isinstance(value.kind, str) or value.kind not in _EVIDENCE_KINDS:
        raise ValueError(f"{field_name}.kind is not canonical")
    return value


def json_value(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite values are not serializable")
        return value
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, StrEnum):
        return value.value
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: json_value(item) for key, item in asdict(cast(Any, value)).items()}
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise TypeError("serialization mappings require string keys")
        return {key: json_value(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_value(item) for item in value]
    raise TypeError(f"unsupported value for canonical serialization: {type(value).__name__}")


def serialize(value: Any) -> bytes:
    return canonical_json(json_value(value))


def digest_value(value: Any) -> str:
    return digest(json_value(value))
