# AK Operational Memory Flow Report

Date: 2026-06-07 | Authority: Janus Directive — AK-SANDBOX-READINESS & LEGACY LEARNING MIGRATION AUDIT v1.0

## Lifecycle Chain

| Step | Source | Target | Method | Status |
|---|---|---|---|---|
| 1 | Mission | Evidence | record_mission → record_evidence | VERIFIED |
| 2 | Evidence | Lesson Candidate | record_evidence → record_lesson_candidate | VERIFIED |
| 3 | Lesson Candidate | Lesson (approved) | promote_lesson_candidate | VERIFIED |
| 4 | Lesson | Knowledge | promote_to_knowledge | VERIFIED |
| 5 | Knowledge | Skill | promote_to_skill | VERIFIED |
| 6 | Skill | Capability | promote_to_capability | VERIFIED |
| 7 | Capability | Usage | record_capability_usage | VERIFIED |
| 8 | Capability | ROI | record_capability_roi | VERIFIED |

## Table Reference

All records stored in 13 LanceDB tables via NationalMemoryPlatform:

| Table | Records | Retention |
|---|---|---|
| ak_evidence | Evidence items | OPERATIONAL |
| ak_lesson_candidates | Draft lessons | OPERATIONAL |
| ak_lessons | Approved lessons | OPERATIONAL |
| ak_knowledge | Canonical knowledge | CANONICAL |
| ak_skills | Canonical skills | CANONICAL |
| ak_capabilities | Canonical capabilities | CANONICAL |
| ak_capability_usage | Usage logs | OPERATIONAL |
| ak_capability_roi | ROI records | CANONICAL |
| ak_agent_performance | Performance metrics | OPERATIONAL |
| ak_missions | Mission records | OPERATIONAL |
| ak_council_reviews | Council reviews | CANONICAL |
| ak_audit_events | Audit trail | CANONICAL |
| ak_activation_events | Activation history | CANONICAL |

## Governance

- Unreviewed lesson candidates default to DRAFT status
- Approved promotion (DRAFT→APPROVED) captured by promote_lesson_candidate
- Final governance review requires Sage gate for operational capabilities

Operational Memory Flow: **FULL**
