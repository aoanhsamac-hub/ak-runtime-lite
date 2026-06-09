# CAR: Agent Governance Review
**Date:** 2026-06-08
**Phase:** G
**Status:** GAPS_FOUND

## 1. Constitutional Agent Requirements

Per Constitution v1.0 Article 4, each agent's constitutional role:

| Agent | Constitutional Role | Core Authority | Core Prohibition |
|-------|-------------------|----------------|------------------|
| **Janus** | Coordination Centre | Divide tasks, consolidate decisions, create plans, coordinate agents, report to Hung Vuong | Bypass Sage on risk changes, modify production code, change Constitution |
| **Sage** | Constitution & Risk Body | Review risk, block dangerous changes, request rollback, activate safe mode, approve/reject risk kernel changes | Increase risk unilaterally, permit execution when conditions not met |
| **Lang Lieu** | Technical Body | Analyse code, write code, review code, create patches, use Codex/OpenCode | Modify live directly, delete files, modify risk kernel without Sage, merge production without approval |
| **Hermes** | Knowledge, Memory & Training Body | Write lessons, manage memory, create datasets, manage skill registry, standardise docs | Record false lessons, change governance unilaterally, overwrite important memory without backup |
| **Iris** | Market Intelligence Body | Analyse markets, find opportunities, analyse indicators, evaluate strategies, propose signals, manage budget, plan revenue/expenditure, report to Janus | Place orders, change execution logic, bypass risk rules, execute budget expenditures |
| **Helen** | Civilisation Intelligence Body | Analyse macro/news, critique strategy, assess social/political/economic impact, analyse psychosocial phenomena, cross-check with Iris/Yet Kieu, manage external communications | Make direct trading decisions, replace Sage in risk review |
| **Yet Kieu** | Runtime Security Body (CIA+FBI+Military equivalent) | Monitor VPS/MT5/runtime, report system errors, propose technology, control security, collect/provide data | Modify bot live, restart system without process, change risk config |

## 2. Agent Charter Existence

| Agent | FINAL Charter? | Location |
|-------|---------------|----------|
| Janus | **FINAL** YES | `docs/charters/JANUS_CHARTER_v1.0_FINAL.md` |
| Sage | **NOT FOUND** | No charter exists in `docs/charters/`, `docs/agents/sage/`, or anywhere else |
| Lang Lieu | **NOT FOUND** | No charter exists in `docs/charters/`, `docs/agents/lang_lieu/`, or anywhere else |
| Hermes | **FINAL** YES | `docs/charters/HERMES_CHARTER_v1.0_FINAL.md` |
| Iris | **NOT FOUND** | No charter exists in `docs/charters/`, `docs/agents/iris/`, or anywhere else |
| Helen | **NOT FOUND** | No charter exists in `docs/charters/`, `docs/agents/helen/`, or anywhere else |
| Yet Kieu | **NOT FOUND** | No charter exists in `docs/charters/`, `docs/agents/yet_kieu/`, or anywhere else |

**Observation:** Only 2 of 7 agents (Janus, Hermes) have FINAL charters. The remaining 5 agents (Sage, Lang Lieu, Iris, Helen, Yet Kieu) have NO charter of any status - no DRAFT, no FINAL. This is a major governance gap.

**Note on DRAFTS:** The agents directory at `docs/agents/` contains only archived drafts for Janus (`JANUS_CHARTER_DRAFT_v1.0.md`) and Hermes (`HERMES_MEMORY_DATASET_CHARTER_DRAFT_v1.0.md`), both of which are SUPERSEDED by the FINAL charters in `docs/charters/`. No draft or final charters exist for the other 5 agents.

**Additional charters found:** `AK_TREASURY_CHARTER_v1.0_FINAL.md` and `AK_ROYAL_TREASURY_CHARTER_v1.0_FINAL.md` - these are service/domain charters (for the Treasury function), not agent charters. They name Iris as Treasury Operator but Iris itself has no agent charter.

## 3. Agent Law Compliance

Agent Law v1.0 FINAL requires:
1. All agents must follow Governance Before Execution
2. Proposal != Execution != Authorization
3. Knowledge != Permission != Capability
4. Capability != Power

| Agent | FINAL Charter | Mission Clear? | Authority Clear? | Limits Clear? | Forbidden Actions? | Review Chain? | Law Compliant? |
|-------|---------------|---------------|-----------------|---------------|-------------------|--------------|---------------|
| Janus | YES | YES | YES | YES | YES (Section 9) | YES (Sage, HV) | PASS |
| Sage | NO | N/A | N/A | N/A | N/A | N/A | FAIL - no charter |
| Lang Lieu | NO | N/A | N/A | N/A | N/A | N/A | FAIL - no charter |
| Hermes | YES | YES | YES | YES | YES (Section 5: no LanceDB direct, Section 3 limits) | YES (Sage, Janus) | PASS |
| Iris | NO | N/A | N/A | N/A | N/A | N/A | FAIL - no charter |
| Helen | NO | N/A | N/A | N/A | N/A | N/A | FAIL - no charter |
| Yet Kieu | NO | N/A | N/A | N/A | N/A | N/A | FAIL - no charter |

**Compliance Verdict:** Only Janus and Hermes satisfy Agent Law requirements. The remaining 5 agents are non-compliant due to absence of governing charters.

## 4. Governance Charter Compliance

Governance Charter v1.0 defines 5 levels of change approval:

| Level | Review Required | Description |
|-------|----------------|-------------|
| 0 | No review | Typo fixes, notes, reports, log analysis, checklists |
| 1 | Janus review | Directory structure, naming, new docs, workflows |
| 2 | Lang Lieu review | Non-execution code, refactoring, tests, dashboards |
| 3 | Sage review | Risk kernel, execution logic, MT5 orders, portfolio, live config, emergency stop |
| 4 | Hung Vuong approval | Constitution changes, system goals, agent authority changes, large live deploys, overall risk/spending increase |

**Implementation status in charters:**

| Charter | Governance Levels Implemented? | Evidence |
|---------|-------------------------------|----------|
| Janus FINAL | **Partial** | Section 5 (Governance Authority) maps: Risk Review -> Sage (Level 3), Approval Gate -> Janus+Sage (Level 3), Constitutional Gate -> Hung Vuong (Level 4). Level 1 (Janus only) and Level 2 (Lang Lieu) are not explicitly codified in the charter. |
| Hermes FINAL | **Not addressed** | No reference to governance change levels. Hermes has lifecycle governance transitions (Section 8) but these map to knowledge transitions, not the 5-level charter. |
| Treasury FINAL | **Not addressed** | No reference to governance change levels. Treasury has its own budget authority matrix (Section 5) which maps Iris->Janus->Sage->Hung Vuong but doesn't reference Level 2 (Lang Lieu review). |
| Missing charters | **N/A** | Sage, Lang Lieu, Iris, Helen, Yet Kieu - no charter exists to evaluate. |

**Service-level governance implementation:**
- `services/learning_governance_gate.py` and `services/independent_review_gate.py` exist, implementing governance gates at the service layer.
- `governance/governance_gate.py` and `governance/approval_engine.py` implement the approval routing.
- The actual enforcement of the 5-level hierarchy in the codebase versus the charter definition could not be fully verified without reviewing each service's governance gate usage.

**Gap:** The 5-level governance hierarchy is defined in the Governance Charter but is only partially reflected in the Janus charter and not systematically adopted across all agent charters or services.

## 5. Service-to-Agent Mapping

Based on the service file names in `services/` and their functional ownership:

| Service | Governing Agent | Rationale |
|---------|----------------|-----------|
| `treasury_allocation_engine` | **Iris** | Treasury operations are under Iris per Treasury Charter |
| `treasury_audit_service` | **Iris / Sage** | Operations under Iris, audit/review under Sage |
| `treasury_evidence_collector` | **Iris** | Evidence for treasury operations |
| `treasury_health_monitor` | **Iris** | Treasury health monitoring |
| `treasury_impact_tracker` | **Iris** | Treasury impact assessment |
| `treasury_reporting_service` | **Iris** | Treasury reporting |
| `treasury_revenue_ingestion` | **Iris** | Revenue tracking |
| `treasury_status_monitor` | **Iris** | Treasury status monitoring |
| `treasury_transaction_manager` | **Iris** | Transaction management |
| `kingdom_goal_manager` | **Janus** | Goal/planning under Janus coordination |
| `kingdom_planning_engine` | **Janus** | Planning under Janus |
| `kingdom_program_manager` | **Janus** | Program management under Janus |
| `kingdom_scheduler` | **Janus** | Scheduling under Janus coordination |
| `kingdom_health_aggregator` | **Janus / Sage** | Health aggregation spans coordination and governance |
| `kingdom_performance_monitor` | **Janus** | Performance monitoring under coordination |
| `kingdom_status_aggregator` | **Janus** | Status aggregation under coordination |
| `agent_status_monitor` | **Janus** | Agent status per coordination mandate |
| `governance_health_monitor` | **Sage** | Governance health is Sage's domain |
| `security_status_monitor` | **Yet Kieu** | Security monitoring is Yet Kieu's domain |
| `knowledge_health_monitor` | **Hermes** | Knowledge health is Hermes' domain |
| `knowledge_roi_engine` | **Hermes** | Knowledge ROI under Hermes |
| `capability_adoption_engine` | **Hermes** | Capability lifecycle under Hermes |
| `capability_discovery_engine` | **Hermes** | Capability lifecycle under Hermes |
| `capability_evidence_engine` | **Hermes** | Capability lifecycle under Hermes |
| `capability_evolution_loop` | **Hermes** | Capability lifecycle under Hermes |
| `capability_family_engine` | **Hermes** | Capability lifecycle under Hermes |
| `capability_graph_engine` | **Hermes** | Capability lifecycle under Hermes |
| `capability_health_monitor` | **Hermes** | Capability health under Hermes |
| `capability_maturity_engine` | **Hermes** | Capability lifecycle under Hermes |
| `capability_maturity_reassessment_engine` | **Hermes** | Capability lifecycle under Hermes |
| `capability_promotion_readiness_engine` | **Hermes** | Capability lifecycle under Hermes |
| `capability_readiness_engine` | **Hermes** | Capability lifecycle under Hermes |
| `capability_roi_collector` | **Hermes** | Capability lifecycle under Hermes |
| `capability_roi_engine` | **Hermes** | Capability lifecycle under Hermes |
| `capability_usage_collector` | **Hermes** | Capability lifecycle under Hermes |
| `capability_validation_engine` | **Hermes** | Capability lifecycle under Hermes |
| `capability_value_collector` | **Hermes** | Capability lifecycle under Hermes |
| `capability_value_engine` | **Hermes** | Capability lifecycle under Hermes |
| `skill_lifecycle_engine` | **Hermes** | Skill lifecycle under Hermes |
| `skill_deduplication_engine` | **Hermes** | Skill lifecycle under Hermes |
| `skill_discovery_engine` | **Hermes** | Skill lifecycle under Hermes |
| `skill_family_engine` | **Hermes** | Skill lifecycle under Hermes |
| `skill_graph_engine` | **Hermes** | Skill lifecycle under Hermes |
| `skill_maturity_engine` | **Hermes** | Skill lifecycle under Hermes |
| `skill_promotion_engine` | **Hermes** | Skill lifecycle under Hermes |
| `skill_promotion_policy_engine` | **Hermes** | Skill lifecycle under Hermes |
| `skill_validation_engine` | **Hermes** | Skill lifecycle under Hermes |
| `candidate_skill_pipeline` | **Hermes** | Skill pipeline under Hermes |
| `canonical_skill_engine` | **Hermes** | Skill standardisation under Hermes |
| `canonical_capability_engine` | **Hermes** | Capability standardisation under Hermes |
| `learning_signal_engine` | **Hermes** | Learning signals under Hermes knowledge management |
| `signal_clustering_engine` | **Hermes** | Signal processing under Hermes |
| `signal_evidence_collector` | **Hermes** | Evidence collection under Hermes |
| `signal_quality_monitor` | **Hermes** | Signal quality under Hermes |
| `insight_engine` | **Hermes** | Insight generation under Hermes |
| `insight_discovery_engine` | **Hermes** | Insight discovery under Hermes |
| `learning_governance_gate` | **Hermes / Sage** | Learning governance crosses knowledge and risk |
| `learning_audit_layer` | **Hermes** | Learning audit under Hermes |
| `audit_evidence_compiler` | **Sage** | Audit evidence under Sage governance review |
| `program_evidence_collector` | **Janus** | Program evidence under Janus coordination |
| `forecast_accuracy_monitor` | **Iris** | Forecast accuracy under Iris market intelligence |
| `forecast_evidence_collector` | **Iris** | Forecast evidence under Iris |
| `trading_health_monitor` | **Iris** | Trading health under Iris market intelligence |
| `independent_review_gate` | **Sage** | Independent review is Sage's governance role |
| `zone_evidence_collector` | **Iris** | Zone/territory analysis under Iris |
| `zone_quality_monitor` | **Iris** | Zone quality under Iris |
| `services/iris/market_snapshot` | **Iris** | Market snapshot - core Iris function |
| `services/iris/zone_detector` | **Iris** | Zone detection - core Iris function |
| `services/iris/zone_validation_engine` | **Iris** | Zone validation - core Iris function |

**Mapping totals by agent:**
- **Iris:** 18 services (treasury, trading, forecasting, zone analysis)
- **Hermes:** 30 services (capabilities, skills, knowledge, learning, signals)
- **Janus:** 7 services (planning, goals, programs, status, agent monitor)
- **Sage:** 4 services (governance health, audit evidence, independent review, shared with Hermes)
- **Yet Kieu:** 1 service (security status monitor)
- **Helen:** 0 dedicated services found
- **Lang Lieu:** 0 dedicated services found

**Observations:**
- Helen and Lang Lieu have **zero dedicated services**. This may indicate their functions are embedded in other modules (Lang Lieu works via OpenCode/Codex; Helen's macro analysis may be invoked on demand) or that their service layers have not been implemented.
- Yet Kieu has only 1 dedicated service (`security_status_monitor`), which is thin relative to its constitutional scope (VPS, MT5, runtime, security).

## 6. Gaps Identified

| # | Gap | Severity | Description |
|---|-----|----------|-------------|
| G1 | **Missing Agent Charters (5/7)** | CRITICAL | Sage, Lang Lieu, Iris, Helen, and Yet Kieu have no FINAL or DRAFT charter. They cannot operate under bounded authority. |
| G2 | **Agent Law Non-Compliance (5/7)** | CRITICAL | Without charters, 5 agents cannot demonstrate compliance with Agent Law (mission, authority, limits, forbidden actions, review chain). |
| G3 | **Governance Level 2 (Lang Lieu) Not Codified** | HIGH | The Governance Charter requires Lang Lieu review for Level 2 changes (code, tests, refactoring), but no charter defines Lang Lieu's review authority or process. Lang Lieu has no charter at all. |
| G4 | **Governance Levels Not Referenced in Charters** | HIGH | Neither Janus nor Hermes charters reference the 5-level governance hierarchy by level number. The Janus charter has an ad-hoc mapping (Risk Review/Approval Gate/Constitutional Gate) that partially overlaps but is not aligned. |
| G5 | **Helen Has No Service Implementation** | MEDIUM | Helen (Civilisation Intelligence) has constitutional duties in macro/news/social analysis but zero dedicated services. |
| G6 | **Lang Lieu Has No Service Implementation** | MEDIUM | Lang Lieu (Technical Body) has constitutional duties in code analysis/review but zero dedicated services. Code functions are likely embedded ad-hoc. |
| G7 | **Yet Kieu Service Layer Too Thin** | MEDIUM | Yet Kieu has only 1 service (`security_status_monitor`) vs. its broad constitutional scope (VPS, MT5, runtime, security, information collection). |
| G8 | **Skill Files Not Found** | MEDIUM | The glob for `skills/` returned no files. Agent skills may exist as code or YAML registries but no documented skill files were found. |
| G9 | **No Cross-Agent Review Chain Documentation** | MEDIUM | While individual charters (Janus, Hermes) mention Sage review and Hung Vuong approval, there is no consolidated document defining the cross-agent review chain for all 7 agents. |
| G10 | **Service Ownership Not Formally Documented** | LOW | The service-to-agent mapping above was derived from file naming conventions and constitutional roles, not from an official ownership registry. No `service_ownership.yaml` or equivalent exists. |

## 7. Verdict

**OVERALL: GAPS_FOUND - FAIL (conditional)**

The ALKASIK agent governance framework has a constitutional foundation and two well-defined agent charters (Janus, Hermes), but is critically incomplete:

- **5 of 7 agents lack any charter.** Sage, Lang Lieu, Iris, Helen, and Yet Kieu have no FINAL or DRAFT charter document. This means 71% of the agent corps operates without defined mission, authority, limits, forbidden actions, or review chain.
- **Agent Law compliance is at 29%.** Only Janus and Hermes satisfy the requirements of Agent Law v1.0 FINAL.
- **The 5-level governance hierarchy is not properly implemented.** The Governance Charter defines Level 2 as Lang Lieu review, but Lang Lieu has no charter. The hierarchy levels are not referenced in existing charters.
- **Helen and Lang Lieu have zero dedicated services.** Yet Kieu is severely underserved with only 1 service.
- **No formal service ownership registry exists.** The service-to-agent mapping is inferred, not documented.

**Recommended actions (priority order):**

1. **IMMEDIATE:** Create FINAL charters for Sage, Lang Lieu, Iris, Helen, and Yet Kieu.
2. **HIGH:** Codify the 5-level governance hierarchy in all agent charters with explicit level references.
3. **HIGH:** Create dedicated services for Helen and Lang Lieu; expand Yet Kieu's service layer.
4. **MEDIUM:** Create a formal service ownership registry (`service_ownership.yaml`) mapping each service to its governing agent.
5. **MEDIUM:** Create a consolidated cross-agent review chain document.
6. **LOW:** Establish a skills documentation directory and populate it.

