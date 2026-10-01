"""Governed agent-ecosystem runtime semantics (M18).

FDSE owns extension metadata, dependency/lifecycle semantics, provenance, and
quarantine/rollback state. Signature verification, capability grants, artifact
storage, sandboxing, network policy, and execution remain external authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol

from .evidence import digest


class ExtensionKind(StrEnum):
    SKILL = "skill"
    APPLICATION = "application"
    EXTENSION = "extension"
    CONNECTOR = "connector"
    PACKAGE = "package"


class ExtensionState(StrEnum):
    REGISTERED = "registered"
    VERIFIED = "verified"
    ENABLED = "enabled"
    DISABLED = "disabled"
    QUARANTINED = "quarantined"
    ROLLED_BACK = "rolled_back"


@dataclass(frozen=True, slots=True)
class Version:
    major: int
    minor: int
    patch: int = 0

    def __post_init__(self) -> None:
        if min(self.major, self.minor, self.patch) < 0:
            raise ValueError("version components cannot be negative")

    def as_tuple(self) -> tuple[int, int, int]:
        return self.major, self.minor, self.patch


@dataclass(frozen=True, slots=True)
class DependencyConstraint:
    extension_id: str
    minimum: Version
    maximum_exclusive: Version | None = None

    def accepts(self, version: Version) -> bool:
        if version.as_tuple() < self.minimum.as_tuple():
            return False
        if (
            self.maximum_exclusive is not None
            and version.as_tuple() >= self.maximum_exclusive.as_tuple()
        ):
            return False
        return True


@dataclass(frozen=True, slots=True)
class ExtensionProvenance:
    publisher: str
    source: str
    source_revision: str
    build_digest: str
    attestation_digest: str

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.publisher,
                self.source,
                self.source_revision,
                self.build_digest,
                self.attestation_digest,
            )
        ):
            raise ValueError("extension provenance is required")
        for value in (self.build_digest, self.attestation_digest):
            if len(value) != 64 or any(
                char not in "0123456789abcdef" for char in value.lower()
            ):
                raise ValueError("extension provenance digests must be SHA-256 hex")


@dataclass(frozen=True, slots=True)
class ExtensionManifest:
    extension_id: str
    kind: ExtensionKind
    version: Version
    api_version: str
    artifact_digest: str
    signature_digest: str
    provenance: ExtensionProvenance
    dependencies: tuple[DependencyConstraint, ...] = ()
    requested_capabilities: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.extension_id,
                self.api_version,
                self.artifact_digest,
                self.signature_digest,
            )
        ):
            raise ValueError("extension manifest fields are required")
        for value in (self.artifact_digest, self.signature_digest):
            if len(value) != 64 or any(
                char not in "0123456789abcdef" for char in value.lower()
            ):
                raise ValueError("extension manifest digests must be SHA-256 hex")
        if len(set(self.requested_capabilities)) != len(self.requested_capabilities):
            raise ValueError("requested capabilities must be unique")
        dependency_ids = [item.extension_id for item in self.dependencies]
        if len(dependency_ids) != len(set(dependency_ids)):
            raise ValueError("dependency identifiers must be unique")


@dataclass(frozen=True, slots=True)
class CapabilityGrant:
    grant_id: str
    extension_id: str
    capabilities: tuple[str, ...]
    issuer: str
    expires_at: datetime

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (self.grant_id, self.extension_id, self.issuer)
        ):
            raise ValueError("capability grant fields are required")
        if not self.capabilities:
            raise ValueError("capability grant must contain explicit capabilities")
        if len(set(self.capabilities)) != len(self.capabilities):
            raise ValueError("capability grant capabilities must be unique")


class SignatureVerifier(Protocol):
    def verify(self, manifest: ExtensionManifest) -> bool: ...


class CapabilityGrantAuthority(Protocol):
    def verify(
        self,
        manifest: ExtensionManifest,
        grant: CapabilityGrant,
        *,
        now: datetime,
    ) -> bool: ...


class AllowSignatureVerifier:
    def verify(self, manifest: ExtensionManifest) -> bool:
        return True


class DenySignatureVerifier:
    def verify(self, manifest: ExtensionManifest) -> bool:
        return False


class AllowCapabilityGrantAuthority:
    def verify(
        self,
        manifest: ExtensionManifest,
        grant: CapabilityGrant,
        *,
        now: datetime,
    ) -> bool:
        return (
            grant.extension_id == manifest.extension_id
            and now < grant.expires_at
            and set(grant.capabilities).issubset(set(manifest.requested_capabilities))
        )


class DenyCapabilityGrantAuthority:
    def verify(
        self,
        manifest: ExtensionManifest,
        grant: CapabilityGrant,
        *,
        now: datetime,
    ) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class ExtensionRecord:
    manifest: ExtensionManifest
    state: ExtensionState
    previous_version: Version | None = None
    quarantine_reason: str | None = None


class EcosystemRuntime:
    """Deterministic extension registry; it never grants capability authority."""

    def __init__(
        self,
        *,
        signature_verifier: SignatureVerifier,
        grant_authority: CapabilityGrantAuthority,
    ) -> None:
        self.signature_verifier = signature_verifier
        self.grant_authority = grant_authority
        self.records: dict[str, ExtensionRecord] = {}
        self.history: dict[str, tuple[ExtensionManifest, ...]] = {}

    def register(self, manifest: ExtensionManifest) -> ExtensionRecord:
        current = self.records.get(manifest.extension_id)
        if current is not None and manifest.version.as_tuple() <= current.manifest.version.as_tuple():
            raise ValueError("extension version must advance monotonically")
        previous = current.manifest.version if current is not None else None
        self.history[manifest.extension_id] = (
            *self.history.get(manifest.extension_id, ()),
            manifest,
        )
        record = ExtensionRecord(manifest, ExtensionState.REGISTERED, previous)
        self.records[manifest.extension_id] = record
        return record

    def verify(self, extension_id: str) -> ExtensionRecord:
        record = self._record(extension_id)
        if not self.signature_verifier.verify(record.manifest):
            raise PermissionError("extension signature verification failed")
        self.records[extension_id] = ExtensionRecord(
            record.manifest,
            ExtensionState.VERIFIED,
            record.previous_version,
        )
        return self.records[extension_id]

    def enable(
        self,
        extension_id: str,
        *,
        grant: CapabilityGrant | None,
        now: datetime,
    ) -> ExtensionRecord:
        record = self._record(extension_id)
        if record.state is ExtensionState.QUARANTINED:
            raise PermissionError("quarantined extension cannot be enabled")
        if record.state is not ExtensionState.VERIFIED:
            raise PermissionError("extension must be verified before enable")
        self._check_dependencies(record.manifest)
        requested = set(record.manifest.requested_capabilities)
        if requested:
            if grant is None:
                raise PermissionError("explicit capability grant is required")
            if not self.grant_authority.verify(
                record.manifest,
                grant,
                now=now,
            ):
                raise PermissionError("capability grant was not authorized")
        elif grant is not None and grant.capabilities:
            raise ValueError("grant cannot add undeclared capabilities")
        self.records[extension_id] = ExtensionRecord(
            record.manifest,
            ExtensionState.ENABLED,
            record.previous_version,
        )
        return self.records[extension_id]

    def disable(self, extension_id: str) -> ExtensionRecord:
        record = self._record(extension_id)
        if record.state is ExtensionState.QUARANTINED:
            return record
        updated = ExtensionRecord(
            record.manifest,
            ExtensionState.DISABLED,
            record.previous_version,
        )
        self.records[extension_id] = updated
        return updated

    def quarantine(self, extension_id: str, reason: str) -> ExtensionRecord:
        if not reason.strip():
            raise ValueError("quarantine reason is required")
        record = self._record(extension_id)
        updated = ExtensionRecord(
            record.manifest,
            ExtensionState.QUARANTINED,
            record.previous_version,
            reason,
        )
        self.records[extension_id] = updated
        return updated

    def rollback(self, extension_id: str) -> ExtensionRecord:
        record = self._record(extension_id)
        history = self.history.get(extension_id, ())
        candidates = [
            item
            for item in history
            if item.version.as_tuple() < record.manifest.version.as_tuple()
        ]
        if not candidates:
            raise ValueError("no prior extension version is available for rollback")
        previous = max(candidates, key=lambda item: item.version.as_tuple())
        updated = ExtensionRecord(
            previous,
            ExtensionState.ROLLED_BACK,
            None,
        )
        self.records[extension_id] = updated
        return updated

    def manifest_digest(self, extension_id: str) -> str:
        record = self._record(extension_id)
        return digest(
            {
                "id": record.manifest.extension_id,
                "kind": record.manifest.kind.value,
                "version": record.manifest.version.as_tuple(),
                "artifact": record.manifest.artifact_digest,
                "signature": record.manifest.signature_digest,
                "provenance": record.manifest.provenance,
                "dependencies": [
                    (
                        item.extension_id,
                        item.minimum.as_tuple(),
                        item.maximum_exclusive.as_tuple()
                        if item.maximum_exclusive
                        else None,
                    )
                    for item in record.manifest.dependencies
                ],
            }
        )

    def _check_dependencies(self, manifest: ExtensionManifest) -> None:
        for dependency in manifest.dependencies:
            record = self.records.get(dependency.extension_id)
            if record is None or record.state is not ExtensionState.ENABLED:
                raise ValueError(
                    f"dependency is not enabled: {dependency.extension_id}"
                )
            if not dependency.accepts(record.manifest.version):
                raise ValueError(
                    f"dependency version is incompatible: {dependency.extension_id}"
                )

    def _record(self, extension_id: str) -> ExtensionRecord:
        try:
            return self.records[extension_id]
        except KeyError as exc:
            raise KeyError(f"unknown extension: {extension_id}") from exc
