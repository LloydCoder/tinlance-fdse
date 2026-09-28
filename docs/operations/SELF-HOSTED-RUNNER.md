# FDSE Self-Hosted Runner Runbook

## Current policy

The FDSE CI workflow **does not execute repository code on a persistent self-hosted runner**. Public pull requests, merge-queue validation, and main-branch validation run on GitHub-hosted infrastructure.

This is the supported CI path for this public repository.

## Historical decommissioning guidance

The details below are retained only as historical operational records and incident-response guidance. They must not be used to configure a new FDSE CI job.

If the historical runner still exists:

- remove it from the repository's available runners;
- stop and disable its service;
- revoke its registration/authentication material;
- remove cached workspaces and build credentials;
- confirm that no production credentials were stored on the host;
- rebuild/rotate the host if compromise is suspected.

Never place runner registration tokens or credentials in repository files or chat.

## Historical host record

The former repository-scoped runner was:

- Host account: pcidss
- Runner directory: /home/pcidss/actions-runner-fdse
- systemd service: actions.runner.LloydCoder-tinlance-fdse.pcidss-hp.service
- Required labels: self-hosted, Linux, X64, pcidss-hp

These values are historical only.
