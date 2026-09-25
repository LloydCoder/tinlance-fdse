"""Security invariants enforceable without owning execution.

Workspace-path validation here is lexical only. It is not a filesystem
sandbox and does not defend against symlinks, mount points, bind mounts, or
other filesystem topology. Those controls belong to the Agent Platform
sandbox and execution boundary.
"""

from pathlib import PurePosixPath

from .errors import BoundaryViolation


def validate_workspace_relative_path(value: str) -> str:
    """Accept only normalized, relative POSIX paths.

    This validates path syntax and lexical traversal only; it does not access
    the filesystem or establish a security boundary around a workspace.
    """

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
