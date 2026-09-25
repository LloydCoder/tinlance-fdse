import pytest

from fdse.errors import BoundaryViolation
from fdse.security import validate_workspace_relative_path


def test_relative_path_is_accepted() -> None:
    assert validate_workspace_relative_path("src/fdse/service.py") == "src/fdse/service.py"


@pytest.mark.parametrize(
    "value",
    ["/etc/passwd", "../secret", "a/../../secret", "", r"src\fdse\service.py"],
)
def test_path_escape_is_rejected(value: str) -> None:
    with pytest.raises(BoundaryViolation):
        validate_workspace_relative_path(value)


def test_nul_is_rejected() -> None:
    with pytest.raises(BoundaryViolation):
        validate_workspace_relative_path("safe.py\x00evil")
