# P12 — Reference AP/Invoice Transformation

## Status

P12 is a synthetic reference case, not a customer deployment or ROI claim.

## Canonical path

The fixture exercises:

**Process discovery → baseline → DELETE/CODE/AGENT/HUMAN classification → target state → engineering realization → Agent-System binding → governed execution receipt → baseline/target/post-deployment measurement → outcome → handoff.**

The reference uses deterministic fixture evidence and synthetic measurements so the contract graph can be tested without implying external customer evidence.

## Guardrails

- The fixture is explicitly marked synthetic.
- The outcome is INCONCLUSIVE.
- Limitations explicitly state that the measurements are not customer results.
- No pricing, ROI, production, or customer-success claim is derived from the fixture.
- The fixture must remain deterministic and tenant/revision scoped.
- Agent execution remains represented by authority-neutral references; Agent Platform remains the execution and authorization authority.

## Why AP/invoice

Accounts-payable invoice processing is a useful reference workflow because it contains structured intake, deterministic validation, classification/coding, exceptions, financial approval, system integration, measurable cycle time, and clear human decision rights. The reference case is a validation vehicle for the Transformation Domain, not a claim that every AP process has the same economics or architecture.

## Acceptance gate

P12 is complete when the fixture constructs and validates through the lifecycle contract, deterministic serialization/digest is stable, adversarial regression tests remain green, documentation is reconciled, and the full CI workflow is green on the PR head and merged main commit.
