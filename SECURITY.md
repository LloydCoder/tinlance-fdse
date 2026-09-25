# Security Policy

## Scope

FDSE is security-sensitive infrastructure. Security issues include trust-boundary violations, authorization bypass, secret exposure, unsafe execution, path traversal, tenant isolation failures, dependency compromise, and CI/CD weaknesses.

## Reporting

Do not disclose suspected vulnerabilities publicly before coordinated remediation. Report privately through the repository's configured GitHub security reporting mechanism when enabled.

Do not include credentials, access tokens, customer source code, or other secrets in reports.

## Security invariants

1. FDSE never treats customer-controlled text as authority.
2. FDSE does not implement a second agent runtime or security kernel.
3. Consequential execution requires explicit Agent Platform governance.
4. Production Agent Platform endpoints use HTTPS and never embed credentials.
5. Workspace paths must remain relative to the governed workspace and use POSIX separators.
6. Secrets are not accepted as FDSE domain configuration.
7. Tests cover security invariants and failure paths.
8. Self-hosted CI must be restricted to trusted private repositories and must not execute untrusted public/fork workloads.

## Self-hosted CI boundary

The shared `pcidss-hp` machine is intended to provide compute for trusted private Tinlance repositories. It must not execute public-repository or untrusted-fork workloads.

GitHub documents that repository-level runners are dedicated to one repository; a runner shared across multiple repositories requires organization-level runner scope. Persistent self-hosted runners can retain state between jobs and can be compromised by untrusted workflow code, so the host must be treated as a security boundary.

For this FDSE repository, the workflow is deliberately pinned to the `pcidss-hp` label. The runner service must remain online, run as a non-root account, stay patched, and avoid long-lived production credentials. Workspace and cache state should be isolated between repositories when the same physical host runs multiple trusted private-repository runner instances.

The operational recovery procedure is documented in [docs/operations/SELF-HOSTED-RUNNER.md](docs/operations/SELF-HOSTED-RUNNER.md).

## M0 limitation

M0 defines the FDSE-side boundary. It does not claim that the Agent Platform, runner host, or production deployment infrastructure is itself implemented by this repository.
