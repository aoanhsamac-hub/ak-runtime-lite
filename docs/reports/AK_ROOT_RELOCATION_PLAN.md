# AK Root Relocation Plan

Directive: WP-REPO-HYGIENE-01 | Date: 2026-06-08

## Relocation Actions

### Action Group A: Scripts (Low Risk)

| # | Source | Destination | Reason | Legal Basis | Import Impact | Rollback |
|---|---|---|---|---|---|---|
| A1 | ak.bat | scripts/ak.bat | Scripts must be in scripts/ | Repo Governance Decree | None | Copy back |
| A2 | law.bat | scripts/law.bat | Scripts must be in scripts/ | Repo Governance Decree | None | Copy back |

### Action Group B: Tools (Low Risk)

| # | Source | Destination | Reason | Legal Basis | Import Impact | Rollback |
|---|---|---|---|---|---|---|
| B1 | akctl.py | tools/akctl.py | CLI tool belongs in tools/ | Agent Law, Repo Governance | None (self-referencing help text) | Copy back |

### Action Group C: Reports (Medium Risk)

| # | Source | Destination | Reason | Legal Basis | Import Impact | Rollback |
|---|---|---|---|---|---|---|
| C1 | AK_MEMORY.md | docs/reports/AK_MEMORY.md | Memory record is a report | Memory Law, Knowledge Governance | AK_MEMORY.md is not imported by code. Human references only. | Copy back |
| C2 | ARCHIVE_RECOMMENDATIONS.md | docs/reports/ARCHIVE_RECOMMENDATIONS.md | WP35.4A deliverable | Knowledge Governance | None | Copy back |
| C3 | DUPLICATE_ANALYSIS.md | docs/reports/DUPLICATE_ANALYSIS.md | WP35.4A deliverable | Knowledge Governance | None | Copy back |
| C4 | FINAL_CONSOLIDATION_REPORT.md | docs/reports/FINAL_CONSOLIDATION_REPORT.md | WP35.4A deliverable | Knowledge Governance | None | Copy back |
| C5 | KNOWLEDGE_CONSOLIDATION_PLAN.md | docs/reports/KNOWLEDGE_CONSOLIDATION_PLAN.md | WP35.4A deliverable | Knowledge Governance | None | Copy back |
| C6 | MERGE_RECOMMENDATIONS.md | docs/reports/MERGE_RECOMMENDATIONS.md | WP35.4A deliverable | Knowledge Governance | None | Copy back |
| C7 | REPOSITORY_DEPENDENCY_MAP.md | docs/reports/REPOSITORY_DEPENDENCY_MAP.md | WP35.4A deliverable | Knowledge Governance | None | Copy back |
| C8 | REPOSITORY_HEALTH_SCORE.md | docs/reports/REPOSITORY_HEALTH_SCORE.md | WP35.4A deliverable | Knowledge Governance | None | Copy back |
| C9 | REPOSITORY_INVENTORY.md | docs/reports/REPOSITORY_INVENTORY.md | WP35.4A deliverable | Knowledge Governance | None | Copy back |
| C10 | UPDATED_REGISTRY_STRUCTURE.md | docs/reports/UPDATED_REGISTRY_STRUCTURE.md | WP35.4A deliverable | Knowledge Governance | None | Copy back |

### Action Group D: Connector Relocation (Low Risk)

| # | Source | Destination | Reason | Legal Basis | Import Impact | Rollback |
|---|---|---|---|---|---|---|
| D1 | infrastructure/yet_kieu/mt5_health_monitor.py | connectors/mt5/health_monitor.py | MT5 monitoring code belongs with connector | Repo Governance | None (no imports of infrastructure/) | Copy back |

### Action Group E: Service Relocation (HIGH Risk - import updates needed)

| # | Source | Destination | Reason | Legal Basis | Import Impact | Rollback |
|---|---|---|---|---|---|---|
| E1 | intelligence/iris/*.py | services/iris/*.py | Intelligence service belongs in services/ | Repo Governance | **3 files import from intelligence.iris** | Copy back + revert imports |

**Import Impact Details for E1:**
- scripts/run_market_sandbox_scan.py (lines 12-13): `from intelligence.iris.market_snapshot` and `from intelligence.iris.zone_detector`
- scripts/run_market_validation_cycle.py (line 10): `from intelligence.iris.zone_validation_engine`
- tests/test_zone_validation_engine.py (line 3): `from intelligence.iris.zone_validation_engine`

**Required Updates:** Change `from intelligence.iris` → `from services.iris` in 3 files.

### Action Group F: Dashboard Relocation (Low Risk)

| # | Source | Destination | Reason | Legal Basis | Import Impact | Rollback |
|---|---|---|---|---|---|---|
| F1 | interface/dashboard/ | tools/dashboard/ | Dashboard is a tool | Repo Governance | None (no imports of interface/) | Copy back |

### Action Group G: Archive (Low Risk)

| # | Source | Destination | Reason | Legal Basis | Import Impact | Rollback |
|---|---|---|---|---|---|---|
| G1 | _pytest_tmp/ | archive/root_hygiene/20260608_120000/ | Temporary test artifacts | Retention Governance | None | Copy back |
| G2 | audit_output/ | archive/root_hygiene/20260608_120000/ | Empty temp dir | Retention Governance | None | Copy back |
| G3 | backups/ | archive/root_hygiene/20260608_120000/ | Empty dir | Retention Governance | None | Copy back |
| G4 | logs/ | archive/root_hygiene/20260608_120000/ | Empty dir | Retention Governance | None | Copy back |
| G5 | test.txt | archive/root_hygiene/20260608_120000/ | Temporary file | Retention Governance | None | Copy back |

## Summary

| Group | Action | Items | Risk | Requires Sage |
|---|---|---|---|---|
| A | Move scripts | 2 | LOW | No |
| B | Move tools | 1 | LOW | No |
| C | Move reports | 10 | MEDIUM | For AK_MEMORY.md |
| D | Move connector | 1 | LOW | No |
| E | Move service | 1 dir | **HIGH** | Yes (imports) |
| F | Move dashboard | 1 dir | LOW | No |
| G | Archive | 5 items | LOW | No |

## Execution Order

1. Groups A, B (scripts/tools) — lowest risk
2. Group D (connector) — no imports
3. Group F (dashboard) — no imports
4. Group C (reports) — after AK_MEMORY.md cleared
5. Group G (archive) — temporary items
6. Group E (service) — LAST, requires import updates + testing

## Stop Conditions

- **STOP if**: intelligence/ import update breaks any file
- **STOP if**: AK_MEMORY.md is referenced by any automated process
- **STOP if**: Any file contains secrets/credentials
- **STOP if**: Sage approval not obtained for intelligence/ or AK_MEMORY.md
