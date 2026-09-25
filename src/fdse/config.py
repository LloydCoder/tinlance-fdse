"""Configuration validation for the FDSE domain layer."""

import os
from dataclasses import dataclass
from urllib.parse import urlsplit

from .errors import ConfigurationError


@dataclass(frozen=True, slots=True)
class Settings:
    """Non-secret process configuration."""

    environment: str
    agent_platform_endpoint: str

    @classmethod
    def from_environment(cls) -> "Settings":
        environment = os.environ.get("FDSE_ENV", "").strip()
        endpoint = os.environ.get("FDSE_AGENT_PLATFORM_ENDPOINT", "").strip()

        if environment not in {"development", "test", "production"}:
            raise ConfigurationError(
                "FDSE_ENV must be development, test, or production"
            )
        if not endpoint:
            raise ConfigurationError("FDSE_AGENT_PLATFORM_ENDPOINT is required")

        try:
            parsed = urlsplit(endpoint)
            hostname = parsed.hostname
            _ = parsed.port
        except ValueError as exc:
            raise ConfigurationError(
                "FDSE_AGENT_PLATFORM_ENDPOINT is not a valid URL"
            ) from exc

        if not hostname:
            raise ConfigurationError(
                "FDSE_AGENT_PLATFORM_ENDPOINT must contain a hostname"
            )
        if parsed.username is not None or parsed.password is not None:
            raise ConfigurationError(
                "FDSE_AGENT_PLATFORM_ENDPOINT must not contain embedded credentials"
            )
        if parsed.fragment:
            raise ConfigurationError(
                "FDSE_AGENT_PLATFORM_ENDPOINT must not contain a URL fragment"
            )

        is_local_http = (
            parsed.scheme == "http"
            and hostname in {"localhost", "127.0.0.1", "::1"}
        )
        is_https = parsed.scheme == "https"

        if not is_https and not is_local_http:
            raise ConfigurationError(
                "FDSE_AGENT_PLATFORM_ENDPOINT must use HTTPS except for local development"
            )
        if environment == "production" and is_local_http:
            raise ConfigurationError(
                "production requires an HTTPS Agent Platform endpoint"
            )

        return cls(environment=environment, agent_platform_endpoint=endpoint)
