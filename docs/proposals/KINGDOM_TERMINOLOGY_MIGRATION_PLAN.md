# Kingdom Terminology Migration Plan

**KTSP Phase F** | **Date:** 2026-06-08
**Status:** PLAN — Not yet executed.

---

## Overview

6-wave migration. Each wave is independent and can be executed separately. Waves MUST be executed in order.

**Total files affected:** ~46 file renames + ~110 text reference changes

---

## Wave 1: Legal Artifacts

**Scope:** Laws, charters, decrees — text-only replacements
**Files:** ~12
**Risk:** HIGH
**Dependency:** None (can run first)

### Steps

1. Rename `AK_NATIONAL_BUDGET_LAW_v1.0_FINAL.md` → `AK_KINGDOM_BUDGET_LAW_v1.0_FINAL.md`
2. Update internal text: "National Budget Law" → "Kingdom Budget Law" (title, all references)
3. Update internal text: "National Treasury" → "Kingdom Treasury" in document body
4. Update internal text: "National Fund" → "Kingdom Fund" in document body
5. Update `AK_TREASURY_CHARTER_v1.0_FINAL.md` — replace "National Treasury" → "Kingdom Treasury" (7 occurrences)
6. Update `AK_ROYAL_TREASURY_CHARTER_v1.0_FINAL.md` — replace "National Treasury" cross-references
7. Update `AK_CAPABILITY_ECONOMY_FRAMEWORK_v1.0_FINAL.md` — replace "National" → "Kingdom" (6 occurrences)
8. Update `AK_EMERGENCY_RESERVE_FRAMEWORK_v1.0_FINAL.md` — replace "National Fund" → "Kingdom Fund"
9. Update `AK_NATIONAL_BUDGET_LAW_v1.0_REVIEW.md` — file rename + content update

### Verification
- `grep -i "National" docs/laws/ docs/charters/ docs/frameworks/` → 0 matches

---

## Wave 2: Registries

**Scope:** YAML registry file renames + internal wrapper key renames + all code reading them
**Files:** 4 YAML + all services reading them
**Risk:** MEDIUM
**Dependency:** Wave 1 (legal consistency)

### Steps

1. Rename `NATIONAL_GOAL_REGISTRY.yaml` → `KINGDOM_GOAL_REGISTRY.yaml`
   - Update wrapper key: `national_goal_registry:` → `kingdom_goal_registry:`
   - Update all `.get("national_goal_registry", ...)` → `.get("kingdom_goal_registry", ...)`
2. Rename `NATIONAL_PROGRAM_REGISTRY.yaml` → `KINGDOM_PROGRAM_REGISTRY.yaml`
   - Same wrapper key update pattern
3. Rename `NATIONAL_HEALTH_REGISTRY.yaml` → `KINGDOM_HEALTH_REGISTRY.yaml`
   - Same wrapper key update pattern
4. Rename `NATIONAL_STATUS_REGISTRY.yaml` → `KINGDOM_STATUS_REGISTRY.yaml`
   - Same wrapper key update pattern
5. Update `TREASURY_ACCOUNT_REGISTRY.yaml` — Account name "National Treasury" → "Kingdom Treasury"
6. Update `TREASURY_STATUS_REGISTRY.yaml` — Account name "National Treasury" → "Kingdom Treasury"
7. Update `TREASURY_HEALTH_REGISTRY.yaml` — Metric "national_treasury_balance" → "kingdom_treasury_balance"

### Files to Update Registry References

| File | Current Reference | New Reference |
|------|------------------|---------------|
| services/national_goal_manager.py | "NATIONAL_GOAL_REGISTRY.yaml" | "KINGDOM_GOAL_REGISTRY.yaml" |
| services/national_program_manager.py | "NATIONAL_PROGRAM_REGISTRY.yaml" | "KINGDOM_PROGRAM_REGISTRY.yaml" |
| services/national_health_aggregator.py | "NATIONAL_HEALTH_REGISTRY.yaml" | "KINGDOM_HEALTH_REGISTRY.yaml" |
| services/national_status_aggregator.py | "NATIONAL_STATUS_REGISTRY.yaml" | "KINGDOM_STATUS_REGISTRY.yaml" |
| tests/test_national_health_registry.py | "NATIONAL_HEALTH_REGISTRY.yaml" | "KINGDOM_HEALTH_REGISTRY.yaml" |
| tests/test_national_status_aggregation.py | "NATIONAL_STATUS_REGISTRY.yaml" | "KINGDOM_STATUS_REGISTRY.yaml" |
| tests/test_goal_registry.py | "NATIONAL_GOAL_REGISTRY.yaml" | "KINGDOM_GOAL_REGISTRY.yaml" |
| tests/test_program_registry.py | "NATIONAL_PROGRAM_REGISTRY.yaml" | "KINGDOM_PROGRAM_REGISTRY.yaml" |
| services/national_planning_engine.py | REGISTRIES_DIR (indirect) | Inherited |

### Verification
- All services import successfully
- All tests pass
- YAML files parse correctly with new wrapper keys

---

## Wave 3: Reports & Templates

**Scope:** Markdown file renames + text content updates
**Files:** ~19
**Risk:** LOW
**Dependency:** Wave 2 (registry names consistent)

### Steps
1. Rename all 16 reports (see Section 6 in standard)
2. Rename all 3 templates
3. Rename 1 SOP
4. Update text content per text replacement map
5. Update internal cross-references to renamed registries

### Verification
- All cross-references valid
- No broken links to old NATIONAL_* files

---

## Wave 4: Services & Tests

**Scope:** Python file renames + import path updates + content changes
**Files:** 7 services + 4 tests + 1 memory module = 12 source files
**Risk:** HIGH
**Dependency:** Wave 2 (registry names) + Wave 3 (report cross-refs)

### Service Renames

| Old File | New File | Import Changes |
|----------|----------|----------------|
| services/national_goal_manager.py | services/kingdom_goal_manager.py | All `import national_goal_manager` → `import kingdom_goal_manager` |
| services/national_program_manager.py | services/kingdom_program_manager.py | Same pattern |
| services/national_planning_engine.py | services/kingdom_planning_engine.py | + CAP string update |
| services/national_health_aggregator.py | services/kingdom_health_aggregator.py | Same pattern |
| services/national_status_aggregator.py | services/kingdom_status_aggregator.py | Same pattern |
| services/national_performance_monitor.py | services/kingdom_performance_monitor.py | Same pattern |
| services/national_scheduler.py | services/kingdom_scheduler.py | Same pattern |
| memory/national_memory_platform.py | memory/kingdom_memory_platform.py | Same pattern |

### Import Chain Update

All services that do `importlib.import_module(f"services.{name}")` must use new names:

| Importer | Old Import | New Import |
|----------|-----------|------------|
| national_planning_engine.py | `"national_goal_manager"` | `"kingdom_goal_manager"` |
| national_planning_engine.py | `"national_program_manager"` | `"kingdom_program_manager"` |
| national_performance_monitor.py | `"national_goal_manager"` | `"kingdom_goal_manager"` |
| national_performance_monitor.py | `"national_program_manager"` | `"kingdom_program_manager"` |
| national_performance_monitor.py | `"national_planning_engine"` | `"kingdom_planning_engine"` |
| national_performance_monitor.py | `"capability_*"` (unchanged) | (unchanged) |
| national_health_aggregator.py | (internal refs) | (update all) |
| national_status_aggregator.py | (internal refs) | (update all) |
| program_evidence_collector.py | `"national_goal_manager"` | `"kingdom_goal_manager"` |
| program_evidence_collector.py | `"national_program_manager"` | `"kingdom_program_manager"` |

### Test Renames

| Old File | New File |
|----------|----------|
| tests/test_national_health_registry.py | tests/test_kingdom_health_registry.py |
| tests/test_national_planning.py | tests/test_kingdom_planning.py |
| tests/test_national_scheduler.py | tests/test_kingdom_scheduler.py |
| tests/test_national_status_aggregation.py | tests/test_kingdom_status_aggregation.py |

### Verification
- `pytest tests/ -q` → 264+ tests pass
- All services import without ImportError
- All registry keys match

---

## Wave 5: Authority Model

**Scope:** Add REH/RAK/HCK/KAO references to appropriate documentation
**Files:** ~5
**Risk:** LOW
**Dependency:** Wave 3 (docs updated)

### Steps
1. Add authority model to `KINGDOM_TERMINOLOGY_STANDARD.md` (already included in this plan)
2. Update relevant charters to reference new authority bodies
3. Add branch references to governance documentation
4. No code changes — documentation only

---

## Wave 6: Archive Legacy Terms

**Scope:** Move old NATIONAL_* names to legacy reference
**Files:** Archive index update
**Risk:** LOW
**Dependency:** Waves 2-4 (after all renames)

### Steps
1. Create legacy reference mapping in `archive/` or legacy registry
2. Document all old → new name mappings for posterity
3. No file deletion — old names preserved in version history

---

## Rollback Plan

If any wave causes test failures or import errors:

1. **Wave 1 (Legal)**: Revert file rename + text changes in affected docs
2. **Wave 2 (Registries)**: Revert YAML filenames + wrapper keys + all `.get()` calls
3. **Wave 3 (Reports)**: Revert markdown file renames
4. **Wave 4 (Services)**: Revert .py file renames + all import paths + all tests
5. **Waves 5-6**: Trivially revert (no code impact)

**Critical rollback path:** Wave 4 (services) requires reverting import chains in dependent services. Always test after each individual rename.

---

## Effort Estimate

| Wave | Files | Estimated Changes | Complexity |
|------|-------|-------------------|------------|
| 1 | 12 | ~30 text replacements | Medium |
| 2 | 4 YAML + 8 code files | ~20 reference updates | Medium |
| 3 | 19 | ~19 renames + ~30 text updates | Low |
| 4 | 12 .py | ~12 renames + ~40 import updates | High |
| 5 | 5 | ~5 doc additions | Low |
| 6 | 1 | ~1 archive entry | Low |
| **Total** | **~53** | **~131 changes** | |

---

*Plan prepared by KTSP. No changes executed — planning only.*
