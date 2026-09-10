# Security Policy

Tinlance FDSE handles source code, credentials, logs, CI metadata and potentially sensitive customer engineering evidence. Security is therefore a product requirement, not an operational afterthought.

## Reporting

Do not disclose vulnerabilities, credentials, customer data or exploit details in public issues. Use the private security reporting mechanism configured for the repository/organization.

## Security invariants

- Customer repositories are untrusted inputs.
- Agent output is never authorization.
- FDSE cannot bypass Agent Platform policy or approval controls.
- Customer code must never execute directly on the application host.
- GitHub credentials must be scoped to the minimum repository and permission set required.
- Secrets must not be written to ordinary logs or evidence payloads.
- Tenant boundaries must be enforced server-side.
- High-impact actions require explicit human approval.
- Evidence must preserve provenance without exposing hidden model reasoning.

## Security baseline

FDSE security work is informed by OWASP ASVS, OWASP's Agentic Applications guidance, NIST AI-agent identity/authorization work, and supply-chain security practices. These references guide engineering; they do not constitute a certification claim.
