# Decision Trace Pipeline

**Directive:** WP-KP-01 Phase 2
**Date:** 2026-06-07
**Status:** FINAL

---

## 1. Purpose

Define how decision traces are automatically produced from operational agent activity.

## 2. Pipeline Flow

```
Agent Task Completion
        │
        ▼
┌───────────────────┐
│   Validate Input  │ ← decision, reasoning, evidence[], outcome
└───────┬───────────┘
        │ pass
        ▼
┌───────────────────┐
│ Record in Registry│ ← DecisionTraceRegistry.record()
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│     CANDIDATE     │ ← status="DRAFT"
└───────┬───────────┘
        │ Sage reviews
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

| Field | Required | Source |
|-------|----------|--------|
| `agent` | Yes | Agent that made the decision |
| `decision` | Yes | What was decided |
| `reasoning` | Yes | Why the decision was made |
| `evidence` | Yes (≥1 item) | Supporting evidence list |
| `outcome` | Yes | What happened as a result |

## 4. Implementation

**Module:** `pipelines/decision_trace/pipeline.py`
**Class:** `DecisionTracePipeline`

| Method | Description |
|--------|-------------|
| `process(payload)` | Validate input, create trace candidate |
| `submit_for_review(trace_id, reviewer)` | Submit for governance review |
| `approve(trace_id, reviewer)` | Approve after governance review |

## 5. Gates

| Gate | Stage | Authority |
|------|-------|-----------|
| Input validation | Pre-creation | Pipeline (automated) |
| Governance review | CANDIDATE → REVIEWED | Sage |
| Approval | REVIEWED → APPROVED | Sage + Janus |

## 6. Dependencies

- `memory/decision_trace_registry.py` — Record storage
- `memory/schemas/records.py` — DecisionTraceRecord schema

---

*End of Decision Trace Pipeline.*
