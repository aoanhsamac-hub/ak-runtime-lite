# National Knowledge Production Roadmap

**Directive:** WP-KP-01 Phase 9
**Date:** 2026-06-07
**Status:** FINAL

---

## 1. Roadmap Overview

```
STAGE 1                 STAGE 2                 STAGE 3
TRACE PRODUCTION        LESSON PRODUCTION        DATASET PRODUCTION
╔═══════════════════╗   ╔═══════════════════╗   ╔═══════════════════╗
║ Agent decisions    ║   ║ Approved traces   ║   ║ Data sources      ║
║ → DecisionTrace    ║ → ║ → LessonRecord    ║ → ║ → DatasetRecord   ║
║ Pipeline active    ║   ║ Pipeline active   ║   ║ Pipeline active   ║
╚═══════════════════╝   ╚═══════════════════╝   ╚═══════════════════╝
        │                        │                        │
        ▼                        ▼                        ▼
╔══════════════════════════════════════════════════════════════════╗
║                        STAGE 4                                  ║
║                   SKILL DISCOVERY                                ║
║     Repeated lessons → Evidence threshold → SkillRecord         ║
║     Pipeline active with governance review                      ║
╚══════════════════════════════════════════════════════════════════╝
        │
        ▼
╔══════════════════════════════════════════════════════════════════╗
║                        STAGE 5                                  ║
║                 CAPABILITY EVOLUTION                             ║
║     Accumulated skills → Maturity assessment → CapabilityRecord ║
║     Pipeline active with sovereign governance                   ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 2. Stage 1 — Trace Production

**Objective:** Begin recording decision traces from agent operational activity.

| Task | Description | Dependencies | Effort |
|------|-------------|--------------|--------|
| 1.1 | Activate DecisionTracePipeline.process() | Pipelines exist, registries operational | 1 day |
| 1.2 | Train agents to submit traces via AgentMemoryClient | Agent integration | 3 days |
| 1.3 | Establish review cadence (Sage reviews traces daily) | Sage availability | Ongoing |
| 1.4 | Measure trace quality and completeness | LearningMetrics | Ongoing |

**Success Metrics:**
- ≥10 decision traces recorded per week
- ≥80% pass evidence validation on first attempt
- All traces reviewed within 48 hours

**Governance Gate:** Sage must review first 10 traces manually before auto-approval workflow.

---

## 3. Stage 2 — Lesson Production

**Objective:** Extract lessons from approved decision traces.

| Task | Description | Dependencies | Effort |
|------|-------------|--------------|--------|
| 2.1 | Activate LessonProductionPipeline.extract_from_trace() | Stage 1 producing approved traces | 1 day |
| 2.2 | Configure quality thresholds in LessonEvaluator | STD-01 parameters | 1 day |
| 2.3 | Establish lesson review process | Sage + Janus availability | Ongoing |
| 2.4 | Measure lesson quality and source diversity | LearningMetrics | Ongoing |

**Success Metrics:**
- ≥5 lessons extracted from first 20 traces
- ≥70% lesson approval rate after review
- Every lesson traceable to source trace_id

**Risk:** Insufficient approved traces — mitigate by ensuring Stage 1 produces ≥10 traces before Stage 2 activation.

**Dependencies:** Stage 1 producing approved traces.

---

## 4. Stage 3 — Dataset Production

**Objective:** Register datasets from validated data sources.

| Task | Description | Dependencies | Effort |
|------|-------------|--------------|--------|
| 3.1 | Activate DatasetProductionPipeline.process() | Pipeline code ready | 1 day |
| 3.2 | Identify initial data sources for registration | Agent input | 3 days |
| 3.3 | Establish risk classification for each dataset | Sage review | 2 days |
| 3.4 | Register and approve initial datasets | Sage approval | Ongoing |

**Success Metrics:**
- ≥3 datasets registered and approved
- Each dataset has validated source and risk level
- Dataset metadata complete per schema

**Risk:** Data sources may not be immediately available — start with documentation sources (design docs, reports).

**Dependencies:** None (independent of Stage 1–2).

---

## 5. Stage 4 — Skill Discovery

**Objective:** Discover skills from patterns of approved lessons.

| Task | Description | Dependencies | Effort |
|------|-------------|--------------|--------|
| 4.1 | Activate SkillDiscoveryPipeline.discover() | Pipeline code ready | 1 day |
| 4.2 | Configure evidence thresholds | STD-02 parameters | 1 day |
| 4.3 | Monitor for repeated lesson patterns | Hermes observation | Ongoing |
| 4.4 | Review and approve skill candidates | Sage + Janus | Ongoing |

**Success Metrics:**
- ≥2 skills discovered from first 15 approved lessons
- Each skill derived from ≥3 lessons with ≥70% success rate
- Skills traceable to source lessons

**Risk:** Insufficient approved lessons — mitigate by ensuring Stage 2 produces ≥15 lessons before Stage 4 activation.

**Dependencies:** Stage 2 producing approved lessons (≥15 recommended).

---

## 6. Stage 5 — Capability Evolution

**Objective:** Evolve capabilities from accumulated skills.

| Task | Description | Dependencies | Effort |
|------|-------------|--------------|--------|
| 5.1 | Activate CapabilityEvolutionPipeline.evolve() | Pipeline code ready | 1 day |
| 5.2 | Monitor skill accumulation for capability candidates | Hermes observation | Ongoing |
| 5.3 | Assess maturity levels | Maturity model per AK_CAPABILITY_EVOLUTION_PIPELINE.md | Ongoing |
| 5.4 | Sovereign approval for capability activation | Hung Vuong | Per capability |

**Success Metrics:**
- ≥1 capability proposed from first 5 approved skills
- Capability maturity assessed using defined levels
- Capability linked to economic system requirements

**Risk:** Insufficient skills — mitigate by ensuring Stage 4 produces ≥5 skills before Stage 5 activation.

**Dependencies:** Stage 4 producing approved skills (≥5 recommended).

---

## 7. Dependency Graph

```
Stage 1 (Trace) ──────────→ Stage 2 (Lesson) ──────────→ Stage 4 (Skill) ──────────→ Stage 5 (Capability)
       │                                                        │
       │                                                        │
       └────────────────────────────────────────────────────────┘
                                  │
                            Stage 3 (Dataset) — independent path
```

| Stage | Depends On | Blocks |
|-------|------------|--------|
| 1 — Trace | None | Stage 2 |
| 2 — Lesson | Stage 1 | Stage 4 |
| 3 — Dataset | None | None (independent) |
| 4 — Skill | Stage 2 | Stage 5 |
| 5 — Capability | Stage 4 | Economic system design |

---

## 8. Risk Register

| Risk | Stage | Probability | Impact | Mitigation |
|------|-------|-------------|--------|------------|
| Insufficient agent activity for traces | 1 | LOW | HIGH | Create task cadence for agents |
| Poor lesson quality | 2 | MEDIUM | MEDIUM | Configure strict quality thresholds |
| Data sources unavailable | 3 | LOW | LOW | Use documentation as initial sources |
| Insufficient lesson patterns for skills | 4 | MEDIUM | HIGH | Set lower initial evidence threshold (≥3 lessons) |
| Sovereign approval bottleneck | 5 | LOW | MEDIUM | Prepare capability packages with full evidence |
| Pipeline produces artificial knowledge | 1–5 | LOW | CRITICAL | Evidence validation in every pipeline step |

---

## 9. Timeline

```
Week 1–2  │ Stage 1: Trace Production           │ ████░░░░░░░░░░░░░░░░░░░░░░
Week 3–4  │ Stage 2: Lesson Production          │ ░░░░████░░░░░░░░░░░░░░░░░░
Week 3–4  │ Stage 3: Dataset Production         │ ░░░░████░░░░░░░░░░░░░░░░░░
Week 5–8  │ Stage 4: Skill Discovery            │ ░░░░░░░░████████░░░░░░░░░░
Week 9–12 │ Stage 5: Capability Evolution       │ ░░░░░░░░░░░░░░░░████████░░
          │                                        ──────────────────────────
          │                                        Month 1          Month 2
```

---

## 10. Success Criteria

| Stage | Success Criterion | Measurement |
|-------|------------------|-------------|
| 1 | Trace production active | ≥10 traces/week, ≥80% validation pass rate |
| 2 | Lesson production active | ≥5 lessons from first 20 traces, ≥70% approval rate |
| 3 | Dataset production active | ≥3 approved datasets |
| 4 | Skill discovery active | ≥2 skills from first 15 approved lessons |
| 5 | Capability evolution active | ≥1 capability from first 5 approved skills |

---

*End of Knowledge Production Roadmap.*
