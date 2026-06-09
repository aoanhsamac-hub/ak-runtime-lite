# AK Capability Connectivity Report

Date: 2026-06-07 | Authority: Janus Directive — AK-SANDBOX-READINESS & LEGACY LEARNING MIGRATION AUDIT v1.0

## Registry Connectivity Status

| Registry | Connected To | Method | Status |
|---|---|---|---|
| Capability Usage | Capability ROI | record_capability_usage → calculate_roi | CONNECTED |
| Capability ROI | Capability Usage | get_capability_usage + get_capability_roi | CONNECTED |
| Agent Performance | — | record_agent_performance | STANDALONE |
| Evidence | Lesson Candidate | record_evidence → record_lesson_candidate | CONNECTED |
| Lesson Candidate | Lesson | promote_lesson_candidate | CONNECTED |
| Lesson | Knowledge | promote_to_knowledge | CONNECTED |
| Knowledge | Skill | promote_to_skill | CONNECTED |
| Skill | Capability | promote_to_capability | CONNECTED |

## Economy Assessment

| Dimension | Status |
|---|---|
| Usage tracking | CONNECTED |
| ROI calculation | CONNECTED |
| Performance recording | CONNECTED |
| Evidence → Lesson → Capability | CONNECTED |
| Agent adoption status | NOT_TRACKED (pending capability activation) |

Capability Economy Status: **PARTIALLY_CONNECTED**

Note: Agent adoption status is currently `not_tracked` because no capability has been activated beyond DISABLED. Full CONNECTED status requires HUNG_VUONG approval for capability activation.
