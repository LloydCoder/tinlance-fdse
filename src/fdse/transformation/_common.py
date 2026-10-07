# ruff: noqa: E501
# fmt: off
"""Private validation and deterministic serialization helpers."""
from __future__ import annotations
from dataclasses import asdict, is_dataclass
from enum import StrEnum
from typing import Any
from uuid import UUID
from fdse.evidence import canonical_json, digest

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

def json_value(value: Any) -> Any:
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, StrEnum):
        return value.value
    if is_dataclass(value):
        return {key: json_value(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): json_value(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_value(item) for item in value]
    return value

def serialize(value: Any) -> bytes:
    return canonical_json(json_value(value))

def digest_value(value: Any) -> str:
    return digest(json_value(value))
