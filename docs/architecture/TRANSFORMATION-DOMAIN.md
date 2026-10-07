# Transformation Domain Contract

## Status
Phase 1 architectural contract. This document defines the bounded Transformation Domain inside FDSE. It does not claim external production capability, customer outcomes, or replication success.

## Purpose
The Transformation Domain models operational transformation as a versioned, tenant-scoped, evidence-linked, auditable, machine-readable, reproducible domain.
It connects business-process discovery to FDSE engineering without becoming an execution, authorization, workflow-runtime, sandbox, model-access, or deployment system.

## Ownership
FDSE Transformation owns:
- process semantics;
- process steps, actors, systems, dependencies, volumes, and exceptions;
- operational baseline definitions and observations;
- DELETE/CODE/AGENT/HUMAN classification semantics;
- target-state semantics;
- transformation intent and versioning;
- measurement contracts and comparisons;
- transformation outcomes;
- customer handoff semantics;
- replication/adaptation parameters.

FDSE Transformation does not own:
- identity or authentication;
- authorization or policy enforcement;
- approval authority;
- agent runtime execution;
- model access;
- tool/MCP capability authority;
- sandboxing;
- secrets;
- durable workflow orchestration;
- evidence storage authority;
- deployment infrastructure;
- customer-system execution authority.

Those remain with the existing FDSE/Agent Platform boundary and external infrastructure.

## Package boundary
The implementation SHALL live under:

    src/fdse/transformation/

Initial bounded modules:
- process.py — process topology and operational process semantics.
- baseline.py — baseline definitions and observations.
- classification.py — DELETE/CODE/AGENT/HUMAN decisions.
- transformation.py — transformation aggregate and target-state contract.
- measurement.py — metric definitions, measurement windows, observations, comparisons.
- outcome.py — measured transformation results and acceptance state.
- replication.py — adaptation and reuse parameters.
- handoff.py — ownership-transfer and operational handoff semantics.
- __init__.py — intentionally narrow public API.

No Transformation type SHALL be added to fdse.domain merely for convenience.

## Dependency direction
The dependency graph SHALL remain acyclic:

    fdse.contracts
         |
    fdse.evidence / integrity
         |
    fdse.transformation
         |
    existing FDSE engineering semantics
         |
    governed execution boundary
         |
    Agent Platform

Transformation may consume stable FDSE contracts such as tenant scope, evidence references, deterministic digest helpers, evaluation semantics, and engineering entities where required.
Transformation SHALL NOT import Agent Platform implementation details.
Transformation SHALL NOT depend on workflow-runtime, multi-agent-runtime, or ecosystem-runtime implementations for its core domain objects.

## Core lifecycle
    Process discovery
          |
          v
    Baseline
          |
          v
    DELETE/CODE/AGENT/HUMAN
          |
          v
    Target state
          |
          v
    Engineering requirements
          |
          v
    FDSE engineering
          |
          v
    Governed execution
          |
          v
    Evidence
          |
          v
    Measurement
          |
          v
    Outcome
          |
          v
    Handoff
          |
          v
    Replication/adaptation

The domain describes this lifecycle; it does not execute it.

## Scope invariant
Every persisted or externally exchangeable Transformation-domain object SHALL carry explicit scope sufficient to prevent accidental cross-customer or cross-revision association.
At minimum, the canonical transformation aggregate SHALL identify transformation_id, tenant_id, revision, and version.
Process, baseline, classification, measurement, outcome, and replication records SHALL either carry the same scope directly or be unambiguously owned by a scoped parent.
Cross-scope relationships SHALL fail closed.

## Versioning invariant
Domain version and source revision are distinct:
- version identifies the Transformation contract/object revision.
- revision identifies the customer/process source state used to construct or measure it.
A newer source revision MUST NOT silently mutate an existing Transformation object.

## Process contract
A Process represents the operational process being transformed, not an executable workflow.
It may contain process identity/version; purpose; actors; systems; ordered or graph-connected steps; dependencies; transaction volume/frequency; exception classes; process boundaries; and source/evidence references.
Process semantics SHALL NOT execute commands or acquire capabilities.

## Baseline contract
A Baseline represents a measured starting state.
Each material metric SHALL be represented with metric identifier, value, unit, measurement window, population/scope, collection method, source, evidence reference, and confidence/quality metadata where applicable.
Baseline values SHALL NOT be presented as measured facts without provenance.
Economic values SHALL remain explicit about currency, period, assumptions, and derivation.

## Classification contract
The canonical transformation action set is exactly:
- DELETE
- CODE
- AGENT
- HUMAN
A Classification SHALL identify process step, action, rationale, decision owner, constraints, expected effect, relevant risk/governance considerations, and supporting evidence.
The initial contract SHALL NOT introduce additional action categories.

## Target-state contract
A Target State describes the intended operational design after transformation.
It SHALL distinguish current-state references, desired process topology, intended classification, human responsibilities, system/agent responsibilities, integration requirements, governance requirements, and acceptance criteria.
A Target State is descriptive; it does not grant authority to implement itself.

## Measurement contract
Measurement is a first-class domain object.
It SHALL support metric definition, baseline value, target value, observation, measurement window, measurement method, comparison, result status, and evidence reference.
The contract SHALL support at least BASELINE, TARGET, POST_DEPLOYMENT, and FOLLOW_UP.
No universal ROI or improvement percentage SHALL be encoded as an assumed constant.

## Outcome contract
An Outcome represents observed transformation results.
It SHALL preserve transformation identity/version, measurement period, baseline references, target references, observed values, variance, acceptance state, supporting evidence, and limitations/qualification.
ROI MAY be derived from measured inputs but is not the fundamental outcome primitive.

## Replication contract
Replication represents reuse plus adaptation, not blind copying.
A Replication Profile SHALL distinguish reusable methodology/process-discovery/classification/governance/evaluation/KPI/measurement/runbook material; customer-specific process maps/integrations/data contracts/tool bindings/prompts/configuration/golden datasets/economics/training; and learned adaptation parameters/integration lessons/failure patterns/sector-specific patterns.
A Replication Profile SHALL NOT claim replication success merely because it exists.

## Handoff contract
A Handoff SHALL represent transfer to the customer operating environment and ownership model.
It SHALL support delivered artifacts, technical owner, operational owner, training, runbooks, escalation, rollback, acceptance, and ownership-transfer status.
Customer ownership is a contract requirement, not a marketing claim.

## Evidence linkage
Transformation records SHALL reference existing FDSE evidence semantics rather than inventing a second evidence store.
Transformation SHALL be able to link process -> baseline evidence -> classification evidence -> engineering evidence -> measurement evidence -> outcome evidence -> handoff evidence.
Evidence authority remains outside the Transformation package.

## Determinism and integrity
Transformation objects SHALL be immutable/frozen value contracts where practical, following current FDSE conventions.
Canonical serialization SHALL reuse fdse.evidence.canonical_json.
Digest generation SHALL reuse fdse.evidence.digest.
No Transformation module SHALL implement an incompatible canonicalization or hashing scheme.

## Security invariants
The package SHALL reject blank identifiers, reject NUL-containing strings, reject invalid scope relationships, reject invalid revisions, reject duplicate/conflicting identifiers, fail closed on incomplete required evidence, never treat customer process text/model output/tool output/external responses as authority, never contain credentials or secret material, and never grant execution capabilities.

## Public API policy
Only stable domain contracts SHALL be exported from fdse.transformation.
Internal validation helpers, parsing helpers, and implementation details SHALL remain private.
The top-level fdse.__init__ export surface SHALL only be expanded after the bounded package API is stable and covered by regression tests.

## Serialization policy
The first implementation SHALL use deterministic JSON-compatible primitive representations.
Serialization SHALL be deterministic, preserve explicit version, preserve scope, preserve identifiers, preserve enum values, preserve evidence references, avoid timestamps as implicit identity, and avoid lossy conversion.
No database, HTTP API, queue, or persistence engine is introduced by Phase 1.

## Test contract
Before the Transformation Domain is considered implemented, tests SHALL cover at minimum:
1. valid construction of every canonical object;
2. blank/NUL rejection;
3. scope mismatch rejection;
4. revision mismatch rejection;
5. identifier collision rejection;
6. deterministic serialization;
7. deterministic digest;
8. evidence-reference requirements;
9. baseline metric validity;
10. DELETE/CODE/AGENT/HUMAN exclusivity;
11. measurement baseline/target/post-deployment semantics;
12. outcome qualification;
13. replication separation of reusable/customer-specific/learned material;
14. handoff acceptance invariants;
15. public API import stability;
16. regression against all existing FDSE tests.

## Explicit non-goals
Phase 1 SHALL NOT implement database persistence, HTTP service, UI, workflow execution, agent execution, model routing, tool execution, policy enforcement, authorization, approvals, sandboxing, billing, CRM, portfolio command center, PE-specific orchestration, automatic ROI claims, or automatic cross-customer learning.

## Acceptance gate
Phase 1 is complete only when the package boundary is documented; the object model is implemented; public API is intentional and minimal; deterministic serialization/digests are tested; scope/evidence invariants are fail-closed; existing FDSE tests remain green; Transformation tests are green; no Agent Platform authority is duplicated; documentation and repository structure are reconciled; and forensic audit confirms the dependency boundary.

This contract does not certify production transformation capability, customer outcomes, or cross-company replication.