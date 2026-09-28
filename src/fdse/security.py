"""Lexical security invariants; never a substitute for a sandbox."""
from pathlib import PurePosixPath

from .errors import BoundaryViolation


def validate_workspace_relative_path(value: str) -> str:
    """Accept an already-normalized, relative POSIX path only."""

    if not value or "\x00" in value:
        raise BoundaryViolation("workspace path is empty or contains a NUL byte")
    if "\" in value:
        raise BoundaryViolation("workspace path must use POSIX separators")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise BoundaryViolation("workspace path must remain relative")
    normalized = path.as_posix()
    if normalized != value:
        raise BoundaryViolation("workspace path must already be normalized")
    if normalized in {"", "."}:
        raise BoundaryViolation("workspace path must identify a resource")
    return normalized
