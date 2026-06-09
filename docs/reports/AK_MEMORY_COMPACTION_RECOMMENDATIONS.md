# Memory Compaction Recommendations

**Date:** 2026-06-07
**Authority:** Hermes-36-000
**Status:** RECOMMENDATIONS ONLY — NO EXECUTION

---

## Recommendation 1: Consolidate Triplicate Legal Registries

**Current state:** 3 near-identical registry files each listing 15 sovereign documents with 11 metadata fields per document (330 redundant metadata values).

| File | Lines | Redundancy |
|------|-------|------------|
| `sovereign/legal_index.yaml` | 167 | Master index — 15 docs × 11 fields |
| `sovereign/registries/legal_registry.yaml` | 165 | Duplicate — same 15 docs × 11 fields |
| `docs/legal/codex/registries/LEGAL_REGISTRY.yaml` | 165 | Duplicate — same 15 docs × 11 fields |

**Proposed:** Collapse to 1 canonical registry. Designate `sovereign/legal_index.yaml` as the master. Remove the other two from active search paths. Reference master from codex via symlink or import.

**Compaction gain:** ~330 lines eliminated from active namespace. Single source of truth for legal document metadata.

---

## Recommendation 2: Deduplicate Design Docs Superseded by Codex Standards

**Current state:** 6 design documents in `docs/design/` whose content is substantially duplicated as canonical codex standards:

| Design Doc (docs/design/) | Codex Standard | Overlap |
|---------------------------|----------------|---------|
| `AK_LESSON_QUALITY_MODEL.md` | `STD-01_LESSON_QUALITY_v1.0.md` | HIGH |
| `AK_SKILL_TAXONOMY_MODEL.md` | `STD-02_SKILL_TAXONOMY_v1.0.md` | HIGH |
| `AK_LEARNING_METRICS_MODEL.md` | `STD-04_LEARNING_METRICS_v1.0.md` | HIGH |
| `AK_PROMOTION_GOVERNANCE_MODEL.md` | `STD-05_PROMOTION_GOVERNANCE_v1.0.md` | HIGH |
| `AK_CROSS_AGENT_SHARING_POLICY.md` | `POL-03_CROSS_AGENT_SHARING_v1.0.md` | HIGH |
| `AK_SKILL_DISCOVERY_MODEL.md` | `STD-02_SKILL_TAXONOMY_v1.0.md` | PARTIAL |

**Proposed:** Archive design docs post-codex. Codex standards are the canonical, reviewed, accepted versions. Design docs were working drafts superseded upon codex acceptance.

**Compaction gain:** ~573 lines of duplicate doctrine removed from active namespace.

---

## Recommendation 3: Deduplicate Constitution v1.0

**Current state:** 2 identical 294-line copies of Constitution v1.0 exist:
- `docs/governance/ALKASIK_CONSTITUTION_v1.0.md`
- `docs/legal/codex/constitution/CONSTITUTION-00_CONSTITUTION_v1.0.md`

**Proposed:** Archive both v1.0 copies. The authoritative document is `sovereign/constitution/ALKASIK_CONSTITUTION_v1.1_FINAL.docx` (v1.1). Retain only one legacy reference copy if needed for amendment traceability.

**Compaction gain:** ~294 lines eliminated. Single authoritative reference to v1.1 docx.

---

## Recommendation 4: Compress Oversized Review Packages

**Current state:** Multiple review documents exceed 200 lines:

| File | Lines | Issue |
|------|-------|-------|
| `...SKILL_DISCOVERY_DESIGN.md` | 347 | Design + interface + rationale merged |
| `...IMPLEMENTATION_VERIFICATION.md` | 327 | All verification output inline |
| `...EVIDENCE_POLICY_DESIGN.md` | 239 | Design + evidence + trace merged |
| `...MEMORY.md` | 244 | Full WP history accumulated |

**Proposed:** Split each oversized review/design document into:
1. A summary index (≤50 lines) with key findings and links
2. Detailed appendices or referenced artifacts

**Compaction gain:** ~800+ lines of inline detail moved to appendices or archived.

---

## Recommendation 5: Prune Empty Data Directories from Active Tree

**Current state:** 10 directories exist as placeholders with zero content:

| Directory | Intended Purpose |
|-----------|-----------------|
| `memory/knowledge_registry/` | Knowledge records |
| `memory/lessons/` | Serialized lessons |
| `memory/legacy_corpus/` | Legacy corpus |
| `memory/archive_registry/` | Archive index |
| `data/datasets/` | Dataset storage |
| `data/raw/` | Raw data |
| `data/processed/` | Processed data |
| `data/system_maps/` | System maps |
| `sovereign/directives/` | Directive files |
| `sovereign/quarantine/` | Quarantined records |

**Proposed:** Remove empty directories from active namespace. Recreate on first write. Reduces cognitive load and search noise.

**Compaction gain:** 10 nodes removed from active tree.

---

## Recommendation 6: Standardize Registry Schema Across YAML Files

**Current state:** 13 YAML registry files use inconsistent field schemas. Some use `document_name`, others use `name`. Some have `owner_agent`/`reviewer_agent`, others omit.

**Proposed:** Define a single `RegistryRecord` schema with these required fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `name` | string | Display name |
| `type` | string | Record type |
| `status` | string | Status (DRAFT/ACTIVE/DEPRECATED) |
| `version` | string | Version string |
| `owner_agent` | string | Responsible agent |
| `reviewer_agent` | string | Reviewing agent |
| `created_at` | string | ISO 8601 UTC |
| `protection_level` | string | LEVEL_1–LEVEL_4 |

**Normalization gain:** Unified query interface across all registries.

---

## Recommendation 7: Implement Archive Registry

**Current state:** `memory/archive_registry/` is empty. 6 backup archives exist in `archive/` but are not indexed or discoverable programmatically.

**Proposed:** Create a single `archive_registry.yaml` that enumerates all 6 backups with:
- Backup ID and date
- Source directories backed up
- Rationale for backup trigger
- Point-in-time reference to legal_index.yaml contents at time of backup

**Compaction gain:** Enables discovery of historical states without expanding backups.

---

## Recommendation 8: Introduce Registry Versioning

**Current state:** Registries track document versions internally but do not version themselves. Changes to `legal_index.yaml` overwrite in place with no history.

**Proposed:** Add `registry_version` and `last_modified` fields to every YAML registry. Link to an append-only changelog in `governance/audit/`.

**Normalization gain:** Full audit trail for registry mutation.

---

## Summary of Compaction Potential

| Recommendation | Lines Removed | Nodes Removed | Primary Benefit |
|---------------|--------------|---------------|-----------------|
| R1: Consolidate legal registries | ~330 | 2 files | Single source of truth |
| R2: Deduplicate design docs | ~573 | 6 files | Eliminate superseded drafts |
| R3: Deduplicate constitution | ~294 | 1 file | Single authoritative reference |
| R4: Compress reviews | ~800+ | 4 files | Focused summaries |
| R5: Prune empty dirs | — | 10 nodes | Cleaner namespace |
| R6: Normalize schema | — | 13 files | Uniform query interface |
| R7: Archive registry | — | 1 file | Discoverable history |
| R8: Registry versioning | — | 13 files | Mutation audit trail |
| **Total est.** | **~1997+** | **~37 items** | |

---

*End of Compaction Recommendations.*
