# Treasury Operational Audit Process — SOP

**Status:** FINAL
**Authority:** AK_TREASURY_CHARTER_v1.0_FINAL, AK_ROYAL_TREASURY_CHARTER_v1.0_FINAL
**Owner:** Sage
**Reviewer:** Janus
**Approver:** Hung Vuong

---

## 1. Purpose

Standard operating procedure for automated treasury auditing, validating revenue, treasury, allocation, reporting, and audit records for integrity and compliance.

## 2. Authority

| Role | Authority |
|------|-----------|
| Sage | Run full audit, interpret findings, lead remediation |
| Iris | Provide treasury data |
| Janus | Review audit findings, approve remediation |
| Hung Vuong | Approve resolution of CRITICAL/HIGH findings |

## 3. Process Flow

```
Audit Trigger (Scheduled or On-Demand)
    ↓
1. Sage initiates treasury_audit_service.run_full_audit()
    ↓
2. Revenue records audited:
    - Check required fields present
    - Check amounts are positive
    - Check audit_ids present
    ↓
3. Treasury records audited:
    - Check required fields present
    - Check transaction integrity
    ↓
4. Allocation records audited:
    - Check 92/8 split integrity
    - Check non-positive amounts
    ↓
5. Reporting records audited:
    - Check registry status
    ↓
6. Audit records audited:
    - Check for duplicate audit_ids
    ↓
7. Findings compiled with severity (LOW/MEDIUM/HIGH/CRITICAL)
    ↓
8. Audit result returned with pass/fail status
    ↓
9. CRITICAL findings → Immediate escalation to Janus + Hung Vuong
```

## 4. Validation

- Every revenue record must have revenue_id, timestamp, source, amount, authority, status, audit_id
- Every treasury transaction must have transaction_id, timestamp, amount, transaction_type, status, audit_id
- Allocation amounts must be positive
- 92/8 split must be within 1% tolerance
- No duplicate audit_ids
- All required fields populated

## 5. Approval Chain

| Severity | Resolution Required |
|----------|-------------------|
| LOW | Sage resolves, logs to Janus |
| MEDIUM | Sage + Janus review |
| HIGH | Sage + Janus + Hung Vuong |
| CRITICAL | Immediate escalation to Hung Vuong |

## 6. Audit Trail

Each audit record must include:
- audit_id, timestamp, total_findings
- critical_count, high_count, medium_count, low_count
- findings list with severity and description
- pass/fail status

## 7. Escalation

- CRITICAL finding → Sage notifies Janus → Hung Vuong informed immediately
- Repeated HIGH findings → Janus review → Process improvement required
- Allocation split violation → Sage escalates to Hung Vuong
- Duplicate audit_ids → Sage forensic investigation

## 8. References

- AK_TREASURY_CHARTER_v1.0_FINAL.md §7
- AK_ROYAL_TREASURY_CHARTER_v1.0_FINAL.md §8
- docs/sops/TREASURY_AUDIT_PROCESS.md
- services/treasury_audit_service.py
- services/treasury_allocation_engine.py
- docs/schemas/treasury_transaction_schema.json
