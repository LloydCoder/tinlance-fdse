# E5 — Production Integration & System-of-Systems Validation

E5 defines the versioned FDSE-side contract for integrating the engineering semantics layer with FDE Mastery, the Tinlance Agent Platform, Tinlance customer surfaces, providers, CI/CD, artifact registries, provenance/attestation infrastructure, deployment systems, observability, and customer environments.

## Integration boundary

FDSE owns:

- integration contract identity and version;
- required capabilities and evidence requirements;
- authority-owner declaration;
- deterministic system-of-systems representation;
- verification evidence semantics.

FDSE does not own:

- provider credentials or authentication;
- authorization or approval authority;
- execution runtimes;
- durable workflow infrastructure;
- artifact registries;
- signing infrastructure;
- deployment control planes;
- observability backends;
- customer production environments.

## Canonical integration map

| System | FDSE contract role | External authority |
|---|---|---|
| FDE Mastery | Domain execution intent/results | FDE Mastery runtime |
| Agent Platform | Governed execution request/receipt | Agent Platform |
| Tinlance | Customer/commercial surface | Tinlance application |
| GitHub | Repository/revision/provider state | GitHub |
| CI/CD | Check/build/release evidence | CI/CD provider |
| Artifact registry | Artifact identity/location | Registry |
| Provenance | Attestation evidence | Provenance/signing system |
| Deployment | Release/deployment state | Deployment system |
| Observability | Operational evidence | Telemetry/monitoring system |
| Customer environment | E2E execution/evidence | Customer-controlled infrastructure |

## Verification

An integration claim is not treated as verified merely because a contract is declared. SystemOfSystemsGraph.require_verified() requires exactly one explicit VERIFIED evidence record for the requested contract.

This follows the SLSA distinction between provenance production and verification: provenance must be inspected against expected properties rather than treated as proof by existence alone.

## Definition of done

- versioned integration contracts exist;
- authority ownership is explicit;
- verification evidence is explicit and fail-closed;
- deterministic graph digests are stable across insertion order;
- public API and tests are reconciled;
- documentation identifies external production evidence as a separate gate;
- no external authority is duplicated inside FDSE.
