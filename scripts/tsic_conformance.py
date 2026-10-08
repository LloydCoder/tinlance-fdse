#!/usr/bin/env python3
"""Fail-closed FDSE verification against the canonical TSIC adapter."""
from __future__ import annotations
import json
from urllib.request import Request,urlopen
TSIC_REVISION="b30a5926e8af88d9df935b50a45dd21d30cd304a"
ROOT=f"https://raw.githubusercontent.com/LloydCoder/tinlance-system-integration/{TSIC_REVISION}"
REQ={"identity-context","event-envelope","delivery-semantics","trace-context","economic-attribution"}
def get(p):
    q=Request(f"{ROOT}/{p}",headers={"Accept":"application/json","User-Agent":"tinlance-fdse-ci"})
    with urlopen(q,timeout=15) as r:return json.load(r)
def main():
    m=get("manifests/ecosystem.json"); a=get("integrations/fdse/adapter.json"); r=get("catalog/contracts/registry.json")
    s=next(x for x in m["systems"] if x["id"]=="fdse")
    assert s["repository"]=="LloydCoder/tinlance-fdse" and s["governance_role"]=="delivery_orchestration_authority"
    assert a["source_system"]=="tsic" and a["target_system"]=="fdse" and a["status"]=="reference-contract"
    assert {x["tsic_contract"] for x in a["contract_bindings"]}==REQ
    assert {x["id"] for x in r["contracts"]}>=REQ
    assert a["authority"]["integration_contracts"]=="tsic" and a["authority"]["delivery_orchestration"]=="fdse" and a["authority"]["execution_authority"]=="agent-platform"
    required={"delivery_route_is_explicit","engineering_and_transformation_are_distinct_routes","fdse_does_not_grant_platform_execution_authority","evidence_and_outcomes_are_preserved","tsic_remains_integration_authority","agent-platform_remains_execution_authority"}
    assert set(a["invariants"])==required
    print("PASS FDSE TSIC conformance")
if __name__=="__main__":main()
