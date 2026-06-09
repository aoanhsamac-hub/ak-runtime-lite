# Capability Evolution Pipeline

**Directive:** WP-KP-01 Phase 6
**Date:** 2026-06-07
**Status:** FINAL

---

## 1. Purpose

Define how capabilities evolve from accumulated skills.

## 2. Pipeline Flow

```
Multiple Approved/Active Skills
        │
        ▼
┌───────────────────────────────┐
│   Validate Skill Set          │ ← ≥2 skills, all APPROVED or ACTIVE
└───────────┬───────────────────┘
            │ pass
            ▼
┌───────────────────────────────┐
│   Assess Maturity             │ ← EMERGING / DEVELOPING /
│                               │   ESTABLISHED / MATURE
└───────────┬───────────────────┘
            │
            ▼
┌───────────────────────────────┐
│   Build Metrics               │ ← skill_count, active_count,
│                               │   approved_count
└───────────┬───────────────────┘
            │
            ▼
┌───────────────────────────────┐
│   Create Capability Candidate │ ← CapabilityRegistry.create()
└───────────┬───────────────────┘
            │
            ▼
┌───────────────────────────────┐
│          CANDIDATE            │ ← status="DRAFT"
└───────────┬───────────────────┘
            │ Sage reviews
            ▼
┌───────────────────────────────┐
│          APPROVED             │ ← status="APPROVED"
└───────────┬───────────────────┘
            │ Janus activates
            ▼
┌───────────────────────────────┐
│          ACTIVE               │ ← status="ACTIVE"
└───────────────────────────────┘
```

## 3. Maturity Assessment

| Maturity Level | Criteria | Characteristics |
|---------------|----------|-----------------|
| EMERGING | ≥2 approved skills | Initial capability formation |
| DEVELOPING | ≥2 approved, ≥1 active | Active skill usage |
| ESTABLISHED | ≥3 skills, ≥2 active | Reliable capability |
| MATURE | ≥5 skills, ≥3 active | Production-ready capability |

## 4. Implementation

**Module:** `pipelines/capability_evolution/pipeline.py`
**Class:** `CapabilityEvolutionPipeline`

| Method | Description |
|--------|-------------|
| `evolve(name, skill_ids, owner_agent, reviewer_agent)` | Create capability candidate from skill cluster |

## 5. Gates

| Gate | Stage | Authority |
|------|-------|-----------|
| Skill validation | Pre-creation | Pipeline (automated) |
| Governance review | CANDIDATE → APPROVED | Sage + Janus |
| Activation | APPROVED → ACTIVE | Hung Vuong (LEVEL_3+) |

## 6. Dependencies

- `pipelines/skill_discovery/pipeline.py` — Skill pipeline
- `memory/capability_registry.py` — Capability storage
- `memory/skill_registry.py` — Skill lookup

---

*End of Capability Evolution Pipeline.*
