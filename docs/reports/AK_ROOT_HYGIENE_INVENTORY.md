# AK Root Hygiene Inventory

Directive: WP-REPO-HYGIENE-01 | Date: 2026-06-08
Authority: Janus Directive | Classification: REPOSITORY GOVERNANCE

## Root Directory Scan

### Approved Directories (allowed by Repo Governance)
| Directory | Type | Status |
|---|---|---|
| agents/ | dir | ALLOWED |
| archive/ | dir | ALLOWED |
| connectors/ | dir | ALLOWED |
| data/ | dir | ALLOWED |
| docs/ | dir | ALLOWED |
| execution/ | dir | ALLOWED |
| governance/ | dir | ALLOWED |
| learning/ | dir | ALLOWED |
| memory/ | dir | ALLOWED |
| pipelines/ | dir | ALLOWED |
| scripts/ | dir | ALLOWED |
| services/ | dir | ALLOWED |
| sovereign/ | dir | ALLOWED |
| tests/ | dir | ALLOWED |
| tools/ | dir | ALLOWED |
| workflows/ | dir | ALLOWED |

### Unapproved Directories
| Path | Type | Size | Modified | Owner | Category | Proposed Destination | Risk |
|---|---|---|---|---|---|---|---|
| .pytest_cache/ | dir (hidden) | ~50KB | 2026-06-07 | pytest | TEMPORARY | Keep (cache) | LOW |
| .venv/ | dir (hidden) | ~200MB | 2026-06-07 | pip | RUNTIME | Keep (virtualenv) | LOW |
| _pytest_tmp/ | dir | ~500KB | 2026-06-07 | tests | TEMPORARY | archive/root_hygiene/ | LOW |
| audit_output/ | dir (empty) | 0 | 2026-06-08 | OpenCode | TEMPORARY | archive/root_hygiene/ | LOW |
| backups/ | dir (empty) | 0 | 2026-06-06 | Unknown | ARCHIVE | archive/ | LOW |
| infrastructure/ | dir | ~1KB | 2026-06-08 | Yet Kieu | SERVICE | connectors/mt5/ | LOW |
| intelligence/ | dir | ~5KB | 2026-06-08 | Iris | SERVICE | services/iris/ | **HIGH** (imports exist) |
| interface/ | dir | ~10KB | 2026-06-06 | Unknown | TOOL | tools/dashboard/ | LOW |
| logs/ | dir (empty) | 0 | 2026-06-06 | Unknown | ARCHIVE | archive/ | LOW |

### Approved Files (already in approved list)
| File | Type | Size | Status |
|---|---|---|---|
| .gitignore | config | 81 | ALLOWED |
| pyproject.toml | config | 188 | ALLOWED |
| README.md | doc | 337 | ALLOWED |
| requirements.txt | config | 69 | ALLOWED |

### Unapproved Files
| File | Type | Size | Modified | Owner | Category | Destination | Risk |
|---|---|---|---|---|---|---|---|
| .env.example | config | 515 | 2026-06-07 | Unknown | CONFIG | Keep or connectors/ | LOW |
| ak.bat | script | 60 | 2026-06-07 | OpenCode | SCRIPT | scripts/ | LOW |
| akctl.py | script | 3598 | 2026-06-07 | Janus | TOOL | tools/ | LOW |
| AK_MEMORY.md | report | 43073 | 2026-06-08 | Lang Lieu | REPORT | docs/reports/ | **MEDIUM** (referenced) |
| ARCHIVE_RECOMMENDATIONS.md | report | 6264 | 2026-06-08 | WP35.4A | REPORT | docs/reports/ | LOW |
| DUPLICATE_ANALYSIS.md | report | 7768 | 2026-06-08 | WP35.4A | REPORT | docs/reports/ | LOW |
| FINAL_CONSOLIDATION_REPORT.md | report | 4842 | 2026-06-08 | WP35.4A | REPORT | docs/reports/ | LOW |
| KNOWLEDGE_CONSOLIDATION_PLAN.md | report | 5545 | 2026-06-08 | WP35.4A | REPORT | docs/reports/ | LOW |
| law.bat | script | 791 | 2026-06-07 | OpenCode | SCRIPT | scripts/ | LOW |
| MERGE_RECOMMENDATIONS.md | report | 3212 | 2026-06-08 | WP35.4A | REPORT | docs/reports/ | LOW |
| REPOSITORY_DEPENDENCY_MAP.md | report | 3388 | 2026-06-08 | WP35.4A | REPORT | docs/reports/ | LOW |
| REPOSITORY_HEALTH_SCORE.md | report | 3828 | 2026-06-08 | WP35.4A | REPORT | docs/reports/ | LOW |
| REPOSITORY_INVENTORY.md | report | 9328 | 2026-06-08 | WP35.4A | REPORT | docs/reports/ | LOW |
| test.txt | temp | 14 | 2026-06-08 | OpenCode | TEMPORARY | archive/root_hygiene/ | LOW |
| UPDATED_REGISTRY_STRUCTURE.md | report | 3940 | 2026-06-08 | WP35.4A | REPORT | docs/reports/ | LOW |

## Summary

| Category | Count |
|---|---|
| Approved directories | 16 |
| Unapproved directories | 9 (3 hidden, 1 empty) |
| Approved files | 4 |
| Unapproved files | 16 |
| Files requiring import updates | intelligence/ (4 import references) |
| Empty directories | 3 (audit_output/, backups/, logs/) |
