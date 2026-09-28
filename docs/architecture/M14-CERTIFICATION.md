# M14 — E2E Certification

M14 is the FDSE-side **verification contract** for end-to-end certification. It is deliberately not a self-certification mechanism.

## Certification requirements

A certification bundle is eligible for CERTIFIED only when the verifier confirms:

- the expected repository revision, when supplied;
- the expected commit SHA, when supplied;
- required external attestation metadata;
- unique phase names;
- complete M0–M14 phase coverage;
- CERTIFIED status for every required phase;
- a deterministic evidence digest matching the recomputed phase-result digest.

Required external attestation metadata includes an attestation identifier, issuer, workflow-run identifier, and attested commit.

## Authority boundary

The verifier validates evidence supplied by external execution/infrastructure. It does not create the external evidence, authorize production execution, or substitute for the Tinlance Agent Platform.

Therefore:

~~~text
FDSE CI green
    ≠
external Agent Platform healthy
    ≠
production healthy
    ≠
M14 certified
~~~

M14 certification becomes meaningful only when the external execution and attestation systems have actually produced the required evidence.
