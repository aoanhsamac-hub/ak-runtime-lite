# Lesson Production Pipeline

**Directive:** WP-KP-01 Phase 3
**Date:** 2026-06-07
**Status:** FINAL

---

## 1. Purpose

Define how lessons are automatically extracted from approved decision traces.

## 2. Pipeline Flow

```
Approved Decision Trace
        │
        ▼
┌───────────────────┐
│ Extract Evidence  │ ← decision, reasoning, evidence, outcome
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│  Build Lesson     │ ← title, summary, content, source
│  Content          │ ← owner_agent, risk_level, tags
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│ Record in Registry│ ← LessonRegistry.create_candidate()
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│     CANDIDATE     │ ← status="DRAFT"
└───────┬───────────┘
        │ Sage evaluates
        ▼
┌───────────────────┐
│     REVIEWED      │ ← status="REVIEWED"
└───────┬───────────┘
        │ Sage + Janus approve
        ▼
┌───────────────────┐
│     APPROVED      │ ← status="APPROVED"
└───────────────────┘
```

## 3. Evidence Requirements

Lessons MUST be extracted from approved decision traces. Artificial lesson generation is FORBIDDEN.

| Field | Required | Source |
|-------|----------|--------|
| `title` | Yes | Auto-generated from trace.decision |
| `summary` | Yes | trace.outcome |
| `content` | Yes | Structured from trace fields |
| `source` | Yes | `trace:{trace_id}` |
| `owner_agent` | Yes | Agent that created the lesson |
| `reviewer_agent` | Yes | "Sage" (default) |
| `risk_level` | Yes | Inherited from trace |

## 4. Implementation

**Module:** `pipelines/lesson_production/pipeline.py`
**Class:** `LessonProductionPipeline`

| Method | Description |
|--------|-------------|
| `extract_from_trace(trace_id, owner_agent)` | Extract lesson from approved trace |
| `submit_for_review(lesson_id, reviewer)` | Submit for governance review |
| `approve(lesson_id, reviewer)` | Approve after governance review |

## 5. Gates

| Gate | Stage | Authority |
|------|-------|-----------|
| Trace must be APPROVED | Pre-extraction | Pipeline (automated) |
| Quality evaluation | CANDIDATE → REVIEWED | Sage |
| Approval | REVIEWED → APPROVED | Sage + Janus |

## 6. Dependencies

- `pipelines/decision_trace/pipeline.py` — Decision trace production
- `memory/lesson_registry.py` — Lesson storage
- `memory/decision_trace_registry.py` — Trace lookup
- `learning/lesson_evaluator.py` — Quality evaluation

---

*End of Lesson Production Pipeline.*
