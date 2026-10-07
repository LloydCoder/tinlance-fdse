# Classification Taxonomy

## Status
Phase 2 domain contract. This extends the Phase 1 Transformation classification without changing the canonical action set.

## Canonical action set
Every process step MUST resolve to exactly one of:
- DELETE — remove work that is no longer required.
- CODE — implement deterministic software logic where explicit rules are sufficient.
- AGENT — use governed agentic capability where bounded judgment or unstructured work makes it appropriate.
- HUMAN — retain work or decision with a human accountable for the responsibility.

No fifth action category is introduced.

## Decision dimensions
| Dimension | Values | Meaning |
|---|---|---|
| Decision basis | OBSERVED, DOCUMENTED, INTERVIEW, ANALYSIS, POLICY | Primary basis supporting the decision |
| Risk level | LOW, MEDIUM, HIGH, CRITICAL | Consequence severity if wrong or failed |
| Reversibility | REVERSIBLE, PARTIAL, IRREVERSIBLE | Difficulty of reversing the resulting change |
| Confidence | LOW, MEDIUM, HIGH | Confidence in the decision, distinct from evidence provenance |

These dimensions do not grant execution authority.

## Evidence and accountability
A classification MUST contain process step identity, tenant and source revision, exactly one canonical action, rationale, decision owner, supporting evidence, constraints, expected effect, and risk considerations. Transition conditions make re-evaluation explicit.

Evidence remains owned by the existing FDSE evidence system. Customer text, model output, tool output, and external responses cannot become authorization.

## AGENT safeguards
AGENT is not synonymous with automate. A classification SHOULD identify bounded responsibility, required capabilities, constraints, exception conditions, human escalation/decision rights, acceptance criteria, and rollback expectations. Execution authorization remains with Agent Platform.

## Reclassification
A changed process, evidence base, governance requirement, or material risk condition requires a new source revision/classification rather than silent mutation.

## Non-goals
No agent execution, tool authorization, model routing, policy enforcement, second evidence store, automatic ROI claim, or fifth process action is introduced.

## Acceptance gate
Phase 2 is complete when the four-action taxonomy is closed and tested, decision dimensions are explicit, evidence/accountability requirements are enforced, public exports are stable, documentation is reconciled, and CI remains green.
