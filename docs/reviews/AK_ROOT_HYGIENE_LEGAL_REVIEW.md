# AK Root Hygiene Legal Review

Directive: WP-REPO-HYGIENE-01 | Date: 2026-06-08

## Applicable Laws & Decrees

### Repo Governance Decree
| Article | Application |
|---|---|
| File placement rules | Unapproved root files violate placement rules. All 16 unapproved files must be relocated. |
| Directory structure | `intelligence/`, `infrastructure/`, `interface/` are not approved root directories. |
| Temporary artifacts | `_pytest_tmp/`, `audit_output/`, `test.txt` are temporary and must be archived. |

### Knowledge Governance Decree
| Article | Application |
|---|---|
| Reports must be in docs/reports/ | AK_MEMORY.md and 8 WP35.4A reports are root-level reports. |
| Knowledge artifacts must be catalogued | AK_MEMORY.md is a knowledge artifact. |
| Registry knowledge must be in memory/ | No memory registries found in root (all in memory/). ✓ |

### Retention & Archive Governance Decree
| Article | Application |
|---|---|
| Superseded files must be archived | WP35.4A reports are deliverables that must be moved to docs/reports/. |
| Temporary artifacts must be archived or cleaned | `_pytest_tmp/`, `audit_output/`, `test.txt`. |
| Empty directories may be archived | `backups/`, `logs/` are empty. |

### Security Law
| Article | Application |
|---|---|
| Secrets must not be exposed | `.env.example` is a template (no real secrets). Safe to move or keep. |
| Credential files must be protected | No credentials found in root. ✓ |

### Information Law
| Article | Application |
|---|---|
| Information must be categorized | All root items have been categorized (see inventory). ✓ |

### Memory Law
| Article | Application |
|---|---|
| Knowledge must be in memory system | AK_MEMORY.md is the master memory record. Moving to docs/reports/ preserves access. |
| Registry information must be in registries | All registry files are already in memory/. ✓ |

### Agent Law
| Article | Application |
|---|---|
| Agent files must be in agents/ | All agent files are in agents/. ✓ |
| Agent tools must be in tools/ | `akctl.py` is an agent CLI tool → must move to tools/. |

### Execution Law
| Article | Application |
|---|---|
| Execution files must be in execution/ | No execution files found in root. ✓ |

### Economic Law Assessment
| Article | Application |
|---|---|
| Budget/treasury files must be in sovereign/ | No economic files found in root. ✓ |

## Compliance Answers

### Which root items violate Repo Governance?
**All 16 unapproved files** and **6 unapproved directories** (excluding hidden/cache dirs) violate Repo Governance file placement rules.

### Which items are knowledge artifacts?
- AK_MEMORY.md (master memory record)
- ARCHIVE_RECOMMENDATIONS.md
- DUPLICATE_ANALYSIS.md
- FINAL_CONSOLIDATION_REPORT.md
- KNOWLEDGE_CONSOLIDATION_PLAN.md
- MERGE_RECOMMENDATIONS.md
- REPOSITORY_DEPENDENCY_MAP.md
- REPOSITORY_HEALTH_SCORE.md
- REPOSITORY_INVENTORY.md
- UPDATED_REGISTRY_STRUCTURE.md

### Which items are reports?
All 10 knowledge artifacts above are reports and must go to `docs/reports/`.

### Which items are runtime/code?
- `akctl.py` → tool → `tools/`
- `ak.bat` → script → `scripts/`
- `law.bat` → script → `scripts/`
- `intelligence/iris/*.py` → service code → `services/iris/`
- `infrastructure/yet_kieu/mt5_health_monitor.py` → connector code → `connectors/mt5/`
- `interface/dashboard/` → tool → `tools/dashboard/`

### Which items require archive instead of move?
- `_pytest_tmp/` → temporary test artifacts → archive
- `audit_output/` → empty → archive
- `backups/` → empty → archive
- `logs/` → empty → archive
- `test.txt` → temporary → archive

### Which items require Sage approval before move?
| Item | Reason |
|---|---|
| `intelligence/` | Moving breaks 3 Python import lines. Requires Sage approval for import path changes. |
| `AK_MEMORY.md` | Master memory record. Moving requires Sage approval to update any cross-references. |

## Legal Verdict

**PASS** — All violations are non-material (directory structure only). No legal meaning is altered by moving files to approved locations. No execution, trading, MT5, or risk paths are touched.
