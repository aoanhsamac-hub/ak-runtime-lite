# National Knowledge Foundation Roadmap

**Directive:** HERMES-CLEANUP-01 Phase 7
**Date:** 2026-06-07
**Status:** ROADMAP ONLY — NO EXECUTION

---

## 1. Vision Statement

Establish a clean, normalized, searchable, versioned, and governance-compliant National Knowledge Foundation for the Alkasik Kingdom.

From this foundation, the Kingdom shall be ready for:
- WP3.5 Phase 1C — Knowledge Population
- Capability Evolution Program
- Economic System Design
- Autonomous Learning Intelligence

---

## 2. Roadmap Overview

```
STAGE 1: CLEANUP          STAGE 2: NORMALIZATION     STAGE 3: POPULATION
╔═══════════════════╗     ╔══════════════════════╗    ╔════════════════════╗
║ Duplicate removal  ║     ║ Registry unification ║    ║ Lesson creation     ║
║ Supersession marks ║ ──→ ║ Schema alignment     ║ ──→║ Skill derivation    ║
║ Archive indexing   ║     ║ Cross-registry index ║    ║ Trace recording     ║
║ Empty dir cleanup  ║     ║ Retrieval tuning     ║    ║ Dataset ingestion   ║
╚═══════════════════╝     ╚══════════════════════╝    ╚════════════════════╝
                                                              │
                                                              ↓
                                  STAGE 4: LEARNING     STAGE 5: CAPABILITY
                                  ╔════════════════════╗ ╔════════════════════╗
                                  ║ Lesson distillation║ ║ Capability assembly║
                                  ║ Skill discovery    ║ ║ Maturity tracking  ║
                                  ║ Quarantine policy  ║ ║ Evolution pipeline ║
                                  ║ Cross-agent learn  ║ ║ Economic system    ║
                                  ╚════════════════════╝ ╚════════════════════╝
```

---

## 3. Stage 1 — Cleanup

**Objective:** Remove duplication, mark supersession, index archives, plan empty directory disposal.

**Dependencies:** None (can start immediately)

**Authority Required:** Sage review + Janus authorization

### Tasks

| # | Task | Deliverable | Effort | Owner |
|---|------|-------------|--------|-------|
| 1.1 | Archive duplicate legal registries | `archive/registry_consolidation/` | 1 hour | Hermes |
| 1.2 | Mark 6 superseded design docs | Deprecation notices in file headers | 30 min | Hermes |
| 1.3 | Archive 2 constitution v1.0 copies | `archive/constitution_v1.0/` | 15 min | Hermes |
| 1.4 | Create archive index | `memory/archive_registry/archive_index.yaml` | 1 hour | Hermes |
| 1.5 | Deprecate/remove 10 empty dirs | `.deprecated` markers or removal | 30 min | Hermes |
| 1.6 | Update codex governance report to reference master legal index | Documentation update | 15 min | Hermes |

**Duration estimate:** 1–2 days
**Exit criteria:** 0 duplicate registries, 0 superseded design docs in active tree, archive index populated, empty dirs marked.

---

## 4. Stage 2 — Normalization

**Objective:** Unify registry schemas, standardize metadata, build cross-registry index, optimize retrieval.

**Dependencies:** Stage 1 complete (clean active tree).

**Authority Required:** Sage review + Janus authorization

### Tasks

| # | Task | Deliverable | Effort | Owner |
|---|------|-------------|--------|-------|
| 2.1 | Normalize YAML registry schema (13 files) | Unified `RegistryRecord` template applied | 2–3 days | Hermes |
| 2.2 | Unify status taxonomy across all registries | All registries use single taxonomy | 1 day | Hermes |
| 2.3 | Unify risk/protection level taxonomy | Single taxonomy: LEVEL_1–LEVEL_4 | 1 day | Hermes |
| 2.4 | Add timestamps and versioning to YAML registries | `created_at`, `updated_at`, `registry_version` | 1 day | Hermes |
| 2.5 | Build cross-registry reference index | `memory/knowledge_registry/cross_reference.yaml` | 2 days | Lang Lieu |
| 2.6 | Persist in-memory registries (5 Python registries) | Boot-time hydration from LanceDB | 1 day | Lang Lieu |
| 2.7 | Add pagination and filtering to all registries | `offset`/`limit`/`status`/`owner` params | 1 day | Lang Lieu |
| 2.8 | Create LanceDB vector indexes | IVF-PQ on lessons, skills, traces | 1 day | Lang Lieu |
| 2.9 | Index YAML registries in LanceDB | `registry_index` table | 1 day | Lang Lieu |
| 2.10 | Implement read-through cache | `memory/cache.py` | 1 day | Lang Lieu |

**Duration estimate:** 2–3 weeks
**Exit criteria:** Single canonical registry strategy documented and implemented. All registries use unified schema. Search performed via indexes. Pagination in place.

---

## 5. Stage 3 — Population

**Objective:** Create initial knowledge corpus: lessons, skills, decision traces, datasets.

**Dependencies:** Stage 2 complete (registries normalized, retrieval optimized).

**Authority Required:** Sage review + Janus authorization + Hung Vuong approval for promotion gates.

### Tasks

| # | Task | Deliverable | Effort | Owner |
|---|------|-------------|--------|-------|
| 3.1 | Define lesson population workflow | Lesson creation → review → approval pipeline | 1 day | Hermes + Sage |
| 3.2 | Create initial lessons from WP history | Lessons learned from WP0–WP3.5 | 2–3 days | All agents |
| 3.3 | Record decision traces from previous work | Trace every WP acceptance/review decision | 2 days | Hermes |
| 3.4 | Derive initial skills from approved lessons | Skill candidates → review → approval | 2 days | Hermes + Sage |
| 3.5 | Register initial datasets | Dataset metadata in DatasetRegistry | 1 day | Hermes |
| 3.6 | Apply quarantine policy to suspect records | QuarantinePolicy.evaluate() | Continuously | Sage |

**Population targets (initial):**
| Record Type | Minimum Target | Stretch Target |
|-------------|---------------|----------------|
| Lessons | 10 | 25 |
| Skills | 3 | 8 |
| Capabilities | 0 (Stage 4) | 1 |
| Decision Traces | 10 | 20 |
| Datasets | 2 | 5 |

**Duration estimate:** 2–4 weeks
**Exit criteria:** ≥10 lessons, ≥3 skills, ≥10 traces, ≥2 datasets registered and governance-approved.

---

## 6. Stage 4 — Learning Intelligence

**Objective:** Activate the learning loop: observe → distill → approve → skill → capability.

**Dependencies:** Stage 3 complete (knowledge corpus exists).

**Authority Required:** Hung Vuong approval (promotion governance requires sovereign authority).

### Tasks

| # | Task | Deliverable | Effort | Owner |
|---|------|-------------|--------|-------|
| 4.1 | Activate LearningLoop.observe() → submit_for_review() → approve() pipeline | End-to-end lesson lifecycle | 1 week | Lang Lieu + Hermes |
| 4.2 | Run DistillationPipeline on approved lessons | Distilled lesson targets | 1 day | Hermes |
| 4.3 | Run KnowledgeCompressionEngine | Compressed knowledge packages | 1 day | Hermes |
| 4.4 | Implement SkillDiscovery from approved lessons | Skill candidate generation | 1 week | Lang Lieu |
| 4.5 | Implement cross-agent learning | CrossAgentLearning model operational | 1 week | Lang Lieu |
| 4.6 | Activate quarantine policy | Automated quarantine of policy-violating records | 2 days | Sage |
| 4.7 | Deploy LearningMetrics | Real-time learning measurement | 3 days | Lang Lieu |

**Duration estimate:** 3–5 weeks
**Exit criteria:** LearningLoop operational with ≥10 lessons distilled to ≥3 skills. Quarantine policy active.

---

## 7. Stage 5 — Capability Evolution

**Objective:** Assemble skills into capabilities, track maturity, enable economic system.

**Dependencies:** Stage 4 complete (skills being actively discovered and approved).

**Authority Required:** Hung Vuong approval (capability evolution impacts sovereign systems).

### Tasks

| # | Task | Deliverable | Effort | Owner |
|---|------|-------------|--------|-------|
| 5.1 | Implement CapabilityEvolution pipeline | Capability assembly from skills | 2 weeks | Lang Lieu |
| 5.2 | Define maturity levels | Maturity level taxonomy and metrics | 1 week | Sage + Hermes |
| 5.3 | Track capability maturity over time | Maturity dashboard (observe-only) | 2 weeks | Iris |
| 5.4 | Link capabilities to economic system design | Capability→Economic requirement mapping | Ongoing | Iris + Sage |
| 5.5 | Enable BehaviorImprovement model | Behavior learning from capability usage | 2 weeks | Lang Lieu |

**Duration estimate:** 4–6 weeks
**Exit criteria:** ≥1 capability assembled from skills, maturity tracking operational, economic system design dependencies documented.

---

## 8. Timeline Summary

```
Stage 1: Cleanup       │ Week 1–2  │ ████░░░░░░░░░░░░░░░░
Stage 2: Normalization │ Week 3–5  │ ░░░░██████░░░░░░░░░░
Stage 3: Population    │ Week 6–9  │ ░░░░░░░░████████░░░░
Stage 4: Learning      │ Week 10–14│ ░░░░░░░░░░░░█████████
Stage 5: Capability    │ Week 15–20│ ░░░░░░░░░░░░░░░░░░██████
                        ──────────────────────────────────
                        │ Q3 2026                        Q4 2026
```

---

## 9. Resource Requirements

| Stage | Primary Agent | Supporting Agents | Key Dependencies |
|-------|---------------|-------------------|------------------|
| 1: Cleanup | Hermes | Lang Lieu | None |
| 2: Normalization | Hermes + Lang Lieu | Sage | Stage 1 complete |
| 3: Population | All agents | Sage (review) | Stage 2 complete |
| 4: Learning | Lang Lieu + Hermes | Sage + Janus | Stage 3 complete |
| 5: Capability | Lang Lieu + Iris | Sage + Hung Vuong | Stage 4 complete |

---

## 10. Risk Register

| Risk | Stage | Probability | Impact | Mitigation |
|------|-------|-------------|--------|------------|
| Registry normalization breaks existing references | Stage 2 | MEDIUM | HIGH | Archive before change; update all references |
| Population yields low-quality lessons | Stage 3 | MEDIUM | MEDIUM | Quality gates in LessonEvaluator |
| Quarantine policy blocks valid records | Stage 3–4 | LOW | MEDIUM | Sage override path defined |
| Capability evolution blocked by missing skills | Stage 5 | MEDIUM | HIGH | Ensure Stage 4 produces sufficient skills |
| Constitutional conflict during normalization | Any | LOW | CRITICAL | Immediate stop; escalate to Hung Vuong |

---

## 11. Success Criteria

| Criterion | Stage | Measurement |
|-----------|-------|-------------|
| Clean active tree | 1 | 0 duplicate registries, 0 superseded docs |
| Normalized registries | 2 | Single schema across all 13 YAML registries |
| Optimized retrieval | 2 | Search <10ms for 10K records |
| Knowledge populated | 3 | ≥10 lessons, ≥3 skills, ≥10 traces |
| Learning active | 4 | LearningLoop operational, ≥1 distillation cycle |
| Capability evolving | 5 | ≥1 capability tracked with maturity metrics |
| Economic ready | 5 | Economic system design can reference capabilities |

---

*End of National Knowledge Foundation Roadmap.*
