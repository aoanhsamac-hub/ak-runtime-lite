# Knowledge Governance Workflow

**Directive:** WP-KP-01 Phase 7
**Date:** 2026-06-07
**Status:** FINAL

---

## 1. Purpose

Standardize governance responsibilities, approval authorities, and escalation paths across the National Knowledge Production System.

---

## 2. Agent Responsibilities

### Hermes (Memory Corpus Steward)

| Responsibility | Scope | Authority |
|---------------|-------|-----------|
| Pipeline operation | Decision trace, lesson, dataset, skill, capability | Operational |
| Evidence validation | Verify evidence completeness | Operational |
| Candidate creation | Create knowledge candidates from evidence | Operational |
| Metadata management | Ensure metadata standards compliance | Operational |
| Registry maintenance | Maintain registry integrity | Operational |

### Sage (Supreme Governance & Risk Court)

| Responsibility | Scope | Authority |
|---------------|-------|-----------|
| Quality review | Evaluate lesson/skill/capability quality | Review |
| Risk classification | Classify risk level of knowledge artifacts | Review |
| Governance gate | Block or allow promotion | Review |
| Constitutional audit | Verify constitutional compliance | Review |
| Escalation | Escalate to Janus for sovereign decisions | Review |

### Janus (Executive Orchestrator)

| Responsibility | Scope | Authority |
|---------------|-------|-----------|
| Approval | Approve knowledge artifacts LEVEL_3+ | Approval |
| Activation | Activate skills and capabilities | Approval |
| Sovereign decisions | Escalation from Sage | Approval |
| Strategic direction | National knowledge priorities | Approval |

### Lang Lieu (Engineering & Architecture)

| Responsibility | Scope | Authority |
|---------------|-------|-----------|
| Pipeline implementation | Code pipelines for knowledge production | Technical |
| Registry integration | Integrate pipelines with registries | Technical |
| Retrieval optimization | Maintain search performance | Technical |
| Runtime safety | Ensure pipelines do not modify runtime | Technical |

---

## 3. Approval Authority Matrix

| Artifact | Create | Review | Approve | Activate |
|----------|--------|--------|---------|----------|
| Decision Trace | Hermes (auto) | Sage | Sage + Janus | N/A |
| Lesson | Hermes (auto) | Sage | Sage + Janus | N/A |
| Dataset | Hermes | Sage | Sage | N/A |
| Skill | Hermes (auto) | Sage | Sage + Janus | Janus |
| Capability | Hermes (auto) | Sage + Janus | Janus | Hung Vuong |

---

## 4. Escalation Path

```
Level 1: Pipeline Decision (Hermes)
    ↓ issue detected
Level 2: Quality Review (Sage)
    ↓ cannot resolve
Level 3: Governance Escalation (Janus)
    ↓ constitutional matter
Level 4: Sovereign Decision (Hung Vuong)
```

### Escalation Triggers

| Trigger | From | To |
|---------|------|----|
| Quality below threshold | Hermes | Sage |
| Risk classification unclear | Hermes | Sage |
| Cross-agent conflict | Sage | Janus |
| Sovereign asset impact | Sage | Hung Vuong |
| Constitutional question | Janus | Hung Vuong |
| Pipeline technical failure | Hermes | Lang Lieu |

---

## 5. Governance Gates

### Gate 1: Evidence Gate (Hermes)

| Check | Pass Condition |
|-------|---------------|
| Evidence completeness | All required fields present |
| Source validity | Source is a real operational event |
| No artificial generation | Evidence originates from real activity |

### Gate 2: Quality Gate (Sage)

| Check | Pass Condition |
|-------|---------------|
| Lesson quality score | ≥ minimum threshold (per STD-01) |
| Risk classification | Appropriate for artifact type |
| Metadata compliance | All fields populated correctly |
| Constitutional alignment | No conflict with constitution |

### Gate 3: Approval Gate (Janus)

| Check | Pass Condition |
|-------|---------------|
| Governance compliance | All prior gates passed |
| Authority verification | Approver has required authority |
| Strategic alignment | Aligns with national priorities |

### Gate 4: Activation Gate (Hung Vuong for LEVEL_4)

| Check | Pass Condition |
|-------|---------------|
| Sovereign approval | Required for LEVEL_4_CONSTITUTIONAL |
| Capability readiness | Maturity level verified |

---

## 6. Audit Trail

Every governance action is recorded in `governance/audit/audit_log.jsonl`:

| Event | Fields |
|-------|--------|
| Candidate created | artifact_id, type, source, timestamp |
| Review submitted | artifact_id, reviewer, decision, timestamp |
| Approved | artifact_id, approver, level, timestamp |
| Rejected | artifact_id, reviewer, reason, timestamp |
| Activated | artifact_id, activator, timestamp |
| Deprecated | artifact_id, reviewer, reason, timestamp |
| Quarantined | artifact_id, reviewer, reason, timestamp |
| Escalated | artifact_id, from, to, reason, timestamp |

---

*End of Knowledge Governance Workflow.*
