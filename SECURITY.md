# Security Policy

Tinlance FDSE handles source code, credentials, logs, CI metadata and potentially sensitive engineering evidence. Security is a product requirement.

## M0 security invariants

- Customer-controlled and external content is untrusted data.
- Untrusted content cannot grant authorization, capabilities, approvals or policy exceptions.
- Missing authority, tenant identity or required approval fails closed.
- Tenant mismatch is rejected.
- Customer code is never executed directly on the FDSE application host.
- FDSE has no local fallback that bypasses Agent Platform authorization.
- Evidence hashing establishes integrity only; it does not establish authenticity or truth.
- A finding or model assertion is not a verification result.
- CI uses least-privilege workflow permissions.
- Secrets are not stored in source or emitted into logs.

## Reporting

Do not disclose vulnerabilities, credentials, customer data or exploit details in public issues. Use the repository's private security reporting mechanism.

## Scope note

M0 establishes security invariants and gates. Production sandboxing, authorization enforcement, durable tenancy, GitHub integration, and deployment hardening belong to later milestones and/or the Agent Platform.
