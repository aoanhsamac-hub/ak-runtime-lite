# AK_LEARNING_GOVERNANCE_MODEL.md

**Generated:** 2026-06-07T09:30:21Z
**Directive:** WP35-PREP-01 Phase 6 — Governance & Risk Model
**Status:** Design Complete (No Runtime Activation)

---

## 1. Learning Approval Process

```
Step 1: Learning Signal Detected
    |-- Automated, no approval needed
    v
Step 2: Candidate Insight Formed
    |-- Automated, no approval needed
    v
Step 3: Skill Candidate Created (DRAFT)
    |-- Automated discovery
    v
Step 4: Skill Review
    |-- Agent submits for review
    |-- Risk classification determines reviewer
    v
Step 5: Skill Approval/Rejection
    |-- Reviewer decision
    |-- If approved: status -> APPROVED
    |-- If rejected: status -> QUARANTINE with reason
    v
Step 6: Capability Discovery (from active skills)
    |-- Automated, requires min 2 active skills
    v
Step 7: Capability Review
    |-- Sage + Hermes review
    v
Step 8: Capability Approval
    |-- Hung Vuong final approval
    v
Step 9: Agent Inheritance
    |-- Role boundary enforcement
    |-- Agent acceptance
```

## 2. Risk Classification

### 2.1 Classification Matrix

| Factor | LOW (1) | MEDIUM (2) | HIGH (3) | SOVEREIGN (4) |
|--------|---------|------------|----------|---------------|
| Domain | Engineering, Memory | Execution, Agent | Trading, Market | Governance, Risk |
| Confidence | >= 80 | 70-79 | 60-69 | < 60 |
| Evidence | >= 4/5 | 3/5 | 2/5 | <= 1/5 |
| Cross-domain | 1 domain | 2 domains | 3 domains | 4+ domains |
| Agent impact | 1 agent | 2-3 agents | 4-5 agents | 6-7 agents |
| Economic impact | Low | Medium | High | Critical |

### 2.2 Overall Risk Calculation

```
risk_score = max(domain_risk, confidence_risk, evidence_risk,
                 cross_domain_risk, agent_impact_risk, economic_risk)

if risk_score <= 1: LOW
if risk_score <= 2: MEDIUM
if risk_score <= 3: HIGH
if risk_score == 4: SOVEREIGN
```

## 3. Approval Authority by Risk

| Risk Level | Skill Approval | Capability Approval | Emergency Stop |
|------------|---------------|--------------------|----------------|
| LOW | Hermes | Hermes + Sage | Sage |
| MEDIUM | Sage | Sage + Hermes | Sage |
| HIGH | Hung Vuong | Hung Vuong | Hung Vuong |
| SOVEREIGN | Hung Vuong + Council | Hung Vuong + Council | Hung Vuong |

## 4. Audit Process

### 4.1 What Is Audited

- Every status transition (DRAFT -> REVIEWED -> APPROVED -> ACTIVE)
- Every review decision (approve, reject, request evidence)
- Every risk classification
- Every governance gate pass/fail
- Every agent inheritance event
- Every emergency stop trigger

### 4.2 Audit Record Schema

| Field | Description |
|-------|-------------|
| event_id | Unique audit event ID |
| timestamp | When the event occurred |
| event_type | Type of learning event |
| actor | Agent or system that performed the action |
| target_id | The candidate/record affected |
| previous_status | Status before the action |
| new_status | Status after the action |
| reason | Human-readable reason |
| risk_level | Risk classification at time of action |
| authority | Approval authority used |
| evidence_hash | Hash of evidence at time of decision |

### 4.3 Audit Retention

| Audit Type | Retention Period | Archive After |
|------------|-----------------|---------------|
| Status transitions | Permanent | Never |
| Review decisions | Permanent | Never |
| Risk classifications | 5 years | 5 years |
| Agent inheritance | 3 years | 3 years |
| Emergency stops | Permanent | Never |

## 5. Rollback Process

### 5.1 When Rollback Is Authorized

1. Approved skill is found to have incorrect or insufficient evidence
2. Capability causes unexpected negative agent behavior
3. Governance violation is discovered post-approval
4. Security or risk violation detected
5. Hung Vuong orders rollback

### 5.2 Rollback Procedure

1. Identify the record to rollback
2. Determine rollback target status (DRAFT, REVIEWED, etc.)
3. Record rollback reason and authority in audit
4. Execute rollback via status transition
5. Notify affected agents and reviewers
6. Update all dependent records (capabilities using the skill, etc.)

### 5.3 Rollback Authority

| Rollback Type | Authority | Notice Required |
|--------------|-----------|-----------------|
| Skill DRAFT -> REMOVED | Hermes | None |
| Skill REVIEWED -> DRAFT | Sage | 24h |
| Skill APPROVED -> REVIEWED | Sage | 48h |
| Skill ACTIVE -> APPROVED | Hung Vuong | 72h |
| Capability any -> DRAFT | Hung Vuong | 7 days |

## 6. Capability Revocation

### 6.1 Revocation Triggers

- Capability causes sustained negative outcomes
- Constituent skills are revoked or deprecated
- Governance violation in capability operation
- Strategic realignment renders capability obsolete
- Emergency stop activated

### 6.2 Revocation Process

1. Revocation order issued by authorized agent
2. Notify all agents currently using the capability
3. Disable capability for new agent inheritance
4. Allow in-flight operations to complete
5. Mark capability as DEPRECATED
6. Archive after retention period

## 7. Emergency Stop Process

### 7.1 Emergency Stop Triggers

- Active security breach detected
- Learning system attempting governance bypass
- Unauthorized autonomous learning loop detected
- SOVEREIGN-level risk without approval
- Hung Vuong direct order

### 7.2 Emergency Stop Procedure

1. **Immediate halt** — All learning pipeline processing stops
2. **Status freeze** — No transitions permitted
3. **Alert** — All agents notified
4. **Investigation** — Root cause analysis begins
5. **Resolution** — Either resume or permanent halt
6. **Report** — Full incident report generated

### 7.3 Emergency Stop Authority

| Authority | Scope | Duration |
|-----------|-------|----------|
| Sage | Single domain pause | 24 hours |
| Hung Vuong | Global pause | Indefinite |
| Hermes | Single skill/capability | 48 hours |
