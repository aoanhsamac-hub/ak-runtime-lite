# AK Agent Activation Matrix Draft

**Date:** 2026-06-08  
**Author:** Janus  
**Status:** DRAFT — Pending Hung Vuong approval  

---

## 1. Activation States

| State | Description | Set By |
|---|---|---|
| LOCKED | Agent cannot receive missions | Hung Vuong |
| READY_FOR_SANDBOX | Agent ready for sandbox testing | OpenCode (via Human Sovereignty Gate) |
| SANDBOX_ACTIVE | Agent operating in sandbox | Hung Vuong |
| PILOT_ACTIVE | Agent operating in pilot | Hung Vuong |
| OPERATIONAL_LIMITED | Agent operating with restrictions | Hung Vuong |
| OPERATIONAL_APPROVED | Agent fully operational | Hung Vuong |

---

## 2. Current Activation State (All Agents: SANDBOX_ACTIVE)

| Agent | Current | Target | Required Approval | Blockers |
|---|---|---|---|---|
| Janus | SANDBOX_ACTIVE | SANDBOX_ACTIVE | None | — |
| Sage | SANDBOX_ACTIVE | SANDBOX_ACTIVE | None | — |
| Hermes | SANDBOX_ACTIVE | SANDBOX_ACTIVE | None | — |
| Iris | SANDBOX_ACTIVE | SANDBOX_ACTIVE | None | — |
| Helen | SANDBOX_ACTIVE | SANDBOX_ACTIVE | None | — |
| Lang Lieu | SANDBOX_ACTIVE | SANDBOX_ACTIVE | None | — |
| Yet Kieu | SANDBOX_ACTIVE | SANDBOX_ACTIVE | None | — |

---

## 3. Activation Gate Requirements

| Transition | Gate | Approver | Evidence Required |
|---|---|---|---|
| LOCKED → READY_FOR_SANDBOX | Human Sovereignty Gate | OpenCode | Agent identity + boundaries configured |
| READY_FOR_SANDBOX → SANDBOX_ACTIVE | Activation Gate | Hung Vuong | Readiness check PASS |
| SANDBOX_ACTIVE → PILOT_ACTIVE | Activation Gate | Hung Vuong | 7 evidence, 1 lesson, 7 usage, 7 perf |
| PILOT_ACTIVE → OPERATIONAL_LIMITED | Council Review | Hung Vuong | Pilot results + risk assessment |
| OPERATIONAL_LIMITED → OPERATIONAL_APPROVED | Council Review | Hung Vuong | Full evidence package |

---

## 4. SA — Agent Skill Matrix

| Agent | Skills | Capabilities Approved | Capabilities Adopted |
|---|---|---|---|
| Janus | 3 (orchestration) | 1 (orchestration) | 0 (proposed) |
| Sage | 2 (review, veto) | 1 (governance) | 0 (proposed) |
| Hermes | 3 (memory, review, archive) | 1 (memory) | 0 (proposed) |
| Iris | 2 (analysis, proposal) | 0 | 0 |
| Helen | 2 (validation, analysis) | 0 | 0 |
| Lang Lieu | 3 (code, test, engineer) | 1 (engineering) | 0 (proposed) |
| Yet Kieu | 2 (monitor, security) | 0 | 0 |

---

## 5. Readiness Check Criteria

| Criterion | Required | Current (All Agents) | Status |
|---|---|---|---|
| Evidence records | ≥ 7 | 7+ | PASS |
| Lesson candidates | ≥ 1 | 1+ | PASS |
| Capability usage records | ≥ 7 | 7+ | PASS |
| Agent performance records | ≥ 7 | 7+ | PASS |

---

## 6. Next Activation Milestone

```
SANDBOX_ACTIVE
    → Sage review of WP35.5 + WP36
    → Hung Vuong approves PILOT_ACTIVE
    → All 7 agents transition to PILOT_ACTIVE
    → Begin 30-day market sandbox
```
