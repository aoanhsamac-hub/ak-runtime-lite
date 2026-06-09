# Kingdom Situation Room Process — SOP

**Status:** FINAL
**Authority:** Janus Charter v1.0 FINAL, PNSRR Certification
**Owner:** Janus
**Operator:** Iris
**Reviewer:** Sage

---

## 1. Purpose

Standard operating procedure for the Kingdom Situation Room — a unified national awareness layer providing accurate, auditable status and health monitoring across all AK domains.

## 2. Authority

| Role | Authority |
|------|-----------|
| Iris | Operate Situation Room services, generate reports |
| Janus | Oversee national awareness, review status reports |
| Sage | Audit Situation Room integrity, validate health data |

## 3. Data Sources

### Registries
- KINGDOM_HEALTH_REGISTRY.yaml — 8 health domains with scores
- KINGDOM_STATUS_REGISTRY.yaml — 8 status domains
- TREASURY_HEALTH_REGISTRY.yaml — treasury-specific health
- TREASURY_STATUS_REGISTRY.yaml — treasury-specific status
- agents/registry.yaml — agent configuration

### Services
- governance_health_monitor — charter/registry compliance
- agent_status_monitor — 7 agent operational status
- capability_health_monitor — capability maturity/adoption
- knowledge_health_monitor — knowledge registry integrity
- treasury_status_monitor — treasury health aggregation
- security_status_monitor — security posture assessment
- kingdom_status_aggregator — unified status aggregation
- kingdom_health_aggregator — unified health aggregation

## 4. Refresh Cycle

| Cycle | Frequency | Action |
|-------|-----------|--------|
| Health check | Daily | All 8 domain health monitors run; KINGDOM_HEALTH_REGISTRY updated |
| Status aggregation | Daily | kingdom_status_aggregator.aggregate_all() run |
| Health aggregation | Daily | kingdom_health_aggregator.aggregate_health() run |

## 5. Reporting Cycle

| Report | Frequency | Owner | Reviewer | Approver |
|--------|-----------|-------|----------|----------|
| Kingdom Status Report | Weekly | Iris | Janus | Hung Vuong |
| Kingdom Health Report | Weekly | Iris | Sage | Hung Vuong |
| Treasury Health Report | Monthly | Iris | Janus | Sage |
| Treasury Report | Monthly | Iris | Janus | Hung Vuong |

## 6. Escalation Process

| Status Level | Response |
|-------------|----------|
| HEALTHY | Continue monitoring |
| WATCH | Iris flags to Janus; next cycle monitors |
| WARNING | Janus convenes review; Sage audit triggered |
| CRITICAL | Immediate escalation: Janus → Sage → Hung Vuong |

### Escalation Actions
- WARNING: Domain owner notified, remediation plan required within 7 days
- CRITICAL: Full audit triggered, Hung Vuong notified within 1 hour

## 7. Audit Process

Each Situation Room cycle must record:
- Cycle timestamp and duration
- All 8 domain statuses before/after
- Findings from each health check
- Escalations triggered (if any)
- Reports generated

## 8. Process Flow

```
Daily Cycle Start
    ↓
1. Run all domain health monitors (8 services)
    ↓
2. Run kingdom_status_aggregator.aggregate_all()
    ↓
3. Run kingdom_health_aggregator.aggregate_health()
    ↓
4. Check for WARNING/CRITICAL statuses
    ↓
5. If WARNING/CRITICAL: Follow escalation process
    ↓
6. Update registries with results
    ↓
7. If weekly: Generate Kingdom Status Report + Health Report
    ↓
8. Log cycle to audit trail
    ↓
Daily Cycle End
```

## 9. Validation

- All health monitors must return status + score
- All aggregators must update their respective registries
- Escalation must be documented for any WARNING/CRITICAL status
- Reports must use actual data only (no fabrication)

## 10. References

- docs/registries/KINGDOM_HEALTH_REGISTRY.yaml
- docs/registries/KINGDOM_STATUS_REGISTRY.yaml
- services/kingdom_status_aggregator.py
- services/kingdom_health_aggregator.py
- services/governance_health_monitor.py
- services/agent_status_monitor.py
- services/capability_health_monitor.py
- services/knowledge_health_monitor.py
- services/treasury_status_monitor.py
- services/security_status_monitor.py
- docs/templates/KINGDOM_STATUS_REPORT_TEMPLATE.md
- docs/templates/KINGDOM_HEALTH_REPORT_TEMPLATE.md
