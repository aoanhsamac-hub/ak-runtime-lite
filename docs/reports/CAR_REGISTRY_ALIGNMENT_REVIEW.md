# CAR: Registry Alignment Review

**Date:** 2026-06-08
**Phase:** F
**Status:** GAPS_FOUND

## 1. Registries Found

17 YAML registry files found under `docs/registries/`:

| # | Path | Status |
|---|------|--------|
| 1 | `docs/registries/TREASURY_HEALTH_REGISTRY.yaml` | Populated |
| 2 | `docs/registries/PROGRAM_EVIDENCE_REGISTRY.yaml` | Populated |
| 3 | `docs/registries/TRADING_EVIDENCE_REGISTRY.yaml` | Populated |
| 4 | `docs/registries/TREASURY_EVIDENCE_REGISTRY.yaml` | Populated |
| 5 | `docs/registries/TREASURY_IMPACT_REGISTRY.yaml` | Populated |
| 6 | `docs/registries/CAPABILITY_ROI_REGISTRY.yaml` | Populated |
| 7 | `docs/registries/CAPABILITY_VALUE_REGISTRY.yaml` | Populated |
| 8 | `docs/registries/CAPABILITY_USAGE_REGISTRY.yaml` | Populated |
| 9 | `docs/registries/KINGDOM_HEALTH_REGISTRY.yaml` | Populated |
| 10 | `docs/registries/KINGDOM_STATUS_REGISTRY.yaml` | Populated |
| 11 | `docs/registries/KINGDOM_GOAL_REGISTRY.yaml` | Populated |
| 12 | `docs/registries/KINGDOM_PROGRAM_REGISTRY.yaml` | Populated |
| 13 | `docs/registries/TREASURY_TRANSACTION_REGISTRY.yaml` | Empty/INITIALIZED |
| 14 | `docs/registries/TREASURY_STATUS_REGISTRY.yaml` | Empty/INITIALIZED |
| 15 | `docs/registries/TREASURY_ACCOUNT_REGISTRY.yaml` | Default structure |
| 16 | `docs/registries/TREASURY_TRANSACTION_STATUS_REGISTRY.yaml` | Empty/ACTIVE |
| 17 | `docs/registries/TREASURY_REPORT_REGISTRY.yaml` | Empty/INITIALIZED |

## 2. Registry Completeness

### PSOP-01A (Treasury)

| Required Registry | Found | Status |
|---|---|---|
| TREASURY_HEALTH_REGISTRY.yaml | Yes | Populated |
| TREASURY_TRANSACTION_REGISTRY.yaml | Yes | Empty — 0 transactions |
| TREASURY_STATUS_REGISTRY.yaml | Yes | Empty — null balances |
| TREASURY_ACCOUNT_REGISTRY.yaml | Yes | Default structure |
| TREASURY_TRANSACTION_STATUS_REGISTRY.yaml | Yes | Empty — 0 transactions |
| TREASURY_REPORT_REGISTRY.yaml | Yes | Empty — 0 reports |

**Verdict:** All registries exist. Transaction/status/report registries lack real data.

### PSOP-02 (Situation Room)

| Required Registry | Found | Status |
|---|---|---|
| KINGDOM_HEALTH_REGISTRY.yaml | Yes | 8 domains, all HEALTHY, score 100 |
| KINGDOM_STATUS_REGISTRY.yaml | Yes | 8 domains, overall WATCH (datasets/knowledge flagged) |

**Verdict:** Complete.

### PSOP-03 (Planning / CE)

| Required Registry | Found | Status |
|---|---|---|
| KINGDOM_GOAL_REGISTRY.yaml | Yes | 77 goals (test data) |
| KINGDOM_PROGRAM_REGISTRY.yaml | Yes | 44 programs (test data) |
| TREASURY_IMPACT_REGISTRY.yaml | Yes | Program + capability impacts (test data) |

**Verdict:** All exist, but data is synthetic/test.

### PSOP-04 (Evidence)

| Required Registry | Found | Status |
|---|---|---|
| CAPABILITY_USAGE_REGISTRY.yaml | Yes | 7 records (test_agent/test_cap) |
| CAPABILITY_VALUE_REGISTRY.yaml | Yes | 7 records (all $0 values) |
| CAPABILITY_ROI_REGISTRY.yaml | Yes | 14 records (test_cap, zero_cost) |
| TREASURY_EVIDENCE_REGISTRY.yaml | Yes | 28 records (test data) |
| TRADING_EVIDENCE_REGISTRY.yaml | Yes | 70 records (all INITIALIZED) |
| PROGRAM_EVIDENCE_REGISTRY.yaml | Yes | 21 records (synthetic snapshots) |

**Verdict:** All exist. Data is synthetic/initialized across all evidence registries.

## 3. Schema Alignment

| Registry | Wrapper Key | Required Fields | Data Types | Verdict |
|---|---|---|---|---|
| TREASURY_HEALTH_REGISTRY.yaml | `treasury_health_registry:` | created_at, status, health_categories, status_levels | Strings, numbers, timestamps | OK |
| PROGRAM_EVIDENCE_REGISTRY.yaml | `program_evidence_registry:` | created_at, evidence_records, metadata | Strings, numbers, timestamps | OK |
| TRADING_EVIDENCE_REGISTRY.yaml | `trading_evidence_registry:` | created_at, evidence_records, metadata | Strings, numbers, timestamps | OK |
| TREASURY_EVIDENCE_REGISTRY.yaml | `treasury_evidence_registry:` | created_at, evidence_records, metadata | Strings, numbers, timestamps | OK |
| TREASURY_IMPACT_REGISTRY.yaml | `treasury_impact_registry:` | capability_impacts, program_impacts, metadata | Strings, numbers, timestamps | OK |
| CAPABILITY_ROI_REGISTRY.yaml | `capability_roi_registry:` | created_at, evidence_records, metadata | Strings, numbers, timestamps | OK |
| CAPABILITY_VALUE_REGISTRY.yaml | `capability_value_registry:` | created_at, evidence_records, metadata | Strings, numbers, timestamps | OK |
| CAPABILITY_USAGE_REGISTRY.yaml | `capability_usage_registry:` | created_at, evidence_records, metadata | Strings, numbers, timestamps | OK |
| KINGDOM_HEALTH_REGISTRY.yaml | `kingdom_health_registry:` | created_at, health_domains (8), status_levels, metadata | Strings, numbers, timestamps | OK |
| KINGDOM_STATUS_REGISTRY.yaml | `kingdom_status_registry:` | created_at, domains (8), metadata | Strings, numbers, timestamps | OK |
| KINGDOM_GOAL_REGISTRY.yaml | `kingdom_goal_registry:` | created_at, goals, goal_lifecycle, metadata | Strings, numbers, timestamps | OK |
| KINGDOM_PROGRAM_REGISTRY.yaml | `kingdom_program_registry:` | created_at, programs, program_lifecycle, metadata | Strings, numbers, timestamps | OK |
| TREASURY_TRANSACTION_REGISTRY.yaml | `treasury_transaction_registry:` | status, transaction_types, metadata | Strings, numbers, null | OK (empty) |
| TREASURY_STATUS_REGISTRY.yaml | `treasury_status_registry:` | status, accounts, metadata | Strings, null | OK (empty) |
| TREASURY_ACCOUNT_REGISTRY.yaml | `treasury_account_registry:` | status, accounts, metadata | Strings, numbers, null | OK (default) |
| TREASURY_TRANSACTION_STATUS_REGISTRY.yaml | `treasury_transaction_status_registry:` | status, transaction_lifecycle, metadata | Strings, null | OK (empty) |
| TREASURY_REPORT_REGISTRY.yaml | `treasury_report_registry:` | status, report_types, metadata | Strings, null | OK (empty) |

**All schemas are structurally valid.** No missing required fields, correct data types.

## 4. Data Population Status

| Registry | Data Quality | Assessment |
|---|---|---|
| TREASURY_HEALTH_REGISTRY.yaml | Real scores (100), HEALTHY status | Acceptable |
| KINGDOM_HEALTH_REGISTRY.yaml | Real scores (100), HEALTHY status | Acceptable |
| KINGDOM_STATUS_REGISTRY.yaml | Real statuses, WATCH overall | Acceptable |
| KINGDOM_GOAL_REGISTRY.yaml | 77 goals — all test data ("Test Goal", "Get Test", etc.) | Synthetic only |
| KINGDOM_PROGRAM_REGISTRY.yaml | 44 programs — all test data ("Test Program", etc.) | Synthetic only |
| TREASURY_IMPACT_REGISTRY.yaml | Program/capability impacts — test data (500.0, 1000.0) | Synthetic only |
| TREASURY_EVIDENCE_REGISTRY.yaml | 28 records — test data ("test", "test" sources) | Synthetic only |
| TRADING_EVIDENCE_REGISTRY.yaml | 70 records — all INITIALIZED, no real trades | Empty/Initialized |
| CAPABILITY_USAGE_REGISTRY.yaml | 7 records — test_agent/test_cap | Synthetic only |
| CAPABILITY_VALUE_REGISTRY.yaml | 7 records — all $0 values | Empty/Initialized |
| CAPABILITY_ROI_REGISTRY.yaml | 14 records — test_cap/zero_cost | Synthetic only |
| PROGRAM_EVIDENCE_REGISTRY.yaml | 21 records — synthetic snapshots | Synthetic only |
| TREASURY_TRANSACTION_REGISTRY.yaml | 0 transactions | Empty |
| TREASURY_STATUS_REGISTRY.yaml | All balances null | Empty |
| TREASURY_ACCOUNT_REGISTRY.yaml | Accounts defined, no transaction data | Default structure |
| TREASURY_TRANSACTION_STATUS_REGISTRY.yaml | Lifecycle defined, 0 transactions | Empty |
| TREASURY_REPORT_REGISTRY.yaml | 0 reports generated | Empty |

## 5. KTSP Compliance

All 17 registry file names are KTSP-compliant (no `national_` prefix in filenames).

### Violations Found

| File | Line | Issue | Severity |
|---|---|---|---|
| `TREASURY_ACCOUNT_REGISTRY.yaml` | L18 | `data_file: data/treasury/national_treasury.json` | MEDIUM |
| `TREASURY_ACCOUNT_REGISTRY.yaml` | L36 | `data_file: data/treasury/national_fund.json` | MEDIUM |
| `TREASURY_ACCOUNT_REGISTRY.yaml` | L63 | `data_file: data/treasury/national_budget.json` | MEDIUM |
| `TREASURY_ACCOUNT_REGISTRY.yaml` | L11 | `account_id: NAT-001` ("National" remnant) | LOW |
| `TREASURY_ACCOUNT_REGISTRY.yaml` | L29 | `account_id: NFD-001` ("National Fund" remnant) | LOW |
| `TREASURY_TRANSACTION_REGISTRY.yaml` | L21 | `schema: national_expense_schema` | MEDIUM |
| `TREASURY_TRANSACTION_REGISTRY.yaml` | L25 | `schema: national_revenue_schema` | MEDIUM |

### Compliant Registries (10/17)
All `KINGDOM_*` registries, `CAPABILITY_*` registries, `TREASURY_*` evidence/health/impact/report/status/transaction_status registries — no violations.

## 6. Gaps Identified

### Gap 1 — KTSP Naming Violations (7 instances)
**Severity:** MEDIUM
**Files:** `TREASURY_ACCOUNT_REGISTRY.yaml`, `TREASURY_TRANSACTION_REGISTRY.yaml`
**Details:** Three `data_file` paths, two `schema` references, and two `account_id` values still use `national_` prefix. These must be migrated to `kingdom_` per the KTSP rename map.

### Gap 2 — Empty Treasury Registries (4 registries)
**Severity:** HIGH
**Files:** `TREASURY_TRANSACTION_REGISTRY.yaml`, `TREASURY_STATUS_REGISTRY.yaml`, `TREASURY_TRANSACTION_STATUS_REGISTRY.yaml`, `TREASURY_REPORT_REGISTRY.yaml`
**Details:** These registries contain structural definitions only — no transactions, no balances, no reports. They are stuck at `INITIALIZED` status with `null` values.

### Gap 3 — Synthetic/Test Data Only (700+ records across 10 registries)
**Severity:** HIGH
**Files:** `KINGDOM_GOAL_REGISTRY.yaml`, `KINGDOM_PROGRAM_REGISTRY.yaml`, `TREASURY_IMPACT_REGISTRY.yaml`, `TREASURY_EVIDENCE_REGISTRY.yaml`, `TRADING_EVIDENCE_REGISTRY.yaml`, `CAPABILITY_USAGE_REGISTRY.yaml`, `CAPABILITY_VALUE_REGISTRY.yaml`, `CAPABILITY_ROI_REGISTRY.yaml`, `PROGRAM_EVIDENCE_REGISTRY.yaml`
**Details:** All populated registries contain only test/synthetic data (`Test Goal`, `test_capability`, `test_agent`, `Test Program`). No real production data exists in any registry.

### Gap 4 — TREASURY_IMPACT_REGISTRY Status
**Severity:** LOW
**Detail:** `status: INITIALIZED` despite having populated records. This is inconsistent — registries with data should be `ACTIVE`.

### Gap 5 — Null `updated_at` Fields
**Severity:** LOW
**Files:** `TREASURY_HEALTH_REGISTRY.yaml`, `TREASURY_TRANSACTION_REGISTRY.yaml`, `TREASURY_STATUS_REGISTRY.yaml`, `TREASURY_ACCOUNT_REGISTRY.yaml`, `TREASURY_TRANSACTION_STATUS_REGISTRY.yaml`, `TREASURY_REPORT_REGISTRY.yaml`, `KINGDOM_HEALTH_REGISTRY.yaml`, `KINGDOM_STATUS_REGISTRY.yaml`
**Details:** Several registries have `updated_at: null` despite having a `created_at` timestamp. This indicates incomplete update tracking.

## 7. Verdict

**STATUS: GAPS_FOUND**

The registry layer is structurally sound — all 17 required YAML files exist, all schemas are valid, and all PSOP phase registries are accounted for. The KTSP rename has been mostly applied (all filenames are compliant).

However, three critical gaps prevent a COMPLETE rating:

1. **KTSP Naming Violations** — 7 instances of `national_` remnants in `data_file` paths, schema references, and account IDs in treasury registries.

2. **Empty Treasury Core Registries** — The treasury transaction, status, transaction-status, and report registries contain structure only with no operational data.

3. **Synthetic Data Only** — Every populated registry uses test/synthetic data (`test_capability`, `test_agent`, `Test Goal`, `Test Program`). No registry contains real production data.

**Recommendation:** Resolve KTSP naming violations (Gap 1) immediately as they are quick text replacements. Populate treasury core registries with real transaction data (Gap 2) and migrate from synthetic test data to real production data (Gap 3) before the next audit cycle.
