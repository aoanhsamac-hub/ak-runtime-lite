# Alkasik Kingdom Skill Taxonomy Model

**Status:** SUPERSEDED
**Superseded By:** `docs/legal/codex/standards/STD-02_SKILL_TAXONOMY_v1.0.md`
**Supersession Date:** 2026-06-07
**Rationale:** Design content promoted to canonical codex standard. This document retained for design traceability.

## Purpose

Define skill normalization, merge, taxonomy, anti-explosion, and anti-fragmentation controls.

## Cross References

- `docs/design/AK_SKILL_DISCOVERY_MODEL.md`
- `docs/design/AK_PROMOTION_GOVERNANCE_MODEL.md`
- `docs/design/AK_CAPABILITY_EVOLUTION_MODEL.md`
- `docs/architecture/AK_LEARNING_INTELLIGENCE_ARCHITECTURE.md`

## Taxonomy Structure

Skill records should classify into:

```text
domain
task_pattern
trigger_condition
method
evidence_scope
risk_class
applicable_agents
limitations
```

## Normalization

Normalization converts overlapping skill candidates into canonical names and categories.

Normalization requirements:

- Canonical skill name.
- Clear domain.
- Unique trigger condition.
- Evidence references.
- Scope boundaries.
- Risk classification.

## Merge

Skill merge is allowed when candidates share:

- Same domain.
- Same task pattern.
- Compatible trigger conditions.
- Compatible evidence.
- Same or compatible risk class.

Skill merge is blocked when:

- Evidence conflicts.
- Risk class differs and Sage has not reviewed.
- Candidate scope is too broad.
- Candidate would grant new authority.

## Anti-Explosion Controls

Prevent skill explosion by requiring:

- Minimum approved lesson count.
- Similarity check against existing canonical skills.
- Reviewer challenge before new skill creation.
- Retirement of unused duplicate candidates.

## Anti-Fragmentation Controls

Prevent fragmentation by:

- Merging semantically equivalent candidates.
- Rejecting overly narrow skills.
- Maintaining canonical taxonomy categories.
- Recording aliases under canonical skill records.

## Governance Review

Hermes reviews evidence and taxonomy quality.
Sage reviews risk class and protected-domain implications.
Domain reviewer confirms applicability.

## Final Rule

Skills are evidence-backed patterns. Skills are not permissions and do not expand role authority.
