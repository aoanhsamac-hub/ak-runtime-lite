# Treasury Health Report — {{DATE}}

**Date:** {{REPORT_DATE}}
**Author:** Iris
**Reviewer:** Janus
**Status:** {{DRAFT|REVIEW|APPROVED}}

---

## 1. Overall Treasury Health

| Category | Status | Score | Trend |
|----------|--------|-------|-------|
| Revenue Health | {{HEALTHY|WATCH|WARNING|CRITICAL}} | {{SCORE}}/100 | {{UP|DOWN|STABLE}} |
| Treasury Health | {{HEALTHY|WATCH|WARNING|CRITICAL}} | {{SCORE}}/100 | {{UP|DOWN|STABLE}} |
| Budget Health | {{HEALTHY|WATCH|WARNING|CRITICAL}} | {{SCORE}}/100 | {{UP|DOWN|STABLE}} |
| Reserve Health | {{HEALTHY|WATCH|WARNING|CRITICAL}} | {{SCORE}}/100 | {{UP|DOWN|STABLE}} |
| Audit Health | {{HEALTHY|WATCH|WARNING|CRITICAL}} | {{SCORE}}/100 | {{UP|DOWN|STABLE}} |
| **Overall** | **{{STATUS}}** | **{{SCORE}}/100** | |

---

## 2. Revenue Health

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Total Revenue | {{AMOUNT}} | {{TARGET}} | {{HEALTHY|WATCH|WARNING|CRITICAL}} |
| Revenue Sources Active | {{COUNT}}/11 | ≥ 5 | {{HEALTHY|WATCH|WARNING|CRITICAL}} |
| Revenue Growth (MoM) | {{X%}} | > 0% | {{HEALTHY|WATCH|WARNING|CRITICAL}} |
| Collection Rate | {{X%}} | ≥ 95% | {{HEALTHY|WATCH|WARNING|CRITICAL}} |

## 3. Treasury Health

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Kingdom Treasury Balance | {{AMOUNT}} | {{MINIMUM}} | {{HEALTHY|WATCH|WARNING|CRITICAL}} |
| Royal Treasury Balance | {{AMOUNT}} | {{MINIMUM}} | {{HEALTHY|WATCH|WARNING|CRITICAL}} |
| Fund Allocation Rate | {{X%}} | 100% | {{HEALTHY|WATCH|WARNING|CRITICAL}} |
| Transaction Volume | {{COUNT}} | {{TARGET}} | {{HEALTHY|WATCH|WARNING|CRITICAL}} |

## 4. Budget Health

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Budget Execution Rate | {{X%}} | 80-100% | {{HEALTHY|WATCH|WARNING|CRITICAL}} |
| Budget Variance | {{X%}} | ±10% | {{HEALTHY|WATCH|WARNING|CRITICAL}} |
| Underspend Rate | {{X%}} | < 20% | {{HEALTHY|WATCH|WARNING|CRITICAL}} |
| Overspend Rate | {{X%}} | 0% | {{HEALTHY|WATCH|WARNING|CRITICAL}} |

## 5. Reserve Health

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Strategic Reserve Ratio | {{X}} months | ≥ 3 months | {{HEALTHY|WATCH|WARNING|CRITICAL}} |
| Emergency Reserve Ratio | {{X}} months | ≥ 1 month | {{HEALTHY|WATCH|WARNING|CRITICAL}} |
| Reserve Drawdown Count | {{COUNT}} | 0 | {{HEALTHY|WATCH|WARNING|CRITICAL}} |
| Replenishment Rate | {{X%}} | 100% | {{HEALTHY|WATCH|WARNING|CRITICAL}} |

## 6. Audit Health

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Audit Completion Rate | {{X%}} | 100% | {{HEALTHY|WATCH|WARNING|CRITICAL}} |
| Finding Count | {{COUNT}} | ≤ 5 | {{HEALTHY|WATCH|WARNING|CRITICAL}} |
| Critical Findings | {{COUNT}} | 0 | {{HEALTHY|WATCH|WARNING|CRITICAL}} |
| Remediation Rate | {{X%}} | ≥ 90% | {{HEALTHY|WATCH|WARNING|CRITICAL}} |

---

## 7. Critical Alerts

{{LIST_OF_CRITICAL_WARNINGS_OR_NONE}}

## 8. Recommendations

1. {{RECOMMENDATION}}
2. {{RECOMMENDATION}}
3. {{RECOMMENDATION}}

---

**Next check:** {{NEXT_CHECK_DATE}}
