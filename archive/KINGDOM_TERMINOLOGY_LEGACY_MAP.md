# Kingdom Terminology Legacy Mapping

**Created:** 2026-06-08
**Authority:** KTSP Phase F — Migration Execution
**Purpose:** Maps all old NATIONAL_* names to their new KINGDOM_* equivalents for posterity.

## Registry Renames

| Old Name | New Name | Wrapper Key Change |
|----------|----------|-------------------|
| NATIONAL_GOAL_REGISTRY.yaml | KINGDOM_GOAL_REGISTRY.yaml | `national_goal_registry` → `kingdom_goal_registry` |
| NATIONAL_PROGRAM_REGISTRY.yaml | KINGDOM_PROGRAM_REGISTRY.yaml | `national_program_registry` → `kingdom_program_registry` |
| NATIONAL_HEALTH_REGISTRY.yaml | KINGDOM_HEALTH_REGISTRY.yaml | `national_health_registry` → `kingdom_health_registry` |
| NATIONAL_STATUS_REGISTRY.yaml | KINGDOM_STATUS_REGISTRY.yaml | `national_status_registry` → `kingdom_status_registry` |

## Service Renames

| Old Name | New Name |
|----------|----------|
| services/national_goal_manager.py | services/kingdom_goal_manager.py |
| services/national_program_manager.py | services/kingdom_program_manager.py |
| services/national_planning_engine.py | services/kingdom_planning_engine.py |
| services/national_health_aggregator.py | services/kingdom_health_aggregator.py |
| services/national_status_aggregator.py | services/kingdom_status_aggregator.py |
| services/national_performance_monitor.py | services/kingdom_performance_monitor.py |
| services/national_scheduler.py | services/kingdom_scheduler.py |
| memory/national_memory_platform.py | memory/kingdom_memory_platform.py |

## Test Renames

| Old Name | New Name |
|----------|----------|
| tests/test_national_health_registry.py | tests/test_kingdom_health_registry.py |
| tests/test_national_planning.py | tests/test_kingdom_planning.py |
| tests/test_national_scheduler.py | tests/test_kingdom_scheduler.py |
| tests/test_national_status_aggregation.py | tests/test_kingdom_status_aggregation.py |

## Report & Template Renames

| Old Name | New Name |
|----------|----------|
| NATIONAL_HEALTH_REPORT.md | KINGDOM_HEALTH_REPORT.md |
| NATIONAL_PLANNING_REPORT.md | KINGDOM_PLANNING_REPORT.md |
| NATIONAL_PLANNING_READINESS_REVIEW.md | KINGDOM_PLANNING_READINESS_REVIEW.md |
| NATIONAL_SITUATION_ROOM_READINESS_REVIEW.md | KINGDOM_SITUATION_ROOM_READINESS_REVIEW.md |
| NATIONAL_STATUS_REPORT.md | KINGDOM_STATUS_REPORT.md |
| NATIONAL_READINESS_SCORECARD.md | KINGDOM_READINESS_SCORECARD.md |
| NATIONAL_PLANNING_REPORT_TEMPLATE.md | KINGDOM_PLANNING_REPORT_TEMPLATE.md |
| NATIONAL_HEALTH_REPORT_TEMPLATE.md | KINGDOM_HEALTH_REPORT_TEMPLATE.md |
| NATIONAL_STATUS_REPORT_TEMPLATE.md | KINGDOM_STATUS_REPORT_TEMPLATE.md |
| NATIONAL_SITUATION_ROOM_PROCESS.md | KINGDOM_SITUATION_ROOM_PROCESS.md |

## Knowledge Report Renames

| Old Name | New Name |
|----------|----------|
| AK_NATIONAL_KNOWLEDGE_AUDIT.md | AK_KINGDOM_KNOWLEDGE_AUDIT.md |
| AK_NATIONAL_KNOWLEDGE_FOUNDATION_ROADMAP.md | AK_KINGDOM_KNOWLEDGE_FOUNDATION_ROADMAP.md |
| AK_NATIONAL_KNOWLEDGE_GRAPH.md | AK_KINGDOM_KNOWLEDGE_GRAPH.md |
| AK_NATIONAL_KNOWLEDGE_INVENTORY.md | AK_KINGDOM_KNOWLEDGE_INVENTORY.md |
| AK_NATIONAL_KNOWLEDGE_PACKAGE.md | AK_KINGDOM_KNOWLEDGE_PACKAGE.md |

## Audit Renames

| Old Name | New Name |
|----------|----------|
| Q1_NATIONAL_AUDIT_PREPARATION.md | Q1_KINGDOM_AUDIT_PREPARATION.md |
| Q1_AUDIT_EVIDENCE_INDEX.md | Q1_KINGDOM_AUDIT_EVIDENCE_INDEX.md |

## Other Renames

| Old Name | New Name |
|----------|----------|
| AK_NATIONAL_BUDGET_LAW_v1.0_FINAL.md | AK_KINGDOM_BUDGET_LAW_v1.0_FINAL.md |
| AK_NATIONAL_BUDGET_LAW_v1.0_REVIEW.md | AK_KINGDOM_BUDGET_LAW_v1.0_REVIEW.md |
| AK_WP37_NATIONAL_EVOLUTION_FINAL_REPORT.md | AK_WP37_KINGDOM_EVOLUTION_FINAL_REPORT.md |
| data/treasury/national_revenue.json | data/treasury/kingdom_revenue.json |
| data/treasury/national_treasury.json | data/treasury/kingdom_treasury.json |
| data/treasury/national_fund.json | data/treasury/kingdom_fund.json |
| data/treasury/national_expenses.json | data/treasury/kingdom_expenses.json |
| data/treasury/national_budget.json | data/treasury/kingdom_budget.json |
| docs/schemas/national_revenue_schema.json | docs/schemas/kingdom_revenue_schema.json |
| docs/schemas/national_expense_schema.json | docs/schemas/kingdom_expense_schema.json |
| docs/schemas/national_budget_schema.json | docs/schemas/kingdom_budget_schema.json |

## Key Text Replacements Applied

| Source Text | Replacement | Affected Files |
|-------------|-------------|----------------|
| National Treasury | Kingdom Treasury | ~25 files |
| National Fund | Kingdom Fund | ~12 files |
| National Planning | Kingdom Planning | ~7 files |
| National Health | Kingdom Health | ~8 files |
| National Status | Kingdom Status | ~6 files |
| National Program | Kingdom Program | ~6 files |
| National Goal | Kingdom Goal | ~4 files |
| National Awareness | Kingdom Awareness | ~3 files |
| National Performance | Kingdom Performance | ~1 file |
| National Audit | Kingdom Audit | ~1 file |
| National Scheduler | Kingdom Scheduler | ~1 file |
| National Revenue | Kingdom Revenue | ~5 files |
| NATIONAL_TREASURY_SHARE | KINGDOM_TREASURY_SHARE | 1 file |

## Unchanged Legacy Files

The following files retain their original NATIONAL_* names as they are archived DRAFT documents:

- sovereign/laws/budget/AK_NATIONAL_BUDGET_LAW_v0.1_DRAFT.docx
- archive/Project_docs.2026-06-07/AK_NATIONAL_DEVELOPMENT_PROGRAM_v1.0.docx

---

*This map was generated automatically during KTSP migration execution. No old files were deleted — all changes preserved in version history.*
