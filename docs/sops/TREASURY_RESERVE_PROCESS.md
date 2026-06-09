# Treasury Reserve Process — SOP

**Status:** FINAL
**Authority:** AK_KINGDOM_BUDGET_LAW_v1.0_FINAL, AK_EMERGENCY_RESERVE_FRAMEWORK_v1.0_FINAL
**Owner:** Janus
**Operator:** Iris
**Reviewer:** Sage

---

## 1. Purpose

Standard operating procedure for strategic and emergency reserve management.

## 2. Authority

| Role | Authority |
|------|-----------|
| Iris | Monitor reserve levels, propose contributions |
| Janus | Approve reserve operations |
| Sage | Audit reserve compliance |
| Hung Vuong | Approve emergency drawdowns |

## 3. Process Flow

### Monthly Contribution
```
Monthly Revenue
    ↓
Strategic Reserve contribution (10%)
    ↓
Emergency Reserve contribution (5%) [if below target]
    ↓
Operating Budget
    ↓
Development Budget
```

### Strategic Drawdown
```
Janus identifies need
    ↓
Sage validates need
    ↓
Janus approves drawdown
    ↓
Iris executes
    ↓
Replenishment plan created
```

### Emergency Drawdown (per AK_EMERGENCY_RESERVE_FRAMEWORK)
```
Detecting Agent notifies Janus
    ↓
Janus assesses severity
    ↓
Level 1: Janus approval (20% max)
Level 2: Janus + Sage (30% max)
Level 3: Janus + Sage + Hung Vuong (50% max)
    ↓
Iris executes fund release
    ↓
Yet Kieu monitors → Sage audits
    ↓
Replenishment begins
```

## 4. Validation

- Reserve balance must never go negative
- Strategic reserve minimum: 3 months operating budget
- Emergency reserve minimum: 1 month operating budget
- All drawdowns must have approval chain documented
- Replenishment must complete within 90 days

## 5. Approval Chain

| Action | Approval Required |
|--------|-------------------|
| Monthly contribution | Iris → Janus |
| Strategic drawdown | Janus → Sage |
| Emergency drawdown (Level 1, ≤20%) | Janus |
| Emergency drawdown (Level 2, ≤30%) | Janus + Sage |
| Emergency drawdown (Level 3, ≤50%) | Janus + Sage + Hung Vuong |
| Replenishment plan | Iris → Janus → Sage |

## 6. Audit Trail

Each reserve transaction must include:
- transaction_id, reserve_type, transaction_type, amount
- authority, approval_chain, drawdown_level (if emergency)
- status, audit_id, created_at, updated_at

## 7. Escalation

- Reserve target not met for 90+ days → Sage review → Hung Vuong notification
- Unauthorized drawdown → Sage forensic audit → Janus disciplinary
- Reserve depletion → Immediate escalation: Janus → Sage → Hung Vuong
- Replenishment failure → Escalate to Hung Vuong for budget reallocation

## 8. Replenishment Rules

- After drawdown: allocation increases to 10% until target restored
- First call on surplus until fully replenished
- Maximum replenishment: 90 days

## 9. References

- AK_KINGDOM_BUDGET_LAW_v1.0_FINAL.md §6-7
- AK_EMERGENCY_RESERVE_FRAMEWORK_v1.0_FINAL.md
- docs/schemas/reserve_transaction_schema.json
- data/treasury/strategic_reserve.json
- data/treasury/emergency_reserve.json
