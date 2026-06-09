# NCP-R Wave 1 — Agent Activation Review Report

**Date:** 2026-06-08
**Authority:** Janus Directive — NCP-R | Agent Law
**Status:** COMPLETE
**Reviewer:** Janus

---

## Activation Matrix

| Capability Ready | Governance Ready | Result |
|---|---|---|
| YES | YES | PILOT_ACTIVE |
| YES | NO | CONDITIONAL_ACTIVE |
| NO | YES | CONDITIONAL_ACTIVE |
| NO | NO | BLOCKED |

---

## Agent Summary

| Agent | Capability Ready | Governance Ready | Activation Decision | Current State |
|-------|-----------------|------------------|-------------------|--------------|
| Janus | YES | YES | **PILOT_ACTIVE** | SANDBOX_ACTIVE |
| Sage | YES | YES | **PILOT_ACTIVE** | SANDBOX_ACTIVE |
| Hermes | YES | YES | **PILOT_ACTIVE** | SANDBOX_ACTIVE |
| Iris | YES | YES | **PILOT_ACTIVE** | SANDBOX_ACTIVE |
| Lang Lieu | YES | YES | **PILOT_ACTIVE** | SANDBOX_ACTIVE |
| Yet Kieu | YES | YES | **PILOT_ACTIVE** | SANDBOX_ACTIVE |
| Helen | YES | NO | **CONDITIONAL_ACTIVE** | SANDBOX_ACTIVE |

---

## Detailed Agent Reviews

### 1. Janus — PILOT_ACTIVE

| Criteria | Assessment |
|----------|-----------|
| Capability Readiness | PASS — Full agent implementation, orchestration skills, role boundary, memory policy, workflows, tools, prompts |
| Governance Readiness | PASS — Charter DRAFT exists, agent.yaml operational, authority: custodian |
| Operational Readiness | PASS — SANDBOX_ACTIVE, mission planning, routing, council consolidation implemented |
| Security Compliance | PASS — No credential access, propose_only mode, audit hooks |
| Dependency Status | PASS — No external dependencies blocking activation |
| **Activation Recommendation** | **PILOT_ACTIVE** — Upgrade from SANDBOX_ACTIVE. Remove propose_only constraint for orchestration tasks. |

**Risks:** Low. Janus is coordination-only, no execution authority.

**Required Remediation:** None for activation. Charter upgrade DRAFT → FINAL required separately.

---

### 2. Sage — PILOT_ACTIVE

| Criteria | Assessment |
|----------|-----------|
| Capability Readiness | PASS — Governance gate, approval engine, policy engine, audit engine, issue registry all exist |
| Governance Readiness | PASS — agent.yaml operational, authority: custodian |
| Operational Readiness | PASS — SANDBOX_ACTIVE, risk review authority per Risk Law |
| Security Compliance | PASS — LEVEL_2_HIGH+ review authority, propose_only mode |
| Dependency Status | PASS — Depends on governance/ modules, all exist |
| **Activation Recommendation** | **PILOT_ACTIVE** — Sage is the risk review authority. Removing propose_only enables real-time governance. |

**Risks:** Low. Sage only reviews/approves, does not execute.

**Required Remediation:** None.

---

### 3. Hermes — PILOT_ACTIVE

| Criteria | Assessment |
|----------|-----------|
| Capability Readiness | PASS — Memory management, evidence evaluation, lesson distillation, dataset readiness implemented |
| Governance Readiness | PASS — Charter DRAFT exists, agent.yaml operational |
| Operational Readiness | PASS — SANDBOX_ACTIVE, manages 14 NMP tables |
| Security Compliance | PASS — propose_only mode, no credential access |
| Dependency Status | PASS — Depends on memory/, lancedb_adapter/, all exist |
| **Activation Recommendation** | **PILOT_ACTIVE** — Hermes manages the knowledge lifecycle. Removing propose_only enables operational memory management. |

**Risks:** Low. Memory operations are governed by Memory Law + Retention Decree.

**Required Remediation:** None for activation. Charter upgrade DRAFT → FINAL required separately.

---

### 4. Iris — PILOT_ACTIVE

| Criteria | Assessment |
|----------|-----------|
| Capability Readiness | PASS — Market analysis, treasury proposal, economic assessment defined |
| Governance Readiness | PASS — agent.yaml operational, role.md defined |
| Operational Readiness | PASS — SANDBOX_ACTIVE, MT5 observer connected, OHLCV data flowing |
| Security Compliance | PASS — propose_only mode, market observation only |
| Dependency Status | PASS — Depends on services/iris/, MT5 connector (mock/real) |
| **Activation Recommendation** | **PILOT_ACTIVE** — Iris provides economic intelligence. No execution authority. |

**Risks:** Low. Market observation only, no order placement.

**Required Remediation:** None.

---

### 5. Lang Lieu — PILOT_ACTIVE

| Criteria | Assessment |
|----------|-----------|
| Capability Readiness | PASS — Full engineering agent, code review, architecture, build system |
| Governance Readiness | PASS — agent.yaml operational, role.md defined |
| Operational Readiness | PASS — SANDBOX_ACTIVE, implements all WP work packages |
| Security Compliance | PASS — propose_only mode, no deployment authority |
| Dependency Status | PASS — Depends on standard Python toolchain |
| **Activation Recommendation** | **PILOT_ACTIVE** — Lang Lieu is the engineering backbone. |

**Risks:** Low. Propose_only prevents unauthorized deployment.

**Required Remediation:** None.

---

### 6. Yet Kieu — PILOT_ACTIVE

| Criteria | Assessment |
|----------|-----------|
| Capability Readiness | PASS — Security monitoring, incident response, VPS management, runtime observability |
| Governance Readiness | PASS — agent.yaml operational, sole security authority per Security Law |
| Operational Readiness | PASS — SANDBOX_ACTIVE, runtime monitoring |
| Security Compliance | PASS — propose_only mode, CONFIDENTIAL data handler |
| Dependency Status | PASS — Depends on infrastructure/ modules |
| **Activation Recommendation** | **PILOT_ACTIVE** — Yet Kieu is the security authority. |

**Risks:** Low. Security monitoring is read-intensive.

**Required Remediation:** None.

---

### 7. Helen — CONDITIONAL_ACTIVE

| Criteria | Assessment |
|----------|-----------|
| Capability Readiness | PARTIAL — Role defined (macro, information review) but no agent.py code exists; only agent.yaml and role.md |
| Governance Readiness | NOT CONFIRMED — agent.yaml exists but no charter, no full agent implementation verified |
| Operational Readiness | SANDBOX_ACTIVE by status but minimal implementation |
| Security Compliance | PASS — propose_only mode |
| Dependency Status | BLOCKING — External context gathering capability not verified; no LLM connector test |
| **Activation Recommendation** | **CONDITIONAL_ACTIVE** — Condition: Complete agent implementation (agent.py) with information gathering and macro analysis capabilities. |

**Risks:** Medium. Helen's macro analysis dependencies are unclear.

**Required Remediation:**
1. Complete Helen agent.py implementation with information analysis skills
2. Verify LLM connector integration
3. Define external context gathering workflow
4. Create Helen charter (DRAFT minimum)

---

## Activation Summary

| Agent | Current | Recommended | Gate Required |
|-------|---------|-------------|---------------|
| Janus | SANDBOX_ACTIVE | PILOT_ACTIVE | Sage Review → Hung Vuong Approval |
| Sage | SANDBOX_ACTIVE | PILOT_ACTIVE | Sage Self-Certify → Janus Approval |
| Hermes | SANDBOX_ACTIVE | PILOT_ACTIVE | Sage Review → Hung Vuong Approval |
| Iris | SANDBOX_ACTIVE | PILOT_ACTIVE | Sage Review → Janus Approval |
| Lang Lieu | SANDBOX_ACTIVE | PILOT_ACTIVE | Sage Review → Janus Approval |
| Yet Kieu | SANDBOX_ACTIVE | PILOT_ACTIVE | Sage Review → Janus Approval |
| Helen | SANDBOX_ACTIVE | CONDITIONAL_ACTIVE | Complete agent.py + Sage Review → Janus Approval |
