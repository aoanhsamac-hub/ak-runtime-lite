# Skill Discovery Pipeline

**Directive:** WP-KP-01 Phase 5
**Date:** 2026-06-07
**Status:** FINAL

---

## 1. Purpose

Define how skills are discovered from patterns of repeated successful lessons.

## 2. Pipeline Flow

```
Multiple Approved Lessons
        │
        ▼
┌───────────────────────────────┐
│   Validate Evidence Threshold │ ← ≥3 lessons, ≥70% success rate
└───────────┬───────────────────┘
            │ pass
            ▼
┌───────────────────────────────┐
│   Infer Risk Level            │ ← Maximum from source lessons
└───────────┬───────────────────┘
            │
            ▼
┌───────────────────────────────┐
│   Build Test Cases            │ ← From lesson titles
└───────────┬───────────────────┘
            │
            ▼
┌───────────────────────────────┐
│   Create Skill Candidate      │ ← SkillRegistry.create_candidate()
└───────────┬───────────────────┘
            │
            ▼
┌───────────────────────────────┐
│          CANDIDATE            │ ← status="DRAFT"
└───────────┬───────────────────┘
            │ Sage reviews
            ▼
┌───────────────────────────────┐
│          REVIEWED             │ ← status="REVIEWED"
└───────────┬───────────────────┘
            │ Sage + Janus approve
            ▼
┌───────────────────────────────┐
│          APPROVED             │ ← status="APPROVED"
└───────────┬───────────────────┘
            │ Janus activates
            ▼
┌───────────────────────────────┐
│          ACTIVE               │ ← status="ACTIVE" (operational use)
└───────────────────────────────┘
```

## 3. Evidence Threshold

| Requirement | Value | Rationale |
|-------------|-------|-----------|
| Minimum lessons | 3 | Prevents single-instance skills |
| Success rate threshold | ≥70% | Ensures repeatable success |
| Lessons must be APPROVED | Yes | Only governance-approved evidence |
| Source diversity | Recommended | Multiple agents or contexts |

## 4. Implementation

**Module:** `pipelines/skill_discovery/pipeline.py`
**Class:** `SkillDiscoveryPipeline`

| Method | Description |
|--------|-------------|
| `discover(lesson_ids, owner_agent, skill_name, description)` | Create skill candidate from lesson cluster |
| `submit_for_review(skill_id, reviewer)` | Submit for governance review |
| `approve(skill_id, reviewer)` | Approve after governance review |

## 5. Gates

| Gate | Stage | Authority |
|------|-------|-----------|
| Evidence threshold | Pre-creation | Pipeline (automated) |
| Governance review | CANDIDATE → REVIEWED | Sage |
| Approval | REVIEWED → APPROVED | Sage + Janus |
| Activation | APPROVED → ACTIVE | Janus |

## 6. Dependencies

- `pipelines/lesson_production/pipeline.py` — Lesson pipeline
- `memory/skill_registry.py` — Skill storage
- `memory/lesson_registry.py` — Lesson lookup
- `learning/skill_evidence_policy.py` — Evidence evaluation

---

*End of Skill Discovery Pipeline.*
