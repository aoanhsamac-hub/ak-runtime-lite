# Dataset Production Pipeline

**Directive:** WP-KP-01 Phase 4
**Date:** 2026-06-07
**Status:** FINAL

---

## 1. Purpose

Define how datasets are produced from validated data sources.

## 2. Pipeline Flow

```
Data Source Reference
        │
        ▼
┌───────────────────┐
│   Validate Source │ ← name, source, owner_agent, risk_level
└───────┬───────────┘
        │ pass
        ▼
┌───────────────────┐
│ Record in Registry│ ← DatasetRegistry.create()
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│     CANDIDATE     │ ← status="DRAFT"
└───────┬───────────┘
        │ Sage reviews
        ▼
┌───────────────────┐
│     APPROVED      │ ← status="APPROVED"
└───────────────────┘
```

## 3. Evidence Requirements

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Human-readable dataset name |
| `source` | Yes | Where the data originates |
| `owner_agent` | Yes | Agent responsible |
| `reviewer_agent` | Yes | Agent for governance review |
| `risk_level` | Yes | Risk classification |
| `metadata` | No | Optional metadata dict |

## 4. Implementation

**Module:** `pipelines/dataset_production/pipeline.py`
**Class:** `DatasetProductionPipeline`

| Method | Description |
|--------|-------------|
| `process(payload)` | Validate source, create dataset candidate |

## 5. Gates

| Gate | Stage | Authority |
|------|-------|-----------|
| Source validation | Pre-creation | Pipeline (automated) |
| Governance approval | CANDIDATE → APPROVED | Sage |

## 6. Dependencies

- `memory/dataset_registry.py` — Dataset storage
- `memory/schemas/records.py` — DatasetRecord schema

---

*End of Dataset Production Pipeline.*
