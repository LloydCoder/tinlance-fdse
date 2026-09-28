"""Tamper-evident digest helpers for domain records."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, is_dataclass
from typing import Any

from .evidence import canonical_json


def record_digest(record: Any) -> str:
    if is_dataclass(record) and not isinstance(record, type):
        value = asdict(record)
    else:
        value = record
    return hashlib.sha256(canonical_json(value)).hexdigest()


def chain_digest(previous_digest: str, record: Any) -> str:
    if not previous_digest:
        raise ValueError("previous digest is required")
    return hashlib.sha256((previous_digest + record_digest(record)).encode("ascii")).hexdigest()
