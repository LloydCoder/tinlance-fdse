"""Repository and CI provider contracts (M7); no execution authority."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class RepositorySnapshot:
    tenant_id: str
    provider: str
    repository_id: str
    revision: str
    default_branch: str

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.tenant_id,
                self.provider,
                self.repository_id,
                self.revision,
                self.default_branch,
            )
        ):
            raise ValueError("repository snapshot fields are required")


@dataclass(frozen=True, slots=True)
class CheckResult:
    tenant_id: str
    name: str
    status: str
    conclusion: str
    revision: str

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.tenant_id,
                self.name,
                self.status,
                self.conclusion,
                self.revision,
            )
        ):
            raise ValueError("check result fields are required")


class RepositoryReader(Protocol):
    def snapshot(
        self, tenant_id: str, repository_id: str, revision: str
    ) -> RepositorySnapshot: ...


class CIRunReader(Protocol):
    def checks(
        self, tenant_id: str, repository_id: str, revision: str
    ) -> tuple[CheckResult, ...]: ...


class GitHubProvider(Protocol):
    def snapshot(
        self, tenant_id: str, repository_id: str, revision: str
    ) -> RepositorySnapshot: ...
    def checks(
        self, tenant_id: str, repository_id: str, revision: str
    ) -> tuple[CheckResult, ...]: ...
