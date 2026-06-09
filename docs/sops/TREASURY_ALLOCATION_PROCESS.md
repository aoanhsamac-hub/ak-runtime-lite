# Treasury Allocation Process — SOP

**Status:** FINAL
**Authority:** AK_KINGDOM_BUDGET_LAW_v1.0_FINAL, AK_TREASURY_CHARTER_v1.0_FINAL
**Owner:** Iris
**Reviewer:** Sage
**Approver:** Janus

---

## 1. Purpose

Standard operating procedure for allocating revenue between Kingdom Treasury (92%) and Royal Treasury (8%) via the automated allocation engine.

## 2. Authority

| Role | Authority |
|------|-----------|
| Iris | Trigger allocation after revenue ingestion |
| Janus | Oversee allocation integrity |
| Sage | Audit allocation records |

## 3. Process Flow

```
Revenue Recorded (status: RECORDED)
    ↓
1. Iris validates revenue record is ready for allocation
    ↓
2. treasury_allocation_engine.allocate() called
    ↓
3. Revenue amount validated (must be positive)
    ↓
4. 92% calculated → Kingdom Treasury
    ↓
5. 8% calculated → Royal Treasury
    ↓
6. Remainder check → any rounding goes to Kingdom Treasury
    ↓
7. Two transaction records created:
    - Kingdom Treasury: TXN-{YEAR}-{NNNN}
    - Royal Treasury: TXN-{YEAR}-{NNNN}
    ↓
8. Audit ID generated (AUDIT-ALLOC-{timestamp})
    ↓
9. Records written to:
    - data/treasury/kingdom_treasury.json
    - data/treasury/royal_treasury.json
    ↓
10. Allocation result returned with breakdown
```

## 4. Validation

- Revenue amount must be positive
- Kingdom Treasury share: 92%
- Royal Treasury share: 8%
- Sum of shares must equal original revenue amount
- Any remainder from rounding goes to Kingdom Treasury
- Each allocation must reference source revenue_id

## 5. Approval Chain

| Action | Approval Required |
|--------|-------------------|
| Standard allocation (< 10,000) | Iris |
| Large allocation (10,000 - 100,000) | Iris + Janus |
| Extraordinary allocation (> 100,000) | Iris + Janus + Sage |

## 6. Audit Trail

Each allocation record must include:
- transaction_id, timestamp, from_account, to_account
- amount, transaction_type, reference (revenue_id)
- authority, approval_chain, status, audit_id
- created_at, updated_at

## 7. Escalation

- Allocation failure → Iris manually verifies → Janus resolves
- Split discrepancy → Sage audit of allocation engine
- Royal Treasury allocation error → Hung Vuong notified

## 8. References

- AK_KINGDOM_BUDGET_LAW_v1.0_FINAL.md §2
- AK_TREASURY_CHARTER_v1.0_FINAL.md §4
- AK_ROYAL_TREASURY_CHARTER_v1.0_FINAL.md §3
- docs/schemas/treasury_transaction_schema.json
- services/treasury_allocation_engine.py
- data/treasury/kingdom_treasury.json
- data/treasury/royal_treasury.json
