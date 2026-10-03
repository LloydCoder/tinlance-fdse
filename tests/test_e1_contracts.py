from importlib import metadata

import fdse


def test_runtime_and_distribution_versions_are_identical() -> None:
    assert fdse.__version__ == metadata.version("tinlance-fdse")
    assert fdse.__version__ == "1.9.0"


def test_m15_to_m18_contracts_are_public() -> None:
    expected = (
        "ContextBuilder",
        "WorkflowRuntime",
        "MultiAgentRuntime",
        "EcosystemRuntime",
        "WorkflowDefinition",
        "DelegationRequest",
        "ExtensionManifest",
    )
    for name in expected:
        assert hasattr(fdse, name)


def test_permissive_reference_helpers_are_not_production_exports() -> None:
    assert not hasattr(fdse, "AllowAllApprovalGate")
    assert not hasattr(fdse, "AllowIdentityVerifier")
    assert not hasattr(fdse, "NoopPlatformRunMapper")
