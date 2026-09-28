"""Domain security controls and threat-model declarations (M12)."""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum


class ControlClass(StrEnum):
    INPUT = "input"
    TENANT = "tenant"
    SECRET = "secret"
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


_SECRET = re.compile(
    r"(?i)(api[_-]?key|token|password|secret|authorization)\s*[:=]\s*[^\s,;]+"
)


def redact(value: str) -> str:
    if "\x00" in value:
        raise ValueError("NUL is not permitted")
    return _SECRET.sub(lambda match: match.group(1) + "=[REDACTED]", value)
