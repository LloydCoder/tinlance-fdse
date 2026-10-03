# E2 — Engineering Intelligence & Cross-System Semantics

E2 makes FDSE the canonical engineering meaning layer for risk, policy, change, and operational semantics. It does not duplicate FDE Mastery execution systems or the Agent Platform authority plane.

## Canonical semantic chains

Risk:

Asset → Threat → Scenario → Control → Evidence → Finding → Risk → Treatment → Residual Risk

Policy:

Policy → Requirement → Constraint → Guardrail → Approval Requirement → Exception

Change:

Change → Impact → Risk → Required Evidence → Required Evaluation → Approval Requirement → Verification → Release

Operational:

Engineering Objective → SLO → Customer-Impact Threshold → Recovery Objective → Assurance Requirement

All references are bound to tenant, repository, and immutable revision scope. A chain that crosses scope is rejected.

## Ownership boundary

FDSE owns:
- canonical names, relationships, scope, lifecycle-independent semantics, and deterministic graph serialization;
- requirements for evidence, evaluation, approval, verification, and assurance;
- adapters/contracts used by FDE Mastery and other systems to exchange meaning.

FDSE does not own:
- risk scoring algorithms or enterprise risk acceptance;
- policy enforcement or authorization;
- approval decisions;
- workflow scheduling or execution;
- model/tool authority;
- customer UI, billing, or deployment control.

NIST CSF 2.0 is outcome-oriented and non-prescriptive, which is compatible with FDSE defining canonical semantics without hard-coding one organization's implementation method. NIST's Risk Management Framework likewise separates activities such as categorization, control selection, assessment, authorization, and monitoring. These references inform the vocabulary; they do not make FDSE a NIST compliance engine.

## Determinism

EngineeringIntelligenceGraph.snapshot_digest() canonicalizes and sorts both references and relations, so the digest is independent of insertion order.

The graph is a semantic substrate, not an evidence store. Evidence payloads remain represented by the existing evidence/evidence-graph contracts.

## Cross-system contract

Systems may map native objects to SemanticRef and exchange the canonical relationship set without importing or duplicating FDSE runtime authority. Provider-specific identifiers remain opaque strings.

## E2 definition of done

- risk, policy, change, and operational chains exist as typed contracts;
- scope and self-reference invariants are fail-closed;
- semantic identifiers cannot be rebound to a different scoped reference;
- deterministic graph digests are stable across insertion order;
- package public API exposes E2 semantics;
- tests cover happy paths, scope escape, collisions, determinism, and required chain elements;
- documentation and roadmap/changelog are reconciled.
