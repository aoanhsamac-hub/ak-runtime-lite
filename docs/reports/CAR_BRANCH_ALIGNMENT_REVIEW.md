# CAR: Branch Alignment Review

**Date:** 2026-06-08
**Phase:** C
**Status:** GAPS_FOUND

---

## 1. Constitutional Branches

Based on Constitution v1.0 (Article 4 — Phân quyền agent) and the Agent Law v1.0 FINAL, the AK Kingdom defines **7 agent branches**, not 6. The Intelligence domain is split across two constitutionally distinct agents:

| # | Branch | Agent | Constitutional Role | Authority Level |
|---|--------|-------|-------------------|----------------|
| 1 | **Executive Branch** | Janus | Presidential orchestration, coordination, planning, reporting | COORDINATE |
| 2 | **Constitutional Branch** | Sage | Risk review, governance gate, constitutional compliance, veto | REVIEW / VETO |
| 3 | **Technical Branch** | Lang Liêu | Code, architecture, testing, refactoring, platform | EXECUTE (code) |
| 4 | **Knowledge Branch** | Hermes | Memory, lessons, datasets, skills, capabilities, archive | REVIEW |
| 5a | **Market Intelligence Branch** | Iris | Market analysis, treasury/budget management, strategy assessment | PROPOSE |
| 5b | **Civilization Intelligence Branch** | Helen | Macro analysis, news validation, social/political impact, external comms | PROPOSE |
| 6 | **Security Branch** | Yết Kiêu | VPS, MT5, runtime monitoring, incident response, information collection | MONITOR |

**Note on the 6-branch model vs 7-agent reality:** The Constitution defines Iris and Helen as separate agents with distinct scope (Iris = market/economic/treasury; Helen = macro/civilization/external). They share the "Intelligence" domain but have non-overlapping authority. Below, they are assessed as two branches because the Constitution treats them as two separate offices.

---

## 2. Branch Implementation

### 2.1 Executive Branch — Janus

| Criterion | Assessment |
|-----------|-----------|
| Role implemented? | Yes — `agents/janus/agent.py`, `agent.yaml`, `role.md`, `boundaries.md`, `src/agent.py` |
| Charter exists? | Yes — `docs/charters/JANUS_CHARTER_v1.0_FINAL.md` |
| Services owned? | Partial — `kingdom_goal_manager.py`, `kingdom_program_manager.py`, `kingdom_planning_engine.py`, `kingdom_health_aggregator.py`, `kingdom_status_aggregator.py`, `kingdom_performance_monitor.py`, `kingdom_scheduler.py` |
| Skills defined? | **NO** — `agents/janus/skills/` is empty |
| SOPs defined? | **NO** — `workflows.yaml` contains `workflows: []` |
| Authority correctly scoped? | Yes — `role_boundary.py` grants `orchestrate`, `route_task`, `coordinate`, `aggregate_report`, `request_review`; forbids `bypass_sage`, `modify_law`, `direct_execution` |
| Limits respected? | Yes — no direct execution, no bypass of Sage |
| Boundary violations? | None found in code |

### 2.2 Constitutional Branch — Sage

| Criterion | Assessment |
|-----------|-----------|
| Role implemented? | Yes — `agents/sage/agent.py`, `agent.yaml`, `role.md`, `boundaries.md` |
| Charter exists? | **NO** — No `SAGE_CHARTER_v1.0_FINAL.md` in `docs/charters/` |
| Services owned? | Partial — `governance_health_monitor.py`, `independent_review_gate.py` |
| Skills defined? | **NO** — `agents/sage/skills/` is empty |
| SOPs defined? | **NO** — `workflows.yaml` contains `workflows: []` |
| Authority correctly scoped? | Yes — `role_boundary.py` grants `review`, `veto`, `classify_risk`, `require_rollback`, `audit`, `governance_gate_review`; sets `can_veto=True` |
| Limits respected? | Yes — no direct execution, no trading |
| Boundary violations? | None found in code |
| **GAP** | **Missing charter** — Sage has no formal charter document despite being the highest-authority governance agent |

### 2.3 Technical Branch — Lang Liêu

| Criterion | Assessment |
|-----------|-----------|
| Role implemented? | Yes — `agents/lang_lieu/agent.py`, `agent.yaml`, `role.md`, `boundaries.md`, `dev_orchestrator.py` |
| Charter exists? | **NO** — No `LANG_LIEU_CHARTER_v1.0_FINAL.md` |
| Services owned? | None directly — services are shared/domain-oriented |
| Skills defined? | **NO** — `agents/lang_lieu/skills/` is empty |
| SOPs defined? | **NO** |
| Authority correctly scoped? | Yes — `role_boundary.py` grants `code`, `architecture`, `refactor`, `test`, `review_code`, `use_opencode_adapter`; sets `can_code=True`, `can_use_opencode=True`, autonomy `BRANCH_WRITE` |
| Limits respected? | Yes — forbidden from `deploy_live`, `modify_protected_modules_without_sage_review` |
| Boundary violations? | None found |
| **GAP** | **Missing charter**; no coding workflow SOP beyond bootstrap `workflows/coding_cycle/workflow.yaml` |

### 2.4 Knowledge Branch — Hermes

| Criterion | Assessment |
|-----------|-----------|
| Role implemented? | Yes — `agents/hermes/agent.py`, `agent.yaml`, `role.md`, `boundaries.md` |
| Charter exists? | Yes — `docs/charters/HERMES_CHARTER_v1.0_FINAL.md` |
| Services owned? | Extensive — `candidate_skill_pipeline.py`, `canonical_capability_engine.py`, `canonical_skill_engine.py`, `capability_adoption_engine.py`, `capability_discovery_engine.py`, `capability_evidence_engine.py`, `capability_evolution_loop.py`, `capability_family_engine.py`, `capability_graph_engine.py`, `capability_health_monitor.py`, `capability_maturity_engine.py`, `capability_readiness_engine.py`, `capability_roi_engine.py`, `capability_usage_collector.py`, `capability_validation_engine.py`, `capability_value_engine.py`, `knowledge_health_monitor.py`, `knowledge_roi_engine.py`, `learning_governance_gate.py`, `skill_deduplication_engine.py`, `skill_discovery_engine.py`, `skill_family_engine.py`, `skill_graph_engine.py`, `skill_lifecycle_engine.py`, `skill_maturity_engine.py`, `skill_promotion_engine.py`, `skill_promotion_policy_engine.py`, `skill_validation_engine.py` |
| Skills defined? | **NO** — `agents/hermes/skills/` is empty |
| SOPs defined? | **NO** |
| Authority correctly scoped? | Yes — `role_boundary.py` grants `memory_review`, `lesson_review`, `dataset_review`, `skill_review`, `archive_review`, `distillation`; forbids `trading_execution`, `modify_risk_kernel`, `direct_lancedb_backend_access` |
| Limits respected? | Yes |
| Boundary violations? | None found |
| **GAP** | **No skills or SOPs** despite owning the largest service surface area |

### 2.5 Market Intelligence Branch — Iris

| Criterion | Assessment |
|-----------|-----------|
| Role implemented? | Yes — `agents/iris/agent.py`, `agent.yaml`, `role.md`, `boundaries.md` |
| Charter exists? | **NO** |
| Services owned? | `services/iris/market_snapshot.py`, `services/iris/zone_detector.py`, `services/iris/zone_validation_engine.py`; treasury services (`treasury_*.py`) are not explicitly assigned to Iris in code |
| Skills defined? | **NO** |
| SOPs defined? | **NO** |
| Authority correctly scoped? | Yes — `role_boundary.py` grants `market_analysis`, `economic_analysis`, `portfolio_analysis`, `budget_proposal`, `resource_allocation_proposal`; autonomy `READ_ONLY` |
| Limits respected? | Yes — forbidden from `live_execution`, `modify_risk_kernel`, `direct_broker_call` |
| Boundary violations? | Treasury services (`treasury_allocation_engine.py`, `treasury_transaction_manager.py`) perform allocation and transaction recording but are not explicitly owned by any agent in the code. Constitution assigns budget/treasury to Iris. |
| **GAP** | **Missing charter**; treasury services are ownerless in code |

### 2.6 Civilization Intelligence Branch — Helen

| Criterion | Assessment |
|-----------|-----------|
| Role implemented? | Yes — `agents/helen/agent.py`, `agent.yaml`, `role.md`, `boundaries.md` |
| Charter exists? | **NO** |
| Services owned? | None directly — Helen's constitutional role (macro analysis, news validation, external context) has no dedicated service implementation |
| Skills defined? | **NO** |
| SOPs defined? | **NO** |
| Authority correctly scoped? | Yes — `role_boundary.py` grants `information_validation`, `macro_analysis`, `civilization_analysis`, `communication_draft`, `external_context_review` |
| Limits respected? | Yes — forbidden from `modify_execution`, `approve_risk`, `direct_trading` |
| Boundary violations? | None found (but also no implementation to violate from) |
| **GAP** | **Missing charter**; **no services** — Helen has the thinnest implementation of all 7 agents despite a broad constitutional mandate |

### 2.7 Security Branch — Yết Kiêu

| Criterion | Assessment |
|-----------|-----------|
| Role implemented? | Yes — `agents/yet_kieu/agent.py`, `agent.yaml`, `role.md`, `boundaries.md`, `src/agent.py` |
| Charter exists? | **NO** |
| Services owned? | `security_status_monitor.py` |
| Skills defined? | **NO** |
| SOPs defined? | **NO** — `workflows.yaml` not checked (empty likely) |
| Authority correctly scoped? | Yes — `role_boundary.py` grants `monitor_infrastructure`, `security_review`, `incident_response`, `runtime_observation`, `approved_sop_execution` |
| Limits respected? | Yes — forbidden from `modify_law`, `direct_trading`, `read_unapproved_secret` |
| Boundary violations? | Minor: `security_status_monitor.py` checks `services/iris/zone_detector.py` existence — domain crossing into Iris's territory |
| **GAP** | **Missing charter**; thin service coverage for runtime monitoring |

---

## 3. Cross-Branch Coordination

### 3.1 Janus Coordination

| Mechanism | Status |
|-----------|--------|
| Janus coordinates all 7 agents | Implemented in `agents/router.py` — keyword-based routing to all agents |
| Route through `TaskRouter.choose_agent()` | Yes — 7 routing rules cover governance, memory, market, information, code, security, multi-agent |
| Protected module enforcement | Yes — `router.py` blocks tasks touching protected modules without Sage review |
| Council review workflow | Yes — `workflows/council_review.py` orchestrates multi-agent councils with Janus aggregation + Sage risk review |
| Skill files for coordination | **NO** — `agents/janus/skills/` is empty |
| Default routing fallback | Tasks not matching any keyword are routed to Janus (correct default) |

**GAP:** Janus has no Presidential Orchestration skill file, no SOP, no defined coordination workflows (empty `workflows.yaml`).

### 3.2 Sage Risk Review

| Mechanism | Status |
|-----------|--------|
| Risk review gate | Implemented — `router.py` line 46-48: protected module check requires Sage in `required_approvals` |
| Sage review in skill promotion | Yes — `independent_review_gate.py` enforces recommender != reviewer |
| Sage review for capability promotion | Yes — `capability_promotion_readiness_engine.py` references `sage_review` and `sage_outcome` |
| Sage in learning governance | Yes — `learning_governance_gate.py` includes `sage_review_gate` |
| **GAP** | **No formal risk review SOP** — Sage has no defined workflow for risk classification, rollback requests, or safe mode activation |

### 3.3 Lang Liêu Engineering Workflow

| Mechanism | Status |
|-----------|--------|
| Coding workflow exists? | Minimal — `workflows/coding_cycle/workflow.yaml` exists but only says `name: coding_cycle, status: bootstrap` |
| Autonomous coding pipeline | Implemented partially — `candidate_skill_pipeline.py` constrains skills to CANDIDATE/PENDING_REVIEW/DISABLED |
| Code review gates | `role_boundary.py` allows `review_code` for Lang Liêu |
| **GAP** | **No operational coding workflow** — the Constitution mandates Issue → Plan → Code Draft → Review → Test → Sage Review → Janus Approval → Deploy, but this is not encoded in any workflow or SOP |

### 3.4 Hermes Knowledge Lifecycle

| Mechanism | Status |
|-----------|--------|
| Knowledge lifecycle | Fully implemented in services — Evidence → Lesson → Knowledge → Skill → Capability with governance gates |
| Skill lifecycle engine | `skill_lifecycle_engine.py` — 10-stage state machine with governance gates |
| Capability lifecycle | `capability_evolution_loop.py` — 6-state machine: LOCKED→UNLOCKED→EVOLVING_MATURITY→EVOLVING_CYCLE→EVOLVED/ROLLED_BACK |
| Retention governance | Enforced via `candidate_skill_pipeline.py` and skill lifecycle |
| **GAP** | Knowledge lifecycle is implemented in code but **no Hermes SOP** documents the lifecycle process for agents to follow |

---

## 4. Authority Boundary Violations

| # | Violation | Detail | Severity |
|---|-----------|--------|----------|
| 1 | **Treasury services ownerless** | `treasury_allocation_engine.py`, `treasury_transaction_manager.py`, `treasury_health_monitor.py`, `treasury_revenue_ingestion.py`, `treasury_status_monitor.py`, `treasury_audit_service.py`, `treasury_evidence_collector.py`, `treasury_reporting_service.py`, `treasury_impact_tracker.py` — none are assigned to any agent in code. Constitution v1.0 Article 4 assigns budget/treasury to Iris. | MEDIUM |
| 2 | **Yet Kieu crosses into Iris domain** | `security_status_monitor.py` checks `services/iris/zone_detector.py` existence. Zone detection is Iris's domain per Constitution. | LOW |
| 3 | **No Sage charter** | Sage is the highest constitutional authority after Hung Vuong but has no formal charter. The Constitution defines Sage's authority in detail, but there is no charter document detailing its operational scope, gates, or SOPs. | HIGH |
| 4 | **Missing charters for 5 agents** | Sage, Lang Liêu, Iris, Helen, Yết Kiêu all lack charters. Only Janus and Hermes have FINAL charters. | HIGH |
| 5 | **All skills directories empty** | All 7 agents have `skills/` directories that are empty. No agent has any skill file encoding its operational procedures. | HIGH |
| 6 | **Workflows at bootstrap only** | `governance_cycle`, `coding_cycle`, `incident_cycle` all at `status: bootstrap`. Agent-level `workflows.yaml` files are empty for Janus and Sage. | MEDIUM |
| 7 | **Helen has no services** | Helen's constitutional role includes macro analysis, news validation, social impact assessment, communication/external affairs. None of these have corresponding service implementations. | HIGH |

---

## 5. Gaps Identified

### Gap 1: Missing Charters (HIGH)
- **Sage**: No charter. Sage is the constitutional watchdog — missing charter means no formal definition of risk classification levels, review gates, rollback procedures, or safe mode activation protocol.
- **Lang Liêu**: No charter. Missing engineering workflow definition, code review standards, deployment gate criteria.
- **Iris**: No charter. Missing budget management authority definition, treasury proposal workflow, market analysis SOP.
- **Helen**: No charter. Missing macro analysis framework, external communication policy, information validation SOP.
- **Yết Kiêu**: No charter. Missing runtime monitoring SOP, incident response protocol, security alert thresholds.

### Gap 2: Empty Skill Files (HIGH)
All 7 agents have empty `skills/` directories. Skill files are the operational encoding of an agent's constitutional authority into executable procedures. Without them:
- Janus has no orchestration skill
- Sage has no risk review skill
- Lang Liêu has no coding workflow skill
- Hermes has no knowledge lifecycle skill
- Iris has no market analysis skill
- Helen has no intelligence analysis skill
- Yết Kiêu has no security monitoring skill

### Gap 3: No Operational Workflows (MEDIUM)
`governance_cycle`, `coding_cycle`, `incident_cycle` workflows exist but only as bootstrap stubs. The Constitution Article 8 mandates a strict coding pipeline (Issue → Plan → Code Draft → Review → Test → Sage Review → Janus Approval → Deploy) but this is not implemented in any workflow.

### Gap 4: Treasury Services Unassigned (MEDIUM)
8 treasury services exist as standalone modules with no agent ownership. Constitution Article 4 gives Iris "quản trị ngân sách" (budget management) and "cân đối toàn bộ các hoạt động liên quan đến tài chính" (balance all financial activities). These services should be explicitly scoped to Iris.

### Gap 5: Helen Has No Service Implementation (HIGH)
Helen is constitutionally responsible for macro analysis, news validation, social/political impact assessment, communication, and external affairs. None of these functions have any service code. Helen is the only agent with zero service coverage.

### Gap 6: No Risk Review SOP for Sage (MEDIUM)
While `independent_review_gate.py` and `router.py` enforce Sage review at code level, there is no documented SOP defining:
- Risk classification levels (the Constitution references LEVEL_2_HIGH+ and LEVEL_3_CRITICAL+ but these are not defined in code)
- Rollback procedure
- Safe mode activation criteria
- Emergency power invocation protocol

### Gap 7: Charters Directory Incomplete (HIGH)
`docs/charters/` contains only 4 files:
- `AK_ROYAL_TREASURY_CHARTER_v1.0_FINAL.md`
- `AK_TREASURY_CHARTER_v1.0_FINAL.md`
- `JANUS_CHARTER_v1.0_FINAL.md`
- `HERMES_CHARTER_v1.0_FINAL.md`

Missing: `SAGE_CHARTER`, `LANG_LIEU_CHARTER`, `IRIS_CHARTER`, `HELEN_CHARTER`, `YET_KIEU_CHARTER`.

---

## 6. Verdict

```
BRANCH ALIGNMENT: GAPS_FOUND
SEVERITY:         HIGH
RECOMMENDATION:   HALT further feature development until charters and skill files are created
```

**Summary:** The constitutional framework (Constitution v1.0, Agent Law v1.0) is well-defined. The agent runtime framework (`agents/`) is structurally complete — all 7 agents have agent classes, role boundaries, and identity definitions. The services layer is extensive (69 modules) and implements the core governance, treasury, capability, and knowledge functions.

However, the **operational layer is critically underdeveloped**:

1. **5 of 7 agents lack charters** — only Janus and Hermes have FINAL charters
2. **All 7 agents have empty skill directories** — no operational procedures exist
3. **3 core workflows are bootstrap stubs** — governance, coding, and incident cycles are non-operational
4. **Helen has zero service implementation** despite a broad constitutional mandate
5. **Treasury services are ownerless** — constitutionally assigned to Iris but not scoped in code
6. **No risk review SOP** — Sage's constitutional authority is encoded in `role_boundary.py` but has no documented operational protocol

The codebase has strong **structural alignment** with the Constitution at the framework level (`role_boundary.py`, `router.py`, `agent.py`), but **operational alignment is poor** due to missing charters, empty skills, and bootstrap workflows. Until these gaps are closed, agents cannot exercise their constitutional authority through defined, auditable procedures.
