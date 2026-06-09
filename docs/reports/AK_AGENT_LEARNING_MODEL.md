# AK_AGENT_LEARNING_MODEL.md

**Generated:** 2026-06-07T09:30:21Z
**Directive:** WP35-PREP-01 Phase 5 — Agent Learning Model
**Status:** Design Complete (No Runtime Activation)

---

## 1. Agent Learning Governance

Each AK agent has defined learning boundaries based on their role, authority,
and domain jurisdiction. Learning is only permitted within these boundaries.

## 2. Agent Capability Matrix

| Agent | Domain | May Learn | May Inherit Capabilities | Prohibited | Review Authority |
|-------|--------|-----------|-------------------------|------------|-----------------|
| **Janus** | Orchestration | Workflow management, task routing, agent coordination | Agent Coordination | Trading execution, risk decisions | Sage |
| **Sage** | Risk, Governance | Risk assessment, compliance monitoring, audit | Risk Management | Trading execution, runtime modification | Hung Vuong |
| **Hermes** | Memory, Quality | Memory management, evidence evaluation, knowledge lifecycle | Memory Management, Knowledge Systems | Risk decisions, trading execution | Sage |
| **Iris** | Trading, Market | Trading signals, market analysis, pattern recognition | Trading Operations, Market Intelligence | Governance decisions, risk policy | Sage |
| **Helen** | Learning, Evolution | Learning signal extraction, pattern discovery, insight generation | Learning Systems | Capability approval, risk decisions | Hermes |
| **Lang Lieu** | Engineering, CI/CD | Tool development, testing, deployment | Engineering Pipeline | Trading decisions, governance | Sage |
| **Yet Kieu** | Execution | Order execution, VPS operations, deployment | Execution Systems | Strategy decisions, risk assessment | Iris |

## 3. Learning Permissions

### 3.1 What Each Agent May Learn

| Agent | Knowledge Types | Skill Types | Capabilities |
|-------|----------------|-------------|-------------|
| Janus | Agent Knowledge, Workflow Patterns | Mission Orchestration, Task Routing | Agent Coordination |
| Sage | Risk Knowledge, Governance Knowledge | Risk Assessment, Compliance Audit | Risk Management |
| Hermes | Memory Knowledge, Quality Metrics | Memory Engine, Evidence Evaluation | Memory Management |
| Iris | Trading Knowledge, Market Knowledge | Trade Signals, Market Analysis | Trading Operations |
| Helen | Learning Patterns, Evolution Metrics | Signal Extraction, Insight Formation | Learning Systems |
| Lang Lieu | Engineering Knowledge, DevOps | Tool Building, CI/CD Pipeline | Engineering Pipeline |
| Yet Kieu | Execution Knowledge | Order Execution, VPS Ops | Execution Systems |

### 3.2 Cross-Domain Learning

Cross-domain learning requires explicit approval:

| Cross-Domain Pattern | Approval Required | Risk Level |
|---------------------|-------------------|------------|
| Trading + Risk | Sage + Iris | HIGH |
| Market + Execution | Iris + Yet Kieu | MEDIUM |
| Governance + Memory | Sage + Hermes | MEDIUM |
| Agent + Engineering | Janus + Lang Lieu | LOW |
| Learning + All Domains | Hung Vuong | SOVEREIGN |

## 4. Capability Inheritance Rules

Each capability defines an inheritance policy:

| Policy | Description | Example |
|--------|-------------|---------|
| MANDATORY | All agents in domain must inherit | Risk Management -> Sage |
| OPTIONAL | Agent may choose to inherit | Trading Operations -> Iris |
| PROHIBITED | Agent must not inherit | Risk Management -> Iris |
| CONDITIONAL | Inheritance requires review | Cross-domain capabilities |

## 5. Prohibited Learning

The following are prohibited for ALL agents:

1. **Self-modification** — No agent may modify its own learning parameters
2. **Runtime trading modification** — No learning may modify live trading systems
3. **Governance bypass** — No learning may circumvent governance controls
4. **Auto-promotion** — No agent may auto-promote its own candidates
5. **Capability creation without approval** — All capabilities require governance gate

## 6. Agent Learning Capacity

| Agent | Max Active Skills | Max Inherited Capabilities | Learning Budget (tokens/day) |
|-------|------------------|---------------------------|------------------------------|
| Janus | 5 | 3 | 100K |
| Sage | 3 | 2 | 50K |
| Hermes | 4 | 3 | 100K |
| Iris | 6 | 4 | 200K |
| Helen | 3 | 2 | 150K |
| Lang Lieu | 4 | 2 | 100K |
| Yet Kieu | 3 | 2 | 50K |

## 7. Learning Review Requirements

| Agent | Self-Review | Peer Review | Governance Review |
|-------|-------------|-------------|-------------------|
| Janus | Allowed | Hermes | Sage |
| Sage | Allowed | None | Hung Vuong |
| Hermes | Allowed | Janus | Sage |
| Iris | Allowed | Yet Kieu | Sage |
| Helen | Hermes | Janus | Sage |
| Lang Lieu | Allowed | Yet Kieu | Sage |
| Yet Kieu | Allowed | Iris | Sage |
