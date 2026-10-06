## Summary

Describe the change and why it is needed.

## Scope

- [ ] Bug fix
- [ ] Feature
- [ ] Documentation
- [ ] Tests
- [ ] Security hardening
- [ ] Refactor

## Validation

Commands/tests run:

~~~text
make check
~~~

Additional validation:

## Boundary and security review

- [ ] Tenant/repository/revision scope remains explicit.
- [ ] No untrusted content is treated as authority.
- [ ] No credentials or secrets were added.
- [ ] No generic agent authority, sandbox, authorization kernel, or model gateway was introduced.
- [ ] Security-sensitive behavior has regression coverage.

## Documentation

- [ ] Documentation updated where behavior or contracts changed.
- [ ] No production/GA claim is made without external evidence.

## Reviewer notes

Call out compatibility risks, migrations, or external integration evidence required.
