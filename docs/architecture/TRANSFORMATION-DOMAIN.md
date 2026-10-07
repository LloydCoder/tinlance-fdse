# Transformation Domain Contract

## Phase 2 — Classification Taxonomy

Phase 2 closes the classification taxonomy around the existing `Classification` contract. The canonical action set remains exactly DELETE, CODE, AGENT, and HUMAN. Each classification records decision basis, risk level, reversibility, confidence, transition conditions, rationale, decision ownership, constraints, expected effect, risk considerations, and supporting evidence.

The taxonomy is descriptive and evidence-backed. It does not grant execution authority, approval authority, tool capability, model access, sandbox access, or policy authority.

### Canonical taxonomy

- **Action:** DELETE, CODE, AGENT, HUMAN only.
- **Decision basis:** OBSERVED, DOCUMENTED, INTERVIEW, ANALYSIS, POLICY.
- **Risk:** LOW, MEDIUM, HIGH, CRITICAL.
- **Reversibility:** REVERSIBLE, PARTIAL, IRREVERSIBLE.
- **Confidence:** LOW, MEDIUM, HIGH.
- **Transition conditions:** explicit conditions under which a classification should be reconsidered.
- **Evidence:** at least one supporting FDSE evidence reference.

### Phase 2 invariants

- No fifth action category may be introduced.
- A classification without supporting evidence is invalid.
- Non-canonical action values are rejected.
- Invalid decision-basis values are rejected.
- Taxonomy metadata cannot grant execution capability.
- Risk, reversibility, confidence, and transition conditions describe a decision; they do not authorize it.
- Agent Platform remains the authoritative authorization, approval, sandbox, secret, budget, tool, runtime, and audit boundary.

### Phase 2 acceptance gate

The taxonomy is complete when canonical action exclusivity, decision metadata, evidence requirements, fail-closed validation, deterministic serialization, public API stability, documentation, and all FDSE CI gates are green.

## Phase 3 — Process Discovery and Baseline

Phase 3 strengthens the evidence-backed starting state. Process dependencies are now fail-closed: internal dependencies MUST reference another process step, while external dependencies MUST use the explicit `external:` namespace. This prevents silently accepting malformed process graphs without turning the domain into a workflow runtime.

Baseline metric observations now require finite numeric values. Economic observations may explicitly carry currency, period, assumptions, and derivation; when currency is supplied, period and derivation are mandatory. This records an auditable economic basis without making automatic ROI claims.

### Phase 3 invariants

- Process topology cannot contain an unknown internal dependency.
- External dependencies are explicit and non-authoritative.
- Metric values must be finite.
- Economic interpretation requires explicit currency, period, assumptions where applicable, and derivation.
- Baseline evidence remains mandatory.
- Baseline objects remain descriptive and do not execute or authorize work.

### Phase 3 acceptance gate

Phase 3 is complete when process topology validation, baseline economic semantics, finite-value validation, deterministic serialization, regression coverage, documentation reconciliation, and all FDSE CI gates are green.

## Phase 4 — Target-State Design

Phase 4 makes the target operating model explicit. A target state now requires acceptance criteria and human decision rights, and may record exception handling, recovery requirements, and observability requirements. These fields describe the intended operating design; they do not execute it or grant authority.

The target state remains linked to the classified process revision. Every process step must still have exactly one canonical classification, and scope mismatches remain fail-closed.

### Phase 4 invariants

- A target state must contain explicit acceptance criteria.
- A target state must contain explicit human decision rights.
- Exception, recovery, and observability requirements are descriptive contracts.
- Target-state metadata cannot authorize tools, models, agents, systems, or customer-side changes.
- Agent Platform remains the sole generic authorization and consequential execution boundary.

### Phase 4 acceptance gate

Phase 4 is complete when target-state semantics are explicit, acceptance and human decision rights are mandatory, process/classification scope remains fail-closed, regression coverage is green, and documentation is reconciled.

## Phase 5 — Agent-System Binding

Phase 5 introduces an authority-neutral correlation contract between the FDSE operational Transformation Domain and the Tinlance Agent System's `transformation/v1` execution contract.

`AgentSystemBinding` carries references for the FDSE transformation/version, Agent-System transformation/version, tenant, agent identity/version, workspace/task, requested capability references, execution correlation, evidence, measurement, and outcome. It is deliberately a reference object rather than an execution object.

### Boundary invariant

The binding MUST NOT:
- authorize or approve execution;
- grant capabilities;
- select or route models;
- execute tools or agents;
- access secrets or sandbox resources;
- replace Agent OS lifecycle controls;
- replace Agent Platform identity, authorization, policy, budget, approval, sandbox, secret, tool, audit, or runtime authority.

The Agent Platform remains authoritative for consequential execution. The binding exists so a measured business transformation can be traced into and back out of governed Agent-System execution without duplicating authority.

### Phase 5 acceptance gate

Phase 5 is complete when a transformation can be deterministically correlated to the Agent-System transformation contract, agent/workspace/task references, execution/evidence/measurement/outcome references, invalid scope/version inputs fail closed, the public API is stable, and all CI gates are green.

## Phase 6 — Engineering Realization

Phase 6 introduces an authority-neutral engineering realization contract. It maps a target state to explicit engineering requirements, repositories, integrations, agent references, evaluation references, verification references, ownership, and acceptance criteria.

The realization object is not an execution plan in the runtime sense. It does not create workflows, invoke agents, authorize tools, select models, manage credentials, or perform deployments. It records the engineering work required to implement and verify the target state.

### Phase 6 invariants

- Engineering requirements must be explicit.
- Acceptance criteria must be explicit.
- Repository, integration, agent, evaluation, and verification references are identifiers, not authority grants.
- Engineering realization cannot bypass the Agent System governance path.
- Agent Platform remains authoritative for consequential execution and side effects.

### Phase 6 acceptance gate

Phase 6 is complete when target-state semantics can be mapped to explicit engineering requirements and verification references, the public contract is deterministic and fail-closed, documentation is reconciled, and all CI gates are green.

## Phase 7 — Governed Execution and Evidence Receipt

Phase 7 formalizes the FDSE-side receipt of governed Agent-System execution. `GovernedExecutionReceipt` records the transformation/binding/run correlation, policy references, optional approval references, evidence references, outputs, execution state, and limitations.

This is a receipt, not a second runtime. FDSE does not authorize execution, approve actions, issue credentials, select models, invoke tools, manage budgets, or store authoritative execution evidence. Those responsibilities remain with Agent Platform.

Terminal states (SUCCEEDED, FAILED, CANCELLED, PARTIAL) require evidence references so technical execution claims remain auditable. A technical execution result is still distinct from business outcome acceptance.

### Phase 7 acceptance gate

Phase 7 is complete when governed execution can be correlated to the transformation and binding, terminal execution states require evidence, authority remains entirely in Agent Platform, and all CI gates are green.

## Phase 8 — Measurement and Outcome Certification

Phase 8 makes business-result measurement more explicit. Measurements now distinguish directionality (lower-is-better, higher-is-better, target-band, equals, or unspecified), validate finite values, and require baseline/target/comparison/result status for post-deployment and follow-up observations.

Outcomes now use a canonical acceptance state and require the variance metric identifiers to match observed metric identifiers. All observed and variance values must be finite. Evidence remains mandatory. These contracts do not manufacture ROI or declare customer success automatically.

### Phase 8 invariants

- Technical execution success is distinct from business outcome acceptance.
- Post-deployment and follow-up measurements require explicit baseline and target values plus comparison/result semantics.
- Outcome observed metrics and variance metrics must correspond one-to-one.
- Outcome acceptance remains evidence-backed and qualified.
- No universal ROI or improvement percentage is assumed.

### Phase 8 acceptance gate

Phase 8 is complete when measurement semantics can distinguish baseline, target, deployment observation, and follow-up results; outcomes are internally consistent and evidence-backed; and all CI gates are green.

## Phase 9 — Handoff and Replication Qualification

Phase 9 turns handoff and replication into evidence-qualified lifecycle contracts. Replication now progresses through PLANNED, CONFIGURED, DEPLOYED, MEASURED, ACCEPTED, or FAILED. Measured/accepted/failed states require evidence, and a qualified accepted/measured replication must reference a target outcome.

Ownership transfer to TRANSFERRED now requires acceptance evidence. Handoff artifacts, training, runbooks, escalation, recovery, and acceptance remain descriptive operational contracts.

Replication success cannot be self-certified. The source outcome, target transformation, target outcome, and evidence must remain explicit so reuse can be distinguished from proven business replication.

### Phase 9 acceptance gate

Phase 9 is complete when ownership transfer and replication states are evidence-qualified, target outcomes are explicitly linked, self-certification is impossible, and all CI gates are green.

## Phase 10 — GA and Continuous Assurance

Phase 10 closes the repository-level Transformation capability with a cross-object lifecycle consistency contract. `TransformationLifecycle` verifies scope, identity, version, binding, execution receipt, measurement, outcome, handoff, and replication relationships without executing any operation.

`require_ga_contract()` requires the repository-level contract objects to exist and be internally consistent. It does not certify an external customer outcome, production deployment, successful replication, or ROI claim.

### Final forensic closure

The final audit checks:
- all Phase 1–10 contracts are present;
- public exports remain bounded;
- cross-object tenant/revision/version identities fail closed;
- process topology rejects unknown dependencies, cycles, and non-finite volume;
- classification remains exactly DELETE/CODE/AGENT/HUMAN and evidence-backed;
- target state has acceptance criteria and human decision rights;
- Agent-System binding remains authority-neutral;
- terminal execution receipts require evidence;
- measurements and outcomes are finite, internally consistent, and evidence-backed;
- ownership transfer and qualified replication require evidence;
- no second runtime, authorization, policy, sandbox, secret, or evidence authority has been introduced;
- CI, compatibility, packaging, documentation, and provenance gates are green.

### Final boundary

The Transformation Domain is a business/engineering semantic layer. Agent OS manages agent work; Platform SDK transports the contract; Agent Platform remains the authoritative trust and execution boundary.

## Status
Phase 10 repository-level GA contract. Phases 1–10 are implemented and tested in FDSE. This status certifies the repository/domain contract and cross-object consistency only; it does not claim external production capability, customer outcomes, or successful real-world replication.

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
- binding.py — authority-neutral FDSE-to-Agent-System correlation.
- execution.py — governed execution receipt references.
- realization.py — target-state engineering realization.
- lifecycle.py — end-to-end cross-object consistency and repository-level GA contract.
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

## Enterprise closure track P11–P15

The Transformation capability subsequently completed the enterprise closure sequence:

- **P11 — Enterprise Forensic Hardening:** runtime contract validation, referential/state/evidence/measurement integrity, tenant isolation, deterministic serialization, and adversarial regression controls.
- **P12 — Reference AP/Invoice Transformation:** deterministic synthetic end-to-end golden lifecycle.
- **P13 — Enterprise Replication Kit:** reusable methodology separated from target-specific adaptation and qualification evidence.
- **P14 — Agent Platform Integration Proof:** authority-neutral correlation across FDSE, Agent Developer, Agent OS, Platform SDK, and Agent Platform.
- **P15 — Final Transformation Domain Certification:** repository/domain forensic certification with explicit non-certifications for external production and customer outcomes.

The post-P15 independent forensic review identified and closed residual lifecycle runtime-type and transition-input gaps in PR #49. The remediation was re-gated through Python 3.12/3.13 compatibility, quality CI, and merged-main CI. These controls remain within the existing P15 boundary; no new phase or authority plane was introduced.

See TRANSFORMATION-ENTERPRISE-CLOSURE.md and TRANSFORMATION-FINAL-CERTIFICATION.md for the current certification record.
