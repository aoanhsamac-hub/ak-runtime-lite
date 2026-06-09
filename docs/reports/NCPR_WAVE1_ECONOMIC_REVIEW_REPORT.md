# NCP-R Wave 1 — Economic Layer Review Report

**Date:** 2026-06-08
**Authority:** Janus Directive — NCP-R | Royal Economic Architecture Approval
**Status:** COMPLETE
**Reviewer:** Janus

---

## Approved Economic Model Reference

```
Kingdom Revenue
├── Kingdom Treasury (92%)
└── Royal Treasury (8%)

Kingdom Treasury
↓
Kingdom Fund
↓
Budget Allocation
↓
Kingdom Programs
↓
Surplus Distribution
↓
Royal Treasury
```

---

## Required Validation — 10 Items

| # | Framework Item | Status | Decision | Evidence |
|---|---|---|---|---|
| 1 | Kingdom Revenue Framework | EXISTS | APPROVE | treasury_registry.yaml — 9 revenue sources defined |
| 2 | Kingdom Treasury Governance | EXISTS | APPROVE | treasury_registry.yaml — royal_treasury section ACTIVE |
| 3 | Royal Treasury Governance | EXISTS | APPROVE | treasury_registry.yaml — status ACTIVE, authority Hung Vuong |
| 4 | Treasury Charter | MISSING | MISSING | No treasury charter found anywhere; required by Economic Law |
| 5 | National Budget Framework | EXISTS | APPROVE | Budget Law v1.0 REVIEW — workflow defined |
| 6 | Budget Law | EXISTS | REQUIRE_REVISION | v1.0 REVIEW (not FINAL); v0.1 DRAFT exists |
| 7 | Strategic Reserve Framework | EXISTS | APPROVE | Budget Law REVIEW — reserve_fund workflow defined |
| 8 | Emergency Reserve Framework | MISSING | MISSING | No emergency reserve mechanism documented |
| 9 | Capability Economy Framework | EXISTS | APPROVE | Economic Law — ROI tracking, capability lifecycle value, treasury impact |
| 10 | Surplus Distribution Framework | EXISTS | REQUIRE_REVISION | Budget Law REVIEW references surplus → Royal Treasury but lacks allocation percentages |

---

## Economic Gap Analysis

### Missing Laws
- **Treasury Governance Law**: Referenced in Economic Law source path (`sovereign/laws/treasury/`) but no separate Treasury Governance Law exists as a standalone document.

### Missing Charters
- **Treasury Charter**: No charter defining treasury governance structure, authority chain, or operational model.

### Missing Registries
- **Revenue Registry**: `treasury_registry.yaml` lists revenue sources but no separate revenue registry exists.
- **Budget Registry**: No dedicated budget allocation tracking registry.

### Missing Governance
- **Emergency Reserve Governance**: No policy, law, or decree covering emergency reserve activation, funding, or governance.

### Missing Authority Definitions
- **Royal Treasury Authority**: Owner of Royal Treasury not explicitly defined.
- **Surplus Distribution Authority**: Who authorizes surplus distribution from Kingdom Treasury to Royal Treasury is undefined.

---

## Economic Compliance Checklist

| Requirement | Status |
|-------------|--------|
| Kingdom Revenue split (92/8) documented | PARTIAL — ratio exists in directive but not in law |
| Kingdom Treasury governance defined | PASS — treasury_registry.yaml |
| Royal Treasury governance defined | PASS — treasury_registry.yaml |
| Budget allocation workflow defined | PASS — Budget Law REVIEW |
| Strategic reserve defined | PASS — reserve_fund in treasury_registry.yaml |
| Emergency reserve defined | FAIL — MISSING |
| Capability economy framework exists | PASS — Economic Law |
| Capability ROI tracking implemented | PASS — capability_roi_registry.py |
| Treasury impact assessment required before activation | PASS — Economic Law |
| Budget Law in FINAL status | FAIL — currently REVIEW |
| Treasury Charter exists | FAIL — MISSING |

---

## Recommendations

1. **Budget Law**: Upgrade from REVIEW to FINAL with explicit 92/8 revenue split.
2. **Treasury Charter**: Create charter defining treasury governance, authority chain, operational model.
3. **Emergency Reserve Framework**: Define governance for emergency reserve activation.
4. **Surplus Distribution**: Document allocation percentages and authorization chain.
5. **Revenue Registry**: Create separate registry for revenue tracking and classification.
