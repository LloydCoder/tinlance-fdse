# E3 — Assurance, Agentic Security & Supply-Chain Intelligence

E3 adds canonical semantics for assurance, agentic-security relationships, framework mappings, and software supply-chain lineage.

## Assurance

Requirement → Control → Test → Evidence → Result → Assurance

Framework definitions are data/configuration. The semantic layer does not hard-code OWASP ASVS, OWASP Agentic Applications, OWASP MCP, OWASP Agentic Skills, NIST SSDF, SLSA, or customer controls into business logic.

## Agentic security

FDSE models agents, capabilities, skills, tools, connectors, memory, context, delegation, messages, extensions, packages, artifacts, provenance, and trust relationships. It can express relationships such as privilege escalation, capability expansion, delegation abuse, context/memory poisoning, tool poisoning, malicious skills, MCP risks, credential exposure, supply-chain tampering, unexpected execution, and inter-agent trust.

These are semantics and verification requirements. Authentication, authorization, secret storage, runtime execution, tool authority, and enforcement remain external.

## Supply chain

Source → Revision → Dependency → Build → Artifact → Provenance → Attestation → Verification → Release

SLSA 1.2 describes provenance as verifiable information connecting artifacts to how and where they were produced, and its verification guidance emphasizes checking provenance against expected builder and build properties. E3 therefore treats provenance and verification as first-class semantic nodes while leaving signing, builders, registries, and deployment infrastructure external.

OWASP's 2026 Agentic Applications Top 10 provides a broader agentic-risk taxonomy. E3 maps such risks into configurable semantic relations rather than implementing a fixed scanner.

## Definition of done

- typed assurance chain exists;
- framework mappings are configuration-driven;
- agentic security assets and risk relationships are typed;
- supply-chain chain exists end to end;
- scope, collision, and self-reference invariants fail closed;
- deterministic graph digest is stable;
- public API, tests, README, roadmap, and changelog are reconciled.
