# NCP-R Wave 1 — Registry Gap Report

**Date:** 2026-06-08
**Authority:** Janus Directive — NCP-R
**Status:** COMPLETE
**Reviewer:** Janus

---

## 9 Required Registries — Verification

| # | Registry | Exists | Type | Location | Status |
|---|----------|--------|------|----------|--------|
| 1 | Constitution Registry | YES | YAML | sovereign/registries/constitution_registry.yaml | ACTIVE |
| 2 | State Corpus Registry | YES | YAML | sovereign/registries/state_corpus_registry.yaml | RATIFIED |
| 3 | Legal Registry | YES | YAML (×2) | sovereign/registries/legal_registry.yaml + codex/registries/LEGAL_REGISTRY.yaml | DUPLICATE |
| 4 | Capability Registry | YES | Python | memory/capability_registry/official_capability_registry.py | ACTIVE |
| 5 | Skill Registry | YES | YAML (×6) | sovereign/registries/skill_*.yaml | ACTIVE |
| 6 | Agent Registry | PARTIAL | Python (×1) | agents/registry.py, agents/registry.yaml | NEEDS UPGRADE |
| 7 | Treasury Registry | YES | YAML | sovereign/registries/treasury_registry.yaml | ACTIVE |
| 8 | Dataset Registry | PARTIAL | Python | memory/dataset_registry.py | NEEDS YAML INDEX |
| 9 | Memory Registry | NO | — | NationalMemoryPlatform has 14 tables but no dedicated memory registry | MISSING |

---

## Detail

### 1. Constitution Registry
**Decision:** APPROVE
**Issues:** None. Single source of truth. LEVEL_4_CONSTITUTIONAL protection.
**Entries:** 1 (Constitution v1.1 FINAL)

### 2. State Corpus Registry
**Decision:** APPROVE
**Issues:** None. RATIFIED and LOCKED. LEVEL_4_CONSTITUTIONAL protection.
**Entries:** 1 (State Corpus v1.0 FINAL)

### 3. Legal Registry
**Decision:** APPROVE with action
**Issues:** DUPLICATE — exists in both sovereign/registries/legal_registry.yaml (primary) and codex/registries/LEGAL_REGISTRY.yaml (duplicate). The codex copy should be archived.
**Entries:** 15 documents indexed in primary registry.

### 4. Capability Registry
**Decision:** APPROVE
**Location:** `memory/capability_registry/official_capability_registry.py`
**Backend:** Python dataclasses + LanceDB (ak_capabilities table)
**Issues:** No YAML registry file for human-readable reference. Python-only.
**Entries:** Dynamic via LanceDB.

### 5. Skill Registry
**Decision:** APPROVE
**Issues:** None. Complete set of 6 registries in sovereign/registries/.
**Sub-registries:**
- skill_registry.yaml (master)
- skill_dependency_registry.yaml
- skill_lifecycle_registry.yaml
- skill_owner_registry.yaml
- skill_retirement_registry.yaml
- skill_validation_registry.yaml

### 6. Agent Registry
**Decision:** REQUIRE_REVISION
**Issues:**
- `agents/registry.py` exists (AgentRegistry class) but is Python-only
- `agents/registry.yaml` exists but is minimal
- No markdown/YAML index for human or agent reference
- No dedicated agent status tracking
**Required:** Create human-readable agent index with status, authority, capabilities, dependencies

### 7. Treasury Registry
**Decision:** APPROVE
**Issues:** None. Covers royal treasury, revenue registry, reserve fund, digital assets.
**Entries:** 4 sections, 9 revenue sources.

### 8. Dataset Registry
**Decision:** REQUIRE_REVISION
**Issues:**
- `memory/dataset_registry.py` exists as Python class
- No YAML index for human readability
- No dataset lifecycle tracking
- No retention policy enforcement visible
**Required:** Create YAML dataset index with schema, retention, owner, status

### 9. Memory Registry
**Decision:** MISSING
**Issues:**
- No dedicated memory registry file exists
- NationalMemoryPlatform manages 14 tables in LanceDB but no index/registry of what is stored
- No memory record tracking (ak_evidence, ak_lessons, etc. are tables, not a registry)
**Required:** Create memory registry indexing all memory tables, retention policies, compaction schedules

---

## Registry Duplicates

| Primary | Duplicate | Action |
|---------|-----------|--------|
| sovereign/registries/legal_registry.yaml | codex/registries/LEGAL_REGISTRY.yaml | ARCHIVE codex copy |

## Registry Orphans

| Item | Expected Registry | Status |
|------|------------------|--------|
| Budget Law (v1.0 REVIEW) | Legal Registry | FOUND — indexed in legal_registry.yaml |
| Janus Charter DRAFT | Document Registry | FOUND — listed in AK_DOCUMENT_REGISTRY_DRAFT.md |
| Hermes Charter DRAFT | Document Registry | FOUND — listed in AK_DOCUMENT_REGISTRY_DRAFT.md |

No orphan entries detected — all indexed documents exist at their referenced paths.

---

## Authority Conflicts

| Conflict | Registries Involved | Resolution |
|----------|-------------------|------------|
| Legal Registry owner | sovereign legal_registry (owner: Lang Lieu) vs codex LEGAL_REGISTRY (owner: Lang Lieu) | Same owner, no conflict. ARCHIVE codex copy. |
| Approval Matrix owners | governance/registries/approval_matrix.yaml (owner: Janus, reviewer: Sage) | Correct per Governance Charter |
| No conflicts detected across sovereign, governance, and memory registries. |
