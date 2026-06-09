# Duplicate Consolidation Plan

**Directive:** HERMES-CLEANUP-01 Phase 3
**Date:** 2026-06-07
**Status:** PLAN ONLY — NO EXECUTION

---

## 1. Duplicate Inventory

### 1.1 Registry Duplicates

| Group | Files | Lines | Identity | Consolidation Action |
|-------|-------|-------|----------|---------------------|
| **A** | `sovereign/legal_index.yaml` | 167 | MASTER — designated canonical index | RETAIN |
| | `sovereign/registries/legal_registry.yaml` | 165 | DUPLICATE — identical content, legacy path | RETIRE (archive) |
| | `docs/legal/codex/registries/LEGAL_REGISTRY.yaml` | 165 | DUPLICATE — identical content, codex should reference master | RETIRE (archive) |

**Impact of Group A:** 330 lines of redundant metadata across 2 files. 15 documents each with 11 metadata fields duplicated 3× = 330 redundant metadata values.

### 1.2 Design Document Duplicates (Design ↔ Codex)

| Group | Design Doc (docs/design/) | Codex Standard | Lines Each | Overlap |
|-------|--------------------------|----------------|------------|---------|
| **B** | `AK_LESSON_QUALITY_MODEL.md` | `STD-01_LESSON_QUALITY_v1.0.md` | 106 / ~106 | HIGH — same doctrine content |
| **C** | `AK_SKILL_TAXONOMY_MODEL.md` | `STD-02_SKILL_TAXONOMY_v1.0.md` | 87 / ~87 | HIGH — same taxonomy |
| **D** | `AK_LEARNING_METRICS_MODEL.md` | `STD-04_LEARNING_METRICS_v1.0.md` | 73 / ~73 | HIGH — same metrics |
| **E** | `AK_PROMOTION_GOVERNANCE_MODEL.md` | `STD-05_PROMOTION_GOVERNANCE_v1.0.md` | 130 / ~130 | HIGH — same governance |
| **F** | `AK_CROSS_AGENT_SHARING_POLICY.md` | `POL-03_CROSS_AGENT_SHARING_v1.0.md` | 81 / ~81 | HIGH — same policy |
| **G** | `AK_SKILL_DISCOVERY_MODEL.md` | `STD-02_SKILL_TAXONOMY_v1.0.md` | 96 / ~87 | PARTIAL — discovery vs taxonomy |

**Impact of Groups B–F:** ~477 lines of design content duplicated as codex standards. Codex versions are the canonical, reviewed, accepted standards.

### 1.3 Constitution Duplicates

| Group | File | Version | Lines | Status |
|-------|------|---------|-------|--------|
| **H1** | `docs/governance/ALKASIK_CONSTITUTION_v1.0.md` | v1.0 | 294 | SUPERSEDED — legacy markdown |
| **H2** | `docs/legal/codex/constitution/CONSTITUTION-00_CONSTITUTION_v1.0.md` | v1.0 | 294 | SUPERSEDED — identical to H1 |
| **H3** | `sovereign/constitution/ALKASIK_CONSTITUTION_v1.1_FINAL.docx` | v1.1 | — | AUTHORITATIVE — current FINAL |

**Impact of Group H:** 588 lines of superseded constitution content (2 × 294). The authoritative constitution is v1.1 docx.

### 1.4 Full Duplicate Catalog

| ID | Type | Primary (Keep) | Duplicate(s) | Total Redundant |
|----|------|---------------|--------------|-----------------|
| D01 | Registry | `sovereign/legal_index.yaml` | 2 files | 330 lines |
| D02 | Design | `STD-01 (codex)` | `AK_LESSON_QUALITY_MODEL.md` | 106 lines |
| D03 | Design | `STD-02 (codex)` | `AK_SKILL_TAXONOMY_MODEL.md` | 87 lines |
| D04 | Design | `STD-04 (codex)` | `AK_LEARNING_METRICS_MODEL.md` | 73 lines |
| D05 | Design | `STD-05 (codex)` | `AK_PROMOTION_GOVERNANCE_MODEL.md` | 130 lines |
| D06 | Design | `POL-03 (codex)` | `AK_CROSS_AGENT_SHARING_POLICY.md` | 81 lines |
| D07 | Design | `STD-02 (codex)` | `AK_SKILL_DISCOVERY_MODEL.md` (partial) | ~50 lines |
| D08 | Constitution | `sovereign/constitution/*v1.1*` | 2 × v1.0 markdown | 588 lines |
| **Total** | — | — | **10 duplicate files** | **~1,445 lines** |

---

## 2. Canonical Source Mapping

### 2.1 Source of Truth Assignments

| Knowledge Domain | Canonical Source | Fallback / Reference Only |
|-----------------|-----------------|--------------------------|
| Legal document index | `sovereign/legal_index.yaml` | `sovereign/registries/legal_registry.yaml`, `docs/legal/codex/registries/LEGAL_REGISTRY.yaml` |
| Lesson quality doctrine | `docs/legal/codex/standards/STD-01_LESSON_QUALITY_v1.0.md` | `docs/design/AK_LESSON_QUALITY_MODEL.md` |
| Skill taxonomy | `docs/legal/codex/standards/STD-02_SKILL_TAXONOMY_v1.0.md` | `docs/design/AK_SKILL_TAXONOMY_MODEL.md`, `docs/design/AK_SKILL_DISCOVERY_MODEL.md` |
| Learning metrics | `docs/legal/codex/standards/STD-04_LEARNING_METRICS_v1.0.md` | `docs/design/AK_LEARNING_METRICS_MODEL.md` |
| Promotion governance | `docs/legal/codex/standards/STD-05_PROMOTION_GOVERNANCE_v1.0.md` | `docs/design/AK_PROMOTION_GOVERNANCE_MODEL.md` |
| Cross-agent sharing | `docs/legal/codex/policies/POL-03_CROSS_AGENT_SHARING_v1.0.md` | `docs/design/AK_CROSS_AGENT_SHARING_POLICY.md` |
| Constitution | `sovereign/constitution/ALKASIK_CONSTITUTION_v1.1_FINAL.docx` | `docs/governance/ALKASIK_CONSTITUTION_v1.0.md`, `docs/legal/codex/constitution/CONSTITUTION-00_CONSTITUTION_v1.0.md` |

### 2.2 Canonical Source Map Visualization

```
surevy/legal_index.yaml ────────────────────────────────── CANONICAL
    ├── sovereign/registries/legal_registry.yaml ──────── ARCHIVE (duplicate)
    └── docs/legal/codex/registries/LEGAL_REGISTRY.yaml ─ ARCHIVE (duplicate, codex references master)

docs/legal/codex/standards/STD-01..05 ──────────────────── CANONICAL
    └── docs/design/AK_*.md ───────────────────────────── SUPERSEDED (design drafts)

sovereign/constitution/*v1.1*.docx ─────────────────────── CANONICAL
    ├── docs/governance/ALKASIK_CONSTITUTION_v1.0.md ──── ARCHIVE (superseded)
    └── docs/legal/codex/constitution/CONSTITUTION-00_CONSTITUTION_v1.0.md ─ ARCHIVE
```

---

## 3. Consolidation Strategy

### 3.1 Stage 1: Registry Retirement

| Step | Action | Success Criteria |
|------|--------|-----------------|
| 1.1 | Designate `sovereign/legal_index.yaml` as canonical master | Single registry referenced by all queries |
| 1.2 | Archive `sovereign/registries/legal_registry.yaml` | File moved to archive/ — NOT deleted |
| 1.3 | Archive `docs/legal/codex/registries/LEGAL_REGISTRY.yaml` | File moved to archive/ — NOT deleted |
| 1.4 | Update codex governance report to reference master | Cross-reference in codex metadata |

### 3.2 Stage 2: Design Document Supersession

| Step | Action | Success Criteria |
|------|--------|-----------------|
| 2.1 | Mark each superseded design doc as `status: SUPERSEDED` | Metadata updated, content preserved |
| 2.2 | Add forward-reference `superseded_by: codex/<standard>.md` | Navigation from design doc to canonical |
| 2.3 | Archive superseded design docs or leave in place with clear deprecation notice | Decision per Sage review |

### 3.3 Stage 3: Constitution Cleanup

| Step | Action | Success Criteria |
|------|--------|-----------------|
| 3.1 | Confirm v1.1 docx is the sole authoritative version | Hash-verified against sovereign registry |
| 3.2 | Archive both v1.0 markdown copies | Preserved in archive/ with amendment trace |
| 3.3 | Optionally: generate v1.1 markdown canon from docx | Read-only mirror for text search |

---

## 4. Risk Assessment

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Breaking references (codex → legal_registry.yaml) | MEDIUM | Update all references before archiving |
| Losing design draft history | LOW | Archive preserved; no deletion |
| Confusion about canonical source during transition | MEDIUM | Clear supersession notices on deprecated files |
| Codex acceptance package references duplicate registry | LOW | Update acceptance metadata |

---

## 5. Post-Consolidation State

```
Before:  10 duplicate files occupying ~1,445 redundant lines
After:    0 duplicates occupying 0 redundant lines
          All 10 originals preserved in archive/
          Single canonical source for each knowledge domain
```

---

*End of Duplicate Consolidation Plan.*
