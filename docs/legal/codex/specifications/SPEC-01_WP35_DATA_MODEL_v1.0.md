# WP3.5 Data Model Specification

This specification defines future data shapes only. It does not create new registries, databases, or runtime code.

## Lesson Candidate

Fields: lesson_id, owner_agent, source_trace_id, title, context, evidence, outcome, recommendation, risk_level, quality_dimensions, status, created_at, updated_at.

Lifecycle: Draft -> Reviewed -> Approved or Rejected.

Ownership: originating agent owns draft; Hermes owns distillation review.

Review Requirements: Hermes review, Sage review for high risk or protected domain.

Promotion Requirements: complete evidence, quality threshold, no quarantine flag.

Retention Rules: preserve source trace and audit record.

Quarantine Rules: secret exposure, governance bypass, unsafe execution recommendation, missing ownership.

## Approved Lesson

Fields: lesson_id, approved_by, reviewer_agent, approved_at, quality_score, evidence_refs, scope, limitations, reuse_tags.

Lifecycle: Approved -> Retired if contradicted or stale.

Ownership: Hermes maintains knowledge quality; original agent remains source owner.

Review Requirements: periodic stale/contradiction review.

Promotion Requirements: can feed skill discovery only if active and unquarantined.

Retention Rules: never delete; retire with reason.

Quarantine Rules: post-approval security finding or contradicted evidence.

## Skill Candidate

Fields: skill_id, title, pattern, source_lessons, source_traces, confidence, risk_level, applicable_agents, status, created_at.

Lifecycle: Draft -> Reviewed -> Approved -> Active or Rejected.

Ownership: Hermes owns discovery; domain reviewer owns applicability.

Review Requirements: Hermes, Sage, domain reviewer.

Promotion Requirements: evidence threshold, confidence threshold, no unresolved contradiction.

Retention Rules: retain source lessons and rejection/approval history.

Quarantine Rules: unsafe scope, weak evidence, direct execution suggestion, backend bypass.

## Approved Skill

Fields: skill_id, approved_by, activation_status, confidence, evidence_refs, applicable_agents, limits, rollback_plan.

Lifecycle: Approved -> Active -> Retired.

Ownership: Hermes maintains evidence; Sage owns risk re-review.

Review Requirements: activation review before Active.

Promotion Requirements: rollback plan, audit event, no authority expansion.

Retention Rules: preserve all versions and evidence.

Quarantine Rules: unsafe reuse, stale contradiction, governance bypass.

## Capability Candidate

Fields: capability_id, title, source_skills, maturity_level, confidence, benefiting_agents, performance_delta, risk_level, status.

Lifecycle: Draft -> Reviewed -> Approved -> Active or Rejected.

Ownership: Hermes proposes; Sage reviews; Hung Vuong approves high-risk/sovereign capabilities.

Review Requirements: Hermes, Sage, domain reviewer, Hung Vuong when required.

Promotion Requirements: multiple approved skills, reviewed traces, rollback plan.

Retention Rules: preserve maturity transitions.

Quarantine Rules: overclaim, insufficient skills, protected-surface risk without approval.

## Approved Capability

Fields: capability_id, active_status, maturity_level, approved_by, evidence_refs, confidence, scope, limitations, retirement_criteria.

Lifecycle: Approved -> Active -> Retired.

Ownership: governance-controlled; no agent owns unilateral activation.

Review Requirements: periodic performance and risk review.

Promotion Requirements: Active state requires governance approval and no production behavior modification.

Retention Rules: preserve all capability history.

Quarantine Rules: unsafe recommendation, stale or contradicted evidence, unauthorized use.

## Learning Metrics

Fields: metric_id, metric_name, metric_scope, subject_agent, value, calculation_method, source_records, generated_at, reviewer_status.

Lifecycle: Generated -> Reviewed -> Archived.

Ownership: Hermes calculates; Sage reviews risk-sensitive interpretations.

Review Requirements: required before metrics guide promotion decisions.

Promotion Requirements: none; metrics do not promote records.

Retention Rules: preserve calculation inputs and timestamp.

Quarantine Rules: misleading calculation, missing source records, protected data leakage.

## Improvement Recommendation

Fields: recommendation_id, source_capability, target_agent, target_task_type, recommendation_text, confidence, rank, evidence_refs, risk_level, required_reviewers, status.

Lifecycle: Draft -> Reviewed -> Approved Advisory -> Retired.

Ownership: recommendation owner is Hermes or domain reviewer; target agent cannot self-approve.

Review Requirements: Sage for protected/risk recommendations; Hung Vuong for constitutional/sovereign recommendations.

Promotion Requirements: explainable evidence, confidence threshold, audit record.

Retention Rules: preserve recommendation and outcome feedback.

Quarantine Rules: execution/trading/MT5 suggestion, governance bypass, secret exposure, direct backend access.
