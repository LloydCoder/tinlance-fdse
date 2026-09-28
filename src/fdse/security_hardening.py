"""Domain security controls and conservative secret redaction (M12)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum


class ControlClass(StrEnum):
    INPUT = "input"
    TENANT = "tenant"
    SECRET = "secret"  # noqa: S105
    INTEGRITY = "integrity"
    AUTHORITY = "authority"


@dataclass(frozen=True, slots=True)
class SecurityControl:
    control_id: str
    control_class: ControlClass
    statement: str

    def __post_init__(self) -> None:
        if not self.control_id.strip() or not self.statement.strip():
            raise ValueError("security control is required")


_AUTHORIZATION = re.compile(r"(?im)(authorization\s*:\s*)[^\r\n]+")
_SECRET = re.compile(
    r"(?i)(api[_-]?key|token|password|passwd|secret)\s*[:=]\s*"
    r"""(?:"[^"]*"|'[^']*'|[^\s,;}]+)"""
)


def redact(value: str) -> str:
    if "\x00" in value:
        raise ValueError("NUL is not permitted")
    value = _AUTHORIZATION.sub(r"\1[REDACTED]", value)
    return _SECRET.sub(lambda match: match.group(1) + "=[REDACTED]", value)
