# FDSE Self-Hosted Runner Runbook

## Runner

FDSE CI uses the repository-scoped self-hosted runner named pcidss-hp.

- Host account: pcidss
- Runner directory: /home/pcidss/actions-runner-fdse
- systemd service: actions.runner.LloydCoder-tinlance-fdse.pcidss-hp.service
- Required labels: self-hosted, Linux, X64, pcidss-hp
- Runner application: v2.337.0 or newer

The runner is for this private FDSE repository. A physical host may run additional repository-scoped runner instances for other trusted private repositories, but each instance must have its own runner directory and service.

## Python CI coverage

FDSE declares Python >=3.12. The current HP runner validates the CI workflow with the host's native Python 3.14 because the older HP CPU cannot execute the prebuilt CPython 3.12 artifact supplied by actions/setup-python.

This is an infrastructure limitation, not a change to FDSE's supported Python range. Until a compatible runner is available, CI on pcidss-hp proves the workflow on Python 3.14 only. Python 3.12 and 3.13 should be covered on a compatible runner before making compatibility claims specific to those interpreter versions.

## Health check

From the Ubuntu host:

    cd /home/pcidss/actions-runner-fdse
    sudo ./svc.sh status
    systemctl is-enabled actions.runner.LloydCoder-tinlance-fdse.pcidss-hp.service
    systemctl is-active actions.runner.LloydCoder-tinlance-fdse.pcidss-hp.service

The service must be active and the runner must show as online in the repository's GitHub Actions runner settings.

## Recovery

If the service is inactive:

    cd /home/pcidss/actions-runner-fdse
    sudo ./svc.sh start
    sudo ./svc.sh status

If the service fails to start:

    sudo systemctl status actions.runner.LloydCoder-tinlance-fdse.pcidss-hp.service --no-pager
    sudo journalctl -u actions.runner.LloydCoder-tinlance-fdse.pcidss-hp.service -n 100 --no-pager

Do not paste registration tokens, GitHub tokens, or other secrets into tickets, chat, or repository files.

## Host security requirements

- Run the runner as the non-root pcidss account.
- Keep Ubuntu and the runner application patched.
- Do not store production credentials on the runner host.
- Do not route public-repository or untrusted fork workflows to this runner.
- Do not reuse a runner work directory between repository-scoped runner instances.
- Keep repository-specific caches and temporary workspaces isolated where practical.
- Treat any code executed by a trusted private repository as capable of modifying the runner account's accessible files.
- For multiple private repositories on the same physical host, use separate runner directories and systemd services; do not register one repository-scoped runner instance to multiple repositories.

## FDSE CI contract

The workflow deliberately targets:

    runs-on: [self-hosted, Linux, X64, pcidss-hp]

This prevents an unrelated self-hosted runner from silently receiving FDSE jobs. CI is not considered verified until the job is actually executed by a runner matching these labels and the complete workflow finishes successfully.
