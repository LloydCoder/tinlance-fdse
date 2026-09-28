# FDSE Self-Hosted Runner Runbook

FDSE is intentionally public. The persistent repository-scoped runner pcidss-hp is therefore reserved for trusted pushes to main.

## Public PR safety

Pull-request workflows run on GitHub-hosted ubuntu-latest infrastructure. They must never execute on the persistent self-hosted runner.

Do not introduce pull_request_target workflows that check out or execute PR-controlled code.

The self-hosted runner is used only for trusted main-branch pushes and must remain non-root, patched, repository-scoped, and free of production credentials.

## Runner

- Host account: pcidss
- Runner directory: /home/pcidss/actions-runner-fdse
- systemd service: actions.runner.LloydCoder-tinlance-fdse.pcidss-hp.service
- Required labels: self-hosted, Linux, X64, pcidss-hp

## Python coverage

FDSE declares Python >=3.12. Public PR CI validates Python 3.12 on GitHub-hosted infrastructure. The HP runner currently validates trusted main pushes using native Python 3.14 because its CPU cannot execute the required prebuilt CPython 3.12 artifact.

This is an infrastructure limitation, not a reduction of FDSE's supported Python range. A compatible runner should add Python 3.13 and 3.14 matrix coverage before release compatibility claims are expanded.

## Host requirements

- non-root runner account;
- automatic Ubuntu security updates;
- patched runner application;
- no production credentials;
- no public/untrusted PR execution;
- separate workspaces and services for repository-scoped runners;
- rebuild/rotate the host if runner compromise is suspected.

## Health

    cd /home/pcidss/actions-runner-fdse
    sudo ./svc.sh status
    systemctl is-enabled actions.runner.LloydCoder-tinlance-fdse.pcidss-hp.service
    systemctl is-active actions.runner.LloydCoder-tinlance-fdse.pcidss-hp.service

Never place runner registration tokens or credentials in repository files or chat.
