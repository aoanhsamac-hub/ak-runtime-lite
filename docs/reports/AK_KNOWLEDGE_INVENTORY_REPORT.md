# National Knowledge Inventory Report

**Date:** 2026-06-07
**Authority:** Hermes-36-000
**Scope:** D:\AK
**Status:** INVENTORY ONLY — NO EXECUTION

---

## 1. Memory-Related Assets

### 1.1 Code Registries (Python Classes)

| # | Asset | File | Lines | Status |
|---|-------|------|-------|--------|
| 1 | LessonRegistry | `memory/lesson_registry.py` | 51 | IMPLEMENTED |
| 2 | SkillRegistry | `memory/skill_registry.py` | 64 | IMPLEMENTED |
| 3 | CapabilityRegistry | `memory/capability_registry.py` | 59 | IMPLEMENTED |
| 4 | DatasetRegistry | `memory/dataset_registry.py` | 22 | IMPLEMENTED |
| 5 | DecisionTraceRegistry | `memory/decision_trace_registry.py` | 22 | IMPLEMENTED |

### 1.2 YAML Registries

| # | Asset | File | Lines | Status |
|---|-------|------|-------|--------|
| 1 | Legal Index | `sovereign/legal_index.yaml` | 167 | ACTIVE |
| 2 | Legal Registry | `sovereign/registries/legal_registry.yaml` | 165 | ACTIVE |
| 3 | Constitution Registry | `sovereign/registries/constitution_registry.yaml` | 13 | ACTIVE |
| 4 | State Corpus Registry | `sovereign/registries/state_corpus_registry.yaml` | 13 | ACTIVE |
| 5 | Legal Hierarchy | `sovereign/registries/legal_hierarchy.yaml` | 26 | ACTIVE |
| 6 | Directive Registry | `sovereign/registries/directive_registry.yaml` | 13 | ACTIVE |
| 7 | Treasury Registry | `sovereign/registries/treasury_registry.yaml` | 32 | ACTIVE |
| 8 | Codex Legal Registry | `docs/legal/codex/registries/LEGAL_REGISTRY.yaml` | 165 | ACTIVE |
| 9 | Agent Registry | `agents/registry.yaml` | — | ACTIVE |
| 10 | Protected Modules | `governance/registries/protected_modules.yaml` | 48 | ACTIVE |
| 11 | Approval Matrix | `governance/registries/approval_matrix.yaml` | 24 | ACTIVE |
| 12 | Governance Gate Registry | `governance/registries/governance_gate_registry.yaml` | 18 | ACTIVE |
| 13 | Issue Registry | `governance/registries/issue_registry.yaml` | 12 | ACTIVE |

### 1.3 Memory Platform Code

| # | Asset | File | Lines |
|---|-------|------|-------|
| 1 | MemoryInterface | `memory/memory_interface.py` | — |
| 2 | AgentMemoryClient | `memory/agent_memory.py` | — |
| 3 | LanceDBAdapter | `memory/lancedb_adapter.py` | 80 |
| 4 | LearningLoop | `memory/learning_loop.py` | 26 |
| 5 | KnowledgeCompressionEngine | `memory/knowledge_compression.py` | 16 |
| 6 | DistillationPipeline | `memory/distillation_pipeline.py` | 16 |
| 7 | QuarantinePolicy | `memory/quarantine_policy.py` | 20 |
| 8 | Data Schemas | `memory/schemas/records.py` | 234 |

### 1.4 Learning Intelligence Layer

| # | Asset | File | Lines |
|---|-------|------|-------|
| 1 | LearningMetrics | `learning/learning_metrics.py` | — |
| 2 | LessonEvaluator | `learning/lesson_evaluator.py` | — |
| 3 | SkillEvidencePolicy | `learning/skill_evidence_policy.py` | — |

### 1.5 Design Documents (Lesson-Related)

| # | Asset | File | Lines |
|---|-------|------|-------|
| 1 | Lesson Quality Model | `docs/design/AK_LESSON_QUALITY_MODEL.md` | 106 |
| 2 | Lesson Deduplication Model | `docs/design/AK_LESSON_DEDUPLICATION_MODEL.md` | 105 |
| 3 | Skill Discovery Model | `docs/design/AK_SKILL_DISCOVERY_MODEL.md` | 96 |
| 4 | Skill Taxonomy Model | `docs/design/AK_SKILL_TAXONOMY_MODEL.md` | 87 |
| 5 | Capability Evolution Model | `docs/design/AK_CAPABILITY_EVOLUTION_MODEL.md` | 87 |
| 6 | Capability Lifecycle Model | `docs/design/AK_CAPABILITY_LIFECYCLE_MODEL.md` | 115 |
| 7 | Cross-Agent Learning Model | `docs/design/AK_CROSS_AGENT_LEARNING_MODEL.md` | 86 |
| 8 | Cross-Agent Sharing Policy | `docs/design/AK_CROSS_AGENT_SHARING_POLICY.md` | 81 |
| 9 | Learning Metrics Model | `docs/design/AK_LEARNING_METRICS_MODEL.md` | 73 |
| 10 | Behavior Improvement Model | `docs/design/AK_BEHAVIOR_IMPROVEMENT_MODEL.md` | 125 |
| 11 | Promotion Governance Model | `docs/design/AK_PROMOTION_GOVERNANCE_MODEL.md` | 130 |
| 12 | Phase 1A Metrics Notes | `docs/design/AK_WP35_PHASE1A_LEARNING_METRICS_NOTES.md` | — |
| 13 | Phase 1C Evidence Policy Design | `docs/design/AK_WP35_PHASE1C_EVIDENCE_POLICY_DESIGN.md` | 239 |
| 14 | Phase 1E Skill Discovery Design | `docs/design/AK_WP35_PHASE1E_SKILL_DISCOVERY_DESIGN.md` | 347 |

### 1.6 Legal Codex Standards (Canonical Copies)

| # | Asset | File | Lines |
|---|-------|------|-------|
| 1 | STD-01 Lesson Quality | `docs/legal/codex/standards/STD-01_LESSON_QUALITY_v1.0.md` | 106 |
| 2 | STD-02 Skill Taxonomy | `docs/legal/codex/standards/STD-02_SKILL_TAXONOMY_v1.0.md` | 87 |
| 3 | STD-04 Learning Metrics | `docs/legal/codex/standards/STD-04_LEARNING_METRICS_v1.0.md` | 73 |
| 4 | STD-05 Promotion Governance | `docs/legal/codex/standards/STD-05_PROMOTION_GOVERNANCE_v1.0.md` | 130 |
| 5 | POL-03 Cross-Agent Sharing | `docs/legal/codex/policies/POL-03_CROSS_AGENT_SHARING_v1.0.md` | 81 |

### 1.7 Sovereign Documents

| # | Asset | Type | Format |
|---|-------|------|--------|
| 1 | Constitution v1.1 FINAL | Constitution | .docx |
| 2 | State Corpus v1.0 FINAL | State Corpus | .docx |
| 3 | Governance Charter v1.1 Final | Governance Charter | .docx |
| 4 | Agent Law v1.0 FINAL | Agent Law | .docx |
| 5 | Risk Law v1.0 FINAL | Risk Law | .docx |
| 6 | Execution Law v1.0 FINAL | Execution Law | .docx |
| 7 | Economic Law v1.0 FINAL | Economic Law | .docx |
| 8 | Information Law v1.0 FINAL | Information Law | .docx |
| 9 | Memory Law v1.0 FINAL | Memory Law | .docx |
| 10 | Security Law v1.0 FINAL | Security Law | .docx |
| 11 | National Budget Law v0.1 DRAFT | Budget Law | .docx |
| 12 | National Budget Law v1.0 REVIEW | Budget Law | .md |
| 13 | Repo Governance Decree v1.0 FINAL | Decree | .docx |
| 14 | Knowledge Governance Decree v1.0 FINAL | Decree | .docx |
| 15 | Retention Decree v1.0 FINAL | Decree | .docx |

### 1.8 Archive Backups

| # | Backup | Date |
|---|--------|------|
| 1 | Legal Reorganization | 2026-06-07 01:12 |
| 2 | WP0 Bootstrap | 2026-06-07 01:19 |
| 3 | WP1 Governance Engine | 2026-06-07 01:32 |
| 4 | WP2 Agent Framework | 2026-06-07 04:04 |
| 5 | WP3.5 Learning Intelligence Design | 2026-06-07 08:58 |
| 6 | WP3.5 Sage Round 2 | 2026-06-07 09:23 |

### 1.9 Empty / Non-Populated Directories

| # | Path | Expected Content |
|---|------|-----------------|
| 1 | `memory/knowledge_registry/` | Knowledge records |
| 2 | `memory/lessons/` | Serialized lesson files |
| 3 | `memory/legacy_corpus/` | Legacy memory corpus |
| 4 | `memory/archive_registry/` | Archive index |
| 5 | `data/datasets/` | Dataset files |
| 6 | `data/raw/` | Raw data |
| 7 | `data/processed/` | Processed data |
| 8 | `data/system_maps/` | System maps |
| 9 | `sovereign/directives/` | Directives |
| 10 | `sovereign/quarantine/` | Quarantined records |

---

## 2. Identified Duplicates & Issues

### 2.1 Duplicate Registries

| Group | Files | Nature |
|-------|-------|--------|
| A | `sovereign/legal_index.yaml` (167L) | Master index — 15 documents |
| | `sovereign/registries/legal_registry.yaml` (165L) | Near-identical document listing |
| | `docs/legal/codex/registries/LEGAL_REGISTRY.yaml` (165L) | Identical content to legal_registry.yaml |
| B | `docs/governance/ALKASIK_CONSTITUTION_v1.0.md` (294L) | Constitution v1.0 (Vietnamese) |
| | `docs/legal/codex/constitution/CONSTITUTION-00_CONSTITUTION_v1.0.md` (294L) | Exact duplicate |

### 2.2 Duplicate Lessons / Design Documents

| Design Doc (docs/design/) | Codex Canonical Copy | Content Overlap |
|--------------------------|----------------------|-----------------|
| `AK_LESSON_QUALITY_MODEL.md` | `STD-01_LESSON_QUALITY_v1.0.md` | HIGH — same doctrine |
| `AK_SKILL_DISCOVERY_MODEL.md` | `STD-02_SKILL_TAXONOMY_v1.0.md` | PARTIAL — discovery vs taxonomy |
| `AK_SKILL_TAXONOMY_MODEL.md` | `STD-02_SKILL_TAXONOMY_v1.0.md` | HIGH — same taxonomy |
| `AK_LEARNING_METRICS_MODEL.md` | `STD-04_LEARNING_METRICS_v1.0.md` | HIGH — same metrics |
| `AK_PROMOTION_GOVERNANCE_MODEL.md` | `STD-05_PROMOTION_GOVERNANCE_v1.0.md` | HIGH — same governance |
| `AK_CROSS_AGENT_SHARING_POLICY.md` | `POL-03_CROSS_AGENT_SHARING_v1.0.md` | HIGH — same policy |

### 2.3 Oversized Documents (>15KB or >200 lines)

| File | Lines | Est. Size |
|------|-------|-----------|
| `docs/design/AK_WP35_PHASE1E_SKILL_DISCOVERY_DESIGN.md` | 347 | ~18KB |
| `docs/reviews/AK_WP35_PHASE1C_IMPLEMENTATION_VERIFICATION.md` | 327 | ~18KB |
| `docs/governance/ALKASIK_CONSTITUTION_v1.0.md` | 294 | ~15KB |
| `docs/legal/codex/constitution/CONSTITUTION-00_CONSTITUTION_v1.0.md` | 294 | ~15KB |
| `docs/design/AK_WP35_PHASE1C_EVIDENCE_POLICY_DESIGN.md` | 239 | ~13KB |
| `docs/reports/AK_MEMORY.md` | 244 | ~16KB |
| `docs/reviews/AK_WP35_PHASE1C_DESIGN_EVIDENCE_SUMMARY.md` | 221 | ~12KB |
| `docs/reviews/WP35_GOVERNANCE_CONSISTENCY_AUDIT.md` | 187 | ~10KB |
| `docs/architecture/AK_LEARNING_INTELLIGENCE_ARCHITECTURE.md` | 171 | ~9KB |
| `docs/legal/codex/specifications/SPEC-00_WP35_IMPLEMENTATION_v1.0.md` | 129 | ~7KB |
| `docs/legal/codex/specifications/SPEC-01_WP35_DATA_MODEL_v1.0.md` | 131 | ~7KB |
| `docs/specs/AK_WP35_PHASE1E_INTERFACE_SPEC.md` | 157 | ~8KB |
| `docs/specs/AK_WP35_PHASE1C_INTERFACE_SPEC.md` | 153 | ~8KB |
| `docs/reviews/AK_WP35_PHASE1C_SAGE_REVIEW_PACKAGE.md` | 178 | ~10KB |
| `docs/reviews/AK_WP35_PHASE1C_CONTRACT_REVIEW_PACKAGE.md` | 133 | ~7KB |
| `docs/reviews/AK_WP35_PHASE1E_SAGE_REVIEW_PACKAGE.md` | 193 | ~10KB |
| `docs/legal/codex/reports/AK_CODEX_GOVERNANCE_ACTIVATION_REPORT.md` | — | ~12KB |

### 2.4 Redundant Metadata

Each sovereign legal document (15 total) is listed identically in **three** separate registry files:
1. `sovereign/legal_index.yaml` — 15 entries × 11 fields = 165 metadata values
2. `sovereign/registries/legal_registry.yaml` — 15 entries × 11 fields = 165 metadata values
3. `docs/legal/codex/registries/LEGAL_REGISTRY.yaml` — 15 entries × 11 fields = 165 metadata values

**Total redundant metadata fields:** 330 duplications across 3 files.

### 2.5 Retrieval Bottlenecks

| # | Bottleneck | Location | Impact |
|---|------------|----------|--------|
| 1 | In-memory only storage | All 5 code registries (`_records: dict`) | All data lost on process restart |
| 2 | No cross-registry foreign keys | lesson_registry → skill_registry → capability_registry | No JOIN-capable queries |
| 3 | LanceDB-only single backend | `lancedb_adapter.py` | Single point of failure; no fallback |
| 4 | Full-table scan fallback | LanceDBAdapter.search() line 68 | Linear scan on non-vector tables |
| 5 | No persistent indices on YAML registries | All `registries/*.yaml` files | Sequential parse every lookup |
| 6 | No materialized view / summary index | `knowledge_registry/` (empty) | No pre-computed aggregation layer |
| 7 | All registry reads go through `list_records()` | All 5 registries | No pagination, no filtered queries |
| 8 | Archive registry directory empty | `memory/archive_registry/` | No archive index exists |
| 9 | Quarantine directory empty | `sovereign/quarantine/` | No quarantine tracking |
| 10 | LanceDB lazy import + fail-closed | `lancedb_adapter.py` line 29-33 | Silent degradation risk |

---

## 3. Measurements

| Metric | Count | Notes |
|--------|-------|-------|
| **Registry count** | 13 | 5 Python class registries + 8 YAML-based registries (excluding 3 duplicates) |
| **Effective unique registries** | 10 | After accounting for 3-way duplicate of legal registry |
| **Lesson count** | 0 | No persisted lesson records in memory/lessons/ |
| **Lesson design documents** | 14 | In docs/design/ (including duplicates with codex) |
| **Codex standard duplicates** | 5 | Design docs duplicated as codex standards |
| **Trace count** | 0 | No persisted decision trace records |
| **Candidate count** | 0 | No candidate lessons/skills persisted |
| **Dataset count** | 0 | No dataset records persisted |
| **Sovereign legal documents** | 15 | 10 laws, 1 constitution, 1 state corpus, 3 decrees |
| **Archived backups** | 6 | In archive/ directory |
| **Registry YAML duplicates** | 3 | legal_index.yaml, legal_registry.yaml, LEGAL_REGISTRY.yaml |
| **Empty data directories** | 10 | knowledge_registry/, lessons/, legacy_corpus/, archive_registry/, data/datasets/, data/raw/, data/processed/, data/system_maps/, sovereign/directives/, sovereign/quarantine/ |

---

## 4. Proposed Opportunities

### 4.1 Compaction Opportunities

| # | Opportunity | Target | Rationale |
|---|-------------|--------|-----------|
| C1 | Consolidate 3 legal registry files → 1 | legal_index.yaml, legal_registry.yaml, LEGAL_REGISTRY.yaml | Eliminate 330 redundant metadata fields |
| C2 | Deduplicate design docs vs codex standards | 6 design/docs pairs | Design docs are superseded by codex standards |
| C3 | Compress oversized review packages into summary index | Review documents >200 lines | Reduce review artifact sprawl |
| C4 | Consolidate duplicate constitution text | 2 copies of Constitution v1.0 | Only v1.1 is authoritative |
| C5 | Remove empty data directories from active tree | 10 empty directories | Reduce search noise |

### 4.2 Indexing Opportunities

| # | Opportunity | Target | Rationale |
|---|-------------|--------|-----------|
| I1 | Build LanceDB vector indices on lesson content | `lessons` table | Enable semantic search |
| I2 | Create cross-registry reference index | lesson→skill→capability→trace | Enable graph traversal |
| I3 | Materialize knowledge registry view | `memory/knowledge_registry/` | Pre-computed aggregation |
| I4 | Index YAML registries in LanceDB | All `registries/*.yaml` | Fast programmatic lookup |
| I5 | Create archive registry index | `memory/archive_registry/` | Track all archived states |

### 4.3 Archive Opportunities

| # | Opportunity | Target | Rationale |
|---|-------------|--------|-----------|
| A1 | Archive superseded design docs | Duplicate design docs | Clean active namespace |
| A2 | Archive old review packages | WP35 reviews (Phase 1A, 1B) | Historical only; superseded |
| A3 | Archive constitution v1.0 markdown | 2 copies | v1.1 docx is canonical |
| A4 | Archive empty directory structure placeholders | 10 empty dirs | Not needed until populated |

### 4.4 Normalization Opportunities

| # | Opportunity | Target | Rationale |
|---|-------------|--------|-----------|
| N1 | Normalize registry schema across all YAML files | All 13 registries | Standard fields: id, name, status, version, timestamps |
| N2 | Enforce `source_hash` cross-reference integrity | Lesson ↔ Skill ↔ Capability | Ensure referential integrity |
| N3 | Standardize lesson/document status taxonomy | DRAFT, REVIEWED, APPROVED, ACTIVE, DEPRECATED, QUARANTINE | Consistent across all registries |
| N4 | Normalize risk level taxonomy | LEVEL_1_MODERATE through LEVEL_4_CONSTITUTIONAL | Harmonize with sovereign hierarchy |
| N5 | Standardize agent role references | 7 agents consistently named | owner_agent, reviewer_agent, allowed_agents |
| N6 | Normalize timestamps to ISO 8601 UTC | All `created_at` fields | Already partially done in schemas but not enforced across YAML |

---

*End of Inventory Report.*
