# Terminology Inventory

**KTSP Phase B** | **Date:** 2026-06-08
**Scope:** Full scan of docs/, services/, tests/, registries/, reports/, templates/, SOPs, data/, memory/

---

## 1. Filename Inventory

### Files with "NATIONAL_" (uppercase) in filename — 25 files

| Category | Count | Files |
|----------|-------|-------|
| Registries | 4 | NATIONAL_GOAL_REGISTRY.yaml, NATIONAL_HEALTH_REGISTRY.yaml, NATIONAL_PROGRAM_REGISTRY.yaml, NATIONAL_STATUS_REGISTRY.yaml |
| Reports | 10 | NATIONAL_HEALTH_REPORT.md, NATIONAL_PLANNING_REPORT.md, NATIONAL_PLANNING_READINESS_REVIEW.md, NATIONAL_READINESS_SCORECARD.md, NATIONAL_SITUATION_ROOM_READINESS_REVIEW.md, NATIONAL_STATUS_REPORT.md, AK_NATIONAL_KNOWLEDGE_AUDIT.md, AK_NATIONAL_KNOWLEDGE_FOUNDATION_ROADMAP.md, AK_NATIONAL_KNOWLEDGE_GRAPH.md, AK_NATIONAL_KNOWLEDGE_INVENTORY.md, AK_NATIONAL_KNOWLEDGE_PACKAGE.md, AK_WP37_NATIONAL_EVOLUTION_FINAL_REPORT.md |
| Templates | 3 | NATIONAL_HEALTH_REPORT_TEMPLATE.md, NATIONAL_PLANNING_REPORT_TEMPLATE.md, NATIONAL_STATUS_REPORT_TEMPLATE.md |
| SOPs | 1 | NATIONAL_SITUATION_ROOM_PROCESS.md |
| Audit | 1 | Q1_NATIONAL_AUDIT_PREPARATION.md |
| Laws | 1 | AK_NATIONAL_BUDGET_LAW_v1.0_FINAL.md |
| Archive | 2 | AK_NATIONAL_BUDGET_LAW_v0.1_DRAFT.docx, AK_NATIONAL_BUDGET_LAW_v1.0_REVIEW.md |

### Files with "national_" (lowercase) in filename — 32 files

| Category | Count | Files |
|----------|-------|-------|
| Services | 7 | national_goal_manager.py, national_health_aggregator.py, national_performance_monitor.py, national_planning_engine.py, national_program_manager.py, national_scheduler.py, national_status_aggregator.py |
| Tests | 4 | test_national_health_registry.py, test_national_planning.py, test_national_scheduler.py, test_national_status_aggregation.py |
| Data | 5 | national_budget.json, national_expenses.json, national_fund.json, national_revenue.json, national_treasury.json |
| Schemas | 3 | national_budget_schema.json, national_expense_schema.json, national_revenue_schema.json |
| Memory | 1 | national_memory_platform.py |
| Pycache | 12 | (compiled bytecode copies of the 7 services + 4 tests + 1 memory module) |

---

## 2. Content Term Inventory

### Canonical Terms (will be replaced)

| Term | Match Count | Distinct Files | Classification |
|------|-------------|----------------|----------------|
| National Treasury | 58 | 25 | → KINGDOM TREASURY |
| National Fund | 15 | 12 | → KINGDOM FUND |
| National Planning | 15 | 7 | → KINGDOM PLANNING |
| National Health | 12 | 8 | → KINGDOM HEALTH |
| National Status | 11 | 6 | → KINGDOM STATUS |
| National Situation Room | 10 | 7 | → KINGDOM SITUATION ROOM |
| National Program | 7 | 6 | → KINGDOM PROGRAM |
| National Goal | 5 | 4 | → KINGDOM GOAL |
| National Awareness | 5 | 3 | → KINGDOM AWARENESS |
| National Audit | 2 | 1 | → KINGDOM AUDIT OFFICE |
| National Performance | 1 | 1 | → KINGDOM PERFORMANCE |

### Terms that Remain (already canonical)

| Term | Match Count | Reason |
|------|-------------|--------|
| Royal Treasury | 82 | Distinct entity (8% pool), keep |
| Alkasik Kingdom | widespread | Nation name, keep |
| Hung Vuong | widespread | Constitutional monarch, keep |
| Janus | 910 | Agent name, keep |
| Sage | widespread | Agent name, keep |
| Iris | widespread | Agent name, keep |
| Hermes | widespread | Agent name, keep |
| Helen | widespread | Agent name, keep |
| Lang Lieu | widespread | Agent name, keep |
| Yet Kieu | widespread | Agent name, keep |

### Terms NOT Found (new authority model — zero existing references)

| Term | Matches | Status |
|------|---------|--------|
| Royal Executive House (REH) | 0 | NEW — maps Janus executive role |
| Royal Assembly of the Kingdom (RAK) | 0 | NEW — legislative body |
| High Court of the Kingdom (HCK) | 0 | NEW — judicial body |
| Kingdom Audit Office (KAO) | 0 | NEW — maps Sage audit role |
| Executive Branch | 0 | NEW — branch terminology |
| Legislative Branch | 0 | NEW — branch terminology |
| Judicial Branch | 0 | NEW — branch terminology |

---

## 3. Distribution by File Type

| File Type | Files Affected | Type of Change |
|-----------|---------------|----------------|
| YAML registries | 4 file renames + 4 internal key renames | File rename + content change |
| Python services | 7 file renames + import path updates | File rename + content change |
| Python tests | 4 file renames + import path updates | File rename + content change |
| Python memory | 1 file rename + import path updates | File rename + content change |
| JSON data | 5 file renames | File rename only |
| JSON schemas | 3 file renames | File rename only |
| Markdown reports | 16 file renames + text changes | File rename + content change |
| Markdown templates | 3 file renames + text changes | File rename + content change |
| Markdown SOPs | 1 file rename + text changes | File rename + content change |
| Markdown audit | 2 file renames + text changes | File rename + content change |
| Markdown laws/charters | 2 file renames + text changes | File rename + content change |
| **Total** | **~48 files** | |

---

## 4. Classification Summary

| Classification | Count | Criteria |
|---------------|-------|----------|
| Canonical (keep) | ~10 terms | Aligned with Constitution/State Corpus |
| Rename (file + content) | ~38 files | "National" → "Kingdom" prefix change |
| Rename (content only) | ~25 files | "National Treasury" → "Kingdom Treasury" text |
| New (no existing refs) | 4 terms | REH, RAK, HCK, KAO authority model |
| Legacy (archive) | ~12 files | Old names after migration |

---

*Prepared by KTSP Phase B. No changes executed — inventory only.*
