# Alkasik Kingdom Capability Economy Framework v1.0 FINAL

**Date:** 2026-06-08
**Status:** FINAL
**Authority:** Hung Vuong
**Owner:** Janus
**Reviewer:** Sage

---

## 1. Purpose

This framework defines the economic growth loop for Alkasik Kingdom: how skills become capabilities, how capabilities create value, and how value flows back into new capability investment.

---

## 2. Economic Growth Loop

```text
Skill
  ↓ (promotion)
Capability
  ↓ (activation)
Value Creation
  ↓ (treasury impact assessment)
Kingdom Revenue
  ↓ (budget allocation)
Kingdom Treasury
  ↓ (investment)
Kingdom Fund
  ↓ (budget allocation)
Capability Investment
  ↓ (R&D)
New Skills
  └─────────────────────────────→ (loop continues)
```

---

## 3. Value Creation Stages

| Stage | Activity | Economic Metric |
|-------|----------|-----------------|
| Skill | Knowledge formalized | Skill readiness score |
| Capability | Operational skill | Capability ROI |
| Value Creation | Capability generates output | usage_count, total_value |
| Revenue | Value converted to income | revenue_contribution |
| Investment | Revenue reinvested | investment_roi |
| New Skills | R&D produces new skills | skill_creation_rate |

---

## 4. Capability ROI Tracking

Per Economic Law v1.0, every capability must track:

| Metric | Description | Target |
|--------|-------------|--------|
| usage_count | Times invoked | ≥ 10/month for ACTIVE |
| total_value | Estimated value generated | Positive |
| total_cost | Estimated cost incurred | Less than value |
| roi | value / cost ratio | ≥ 1.5 for ADOPTED |
| adoption_status | Lifecycle stage | Per capability lifecycle |

---

## 5. Treasury Impact Assessment

Before any activation state change to PILOT_ACTIVE or higher:

1. Cost projection must be completed (Iris)
2. Budget allocation must be confirmed (Janus)
3. ROI threshold must be met (≥ 1.5 for ADOPTED)
4. Iris must provide economic assessment
5. Sage must verify assessment
6. Janus must approve allocation

---

## 6. Capability Investment Rules

| Investment Type | Source | Approval | Max Allocation |
|----------------|--------|----------|----------------|
| New skill R&D | Kingdom Fund - R&D | Janus | 15% of R&D budget |
| Capability optimization | Kingdom Fund - Operations | Iris → Janus | 10% of ops budget |
| Capability scaling | Kingdom Fund - Growth | Janus → Hung Vuong | 25% of growth fund |
| Emergency capability | Emergency Reserve | Sage + Janus + Hung Vuong | Per emergency rules |

---

## 7. Economic Sustainability Criteria

A capability is economically sustainable when:

- ROI ≥ 1.5 for 3 consecutive months
- usage_count ≥ 10/month
- total_value > total_cost for 6 consecutive months
- Revenue contribution is positive
- Treasury impact is net positive

---

## 8. References

- Economic Law v1.0 FINAL
- AK_KINGDOM_BUDGET_LAW_v1.0_FINAL.md
- AK_TREASURY_CHARTER_v1.0_FINAL.md
- Knowledge Governance Decree v1.0 FINAL
- memory/capability_roi_registry.py
- memory/capability_registry/official_capability_registry.py
