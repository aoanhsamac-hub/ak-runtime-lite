# Treasury Audit Process — SOP

**Status:** FINAL
**Authority:** AK_TREASURY_CHARTER_v1.0_FINAL, AK_ROYAL_TREASURY_CHARTER_v1.0_FINAL
**Owner:** Sage
**Operator:** Sage
**Reviewer:** Janus

---

## 1. Purpose

Standard operating procedure for treasury auditing and compliance verification.

## 2. Authority

| Role | Authority |
|------|-----------|
| Sage | Lead treasury audits |
| Iris | Provide treasury data |
| Janus | Review audit findings |
| Hung Vuong | Approve audit resolution |

## 3. Audit Types

### Monthly Audit
- Revenue reconciliation
- Expense verification
- Budget execution check
- Reserve level check

### Quarterly Audit
- Full treasury review
- Revenue trend analysis
- Budget variance analysis
- Reserve adequacy assessment
- Compliance verification

### Annual Audit
- Full financial audit
- Revenue integrity verification
- Treasury governance review
- Charter compliance check
- External auditor review (Hung Vuong-appointed)

### Event-Driven Audit
- Emergency drawdown audit (within 7 days)
- Disputed transaction review
- Security incident review (with Yet Kieu)
- Governance violation investigation

## 3. Process Flow

```
Audit Trigger
    ↓
Sage defines audit scope
    ↓
Iris provides treasury data
    ↓
Sage reviews records against schemas
    ↓
Sage verifies authority chains
    ↓
Sage checks compliance
    ↓
Audit findings documented
    ↓
Janus reviews findings
    ↓
Hung Vuong approves resolution
    ↓
Remediation tracking
```

## 4. Validation

- Every treasury record must have audit_id
- Audit trail must be complete and unbroken
- All authority chains must be documented
- Schema validation on all records

## 5. Approval Chain

| Stage | Role |
|-------|------|
| Lead auditor | Sage |
| Data provider | Iris |
| Finding reviewer | Janus |
| Resolution approver | Hung Vuong |
| Remediation tracker | Sage |

## 6. Audit Trail

Each audit record must include:
- audit_id, audit_type, audit_date, scope
- findings, severity, status, resolution
- lead_auditor, reviewer, approver
- created_at, updated_at, next_audit_date

## 7. Audit Findings Classification

| Severity | Definition | Response Time |
|----------|-----------|---------------|
| CRITICAL | Law or charter violation | Immediate |
| HIGH | Significant compliance gap | 7 days |
| MEDIUM | Process deviation | 30 days |
| LOW | Documentation issue | 90 days |

## 9. Escalation

- CRITICAL finding → Sage notifies Janus → Hung Vuong informed
- Repeated HIGH findings → Janus review → Process improvement
- Governance violation → Sage escalates to Hung Vuong

## 10. References

- AK_TREASURY_CHARTER_v1.0_FINAL.md §7
- AK_ROYAL_TREASURY_CHARTER_v1.0_FINAL.md §8
- docs/schemas/* (all schemas)
- docs/registries/TREASURY_STATUS_REGISTRY.yaml
