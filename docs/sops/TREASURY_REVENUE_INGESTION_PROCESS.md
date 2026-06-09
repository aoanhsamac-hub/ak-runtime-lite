# Treasury Revenue Ingestion Process — SOP

**Status:** FINAL
**Authority:** AK_KINGDOM_BUDGET_LAW_v1.0_FINAL, AK_TREASURY_CHARTER_v1.0_FINAL
**Owner:** Iris
**Reviewer:** Sage
**Approver:** Janus

---

## 1. Purpose

Standard operating procedure for ingesting, validating, and recording national revenue events via the automated revenue ingestion service.

## 2. Authority

| Role | Authority |
|------|-----------|
| Iris | Operate revenue ingestion, validate source/category |
| Janus | Approve revenue recognition, resolve disputes |
| Sage | Audit revenue ingestion records |

## 3. Process Flow

```
Revenue Event Detected
    ↓
1. Iris prepares revenue data (source, category, amount, authority)
    ↓
2. Validate source (must be from approved list of 11)
    ↓
3. Validate category (Operating/Capital/Extraordinary)
    ↓
4. Validate amount (must be positive)
    ↓
5. Validate authority (must be identified)
    ↓
6. treasury_revenue_ingestion.ingest_revenue() called
    ↓
7. Revenue record created with REV-{YEAR}-{NNNN} ID
    ↓
8. Audit ID generated (AUDIT-REV-{timestamp})
    ↓
9. Record written to data/treasury/kingdom_revenue.json
    ↓
10. Revenue status set to RECORDED
    ↓
11. Allocation trigger: treasury_allocation_engine.allocate()
```

## 4. Validation

- Source must be from: Trading, Investment, Service, Technology, Licensing, Consulting, Education, Content, E-Commerce, Infrastructure, Other
- Category must be: Operating, Capital, or Extraordinary
- Amount must be positive numeric value
- Authority must be a non-empty string
- Revenue ID auto-generated with sequential format

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

- Invalid source → Iris recategorizes → Janus approves
- Negative or zero amount → Returned for correction
- Unidentified authority → Escalate to Janus
- Ingestion service failure → Fallback to manual TREASURY_REVENUE_PROCESS.md

## 8. References

- AK_KINGDOM_BUDGET_LAW_v1.0_FINAL.md §1
- AK_TREASURY_CHARTER_v1.0_FINAL.md §4
- docs/schemas/kingdom_revenue_schema.json
- services/treasury_revenue_ingestion.py
- data/treasury/kingdom_revenue.json
- docs/sops/TREASURY_REVENUE_PROCESS.md
