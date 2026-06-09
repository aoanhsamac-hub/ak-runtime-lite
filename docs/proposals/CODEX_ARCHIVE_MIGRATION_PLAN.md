# Codex Archive Migration Plan

**Date:** 2026-06-08
**Status:** PROPOSAL
**Authority:** NCP-R Wave 2
**Owner:** Janus
**Reviewer:** Sage

---

## 1. Background

The `docs/legal/codex/` directory contains 47 files from the legal reorganization Phase 1. All content has been superseded by canonical documents in `docs/legal/canon/` and `sovereign/`. NCP-R Wave 1 classified the entire codex/ as SUPERSEDED.

---

## 2. Migration Scope

| Item | Current Location | Size | Status |
|------|-----------------|------|--------|
| codex/ root (28 files) | docs/legal/codex/ | ~50 KB | SUPERSEDED |
| codex/audits/ (1 file) | docs/legal/codex/audits/ | ~3 KB | SUPERSEDED |
| codex/constitution/ (2 files) | docs/legal/codex/constitution/ | ~11 KB | SUPERSEDED |
| codex/laws/ (2 files) | docs/legal/codex/laws/ | ~2.5 KB | SUPERSEDED |
| codex/policies/ (4 files) | docs/legal/codex/policies/ | ~5 KB | SUPERSEDED |
| codex/registries/ (1 file) | docs/legal/codex/registries/ | ~6 KB | SUPERSEDED |
| codex/reports/ (5 files) | docs/legal/codex/reports/ | ~4 KB | SUPERSEDED |
| codex/reviews/ (2 files) | docs/legal/codex/reviews/ | ~5 KB | SUPERSEDED |
| codex/specifications/ (2 files) | docs/legal/codex/specifications/ | ~11 KB | SUPERSEDED |
| codex/standards/ (4 files) | docs/legal/codex/standards/ | ~11 KB | SUPERSEDED |

---

## 3. Migration Rules

1. **No deletion** — all files preserved
2. **Archive only** — move to archive/ directory
3. **Preserve references** — maintain directory structure under archive/
4. **Preserve audit trail** — migration log created

---

## 4. Migration Plan

### Step 1: Create archive directory
- Create `archive/legal/codex/`

### Step 2: Copy codex/ to archive/
- Copy all files and subdirectories preserving structure
- Source: `docs/legal/codex/`
- Destination: `archive/legal/codex/`

### Step 3: Verify copy integrity
- Compare file counts (47 files expected)
- Compare total sizes

### Step 4: Update references
- No active references to codex/ exist in current governance
- AK MEMORY.md entry notes codex/ is archived

### Step 5: Add archive marker
- Create `archive/legal/codex/ARCHIVE_MANIFEST.md` with:
  - Archive date
  - Original location
  - Migration reason
  - Superseding documents

### Step 6: Remove codex/ from docs/legal/
- Only after verification
- Per Repo Governance Decree: archive first, no deletion

---

## 5. Archive Destination Structure

```
archive/legal/codex/
├── ARCHIVE_MANIFEST.md
├── (all codex/ root files)
├── audits/
│   └── REPORT-07_COMPLIANCE_AUDIT.md
├── constitution/
│   ├── CONSTITUTION-00_CONSTITUTION_v1.0.md
│   └── CONSTITUTION-00_CONSTITUTION_v1.1.md
├── laws/
│   ├── LAW-00_AK_CODEX_GOVERNANCE_CODE_v1.0.md
│   └── LAW-04_MEMORY_v1.0.md
├── policies/
│   ├── POL-01_NO_LEGACY_RUNTIME_v1.0.md
│   ├── POL-02_PROJECT_CHARTER_v1.0.md
│   ├── POL-03_CROSS_AGENT_SHARING_v1.0.md
│   └── POL-04_AK_CODEX_INTEGRATION_POLICY_v1.0.md
├── registries/
│   └── LEGAL_REGISTRY.yaml
├── reports/
│   ├── AK_AUTHORITY_RESOLUTION_STANDARD.md
│   ├── AK_CODEX_GOVERNANCE_ACTIVATION_REPORT.md
│   ├── AK_CODEX_RELEASE_REPORT.md
│   ├── AK_CODEX_RELEASE_v1.0.md
│   ├── AK_COMPLIANCE_INTEGRATION_MODEL.md
│   ├── AK_CONSTITUTIONAL_AUDIT_MODEL.md
│   └── AK_CONSTITUTIONAL_QUERY_STANDARD.md
├── reviews/
│   ├── REV-01_WP35_PHASE1A_v1.0.md
│   └── REV-02_WP35_PHASE1B_v1.0.md
├── specifications/
│   ├── SPEC-00_WP35_IMPLEMENTATION_v1.0.md
│   └── SPEC-01_WP35_DATA_MODEL_v1.0.md
└── standards/
    ├── STD-01_LESSON_QUALITY_v1.0.md
    ├── STD-02_SKILL_TAXONOMY_v1.0.md
    ├── STD-04_LEARNING_METRICS_v1.0.md
    └── STD-05_PROMOTION_GOVERNANCE_v1.0.md
```

---

## 6. Verification

| Check | Method | Expected |
|-------|--------|----------|
| File count | Count in archive vs original | 47 files |
| Directory structure | Tree comparison | Identical |
| File integrity | SHA-256 spot check | 5 random files match |
| References | Grep for codex/ references | No active governance references |

---

## 7. Post-Migration

After migration:
- `docs/legal/canon/` is the sole legal source of truth
- All governance references point to canon only
- Archive retains full history as required by Retention Decree
- No codex files remain in `docs/legal/`

---

## 8. References

- NCP-R Wave 1 — Canon Consolidation Report
- Repo Governance Decree v1.0 FINAL
- Retention & Archive Governance Decree v1.0 FINAL
