# WP35-1C-01-05: Governance & Audit Report

## Governance Gate Results
| Record Type | Passed | Failed | Pass Rate |
|-------------|--------|--------|-----------|
| Signals | 323 | 0 | 100% |
| Insights | 6 | 0 | 100% |
| Candidate Skills | 6 | 0 | 100% |
| **Total** | **335** | **0** | **100%** |

## Governance Gates
Each record is checked against 7 gates:
1. **traceability** — Source fields present (source_kind/source_id/source_hash for signals; source_signal_ids for insights; source_insight_ids + source_signal_ids for skills)
2. **evidence_quality** — Evidence dictionary is non-empty
3. **confidence_threshold** — Confidence score >= 0.3
4. **ownership** — Owner agent is in allowed set
5. **review_authority** — Reviewer agent is in allowed set (Sage, Hermes, Hung Vuong, Admin)
6. **risk_appropriate** — Risk level is a valid value
7. **no_auto_promotion / status_locked** — Status is CANDIDATE (signals/insights) or full lock (skills)

## Audit Trail
| Event | Count |
|-------|-------|
| PIPELINE_RUN | 1 |
| DRY_RUN | 1 |

## Audit Layer Capabilities
- Record events with agent, action, record_type, record_id, details
- Filter by agent, action, record_type
- Get full trail by record_id
- Export to dict
- Clear audit log
- Reject unknown actions
