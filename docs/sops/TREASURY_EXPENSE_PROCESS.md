# Treasury Expense Process — SOP

**Status:** FINAL
**Authority:** AK_KINGDOM_BUDGET_LAW_v1.0_FINAL, AK_TREASURY_CHARTER_v1.0_FINAL
**Owner:** Iris
**Reviewer:** Sage
**Approver:** Janus

---

## 1. Purpose

Standard operating procedure for approving, recording, and settling national expenses.

## 2. Authority

| Role | Authority |
|------|-----------|
| Proposer | Any agent |
| Iris | Review and validate expense |
| Janus | Approve expense within budget |
| Sage | Audit expense compliance |

## 3. Process Flow

```
Expense Request
    ↓
1. Agent submits expense request with justification
    ↓
2. Iris validates: within budget? correct category?
    ↓
3. If valid: Janus approves
    ↓
4. If budget check fails: Sage review
    ↓
5. Expense recorded in kingdom_expenses.json
    ↓
6. Payment executed (authorized)
    ↓
7. Audit record created
```

## 4. Validation Rules

- Must have approved budget line item
- Category must match Budget Law §3
- Amount must not exceed remaining budget
- Authority chain must be complete

## 5. Approval Chain

| Amount Range | Approval Required |
|-------------|-------------------|
| < 500 | Iris only |
| 500 - 5,000 | Iris + Janus |
| 5,000 - 50,000 | Iris + Janus + Sage |
| > 50,000 | Iris + Janus + Sage + Hung Vuong |

## 6. Audit Trail

Each expense record must include:
- expense_id, timestamp, category, amount
- authority, budget_line, status, audit_id
- vendor, description

## 7. Escalation

- Budget exceeded → Iris flags → Janus reallocates → Sage approves
- Unauthorized expense → Yet Kieu investigation → Sage review
- Payment failure → Iris investigates → Janus resolution

## 8. References

- AK_KINGDOM_BUDGET_LAW_v1.0_FINAL.md §3, §5
- AK_TREASURY_CHARTER_v1.0_FINAL.md §5
- docs/schemas/kingdom_expense_schema.json
- data/treasury/kingdom_expenses.json
