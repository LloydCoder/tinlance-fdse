#!/usr/bin/env python3
"""Fail-closed FDSE verification against the canonical TSIC adapter."""
from __future__ import annotations

import json
from urllib.request import urlopen

TSIC_REVISION = "b30a5926e8af88d9df935b50a45dd21d30cd304a"
RAW_ROOT = (
    "https://raw.githubusercontent.com/LloydCoder/tinlance-system-integration/"
    f"{TSIC_REVISION}"
)
REQUIRED = {
    "identity-context",
    "event-envelope",
    "delivery-semantics",
    "trace-context",
    "economic-attribution",
}


def get(path: str) -> dict:
    url = f"{RAW_ROOT}/{path}"
    with urlopen(url, timeout=15) as response:  # noqa: S310
        return json.load(response)


def main() -> None:
    manifest = get("manifests/ecosystem.json")
    adapter = get("integrations/fdse/adapter.json")
    registry = get("catalog/contracts/registry.json")
    system = next(item for item in manifest["systems"] if item["id"] == "fdse")

    assert system["repository"] == "LloydCoder/tinlance-fdse"
    assert system["governance_role"] == "delivery_orchestration_authority"
    assert adapter["source_system"] == "tsic"
    assert adapter["target_system"] == "fdse"
    assert adapter["status"] == "reference-contract"
    assert (
        {item["tsic_contract"] for item in adapter["contract_bindings"]} == REQUIRED
    )
    assert {item["id"] for item in registry["contracts"]} >= REQUIRED

    authority = adapter["authority"]
    assert authority["integration_contracts"] == "tsic"
    assert authority["delivery_orchestration"] == "fdse"
    assert authority["execution_authority"] == "agent-platform"

    required_invariants = {
        "delivery_route_is_explicit",
        "engineering_and_transformation_are_distinct_routes",
        "fdse_does_not_grant_platform_execution_authority",
        "evidence_and_outcomes_are_preserved",
        "tsic_remains_integration_authority",
        "agent-platform_remains_execution_authority",
    }
    assert set(adapter["invariants"]) == required_invariants
    print("PASS FDSE TSIC conformance")


if __name__ == "__main__":
    main()
