from datetime import UTC, datetime, timedelta

import pytest

from fdse.ecosystem_runtime import (
    CapabilityGrant,
    DependencyConstraint,
    EcosystemRuntime,
    ExtensionKind,
    ExtensionManifest,
    ExtensionProvenance,
    ExtensionState,
    Version,
)

NOW = datetime(2026, 10, 1, tzinfo=UTC)


class AllowSignatureVerifier:
    def verify(self, manifest: ExtensionManifest) -> bool:
        return True


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
            and set(grant.capabilities).issubset(
                set(manifest.requested_capabilities)
            )
        )


def provenance() -> ExtensionProvenance:
    return ExtensionProvenance(
        "publisher",
        "https://example.invalid/source",
        "abc",
        "a" * 64,
        "b" * 64,
    )


def manifest(
    extension_id: str,
    version: Version | None = None,
    *,
    dependencies: tuple[DependencyConstraint, ...] = (),
    capabilities: tuple[str, ...] = (),
) -> ExtensionManifest:
    version = version or Version(1, 0, 0)
    return ExtensionManifest(
        extension_id,
        ExtensionKind.SKILL,
        version,
        "fdse.ecosystem.v1",
        "c" * 64,
        "d" * 64,
        provenance(),
        dependencies,
        capabilities,
    )


def runtime() -> EcosystemRuntime:
    return EcosystemRuntime(
        signature_verifier=AllowSignatureVerifier(),
        grant_authority=AllowCapabilityGrantAuthority(),
    )


def grant(extension_id: str, capabilities: tuple[str, ...]) -> CapabilityGrant:
    return CapabilityGrant(
        f"grant:{extension_id}",
        extension_id,
        capabilities,
        "agent-platform-governance",
        NOW + timedelta(hours=1),
    )


def test_enable_requires_verification_and_explicit_grant() -> None:
    rt = runtime()
    rt.register(manifest("skill-a", capabilities=("repository.read",)))
    with pytest.raises(PermissionError):
        rt.enable("skill-a", grant=grant("skill-a", ("repository.read",)), now=NOW)
    rt.verify("skill-a")
    enabled = rt.enable(
        "skill-a",
        grant=grant("skill-a", ("repository.read",)),
        now=NOW,
    )
    assert enabled.state is ExtensionState.ENABLED


def test_grant_cannot_add_undeclared_capability() -> None:
    rt = runtime()
    rt.register(manifest("skill-a"))
    rt.verify("skill-a")
    with pytest.raises(ValueError):
        rt.enable(
            "skill-a",
            grant=grant("skill-a", ("network.write",)),
            now=NOW,
        )


def test_dependency_constraints_are_enforced() -> None:
    rt = runtime()
    rt.register(manifest("base", Version(1, 2, 0)))
    rt.verify("base")
    rt.enable("base", grant=None, now=NOW)
    rt.register(
        manifest(
            "consumer",
            dependencies=(
                DependencyConstraint("base", Version(1, 1, 0), Version(2, 0, 0)),
            ),
        )
    )
    rt.verify("consumer")
    assert rt.enable("consumer", grant=None, now=NOW).state is ExtensionState.ENABLED


def test_quarantine_blocks_enable_and_rollback_restores_prior_version() -> None:
    rt = runtime()
    rt.register(manifest("skill", Version(1, 0, 0)))
    rt.verify("skill")
    rt.enable("skill", grant=None, now=NOW)
    rt.register(manifest("skill", Version(1, 1, 0)))
    rt.verify("skill")
    quarantined = rt.quarantine("skill", "malicious behavior observed")
    assert quarantined.state is ExtensionState.QUARANTINED
    with pytest.raises(PermissionError):
        rt.enable("skill", grant=None, now=NOW)
    rolled_back = rt.rollback("skill")
    assert rolled_back.state is ExtensionState.ROLLED_BACK
    assert rolled_back.manifest.version == Version(1, 0, 0)


def test_invalid_signature_is_fail_closed() -> None:
    class Deny:
        def verify(self, manifest: ExtensionManifest) -> bool:
            return False

    rt = EcosystemRuntime(
        signature_verifier=Deny(),
        grant_authority=AllowCapabilityGrantAuthority(),
    )
    rt.register(manifest("bad"))
    with pytest.raises(PermissionError):
        rt.verify("bad")


def test_manifest_digest_is_deterministic_and_complete() -> None:
    rt = runtime()
    rt.register(manifest("skill", capabilities=("repository.read",)))
    first = rt.manifest_digest("skill")
    second = rt.manifest_digest("skill")
    assert first == second
    rt.records["skill"] = rt.records["skill"].__class__(
        rt.records["skill"].manifest,
        rt.records["skill"].state,
        rt.records["skill"].previous_version,
    )
    assert rt.manifest_digest("skill") == first


def test_expired_and_wrong_extension_grants_fail_closed() -> None:
    rt = runtime()
    rt.register(manifest("skill", capabilities=("repository.read",)))
    rt.verify("skill")
    expired = CapabilityGrant(
        "expired",
        "skill",
        ("repository.read",),
        "agent-platform-governance",
        NOW,
    )
    with pytest.raises(PermissionError):
        rt.enable("skill", grant=expired, now=NOW)
    wrong = grant("other", ("repository.read",))
    with pytest.raises(PermissionError):
        rt.enable("skill", grant=wrong, now=NOW)


def test_naive_time_is_rejected() -> None:
    with pytest.raises(ValueError):
        CapabilityGrant(
            "grant",
            "skill",
            ("repository.read",),
            "agent-platform-governance",
            datetime(2026, 10, 1),
        )


def test_invalid_dependency_range_and_self_dependency_fail_closed() -> None:
    with pytest.raises(ValueError):
        DependencyConstraint("base", Version(2, 0, 0), Version(2, 0, 0))
    with pytest.raises(ValueError):
        manifest(
            "self",
            dependencies=(DependencyConstraint("self", Version(1, 0, 0)),),
        )
