import pytest

from fdse.config import Settings
from fdse.errors import ConfigurationError


def test_production_requires_https(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FDSE_ENV", "production")
    monkeypatch.setenv("FDSE_AGENT_PLATFORM_ENDPOINT", "http://example.invalid")

    with pytest.raises(ConfigurationError):
        Settings.from_environment()


def test_local_endpoint_is_allowed_for_tests(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FDSE_ENV", "test")
    monkeypatch.setenv("FDSE_AGENT_PLATFORM_ENDPOINT", "http://127.0.0.1:8080")

    settings = Settings.from_environment()
    assert settings.environment == "test"


def test_external_http_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FDSE_ENV", "development")
    monkeypatch.setenv("FDSE_AGENT_PLATFORM_ENDPOINT", "http://example.invalid")

    with pytest.raises(ConfigurationError):
        Settings.from_environment()


def test_https_requires_a_hostname(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FDSE_ENV", "production")
    monkeypatch.setenv("FDSE_AGENT_PLATFORM_ENDPOINT", "https:///missing-host")

    with pytest.raises(ConfigurationError):
        Settings.from_environment()


def test_production_rejects_local_http(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FDSE_ENV", "production")
    monkeypatch.setenv("FDSE_AGENT_PLATFORM_ENDPOINT", "http://localhost:8080")

    with pytest.raises(ConfigurationError):
        Settings.from_environment()


def test_https_endpoint_is_accepted(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FDSE_ENV", "production")
    monkeypatch.setenv("FDSE_AGENT_PLATFORM_ENDPOINT", "https://agent.example.test")

    settings = Settings.from_environment()
    assert settings.agent_platform_endpoint == "https://agent.example.test"


@pytest.mark.parametrize(
    "endpoint",
    [
        "https://user:password@agent.example.test",
        "https://agent.example.test/path#fragment",
        "https://[invalid",
    ],
)
def test_unsafe_endpoint_forms_are_rejected(monkeypatch: pytest.MonkeyPatch, endpoint: str) -> None:
    monkeypatch.setenv("FDSE_ENV", "production")
    monkeypatch.setenv("FDSE_AGENT_PLATFORM_ENDPOINT", endpoint)

    with pytest.raises(ConfigurationError):
        Settings.from_environment()
