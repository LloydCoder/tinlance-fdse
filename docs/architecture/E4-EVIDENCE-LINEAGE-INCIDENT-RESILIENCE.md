# E4 — Evidence Spine, Lineage, Incident & Resilience Intelligence

E4 makes causal and evidentiary lineage explicit across the engineering lifecycle.

## Evidence spine

Customer Request → Context → Plan → Risk → Policy → Agent/Workflow → Change → Execution → Observation → Evidence → Finding → Evaluation → Assurance → Certification → Release → Incident/Feedback → Context

Every required lineage record preserves tenant, repository, immutable revision, actor/agent, timestamp, payload digest, provenance reference, authority reference, and causal relationship.

## Incident semantics

Signal → Incident → Detection → Triage → Containment → Investigation → Remediation → Verification → Closure

FDSE defines the semantics. FDE Mastery or operational systems may execute incident workflows; FDSE does not become an incident-management runtime.

## Resilience semantics

Engineering Objective → Dependency → Failure Mode → Recovery Objective → Validation

Recovery targets and operational enforcement remain external. FDSE records the meaning and evidence relationships needed for assurance.

## Boundary and determinism

The E4 graph is not an evidence blob store and does not issue approvals or certifications. It provides canonical lineage relationships and deterministic serialization. Existing evidence and certification contracts remain authoritative for their respective domains.

## Definition of done

- evidence spine semantics exist end to end;
- lineage metadata is mandatory and scope-safe;
- causal, incident, and resilience semantics are typed;
- digests are deterministic;
- adversarial tests cover timestamp, digest, scope, exact relation coverage, duplicate metadata, and self-reference failures;
- public API, docs, roadmap, changelog, and repository structure are reconciled.
