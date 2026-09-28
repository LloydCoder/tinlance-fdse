# FDSE Self-Hosted Runner Runbook

## Current policy

The FDSE CI workflow no longer executes repository code on the persistent self-hosted runner. Public pull requests, merge-queue validation, and main-branch validation run on GitHub-hosted infrastructure.

This is the safer default for a public repository: GitHub's secure-use guidance recommends least-privilege workflow permissions and immutable Action references, and a persistent runner should not be exposed to untrusted repository-controlled execution.

The historical host details below are retained only as decommissioning/incident-response information. They are **not** a supported CI execution path.

## Decommissioning requirements

If the historical runner still exists:

- remove it from the repository's available runners;
- stop and disable its service;
- revoke its registration/authentication material;
- remove cached workspaces and build credentials;
- confirm that no production credentials were ever stored on the host;
- rebuild/rotate the host if compromise is suspected.

Never place runner registration tokens or credentials in repository files or chat.

## Historical host record

The former repository-scoped runner was:

- Host account: pcidss
- Runner directory: /home/pcidss/actions-runner-fdse
- systemd service: actions.runner.LloydCoder-tinlance-fdse.pcidss-hp.service
- Required labels: self-hosted, Linux, X64, pcidss-hp

These values are historical operational records only and must not be used to configure new CI jobs.
