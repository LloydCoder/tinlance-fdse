# Security Policy

## Scope

FDSE is security-sensitive infrastructure. Security issues include trust-boundary violations, authorization bypass, secret exposure, unsafe execution, path traversal, tenant-isolation failures, dependency compromise, and CI/CD weaknesses.

## Reporting

Do not disclose suspected vulnerabilities publicly before coordinated remediation. Report privately through the repository's configured GitHub security reporting mechanism when enabled.

Do not include credentials, access tokens, customer source code, or other secrets in reports.

## Security invariants

1. FDSE never treats customer-controlled text as authority.
2. FDSE does not implement a second agent runtime or security kernel.
3. Consequential execution requires the Agent Platform governance path.
4. Production Agent Platform endpoints use HTTPS and never embed credentials.
5. Workspace paths must remain relative to the governed workspace and use POSIX separators.
6. Secrets are not accepted as FDSE domain configuration.
7. Tests cover security invariants and failure paths.
8. Current public-repository CI runs on GitHub-hosted runners and does not execute untrusted workloads on a persistent Tinlance self-hosted runner.

## CI/CD boundary

The current .github/workflows/ci.yml workflow uses GitHub-hosted runners. This is intentional for the public repository: a persistent self-hosted runner creates a durable trust boundary and can retain state between jobs.

Workflow controls include:

- explicit least-privilege permissions;
- immutable full-length commit-SHA action references;
- pull-request and merge-queue validation;
- dependency auditing;
- build validation;
- artifact provenance attestation for main-branch distributions.

GitHub recommends least-privilege workflow permissions and full-length SHA pinning for third-party actions. Artifact attestations establish signed provenance linking a build artifact to its workflow, repository, commit, and triggering event; consumers must still verify the attestation and evaluate the artifact itself.

## Historical self-hosted runner

A persistent self-hosted runner was previously used during early FDSE development. It is no longer part of the current CI execution path.

The historical runner details are retained in [docs/operations/SELF-HOSTED-RUNNER.md](docs/operations/SELF-HOSTED-RUNNER.md) solely for decommissioning and incident-response purposes.

If that historical runner still exists:

- remove it from the repository's available runners;
- stop and disable its service;
- revoke its registration/authentication material;
- remove cached workspaces and build credentials;
- confirm that no production credentials were stored on the host;
- rebuild/rotate the host if compromise is suspected.

Never place runner registration tokens or credentials in repository files or chat.

## M0 limitation

M0 defines the FDSE-side security boundary. It does not claim that the Agent Platform, GitHub infrastructure, runner infrastructure, or production deployment environment is itself implemented by this repository.
