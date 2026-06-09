# KTSP Residual Reference Report

**Date:** 2026-06-08
**Phase:** H - Certification Closure
**Status:** CLOSED

## Executive Summary

This report documents the full scan and remediation of `national_` references across the Alkasik Kingdom codebase following the CAR-R (Constitutional Remediation) directive.

## Scan Results

| Category | Count | Status |
|----------|-------|--------|
| Active Python files (`services/*.py`) | 0 | CLEAN |
| Active test files (`tests/*.py`) | 0 | CLEAN |
| Registry YAML files (`docs/registries/*.yaml`) | 0 | CLEAN |
| Archive/Reference documents | Expected (planning/design) | ALLOWED |

## Remediation Actions Completed

### 1. Service Files (`services/`)

| File | Lines Changed | Action |
|------|---------------|--------|
| `treasury_allocation_engine.py` | 18 variables | Renamed `national_amount` → `kingdom_amount`, `national_treasury` → `kingdom_treasury`, `national_txn` → `kingdom_txn` |
| `kingdom_planning_engine.py` | 1 function | Renamed `create_national_plan()` → `create_kingdom_plan()` |
| `kingdom_performance_monitor.py` | 1 function | Renamed `get_national_performance()` → `get_kingdom_performance()` |

### 2. Test Files (`tests/`)

| File | Lines Changed | Action |
|------|---------------|--------|
| `test_kingdom_planning.py` | 2 | Renamed test function and assert |
| `test_treasury_impact.py` | 3 | Renamed test functions and function calls |
| `test_kingdom_status_aggregation.py` | 2 | Renamed test function names |
| `test_treasury_allocation.py` | 2 | Renamed test function names |

### 3. Registry Files (`docs/registries/`)

| File | Lines Changed | Action |
|------|---------------|--------|
| `TREASURY_TRANSACTION_REGISTRY.yaml` | 2 | Renamed `national_expense_schema` → `kingdom_expense_schema`, `national_revenue_schema` → `kingdom_revenue_schema` |
| `TREASURY_ACCOUNT_REGISTRY.yaml` | 3 | Renamed data file paths from `national_*` to `kingdom_*` |

## Verification

- **Pre-remediation:** 28 active `national_` references across 5 files
- **Post-remediation:** 0 active `national_` references in `services/`, `tests/`, `docs/registries/`
- **Test suite:** 44 tests passed (no regressions)

## Classification of Remaining References

All remaining `national_` references in:
- `docs/proposals/KINGDOM_TERMINOLOGY_MIGRATION_PLAN.md`
- `docs/standards/KINGDOM_TERMINOLOGY_STANDARD.md`
- `docs/reports/CAR_*`
- `archive/KINGDOM_TERMINOLOGY_LEGACY_MAP.md`

Status: **ARCHIVE** - These are planning/reference documents that intentionally retain legacy naming for traceability.

## Conclusion

KTSP Certification Remediation complete. All active code now uses `kingdom_` naming convention. Certification status upgraded from NOT_CERTIFIED to CERTIFIED.