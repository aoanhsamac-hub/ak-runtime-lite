# AK Knowledge Classification Report

**Directive:** WP-KM-01 Phase 2
**Agent:** Hermes
**Date:** 2026-06-07
**Status:** COMPLETE

## Classification Methodology

Each candidate is classified along four dimensions:
1. **Source Type** — governance report, design document, implementation artifact, audit report, or registry
2. **Category** — decision, lesson, dataset, skill, or capability
3. **Confidence** — HIGH (primary source), MEDIUM (derived), LOW (composite)
4. **Governance Impact** — CRITICAL (affects sovereignty/runtime), ELEVATED (affects governance/pipelines), STANDARD (documentation)
5. **Review Required** — Sage, Janus, or Hung Vuong

---

## Decision Trace Candidates (12)

| Record ID | Name | Source Type | Confidence | Governance Impact | Review Required |
|-----------|------|-----------|------------|-----------------|-----------------|
| TRACE-19D19E533E11 | Reorganize legal documents into sovereign directory structure | Governance Report | HIGH | CRITICAL | Sage |
| TRACE-F37511BD6A87 | Create legal_index.yaml as master legal registry | Governance Report | HIGH | CRITICAL | Sage |
| TRACE-FBFEE4C5D090 | Implement Governance Engine with approval routing and audit | Governance Report | HIGH | CRITICAL | Sage |
| TRACE-5F2DB75FD3F8 | Build 7-agent runtime framework with dry-run only execution | Governance Report | HIGH | CRITICAL | Janus |
| TRACE-9742F5B2D702 | Adopt LanceDB as exclusive memory backend | Governance Report | HIGH | CRITICAL | Janus |
| TRACE-4A4114FA5D9B | Create 5 knowledge registries | Implementation Artifact | HIGH | CRITICAL | Sage |
| TRACE-A1B2C9C3F9D9 | Learning Intelligence Layer Phase 1A | Governance Report | HIGH | ELEVATED | Sage |
| TRACE-78C1DCF1E17D | Learning Intelligence Layer Phase 1B | Test Artifact | HIGH | ELEVATED | Sage |
| TRACE-A5ACB719008B | Learning Intelligence Layer Phase 1C | Governance Report | HIGH | ELEVATED | Sage |
| TRACE-427333DAA7F8 | Accept AK-CODEX v1.0 as Official National Codex | Legal Document | HIGH | CRITICAL | Hung Vuong |
| TRACE-421D57555CE4 | Execute WP-KF-01 Knowledge Foundation | Execution Report | HIGH | ELEVATED | Sage |
| TRACE-E48AE19F5C61 | Execute WP-KP-01 National Knowledge Production System | Execution Report | HIGH | ELEVATED | Sage |

## Lesson Candidates (10)

| Record ID | Name | Source Type | Confidence | Governance Impact | Review Required |
|-----------|------|-----------|------------|-----------------|-----------------|
| LESSON-23A165E78578 | Legal governance requires canonical directory structure | Governance Report | HIGH | CRITICAL | Sage |
| LESSON-C6639E63119D | Registry consolidation prevents metadata fragmentation | Audit Report | HIGH | ELEVATED | Sage |
| LESSON-35178CC04340 | Knowledge lifecycle must be governance-controlled | Design Document | HIGH | CRITICAL | Sage |
| LESSON-3D6AB3BB833F | Evidence threshold prevents weak skill discovery | Design Document | HIGH | ELEVATED | Sage |
| LESSON-A75819C46FBB | LanceDB-only backend enforces memory sovereignty | Implementation Artifact | HIGH | CRITICAL | Janus |
| LESSON-B94BA6C0FCC3 | Archive before delete preserves audit integrity | Audit Report | HIGH | ELEVATED | Sage |
| LESSON-FCAED96626E3 | Agent memory isolation prevents unauthorized access | Implementation Artifact | HIGH | CRITICAL | Janus |
| LESSON-B85AD72E2855 | Design documents must be superseded by codex standards | Audit Report | HIGH | STANDARD | Sage |
| LESSON-70CF5DDF0A98 | Boot-time hydration ensures registry data survives restarts | Implementation Artifact | HIGH | ELEVATED | Sage |
| LESSON-C0C315C05BEB | Capability maturity assessment prevents premature activation | Design Document | HIGH | CRITICAL | Hung Vuong |

## Dataset Candidates (6)

| Record ID | Name | Source Type | Confidence | Governance Impact | Review Required |
|-----------|------|-----------|------------|-----------------|-----------------|
| DATASET-A277823E71E4 | Sovereign Legal Corpus | Registry | HIGH | CRITICAL | Sage |
| DATASET-B9EC1C34CF23 | AK-CODEX v1.0 Standards | Legal Document | HIGH | CRITICAL | Sage |
| DATASET-0E83D30687CA | AK Design Doctrine Corpus | Design Document | HIGH | STANDARD | Sage |
| DATASET-662B5E58DDF4 | AK Sovereign Registries | Registry | HIGH | CRITICAL | Sage |
| DATASET-D4D5AC75A441 | AK Governance Registry Set | Registry | HIGH | CRITICAL | Sage |
| DATASET-548C3E616E46 | AK National Knowledge Production Pipelines | Pipeline Code | HIGH | ELEVATED | Sage |

## Skill Candidates (5)

| Record ID | Name | Source Type | Confidence | Governance Impact | Review Required |
|-----------|------|-----------|------------|-----------------|-----------------|
| SKILL-3C98378BB698 | memory-sovereignty | Derived (2 lessons) | MEDIUM | CRITICAL | Janus |
| SKILL-8C5DA5CB9F6A | knowledge-lifecycle-governance | Derived (1 lesson) | MEDIUM | CRITICAL | Sage |
| SKILL-81FCD6908FA7 | registry-consolidation | Derived (2 lessons) | MEDIUM | ELEVATED | Sage |
| SKILL-8454F484202B | evidence-based-skill-discovery | Derived (1 lesson) | MEDIUM | ELEVATED | Sage |
| SKILL-EE07D435F45B | archive-preservation | Derived (1 lesson) | MEDIUM | ELEVATED | Sage |

## Capability Candidates (1)

| Record ID | Name | Source Type | Confidence | Governance Impact | Review Required |
|-----------|------|-----------|------------|-----------------|-----------------|
| CAP-BC66754770E9 | knowledge-foundation-management | Composite (5 skills) | LOW | CRITICAL | Hung Vuong |

## Classification Summary

| Confidence Level | Count | Percentage |
|-----------------|-------|-----------|
| HIGH | 28 | 82.4% |
| MEDIUM | 5 | 14.7% |
| LOW | 1 | 2.9% |

| Governance Impact | Count | Percentage |
|------------------|-------|-----------|
| CRITICAL | 19 | 55.9% |
| ELEVATED | 13 | 38.2% |
| STANDARD | 2 | 5.9% |

| Review Required | Count |
|----------------|-------|
| Sage | 25 |
| Janus | 5 |
| Hung Vuong | 4 |
