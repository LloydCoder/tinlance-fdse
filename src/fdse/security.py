"""Security invariants that can be enforced without owning execution."""

from pathlib import PurePosixPath

from .errors import BoundaryViolation


def validate_workspace_relative_path(value: str) -> str:
    """Accept only normalized, relative POSIX paths."""

    if not value or "\x00" in value:
        raise BoundaryViolation("workspace path is empty or contains a NUL byte")
    if "\\" in value:
        raise BoundaryViolation("workspace path must use POSIX separators")

    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise BoundaryViolation("workspace path must remain relative to the governed workspace")

    normalized = path.as_posix()
    if normalized in {"", "."}:
        raise BoundaryViolation("workspace path must identify a resource")

    return normalized
