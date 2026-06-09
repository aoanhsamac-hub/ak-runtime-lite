# Treasury Budget Process — SOP

**Status:** FINAL
**Authority:** AK_KINGDOM_BUDGET_LAW_v1.0_FINAL, AK_TREASURY_CHARTER_v1.0_FINAL
**Owner:** Janus
**Operator:** Iris
**Reviewer:** Sage
**Approver:** Hung Vuong

---

## 1. Purpose

Standard operating procedure for budget proposal, allocation, execution, and reporting.

## 2. Authority

| Role | Authority |
|------|-----------|
| Iris | Prepare budget proposal |
| Janus | Coordinate and consolidate |
| Sage | Risk and compliance review |
| Hung Vuong | Final approval |

## 3. Process Flow

### Monthly
```
Iris prepares monthly budget proposal
    ↓
Sage reviews for risk compliance
    ↓
Janus coordinates and consolidates
    ↓
Hung Vuong approves
    ↓
Budget recorded in kingdom_budget.json
```

### Quarterly
```
Budget execution review
    ↓
Surplus/deficit analysis
    ↓
Reserve rebalancing
    ↓
Next quarter allocation adjustment
    ↓
Hung Vuong approval
```

### Annual
```
Full annual budget proposal
    ↓
Strategic priority review
    ↓
Revenue projection update
    ↓
Reserve target setting
    ↓
Hung Vuong final approval
```

## 4. Budget Categories

Per Budget Law §3: Infrastructure, Knowledge, Dataset, Security, Operations, R&D, StrategicReserve, EmergencyReserve, Growth.

## 5. Validation

- Total allocations must not exceed available funds
- Reserve allocations must meet minimum requirements
- Budget must balance (allocated + reserve = available)
- Each category must have defined priority

## 6. Approval Chain

| Budget Type | Approval Required |
|------------|-------------------|
| Monthly operational | Iris + Janus + Sage |
| Quarterly adjustment | Iris + Janus + Sage + Hung Vuong |
| Annual budget | Full chain: Iris → Janus → Sage → Hung Vuong |
| Emergency budget | Expedited: Iris → Janus → Sage → Hung Vuong |

## 7. Audit Trail

Each budget record must include:
- budget_id, fiscal_period, category, allocated_amount
- authority, approval_chain, status, audit_id

## 8. Escalation

- Budget overrun (per-category) → Iris investigates → Janus approves reallocation
- Budget deficit (total) → Janus convenes emergency review → Sage risk assessment → Hung Vuong approval
- Unauthorized spending → Sage audit → Janus disciplinary review
- Disputed allocation → Escalate to Hung Vuong for final decision

## 9. References

- AK_KINGDOM_BUDGET_LAW_v1.0_FINAL.md §3-5
- AK_TREASURY_CHARTER_v1.0_FINAL.md §5
- docs/schemas/kingdom_budget_schema.json
- data/treasury/kingdom_budget.json
