# Treasury Revenue Process — SOP

**Status:** FINAL
**Authority:** AK_KINGDOM_BUDGET_LAW_v1.0_FINAL, AK_TREASURY_CHARTER_v1.0_FINAL
**Owner:** Iris
**Reviewer:** Sage
**Approver:** Janus

---

## 1. Purpose

Standard operating procedure for recording, verifying, and settling national revenue.

## 2. Authority

| Role | Authority |
|------|-----------|
| Iris | Record revenue, verify source |
| Janus | Approve revenue recognition |
| Sage | Audit revenue records |

## 3. Process Flow

```
Revenue Event
    ↓
1. Iris identifies revenue source
    ↓
2. Iris records revenue in kingdom_revenue.json
    ↓
3. Iris classifies source per Budget Law §1
    ↓
4. Janus verifies revenue classification
    ↓
5. If amount > threshold: Sage audit required
    ↓
6. Revenue status set to VERIFIED
    ↓
7. Revenue deposited to Kingdom Treasury
    ↓
8. Audit record created
```

## 4. Validation Rules

- Revenue source must be from approved list (Budget Law §1)
- Amount must be positive
- Authority must be identified
- Each revenue record must have audit_id

## 5. Approval Chain

| Amount Range | Approval Required |
|-------------|-------------------|
| < 1,000 | Iris only |
| 1,000 - 10,000 | Iris + Janus |
| 10,000 - 100,000 | Iris + Janus + Sage |
| > 100,000 | Iris + Janus + Sage + Hung Vuong |

## 6. Audit Trail

Each revenue record must include:
- revenue_id, timestamp, source, category, amount
- authority, reference, status, audit_id
- created_at, updated_at

## 7. Escalation

- Disputed revenue → Iris investigates → Janus resolves
- Unidentified source → Escalate to Janus → Hung Vuong if persistent
- Reconciliation failure → Sage audit

## 8. References

- AK_KINGDOM_BUDGET_LAW_v1.0_FINAL.md §1
- AK_TREASURY_CHARTER_v1.0_FINAL.md §4
- docs/schemas/kingdom_revenue_schema.json
- data/treasury/kingdom_revenue.json
