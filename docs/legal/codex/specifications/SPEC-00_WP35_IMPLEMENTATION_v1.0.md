# WP3.5 Implementation Specification

This specification defines future modules only. It does not create runtime code, databases, registries, tests, or memory backends.

## Lesson Evaluator

Purpose: Score lesson candidates for quality, reuse, danger, and promotion eligibility.

Inputs: lesson candidate, decision trace references, evidence records, risk classification.

Outputs: quality score, risk flags, eligibility recommendation, required reviewers.

Dependencies: MemoryInterface, lesson registry, decision trace registry, Governance Gate, Hermes review, Sage review.

Governance Requirements: No autonomous promotion. Sage review required for high-risk or protected-domain lessons.

Failure Modes: false positive quality, missed secret risk, overgeneralization, incomplete evidence.

Test Requirements: deterministic scoring, risk penalty, disqualification rules, protected-domain reviewer requirement.

Acceptance Criteria: evaluator produces explainable score and never changes lesson lifecycle without governance approval.

## Skill Discovery

Purpose: Detect evidence-backed skill candidates from approved lessons.

Inputs: approved lessons, reviewed traces, pattern clusters, risk data.

Outputs: skill candidate, confidence score, evidence references, rejection reason if insufficient.

Dependencies: lesson registry, skill registry, Hermes distillation, Sage risk review.

Governance Requirements: minimum evidence thresholds, reviewer confirmation, no direct activation.

Failure Modes: coincidence treated as skill, weak evidence, duplicate skill, unsafe scope.

Test Requirements: threshold enforcement, rejected patterns, confidence calculation, governance review requirement.

Acceptance Criteria: skill candidate emerges from evidence and remains Draft until reviewed.

## Capability Evolution

Purpose: Detect capability candidates from approved or active skills.

Inputs: approved skills, active skills, reviewed traces, performance deltas, cross-agent reuse data.

Outputs: capability candidate, maturity level, confidence score, required approval path.

Dependencies: skill registry, capability registry, learning metrics, Governance Gate.

Governance Requirements: Sage review and Hung Vuong approval for constitutional, governance, security, or execution-adjacent capabilities.

Failure Modes: capability overclaim, insufficient skill base, stale evidence, unsafe activation.

Test Requirements: maturity transition validation, evidence count, rollback readiness, highest-risk classification.

Acceptance Criteria: capability remains recommendation-only and cannot grant authority.

## Cross Agent Learning

Purpose: Allow approved knowledge from one agent to benefit other agents after Hermes distillation and governance review.

Inputs: approved lessons, active skills, active capabilities, ownership metadata, review state.

Outputs: cross-agent recommendation, applicable agents, isolation restrictions, quarantine flags.

Dependencies: AgentMemoryClient, MemoryInterface, Hermes, Sage, role boundaries.

Governance Requirements: no unreviewed cross-agent propagation; protected records require Sage review.

Failure Modes: leakage, wrong target agent, role boundary violation, unsafe recommendation.

Test Requirements: ownership enforcement, isolation enforcement, quarantine enforcement, approved-only sharing.

Acceptance Criteria: only approved and safe knowledge is shared; drafts stay isolated.

## Learning Metrics

Purpose: Measure whether AK is improving decision quality and reuse.

Inputs: lesson scores, skill counts, capability maturity, reuse events, review outcomes, quarantine rates.

Outputs: agent metrics, system metrics, reuse metrics, capability growth metrics, learning score.

Dependencies: existing memory records, audit records, review states.

Governance Requirements: metrics are advisory and cannot trigger promotion automatically.

Failure Modes: metric gaming, misleading aggregate score, stale data.

Test Requirements: deterministic formulas, missing data handling, no automatic promotion trigger.

Acceptance Criteria: metrics explain system learning without modifying behavior.

## Behavior Improvement

Purpose: Generate ranked recommendations from decision traces, lessons, skills, and capabilities.

Inputs: current task context, approved knowledge, active skills/capabilities, risk classification.

Outputs: recommendation, rank, confidence, evidence, required reviewers, governance status.

Dependencies: MemoryInterface, Governance Gate, promotion state, role boundaries.

Governance Requirements: recommendation-only; protected changes require Sage review.

Failure Modes: wrong recommendation, low confidence recommendation, unsafe protected-surface advice.

Test Requirements: rank calculation, confidence threshold, protected-domain block/review requirement.

Acceptance Criteria: recommendations are explainable, auditable, and never self-executing.

## Promotion Governance

Purpose: Enforce lifecycle transitions and review gates for lessons, skills, and capabilities.

Inputs: candidate record, scores, evidence, reviewers, approvers, risk classification.

Outputs: promotion decision, rejection reason, rollback requirement, audit event.

Dependencies: Governance Gate, approval matrix, audit engine, Hermes, Sage, Hung Vuong approval for high risk.

Governance Requirements: no self-approval, no autonomous promotion, highest-risk wins.

Failure Modes: missing reviewer, incorrect approval path, rollback not available, unsafe activation.

Test Requirements: transition validation, rejection workflow, rollback workflow, audit append.

Acceptance Criteria: promotion decisions are governed, auditable, reversible, and recommendation-only.
