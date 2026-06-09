# Alkasik Kingdom Lesson Deduplication Model

Status: READY FOR SAGE ROUND 2 REVIEW

## Purpose

Define how lesson deduplication, merge, and compression preserve decision trace, auditability, and lineage.

## Cross References

- `docs/design/AK_LESSON_QUALITY_MODEL.md`
- `docs/design/AK_PROMOTION_GOVERNANCE_MODEL.md`
- `docs/design/AK_BEHAVIOR_IMPROVEMENT_MODEL.md`
- `docs/architecture/AK_LEARNING_INTELLIGENCE_ARCHITECTURE.md`

## Non-Loss Principle

Deduplication must not delete or obscure source records.

Required preservation:

- Original lesson id.
- Source decision trace.
- Owner agent.
- Reviewer agent.
- Evidence references.
- Audit references.
- Merge/compression reason.

## Deduplication

A duplicate lesson is a lesson with substantially identical trigger, reasoning, evidence, and recommendation.

Deduplication allowed when:

- Source trace exists.
- Evidence references are preserved.
- No unresolved contradiction exists between candidate records.
- Hermes confirms semantic overlap.

Deduplication output:

- Canonical lesson reference.
- Duplicate mapping.
- Preserved source lineage.
- Review note.

## Merge

Merge combines compatible lessons into a stronger canonical lesson.

Merge is forbidden when:

- Lessons have conflicting evidence.
- Risk classes differ and Sage has not reviewed.
- Ownership is unclear.
- Any record is quarantined.

Merge output must include:

- Canonical lesson id.
- Merged source ids.
- Evidence union.
- Scope and limits.
- Reviewer decision.

## Compression

Compression summarizes multiple approved lessons into a compact reusable learning record.

Compression must preserve:

- Links to all source lessons.
- Links to decision traces.
- Audit trail.
- Evidence limits.
- Reviewer notes.

Compression cannot create a skill or capability without separate promotion governance.

## Auditability

Every deduplication, merge, or compression decision must be auditable.

Audit record should include:

- Actor.
- Action.
- Target lesson ids.
- Result.
- Issue id if non-trivial.
- Reviewer.

## Quarantine Rules

Quarantine instead of merge when:

- Secret exposure is suspected.
- Governance bypass is recommended.
- Execution/trading/MT5/deployment/broker action is recommended.
- Source lineage is missing.

## Final Rule

Deduplication reduces noise. It never destroys lineage.
