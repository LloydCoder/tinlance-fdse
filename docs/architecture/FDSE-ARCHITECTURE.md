# FDSE Architecture

## Purpose

This document defines the canonical high-level architecture of Tinlance FDSE.

FDSE has **two first-class domain routes**:

1. **Engineering**
2. **Transformation**

They share an FDSE governance and evidence plane. Consequential execution may cross into the Tinlance Agent System, where the Agent Platform remains the authority for generic agent execution and security primitives.

This architecture deliberately does **not** introduce a fifth Agent System repository, does **not** extend the core roadmap to M19, and does **not** move platform authority into FDSE.

## Canonical architecture

~~~mermaid
flowchart TB
    C[Customer / Organization] --> F[Tinlance FDSE]
    F --> I[Intake<br/>Scope • Context • Constraints]
    I --> R{Select FDSE Domain Route}

    R --> E1
    subgraph ENG["ENGINEERING ROUTE"]
        direction TB
        E1[Discovery<br/>System • Risk • Requirements]
        E2[Engineering Design<br/>Architecture • Plan • Controls]
        E3[Implementation / Remediation<br/>Build • Change • Harden]
        E4[Evidence Collection<br/>Artifacts • Telemetry • Provenance]
        E5[Evaluation<br/>Tests • Validation • Findings]
        E6[Workflow / Certification<br/>Decision • Acceptance • Closure]
        E1 --> E2 --> E3 --> E4 --> E5 --> E6
    end

    R --> T1
    subgraph TRANS["TRANSFORMATION ROUTE"]
        direction TB
        T1[Process Discovery<br/>Current State]
        T2[Baseline<br/>Metrics • Evidence • Constraints]
        T3[Classification<br/>Process • Risk • Operating Model]
        T4[Target-State Design<br/>Future State • Controls • KPIs]
        T5[Transformation Realization<br/>Change • Configure • Implement]
        T6[Governed Execution<br/>Controlled Change + Evidence]
        T7[Measurement<br/>Baseline vs Target]
        T8[Outcome<br/>Variance • Effectiveness • Acceptance]
        T9[Handoff<br/>Ownership • Training • Acceptance]
        T10[Replication<br/>Method • Kit • Adaptation]
        T1 --> T2 --> T3 --> T4 --> T5 --> T6 --> T7 --> T8 --> T9 --> T10
    end

    E6 --> G1
    T10 --> G1
    subgraph GOV["FDSE SHARED GOVERNANCE + EVIDENCE PLANE"]
        direction LR
        G1[Versioned Contracts]
        G2[Evidence + Provenance]
        G3[Validation + Evaluation]
        G4[Outcome / Decision Records]
        G5[Handoff + Certification]
        G1 --> G2 --> G3 --> G4 --> G5
    end

    G5 --> O[Governed Intent / Execution Request]

    O -. governed execution .-> A
    subgraph AGENT["TINLANCE AGENT SYSTEM"]
        direction TB
        AD[Agent Developer<br/>Agent construction • development • composition]
        OS[Agent OS<br/>Workspace • Lifecycle • Fleet]
        SDK[Agent Platform SDK<br/>Developer Interface]
        A[Agent Platform<br/>Execution Authority]
        AD --> OS --> SDK --> A

        subgraph AUTH["PLATFORM AUTHORITY"]
            direction LR
            A1[Identity + Authorization]
            A2[Policy + Approvals]
            A3[Runtime + Sandbox]
            A4[Tools + MCP]
            A5[Secrets + Budgets]
            A6[Evidence + Audit]
            A7[Observability]
            A --> A1
            A --> A2
            A --> A3
            A --> A4
            A --> A5
            A --> A6
            A --> A7
        end
    end

    A -. execution receipts / evidence .-> E4
    A -. execution receipts / evidence .-> T6
    A -. measurements / outcomes .-> T7
    T10 -. reusable transformation methodology .-> T4
~~~

GitHub renders Mermaid diagrams directly in Markdown. The diagram uses explicit node IDs for cross-boundary links rather than relying on ambiguous visual inference from group labels. citeturn0search5turn0search0

## Domain routes

### Engineering route

The Engineering route covers forward-deployed engineering work:

```text
Discovery
  ↓
Engineering Design
  ↓
Implementation / Remediation
  ↓
Evidence Collection
  ↓
Evaluation
  ↓
Workflow / Certification
```

FDSE owns the engineering-domain semantics, revision/tenant scoping, evidence and evaluation contracts, workflow semantics, and certification semantics.

### Transformation route

The Transformation route is a first-class FDSE capability:

```text
Process Discovery
  ↓
Baseline
  ↓
Classification
  ↓
Target-State Design
  ↓
Transformation Realization
  ↓
Governed Execution
  ↓
Measurement
  ↓
Outcome
  ↓
Handoff
  ↓
Replication
```

The Transformation route corresponds to the P1–P15 capability track described in the canonical roadmap. It is bounded inside FDSE and does not become a new core M-phase or Agent System repository.

P12's AP/invoice lifecycle is a deterministic synthetic reference workflow. P13's replication kit is a reusable contract. P14 is an authority-neutral integration proof. P15 is a repository/domain certification gate. None of these artifacts, by themselves, certify external production, customer outcomes, regulatory compliance, or successful real-world replication.

## Shared FDSE governance and evidence plane

The two routes converge on a common FDSE governance/evidence boundary.

FDSE's shared responsibilities include:

- versioned domain contracts;
- tenant and revision integrity;
- evidence and provenance;
- deterministic validation and evaluation;
- outcome and decision records;
- handoff and certification semantics;
- fail-closed domain invariants.

This convergence does **not** mean that Engineering and Transformation become one lifecycle. Their domain states, objects, measurements, and qualification rules remain distinct.

## Agent System boundary

The Tinlance Agent System is external to the FDSE domain layer.

The authority/integration chain is:

```text
Agent Developer
    ↓
Agent OS
    ↓
Agent Platform SDK
    ↓
Agent Platform
```

Agent Developer is the developer-facing construction and composition layer in the Tinlance Agent System. It does not replace or absorb Agent OS lifecycle/workspace authority, the SDK developer interface, or Agent Platform execution/policy authority.

The Agent Platform owns generic authority and execution primitives, including:

- identity and authorization;
- policy enforcement;
- approval workflows;
- agent/runtime execution;
- sandboxing and isolation;
- tools and MCP capability control;
- secrets and budgets;
- evidence and audit;
- observability.

FDSE must consume those capabilities through explicit, versioned interfaces. It must not create a competing runtime, policy engine, sandbox, identity/authorization kernel, or audit kernel.

## Governed execution semantics

A consequential action follows this architectural pattern:

```text
FDSE domain semantics
        ↓
FDSE governance + evidence
        ↓
Governed intent / execution request
        ↓
Agent Platform policy + approval boundary
        ↓
Agent Platform runtime / sandbox / tools
        ↓
Execution receipt + evidence + telemetry
        ↓
FDSE evidence / evaluation / measurement
```

The dotted arrows in the canonical diagram represent this boundary crossing and feedback relationship.

They do not mean that FDSE becomes the runtime authority.

## Transformation feedback and replication

Transformation is intentionally closed-loop:

```text
Transformation realization
        ↓
Governed execution
        ↓
Measurement
        ↓
Outcome
        ↓
Handoff
        ↓
Replication
        └──────────────→ target-state design / future adaptation
```

Replication is therefore not represented as a generic deployment step. It is a qualified transformation capability that carries reusable methodology, source/target lineage, customer-specific adaptation, measurement, deployment/rollback, handoff/training, and supporting evidence.

## Architectural invariants

The following invariants must remain true:

1. Engineering and Transformation remain distinct first-class FDSE domain routes.
2. Transformation remains a bounded capability track inside FDSE.
3. The core FDSE roadmap ends at M18; there is intentionally no M19.
4. FDSE does not own generic agent authority.
5. Consequential execution crosses the Agent Platform governance boundary.
6. Untrusted customer or external content cannot grant authority.
7. Evidence, findings, evaluation, certification, and outcomes remain semantically distinct.
8. Agent Platform receipts/evidence can feed FDSE domain evidence but do not transfer execution authority to FDSE.
9. Transformation replication does not self-certify real-world success.
10. Repository-level implementation is not equivalent to external production certification.

## Canonical references

- [FDSE M0–M18 Roadmap](ROADMAP.md)
- [FDSE / Agent Platform Boundary](BOUNDARY.md)
- [Transformation Domain](TRANSFORMATION-DOMAIN.md)
- [Enterprise Validation and Certification](E6-VALIDATION-CERTIFICATION-GA.md)

The README diagram and this document must remain semantically aligned. If either changes, update both in the same documentation change whenever the architectural contract changes.
