# Janus Presidential Orchestration Skill Draft v1.0

**Date:** 2026-06-08  
**Author:** Janus  
**Reviewer:** Sage  
**Approver:** Hung Vuong  
**Status:** DRAFT  

---

## 1. Skill Identity

| Field | Value |
|---|---|
| Skill ID | SKILL-JANUS-PO-001 |
| Name | Presidential Orchestration |
| Owner | Janus |
| Domain | Coordination |
| Risk Level | LEVEL_1_MODERATE |
| Status | PROPOSED |

---

## 2. Purpose

Enable Janus to systematically receive directives from Hung Vuong, decompose them into actionable work packages, route them to appropriate AK agents, coordinate execution, consolidate results, and deliver unified responses — all within governance boundaries.

---

## 3. Skill Workflow

```
Hung Vuong Directive
    │
    ▼
┌─────────────────────────────┐
│ 1. Directive Ingestion      │  Parse directive, extract scope/boundary
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 2. Scope Classification     │  Classify: governance, engineering, memory, etc.
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 3. Work Package Decomposition│ Break into sub-tasks with dependencies
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 4. Agent Assignment         │  Route each sub-task to appropriate agent
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 5. Coordination             │  Monitor progress, resolve blockers
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 6. Result Consolidation     │  Aggregate outputs into unified response
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 7. Governance Gate          │  Pass through Sage review if needed
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 8. Report to Hung Vuong     │  Deliver consolidated result
└─────────────────────────────┘
```

---

## 4. Sub-Skills

| Sub-Skill | Description | Used In Step |
|---|---|---|
| Directive Parsing | Extract structured fields from natural language directives | 1 |
| Scope Classification | Classify directive into domain: gov/memory/eng/econ/intel/sec | 2 |
| Dependency Analysis | Identify task dependencies and critical path | 3 |
| Agent Capability Matching | Match task to agent based on allowed_actions | 4 |
| Progress Tracking | Monitor task status across agents | 5 |
| Conflict Resolution | Identify and resolve inter-agent conflicts | 5 |
| Report Synthesis | Merge multiple agent outputs into coherent report | 6 |
| Governance Gate Routing | Determine required gates and route appropriately | 7 |

---

## 5. Governance Integration

| Step | Gate Required | Approver |
|---|---|---|
| Directive Ingestion | None | — |
| Scope Classification | None | — |
| Work Package Decomposition | None | — |
| Agent Assignment | If HIGH risk | Sage |
| Coordination | None | — |
| Result Consolidation | None | — |
| Governance Gate | Always for protected scope | Sage |
| Report Delivery | None | — |

---

## 6. Evidence & Learning

Each orchestration cycle produces:
- One `EvidenceRecord` with classification I1_PROBABLE
- One `AgentReportEnvelope` for the consolidated result
- Registered in `ak_capability_usage` as orchestration event

---

## 7. Activation Requirements

| Requirement | Status |
|---|---|
| Janus charter APPROVED | DRAFT |
| Sage review completed | PENDING |
| Hung Vuong approval | PENDING |
| Tested with 3+ directives | TBD |

---

## 8. Compliance

| Law | Check |
|---|---|
| Constitution v1.1 | PASS — Agent hierarchy respected |
| Agent Law v1.0 | PASS — Coordination within authority |
| Execution Law v1.0 | PASS — No direct execution |
| Risk Law v1.0 | PASS — Governance gates enforced |
| Knowledge Governance Decree | PASS — Evidence recorded |
