# Security Policy

## Scope

Tinlance FDSE is security-sensitive domain infrastructure. Report issues involving:

- trust-boundary violations or authority escalation;
- tenant, repository, or revision isolation failures;
- secret or credential exposure;
- unsafe execution or path handling;
- dependency or supply-chain compromise;
- CI/CD security weaknesses;
- certification or evidence-integrity bypasses.

## Private reporting

**Do not disclose suspected vulnerabilities in a public issue, discussion, pull request, or social post.**

Use GitHub's private vulnerability reporting/security-advisory mechanism when it is enabled for this repository. If private reporting is unavailable, contact **security@tinlance.com** and include only the minimum information required to reproduce and triage the issue.

Do not include live credentials, access tokens, customer source code, or other sensitive data in a report.

## Response targets

These are maintainer targets, not guarantees:

| Step | Target |
|---|---|
| Initial acknowledgement | Within 3 business days |
| Initial triage | Within 7 calendar days |
| Remediation plan | Within 14 calendar days for confirmed issues |
| Coordinated disclosure | Agreed with the reporter based on risk and remediation status |

Critical issues may be handled faster.

## What to include

- affected version or commit;
- affected component/file;
- concise reproduction steps;
- expected and observed behavior;
- security impact;
- relevant logs or traces with secrets removed;
- a suggested mitigation, if known.

## Security boundaries

FDSE treats customer repository content, source code, generated artifacts, dependency metadata, model output, tool output, external responses, and build/test output as untrusted.

FDSE does not own:

- authentication or authorization;
- human approval authority;
- generic agent execution;
- filesystem/process sandboxing;
- model credentials;
- generic tool authority;
- durable platform evidence/trajectory infrastructure;
- deployment infrastructure.

Consequential actions must cross the Tinlance Agent Platform governance boundary.

## CI/CD controls

The public CI workflow currently:

- runs on GitHub-hosted runners;
- declares least-privilege permissions;
- uses full-length commit-SHA action references;
- validates lint, formatting, typing, tests, dependency audit, build, and documentation links;
- validates Python 3.12/3.13 compatibility on pull requests and merge queues;
- produces build provenance attestations on main-branch distributions.

## Historical runner

A persistent self-hosted runner was used during early development and is not part of the current public CI path. Historical decommissioning guidance is retained in [docs/operations/SELF-HOSTED-RUNNER.md](docs/operations/SELF-HOSTED-RUNNER.md).

If a historical runner still exists, remove it, revoke registration credentials, clear cached workspaces/credentials, and investigate for compromise before reuse.

## Disclosure

After remediation, the maintainer may coordinate public disclosure through GitHub Security Advisories or another appropriate channel. Do not publish exploit details before coordinated remediation.
