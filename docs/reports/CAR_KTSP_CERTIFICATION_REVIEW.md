# CAR: KTSP Certification Review
**Date:** 2026-06-08
**Phase:** H
**Status:** GAPS_FOUND

## 1. KTSP Overview

The Kingdom Terminology Migration Plan defines a 6-wave migration replacing all "National"/"national_" terminology with "Kingdom"/"kingdom_" across ~53 files and ~131 changes:

| Wave | Scope | Files | Risk |
|------|-------|-------|------|
| Wave 1 | Legal artifacts (laws, charters, frameworks) | ~12 | HIGH |
| Wave 2 | YAML registries + wrapper keys + code references | 4 YAML + 8 code | MEDIUM |
| Wave 3 | Reports & templates (markdown) | ~19 | LOW |
| Wave 4 | Services & tests (.py) | 12 | HIGH |
| Wave 5 | Authority model (REH/RAK/HCK/KAO) documentation | ~5 | LOW |
| Wave 6 | Archive legacy map | 1 | LOW |

## 2. Wave-by-Wave Verification

### Wave 1 (Legal) — PASS
- AK_MEMORY.md references `AK_KINGDOM_BUDGET_LAW_v1.0_REVIEW.md` at `sovereign/laws/budget/`; no `NATIONAL_` law file references found in active docs.
- No remaining `national_` files found under `docs/` via glob.

### Wave 2 (Registries) — GAPS REMAIN
- YAML registry files correctly renamed: `KINGDOM_GOAL_REGISTRY.yaml`, `KINGDOM_PROGRAM_REGISTRY.yaml`, `KINGDOM_HEALTH_REGISTRY.yaml`, `KINGDOM_STATUS_REGISTRY.yaml` all present.
- Internal wrapper keys updated correctly in service code (`.get("kingdom_goal_registry", ...)`, etc.).
- **GAP:** `TREASURY_TRANSACTION_REGISTRY.yaml` references `national_expense_schema` (line 21) and `national_revenue_schema` (line 25) — should be `kingdom_expense_schema` and `kingdom_revenue_schema`.
- **GAP:** `TREASURY_ACCOUNT_REGISTRY.yaml` references `data/treasury/national_treasury.json` (line 18), `data/treasury/national_fund.json` (line 36), and `data/treasury/national_budget.json` (line 63) — actual files are `kingdom_treasury.json`, `kingdom_fund.json`, `kingdom_budget.json`.

### Wave 3 (Reports & Templates) — PASS
- Glob for `*national_*` files under `docs/` returned 0 matches. All 16+ reports, 3 templates, and 1 SOP appear renamed.
- Data files (`data/treasury/`) and schema files (`docs/schemas/`) all use `kingdom_` prefix.

### Wave 4 (Services & Tests) — GAPS REMAIN
- All service files confirmed renamed to `kingdom_` prefix: `kingdom_goal_manager.py`, `kingdom_program_manager.py`, `kingdom_health_aggregator.py`, `kingdom_status_aggregator.py`, `kingdom_planning_engine.py`, `kingdom_performance_monitor.py`.
- Memory module: `memory/kingdom_memory_platform.py` confirmed.
- Registry file references in services correctly use `KINGDOM_*` paths and `kingdom_*` wrapper keys.
- **GAP:** `services/kingdom_planning_engine.py:26` — function `create_national_plan()` still uses "national" in its name.
- **GAP:** `services/kingdom_performance_monitor.py:18` — function `get_national_performance()` still uses "national" in its name.
- **GAP:** `services/treasury_allocation_engine.py` — 18 internal variable references using "national" prefix: `national_amount` (lines 49, 51, 53, 69, 118), `national_treasury` (lines 58, 61, 64, 98, 99, 100, 101, 102, 103, 114), `national_txn`/`national_txn_id` (lines 61, 64, 98, 99, 100, 114).

### Wave 5 (Authority Model) — PASS
- `KINGDOM_TERMINOLOGY_STANDARD.md` §1 documents REH, RAK, HCK, KAO with full hierarchy and authority mapping (lines 9–41).

### Wave 6 (Archive) — PASS
- `archive/KINGDOM_TERMINOLOGY_LEGACY_MAP.md` exists with 113 lines mapping all old→new names across registries, services, tests, reports, knowledge docs, audit files, data files, and schemas.

## 3. Remaining national_ References

### In Active Code (services/)
| File | Line | Reference | Type |
|------|------|-----------|------|
| `services/treasury_allocation_engine.py` | 49, 51, 53, 69, 118 | `national_amount` | Variable name |
| `services/treasury_allocation_engine.py` | 58, 61, 64, 98, 99, 100, 101, 102, 103, 114 | `national_treasury` | Variable name |
| `services/treasury_allocation_engine.py` | 61, 64, 98 | `national_txn_id` / `national_txn` | Variable name |
| `services/kingdom_planning_engine.py` | 26 | `create_national_plan` | Function name |
| `services/kingdom_performance_monitor.py` | 18 | `get_national_performance` | Function name |
| **Subtotal (code):** | | **23 references in 3 files** | |

### In Active Registries (docs/registries/)
| File | Line | Reference | Type |
|------|------|-----------|------|
| `TREASURY_TRANSACTION_REGISTRY.yaml` | 21 | `national_expense_schema` | Schema reference |
| `TREASURY_TRANSACTION_REGISTRY.yaml` | 25 | `national_revenue_schema` | Schema reference |
| `TREASURY_ACCOUNT_REGISTRY.yaml` | 18 | `data/treasury/national_treasury.json` | Data file path |
| `TREASURY_ACCOUNT_REGISTRY.yaml` | 36 | `data/treasury/national_fund.json` | Data file path |
| `TREASURY_ACCOUNT_REGISTRY.yaml` | 63 | `data/treasury/national_budget.json` | Data file path |
| **Subtotal (registries):** | | **5 references in 2 files** | |

### In Archived/Reference Docs (no action needed)
Remaining `national_` references in `docs/proposals/KINGDOM_TERMINOLOGY_MIGRATION_PLAN.md`, `docs/standards/KINGDOM_TERMINOLOGY_STANDARD.md`, `docs/reports/TERMINOLOGY_IMPACT_ANALYSIS.md`, `docs/reports/TERMINOLOGY_INVENTORY.md`, `docs/reports/KTSP_REVIEWER_LOOP_REPORT.md`, `docs/reports/AK_LEGACY_KNOWLEDGE_TRACEABILITY_MAP.md`, and `archive/KINGDOM_TERMINOLOGY_LEGACY_MAP.md` are expected (these are planning/archive documents referencing old names by design).

### Total Active: 28 references in 5 files

## 4. Legacy Map Assessment

`archive/KINGDOM_TERMINOLOGY_LEGACY_MAP.md` is comprehensive and accurate:
- Covers all registry, service, test, report, knowledge, audit, data, and schema renames.
- Correctly identifies 2 unchanged legacy files (archived DRAFT .docx files).
- Documents 12 key text replacements with affected file counts.
- **Minor omission:** Does not explicitly list internal function renames (`create_national_plan` → `create_kingdom_plan`, `get_national_performance` → `get_kingdom_performance`) or the `treasury_allocation_engine.py` variable renames — but these are internal code changes, not file-level renames.

## 5. Naming Standard Compliance

All renamed entities follow `KINGDOM_TERMINOLOGY_STANDARD.md`:
- ✅ Service files: `kingdom_*` prefix
- ✅ Registry YAML files: `KINGDOM_*` prefix
- ✅ Registry wrapper keys: `kingdom_*_registry`
- ✅ Report/template files: `KINGDOM_*` prefix
- ✅ Data files: `kingdom_*` prefix
- ✅ Schema files: `kingdom_*` prefix
- ✅ Memory module: `kingdom_memory_platform.py`
- ✅ Authority model: REH/RAK/HCK/KAO documented
- ❌ Function names in code still use `national_` (non-compliant with standard §7 text replacement map)
- ❌ Internal variable names in `treasury_allocation_engine.py` still use `national_` (non-compliant)
- ❌ Registry YAML content references still use `national_` (non-compliant with standard §3 registry rename map)

## 6. Certification

| Category | Verdict |
|----------|---------|
| CERTIFIED | 0 remaining `national_` references in active code/docs |
| CONDITIONAL | Non-critical remnants in archived/legacy docs only |
| **NOT_CERTIFIED** | **Active references remain** — 28 instances across 5 files |

## 7. Verdict

**NOT_CERTIFIED.** While the file-level rename campaign (Waves 1–4) was successfully executed — all service, registry, test, report, data, and schema files now use `kingdom_`/`KINGDOM_` prefixes — there are 28 remaining `national_` references in active code and registry content:

1. **3 service files** have 23 internal references (function names, variable names) still using `national_` — these are in `treasury_allocation_engine.py`, `kingdom_planning_engine.py`, and `kingdom_performance_monitor.py`.
2. **2 registry YAML files** have 5 references to `national_*` schema names and data file paths that no longer exist under those names — `TREASURY_TRANSACTION_REGISTRY.yaml` and `TREASURY_ACCOUNT_REGISTRY.yaml`.

**Recommended Remediation:**
- Rename `create_national_plan` → `create_kingdom_plan` in `kingdom_planning_engine.py`
- Rename `get_national_performance` → `get_kingdom_performance` in `kingdom_performance_monitor.py`
- Rename all `national_*` variables → `kingdom_*` in `treasury_allocation_engine.py` (18 changes)
- Update schema references in `TREASURY_TRANSACTION_REGISTRY.yaml` (`national_` → `kingdom_`)
- Update data file paths in `TREASURY_ACCOUNT_REGISTRY.yaml` (`national_` → `kingdom_`)

After remediation, re-run grep verification. If 0 matches remain in `services/` and `docs/registries/`, certify as COMPLETE.
