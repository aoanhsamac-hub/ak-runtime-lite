# CAR: Treasury Alignment Review

**Date:** 2026-06-08
**Phase:** E
**Status:** GAPS_FOUND

## 1. Legal Requirements Summary

| Source | Key Requirements |
|--------|-----------------|
| **Economic Law** | ROI tracking per capability; treasury impact assessment before PILOT_ACTIVE+; mandatory metrics (usage_count, total_value, total_cost, roi, adoption_status); capability lifecycle value stages |
| **Budget Law (Art 2, 4)** | 92/8 mandatory revenue split; 9 budget categories (Infrastructure, Knowledge, Dataset, Security, Operations, R&D, Strategic Reserve, Emergency Reserve, Growth Fund); monthly/quarterly/annual budget cycles; Strategic Reserve (3mo min, 10% allocation); Emergency Reserve (1mo, 5% allocation); surplus distribution rules |
| **Treasury Charter** | 92/8 split compliance; Kingdom Fund with 5 sub-funds; monthly/quarterly/annual reporting; append-only audit trail; Sage quarterly review; annual external audit; TIA for any PILOT_ACTIVE+ activation |
| **Royal Treasury Charter** | 92/8 split; legal separation from Kingdom Treasury; Hung Vuong sole authority over 8%; surplus distribution up to 50%; quarterly Sage compliance review; annual confidential audit |
| **Capability Economy Framework** | ROI threshold >= 1.5 for ADOPTED; usage_count >= 10/month for ACTIVE; 6-step Treasury Impact Assessment; economic sustainability criteria (ROI >= 1.5 for 3mo, value > cost for 6mo) |
| **Emergency Reserve Framework** | 7 defined emergency events; 5% monthly allocation until 1mo target; usage triggers & limits per event type; 3-level escalation; replenishment at 10% until restored (max 90 days); post-event Sage audit within 7 days |

## 2. Implementation Assessment

| Requirement | Status | Evidence |
|-------------|--------|----------|
| 92/8 split | **ALIGNED** | `treasury_allocation_engine.py` enforces KINGDOM_TREASURY_SHARE=0.92 / ROYAL_TREASURY_SHARE=0.08; validated by `treasury_audit_service.py:validate_allocation_records()` |
| Budget cycle (monthly/quarterly/annual) | **PARTIAL** | `treasury_reporting_service.py` has `generate_monthly_report()`, `generate_quarterly_report()`, `generate_health_report()`. TREASURY_REPORT_REGISTRY defines monthly/quarterly types with TEMPLATE_READY status. No automated cycle scheduler (Iris proposal -> Sage review -> Janus coordination -> HV approval). |
| Strategic Reserve (3mo min, 10%) | **PARTIAL** | TREASURY_ACCOUNT_REGISTRY has Strategic Reserve with "10% monthly" allocation. `treasury_health_monitor.py:check_reserve_health()` monitors reserve transactions. **No hard-coded 3-month minimum balance check in any service.** |
| Emergency Reserve (1mo, 5%) | **PARTIAL** | TREASURY_ACCOUNT_REGISTRY has Emergency Reserve with "5% monthly" allocation. `check_reserve_health()` tracks activity. **No explicit target cap (1mo operating budget) enforcement or stop-funding logic in code.** |
| TIA before PILOT_ACTIVE+ | **ALIGNED** | `treasury_impact_tracker.py` provides `record_program_impact()` and `record_capability_impact()`. TREASURY_IMPACT_REGISTRY records program and capability impacts. Capability Economy Framework (Section 5) defines the 6-step assessment process. |
| Capability ROI tracking | **ALIGNED** | `capability_roi_engine.py` tracks usage_count, total_value, total_cost, roi, adoption_status via `record_capability_roi()`. `capability_value_engine.py` tracks value metrics. References `memory.capability_roi_registry`. |
| Audit trail (append-only) | **ALIGNED** | `treasury_audit_service.py` validates records, runs full audits. Every revenue/allocation/transaction record carries a generated audit_id. `treasury_transaction_manager.py` implements PROPOSED->VALIDATED->APPROVED->RECORDED->AUDITED lifecycle. Data files are append-only (entries array). |
| 9 budget categories | **PARTIAL** | Budget Law lists 9: Infrastructure, Knowledge, Dataset, Security, Operations, R&D, Strategic Reserve, Emergency Reserve, Growth Fund. Treasury Charter (Section 3) lists only 7 + "Other Programs" — **Growth Fund is present in the structure diagram but omitted from the budget allocation list under Kingdom Treasury.** No code-level validation of all 9 categories. |

## 3. Registry Alignment

| Registry | Aligns With | Status |
|----------|-------------|--------|
| TREASURY_ACCOUNT_REGISTRY | Budget Law (accounts, 92/8 split, reserves) | **ALIGNED** — 6 accounts with correct allocations |
| TREASURY_STATUS_REGISTRY | Treasury Charter (account structure) | **ALIGNED** — Kingdom Treasury, Royal Treasury, Kingdom Fund, Strategic Reserve, Emergency Reserve |
| TREASURY_TRANSACTION_REGISTRY | Treasury Charter, Budget Law (transaction types) | **ALIGNED** — 6 transaction types with approval chains |
| TREASURY_TRANSACTION_STATUS_REGISTRY | Treasury Charter (audit lifecycle) | **ALIGNED** — 5-stage lifecycle (PROPOSED->AUDITED) |
| TREASURY_IMPACT_REGISTRY | Economic Law, Capability Economy Framework | **ALIGNED** — program_impacts + capability_impacts arrays |
| TREASURY_HEALTH_REGISTRY | Treasury Charter (reporting) | **ALIGNED** — 5 health categories covering all treasury domains |
| TREASURY_REPORT_REGISTRY | Budget Law (monthly/quarterly/annual) | **ALIGNED** — 3 report types with templates |
| TREASURY_EVIDENCE_REGISTRY | Treasury Charter (audit evidence) | **ALIGNED** — evidence records linked to treasury_impact_id |

**Note:** All 8 registries exist and are structurally aligned. Some show `status: INITIALIZED` and `balance: null` — they are structurally correct but not yet populated with real production data.

## 4. Service Alignment

| Service | Legal Requirement | Alignment |
|---------|-----------------|-----------|
| `treasury_revenue_ingestion.py` | Budget Law Art 1 (revenue sources) | **ALIGNED** — validates against 11 revenue sources from Budget Law; assigns audit_id to every record |
| `treasury_allocation_engine.py` | Budget Law Art 2 (92/8 split) | **ALIGNED** — enforces mandatory 92/8 split; generates audit trail per allocation |
| `treasury_transaction_manager.py` | Treasury Charter (audit, lifecycle) | **ALIGNED** — 5-stage lifecycle with validation, approval, recording, auditing |
| `treasury_reporting_service.py` | Budget Law Art 4 (cycles), Treasury Charter Sec 6 | **ALIGNED** — monthly, quarterly, and health report generation |
| `treasury_health_monitor.py` | Treasury Charter (compliance, reserves) | **ALIGNED** — monitors revenue, treasury, budget, reserve, and audit health |
| `treasury_audit_service.py` | Treasury Charter Sec 7 (audit) | **ALIGNED** — full audit run validates revenue, treasury, allocation, reporting, and audit records; validates 92% ratio |
| `treasury_impact_tracker.py` | Economic Law (TIA), Capability Economy Framework | **ALIGNED** — records program and capability treasury impacts |
| `capability_value_engine.py` | Economic Law (value metrics) | **ALIGNED** — assesses usage_value, quality_value, adoption_value, total_value |
| `capability_roi_engine.py` | Economic Law (ROI tracking), Capability Economy Framework | **ALIGNED** — records capability ROI with usage_count, total_value, total_cost, roi |

## 5. Gaps Identified

| # | Gap | Severity | Source Requirement | Recommendation |
|---|-----|----------|-------------------|---------------|
| G1 | No automated Strategic Reserve minimum balance enforcement (3mo operating budget) | **HIGH** | Budget Law Sec 6 | Add `check_strategic_reserve_minimum()` to `treasury_health_monitor.py` that compares balance against 3x monthly operating budget |
| G2 | No Emergency Reserve target cap logic (stop at 1mo operating budget) | **MEDIUM** | Emergency Reserve Framework Sec 3 | Add cap check in `treasury_allocation_engine.py` to stop 5% allocation when target met |
| G3 | Budget categories incomplete in Treasury Charter allocation list — Growth Fund listed in structure diagram but omitted from budget allocation list | **LOW** | Budget Law Sec 3 | Update Treasury Charter Sec 3 allocation list to include Growth Fund explicitly |
| G4 | No automated budget cycle scheduling service | **MEDIUM** | Budget Law Sec 4 | Create a `treasury_budget_cycle.py` service that orchestrates Iris proposal -> Sage review -> Janus coordination -> HV approval per month/quarter/year |
| G5 | No dedicated surplus distribution service | **LOW** | Budget Law Sec 8, Royal Treasury Charter Sec 7 | Create a `treasury_surplus_service.py` implementing Janus certification, Sage verification, HV authorization, up to 50% distribution |
| G6 | ROI threshold enforcement (>= 1.5 for ADOPTED) not hard-coded in capability services | **MEDIUM** | Capability Economy Framework Sec 4, 7 | Add threshold validation in `capability_roi_engine.py` that flags capabilities below 1.5 ROI for ADOPTED stage |
| G7 | Economic sustainability criteria (3 consecutive months ROI >= 1.5, 6 months value > cost) not auto-evaluated | **MEDIUM** | Capability Economy Framework Sec 7 | Add `check_economic_sustainability()` to `capability_value_engine.py` or `treasury_health_monitor.py` |
| G8 | No dedicated Royal Treasury service implementations | **LOW** | Royal Treasury Charter | Consider creating `royal_treasury_manager.py` and `royal_treasury_audit_service.py` for the separate governance path |

## 6. Verdict

**ALIGNED (with gaps).** The treasury legal framework, implementation services, and registries are substantially aligned. All critical requirements are covered: the 92/8 split is enforced in code and validated by audit, capability ROI tracking exists end-to-end, treasury impact assessments are recorded, audit trails are append-only with a defined lifecycle, and 8 treasury registries provide structural alignment with legal mandates.

**8 gaps were identified** (1 HIGH, 3 MEDIUM, 3 LOW, 1 informational). The highest-priority gap (G1) is the absence of automated Strategic Reserve minimum balance enforcement — the code tracks reserve transactions but does not enforce the 3-month operating budget minimum. G2 and G6 should also be addressed before operational go-live.

**Status: GAPS_FOUND — Recommend remediation of G1, G2, G4, G6 before declaring full alignment.**
