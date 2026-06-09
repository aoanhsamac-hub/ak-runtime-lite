# Terminology Impact Analysis

**KTSP Phase E** | **Date:** 2026-06-08

---

## 1. Legal Impact

### Affected Legal Documents

| Document | Term Changes | Risk Level | Notes |
|----------|-------------|------------|-------|
| AK_NATIONAL_BUDGET_LAW_v1.0_FINAL.md | "National" → "Kingdom" in title + body | HIGH | FINAL law — title change has constitutional weight |
| AK_TREASURY_CHARTER_v1.0_FINAL.md | "National Treasury" → "Kingdom Treasury" (7 occurrences) | HIGH | Charter references national treasury operations |
| AK_ROYAL_TREASURY_CHARTER_v1.0_FINAL.md | References to "National Treasury" → "Kingdom Treasury" | HIGH | Cross-reference term changes |
| AK_CAPABILITY_ECONOMY_FRAMEWORK_v1.0_FINAL.md | "National" → "Kingdom" (6 occurrences) | MEDIUM | Framework document |
| AK_EMERGENCY_RESERVE_FRAMEWORK_v1.0_FINAL.md | "National Fund" → "Kingdom Fund" | MEDIUM | Framework document |

**Risk:** Legal term changes may affect authority chains defined in FINAL documents.
**Recommendation:** Wave 1 must include constitutional review of each term change.

### Constitution Impact

| Document | "National" Matches | Impact |
|----------|-------------------|--------|
| ALKASIK_CONSTITUTION_v1.0.md | 0 | NONE — Constitution uses Vietnamese, no English "National" terms |
| ALKASIK_STATE_CORPUS_v1.0_FINAL | PENDING | Requires full scan |

---

## 2. Charter Impact

| Charter | Affected | Term | Action |
|---------|----------|------|--------|
| AK_TREASURY_CHARTER_v1.0_FINAL.md | YES | National Treasury → Kingdom Treasury | Content update |
| AK_ROYAL_TREASURY_CHARTER_v1.0_FINAL.md | YES | National Treasury refs → Kingdom Treasury | Cross-ref update |
| JANUS_CHARTER_v1.0_FINAL.md | NO | No "National" references | None |
| HERMES_CHARTER_v1.0_FINAL.md | NO | No "National" references | None |

---

## 3. Registry Impact

### File Renames (4 registries)

| Current Name | New Name | Internal Key Change | Service Impact |
|-------------|----------|---------------------|----------------|
| NATIONAL_GOAL_REGISTRY.yaml | KINGDOM_GOAL_REGISTRY.yaml | `national_goal_registry:` → `kingdom_goal_registry:` | All services reading goals |
| NATIONAL_PROGRAM_REGISTRY.yaml | KINGDOM_PROGRAM_REGISTRY.yaml | `national_program_registry:` → `kingdom_program_registry:` | All services reading programs |
| NATIONAL_HEALTH_REGISTRY.yaml | KINGDOM_HEALTH_REGISTRY.yaml | `national_health_registry:` → `kingdom_health_registry:` | Health aggregator, monitors |
| NATIONAL_STATUS_REGISTRY.yaml | KINGDOM_STATUS_REGISTRY.yaml | `national_status_registry:` → `kingdom_status_registry:` | Status aggregator |

**Critical:** Each YAML registry has a wrapper key that must match the filename. Renaming requires updating every `.get("national_*_registry", {})` call in every service and test.

### Internal References in Treasury Registries

| Registry | Term | Occurrences |
|----------|------|-------------|
| TREASURY_ACCOUNT_REGISTRY.yaml | "National Treasury" (account name) | 2 |
| TREASURY_STATUS_REGISTRY.yaml | "National Treasury" (account name) | 1 |
| TREASURY_HEALTH_REGISTRY.yaml | "national_treasury_balance" (metric) | 1 |
| TREASURY_TRANSACTION_REGISTRY.yaml | "National Fund" references | 2 |

---

## 4. Service Impact

### File Renames + Content Changes (7 services)

| Current Name | New Name | Internal Changes |
|-------------|----------|------------------|
| national_goal_manager.py | kingdom_goal_manager.py | Import path, registry key access |
| national_program_manager.py | kingdom_program_manager.py | Import path, registry key access |
| national_planning_engine.py | kingdom_planning_engine.py | Import path, CAP_VIOLATION string |
| national_health_aggregator.py | kingdom_health_aggregator.py | Import path, registry key access |
| national_status_aggregator.py | kingdom_status_aggregator.py | Import path, registry key access |
| national_performance_monitor.py | kingdom_performance_monitor.py | Import path, service name refs |
| national_scheduler.py | kingdom_scheduler.py | Import path |

### Import Chain Impact

Each service is imported by:
- Other services via `importlib.import_module(f"services.{name}")`
- Test files via `from services import {name}`
- `services/__init__.py` if exported

**Highest risk:** `national_planning_engine.py` imports both `national_goal_manager.py` and `national_program_manager.py` — creates transitive rename dependencies.

### Dependent Services (import national_* services)

| Service | Imports | Nature |
|---------|---------|--------|
| national_planning_engine.py | goal_manager, program_manager | Direct |
| national_performance_monitor.py | goal_manager, program_manager, planning_engine | Direct |
| program_evidence_collector.py | goal_manager, program_manager | Direct |
| audit_evidence_compiler.py | (via registry YAML, not direct import) | Indirect |
| treasury_impact_tracker.py | (none national_*) | None |
| capability_* engines | (none national_*) | None |

---

## 5. Test Impact

| Test File | Imports | Change Type |
|-----------|---------|-------------|
| test_national_health_registry.py | yaml, REGISTRIES_DIR | File rename + import path |
| test_national_planning.py | goal_manager, program_manager, planning_engine | File rename + import path |
| test_national_scheduler.py | national_scheduler | File rename + import path |
| test_national_status_aggregation.py | status_aggregator, health_aggregator | File rename + import path |
| test_program_registry.py | TREASURY_IMPACT_REGISTRY (no national_*) | None |
| test_program_evidence.py | program_evidence_collector (no national_*) | None |

---

## 6. Documentation Impact

### Reports (16 files)

| File | Term Change | Type |
|------|-------------|------|
| NATIONAL_HEALTH_REPORT.md | Kingdom Health | Rename + text |
| NATIONAL_PLANNING_REPORT.md | Kingdom Planning | Rename + text |
| NATIONAL_PLANNING_READINESS_REVIEW.md | Kingdom Planning | Rename + text |
| NATIONAL_READINESS_SCORECARD.md | Kingdom | Rename + text |
| NATIONAL_SITUATION_ROOM_READINESS_REVIEW.md | Kingdom Situation Room | Rename + text |
| NATIONAL_STATUS_REPORT.md | Kingdom Status | Rename + text |
| AK_NATIONAL_KNOWLEDGE_AUDIT.md | Kingdom Knowledge | Rename only |
| AK_NATIONAL_KNOWLEDGE_FOUNDATION_ROADMAP.md | Kingdom Knowledge | Rename only |
| AK_NATIONAL_KNOWLEDGE_GRAPH.md | Kingdom Knowledge | Rename only |
| AK_NATIONAL_KNOWLEDGE_INVENTORY.md | Kingdom Knowledge | Rename only |
| AK_NATIONAL_KNOWLEDGE_PACKAGE.md | Kingdom Knowledge | Rename only |
| AK_WP37_NATIONAL_EVOLUTION_FINAL_REPORT.md | Kingdom Evolution | Rename only |
| Q1_NATIONAL_AUDIT_PREPARATION.md | Kingdom Audit | Rename + text |
| CAPABILITY_ECONOMY_MATURITY_REPORT.md | (no National) | None |
| NATIONAL_PLANNING_MATURITY_REPORT.md | Kingdom Planning | Rename + text |
| NATIONAL_AWARENESS_MATURITY_REPORT.md | Kingdom Awareness | Rename + content |

### Templates (3 files)

| File | Term Change | Type |
|------|-------------|------|
| NATIONAL_HEALTH_REPORT_TEMPLATE.md | Kingdom Health | Rename + text |
| NATIONAL_PLANNING_REPORT_TEMPLATE.md | Kingdom Planning | Rename + text |
| NATIONAL_STATUS_REPORT_TEMPLATE.md | Kingdom Status | Rename + text |

### SOPs (1 file)

| File | Term Change | Type |
|------|-------------|------|
| NATIONAL_SITUATION_ROOM_PROCESS.md | Kingdom Situation Room | Rename + text |

### Data Files (5 files)

| File | Change |
|------|--------|
| data/treasury/national_treasury.json | File rename only |
| data/treasury/national_fund.json | File rename only |
| data/treasury/national_revenue.json | File rename only |
| data/treasury/national_expenses.json | File rename only |
| data/treasury/national_budget.json | File rename only |

### Schema Files (3 files)

| File | Change |
|------|--------|
| docs/schemas/national_revenue_schema.json | File rename only |
| docs/schemas/national_expense_schema.json | File rename only |
| docs/schemas/national_budget_schema.json | File rename only |

---

## 7. Impact Summary

| Impact Category | File Renames | Content Changes | Risk |
|-----------------|-------------|-----------------|------|
| Legal | 2 | ~20 text refs | HIGH |
| Charters | 0 | ~10 text refs | HIGH |
| Registries | 4 | 4 wrapper keys + 5 account refs | MEDIUM |
| Services | 7 | ~20 import paths + strings | HIGH |
| Tests | 4 | ~10 import paths | MEDIUM |
| Reports | 16 | ~30 text refs | LOW |
| Templates | 3 | ~6 text refs | LOW |
| SOPs | 1 | ~4 text refs | LOW |
| Data | 5 | 0 (file only) | LOW |
| Schemas | 3 | 0 (file only) | LOW |
| Memory | 1 | ~5 import refs | MEDIUM |
| **Total** | **~46 files** | **~110 text refs** | |

---

## 8. Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Legal term changes affect authority chains | Constitutional review before any legal rename |
| Service import chains break | Wave 4 (services) must update ALL import paths simultaneously |
| Registry wrapper key mismatch | Update all `.get("national_*")` → `.get("kingdom_*")` in same commit |
| Test failures from renamed services | Run full test suite after each rename wave |
| Cross-document term inconsistency | Central term map in KINGDOM_TERMINOLOGY_STANDARD.md |

---

*Prepared by KTSP Phase E. No changes executed — impact analysis only.*
