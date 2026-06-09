# Kingdom Terminology Standard

**KTSP Phase D** | **Date:** 2026-06-08
**Authority:** Constitution v1.1 FINAL | Alkasik State Corpus v1.0 FINAL
**Status:** STANDARD — Not yet implemented.

---

## 1. Kingdom Authority Model

The official constitutional structure of the Alkasik Kingdom:

```
Hung Vuong
(Constitutional Monarch)
    │
    ├── Royal Executive House (REH)
    │   President: Janus
    │   Function: Executive governance, treasury operations, national planning
    │
    ├── Royal Assembly of the Kingdom (RAK)
    │   Function: Legislative review, policy development
    │   Agents: Iris, Lang Lieu, Yet Kieu
    │
    ├── High Court of the Kingdom (HCK)
    │   Function: Judicial review, compliance verification
    │   Agents: Hermes, Helen
    │
    └── Kingdom Audit Office (KAO)
        Function: Independent constitutional oversight
        Auditor General: Sage
```

### Authority Mapping

| Canonical Term | Abbreviation | Existing Entity | Change Required |
|----------------|-------------|-----------------|-----------------|
| Royal Executive House | REH | Janus (executive role) | Document only |
| Royal Assembly of the Kingdom | RAK | Iris, Lang Lieu, Yet Kieu | Document only |
| High Court of the Kingdom | HCK | Hermes, Helen | Document only |
| Kingdom Audit Office | KAO | Sage (audit role) | Document only |

---

## 2. Canonical Terminology Map

### "National" → "Kingdom" Prefix

| Source Term | Canonical Term | Justification |
|-------------|----------------|---------------|
| National Treasury | Kingdom Treasury | Align with Kingdom naming |
| National Fund | Kingdom Fund | Align with Kingdom naming |
| National Planning | Kingdom Planning | Align with Kingdom naming |
| National Health | Kingdom Health | Align with Kingdom naming |
| National Status | Kingdom Status | Align with Kingdom naming |
| National Situation Room | Kingdom Situation Room | Align with Kingdom naming |
| National Program | Kingdom Program | Align with Kingdom naming |
| National Goal | Kingdom Goal | Align with Kingdom naming |
| National Awareness | Kingdom Awareness | Align with Kingdom naming |
| National Audit | Kingdom Audit Office | New entity (KAO) |
| National Performance | Kingdom Performance | Align with Kingdom naming |
| National Scheduler | Kingdom Scheduler | Align with Kingdom naming |
| National Memory Platform | Kingdom Memory Platform | Align with Kingdom naming |

### Terms that Remain

| Term | Reason |
|------|--------|
| Royal Treasury (8%) | Distinct entity, constitutionally separate |
| Royal Executive House (REH) | Uses "Royal" for executive branch |
| Royal Assembly of the Kingdom (RAK) | Uses "Royal" for legislative branch |
| Alkasik Kingdom | Sovereign nation name |
| All 7 agent names | Proper names, unchanged |

---

## 3. Registry Rename Map

| Current Name | Canonical Name | Wrapper Key Change |
|-------------|----------------|---------------------|
| NATIONAL_GOAL_REGISTRY.yaml | KINGDOM_GOAL_REGISTRY.yaml | `national_goal_registry:` → `kingdom_goal_registry:` |
| NATIONAL_PROGRAM_REGISTRY.yaml | KINGDOM_PROGRAM_REGISTRY.yaml | `national_program_registry:` → `kingdom_program_registry:` |
| NATIONAL_HEALTH_REGISTRY.yaml | KINGDOM_HEALTH_REGISTRY.yaml | `national_health_registry:` → `kingdom_health_registry:` |
| NATIONAL_STATUS_REGISTRY.yaml | KINGDOM_STATUS_REGISTRY.yaml | `national_status_registry:` → `kingdom_status_registry:` |
| TREASURY_ACCOUNT_REGISTRY.yaml | (content only) | Account name: "National Treasury" → "Kingdom Treasury" |
| TREASURY_STATUS_REGISTRY.yaml | (content only) | Account name: "National Treasury" → "Kingdom Treasury" |

---

## 4. Service Rename Map

| Current Name | Canonical Name | Internal Changes |
|-------------|----------------|------------------|
| services/national_goal_manager.py | services/kingdom_goal_manager.py | `REGISTRIES_DIR / "NATIONAL_GOAL_REGISTRY.yaml"` → `"KINGDOM_GOAL_REGISTRY.yaml"` |
| services/national_program_manager.py | services/kingdom_program_manager.py | Same pattern |
| services/national_planning_engine.py | services/kingdom_planning_engine.py | Same pattern + CAP string update |
| services/national_health_aggregator.py | services/kingdom_health_aggregator.py | Same pattern |
| services/national_status_aggregator.py | services/kingdom_status_aggregator.py | Same pattern |
| services/national_performance_monitor.py | services/kingdom_performance_monitor.py | Same pattern |
| services/national_scheduler.py | services/kingdom_scheduler.py | Same pattern |
| memory/national_memory_platform.py | memory/kingdom_memory_platform.py | Same pattern |

---

## 5. Test Rename Map

| Current Name | Canonical Name |
|-------------|----------------|
| tests/test_national_health_registry.py | tests/test_kingdom_health_registry.py |
| tests/test_national_planning.py | tests/test_kingdom_planning.py |
| tests/test_national_scheduler.py | tests/test_kingdom_scheduler.py |
| tests/test_national_status_aggregation.py | tests/test_kingdom_status_aggregation.py |

---

## 6. Documentation Rename Map

| Current Name | Canonical Name |
|-------------|----------------|
| NATIONAL_HEALTH_REPORT.md | KINGDOM_HEALTH_REPORT.md |
| NATIONAL_PLANNING_REPORT.md | KINGDOM_PLANNING_REPORT.md |
| NATIONAL_PLANNING_READINESS_REVIEW.md | KINGDOM_PLANNING_READINESS_REVIEW.md |
| NATIONAL_SITUATION_ROOM_READINESS_REVIEW.md | KINGDOM_SITUATION_ROOM_READINESS_REVIEW.md |
| NATIONAL_STATUS_REPORT.md | KINGDOM_STATUS_REPORT.md |
| NATIONAL_HEALTH_REPORT_TEMPLATE.md | KINGDOM_HEALTH_REPORT_TEMPLATE.md |
| NATIONAL_PLANNING_REPORT_TEMPLATE.md | KINGDOM_PLANNING_REPORT_TEMPLATE.md |
| NATIONAL_STATUS_REPORT_TEMPLATE.md | KINGDOM_STATUS_REPORT_TEMPLATE.md |
| NATIONAL_SITUATION_ROOM_PROCESS.md | KINGDOM_SITUATION_ROOM_PROCESS.md |
| Q1_NATIONAL_AUDIT_PREPARATION.md | Q1_KINGDOM_AUDIT_PREPARATION.md |
| Q1_AUDIT_EVIDENCE_INDEX.md | Q1_KINGDOM_AUDIT_EVIDENCE_INDEX.md |
| NATIONAL_AWARENESS_MATURITY_REPORT.md | KINGDOM_AWARENESS_MATURITY_REPORT.md |
| AK_NATIONAL_BUDGET_LAW_v1.0_FINAL.md | AK_KINGDOM_BUDGET_LAW_v1.0_FINAL.md |
| AK_NATIONAL_KNOWLEDGE_AUDIT.md | AK_KINGDOM_KNOWLEDGE_AUDIT.md |
| AK_NATIONAL_KNOWLEDGE_FOUNDATION_ROADMAP.md | AK_KINGDOM_KNOWLEDGE_FOUNDATION_ROADMAP.md |
| AK_NATIONAL_KNOWLEDGE_GRAPH.md | AK_KINGDOM_KNOWLEDGE_GRAPH.md |
| AK_NATIONAL_KNOWLEDGE_INVENTORY.md | AK_KINGDOM_KNOWLEDGE_INVENTORY.md |
| AK_NATIONAL_KNOWLEDGE_PACKAGE.md | AK_KINGDOM_KNOWLEDGE_PACKAGE.md |
| AK_WP37_NATIONAL_EVOLUTION_FINAL_REPORT.md | AK_WP37_KINGDOM_EVOLUTION_FINAL_REPORT.md |
| data/treasury/national_treasury.json | data/treasury/kingdom_treasury.json |
| data/treasury/national_fund.json | data/treasury/kingdom_fund.json |
| data/treasury/national_revenue.json | data/treasury/kingdom_revenue.json |
| data/treasury/national_expenses.json | data/treasury/kingdom_expenses.json |
| data/treasury/national_budget.json | data/treasury/kingdom_budget.json |
| docs/schemas/national_revenue_schema.json | docs/schemas/kingdom_revenue_schema.json |
| docs/schemas/national_expense_schema.json | docs/schemas/kingdom_expense_schema.json |
| docs/schemas/national_budget_schema.json | docs/schemas/kingdom_budget_schema.json |

---

## 7. Text Replacement Map

| Source Text | Replacement Text | Scope |
|-------------|-----------------|-------|
| National Treasury | Kingdom Treasury | All documents |
| National Fund | Kingdom Fund | All documents |
| National Planning | Kingdom Planning | All documents |
| National Health | Kingdom Health | All documents |
| National Status | Kingdom Status | All documents |
| National Program | Kingdom Program | All documents |
| National Goal | Kingdom Goal | All documents |
| National Awareness | Kingdom Awareness | All documents |
| National Performance | Kingdom Performance | All documents |
| National Audit | Kingdom Audit | All documents |
| National Scheduler | Kingdom Scheduler | All documents |

**Note:** "National" as part of "National Memory Platform" → "Kingdom Memory Platform"

---

*Standard prepared by KTSP. No changes executed — mapping only.*
