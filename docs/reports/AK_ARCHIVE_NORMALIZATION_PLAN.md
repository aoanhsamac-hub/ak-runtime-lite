# Archive Normalization Plan

**Directive:** HERMES-CLEANUP-01 Phase 6
**Date:** 2026-06-07
**Status:** PLAN ONLY — NO EXECUTION

---

## 1. Current Archive State

### 1.1 Existing Backups

| Backup ID | Directory | Date | Contents | Size | Indexed? |
|-----------|-----------|------|----------|------|----------|
| ARCH-001 | `archive/legal_reorganization/backup_20260607_011203/` | 2026-06-07 01:12 | sovereign/laws/ .docx files | ~80KB | NO |
| ARCH-002 | `archive/wp0_bootstrap_backup/backup_20260607_011903/` | 2026-06-07 01:19 | sovereign/legal_index.yaml, registries | ~50KB | NO |
| ARCH-003 | `archive/wp1_governance_engine_backup/backup_20260607_013241/` | 2026-06-07 01:32 | governance/*.yaml | ~30KB | NO |
| ARCH-004 | `archive/wp2_agent_framework_backup/backup_20260607_040410/` | 2026-06-07 04:04 | agents/*/ | ~80KB | NO |
| ARCH-005 | `archive/wp35_learning_intelligence_design_backup/backup_20260607_085853/` | 2026-06-07 08:58 | memory.md, design docs | ~60KB | NO |
| ARCH-006 | `archive/wp35_sage_round2_backup/backup_20260607_092305/` | 2026-06-07 09:23 | *.md review docs | ~40KB | NO |

**Total archive size:** ~340KB (estimate)
**Current discoverability:** Manual directory listing only
**Current retrieval method:** File Explorer / `Get-ChildItem -Recurse`

### 1.2 Empty Archive Infrastructure

| Path | Purpose | Status |
|------|---------|--------|
| `memory/archive_registry/` | Archive index directory | EMPTY |
| `memory/archive_registry/` | No index file exists | NOT CREATED |

---

## 2. Lifecycle Classification

### 2.1 State Definitions

| Lifecycle State | Definition | Retention Policy | Example |
|----------------|------------|-----------------|---------|
| **ACTIVE** | Currently authoritative, in operational use | Permanent in working tree | `sovereign/legal_index.yaml` |
| **DEPRECATED** | Superseded but still accessible in working tree | Retained in place with deprecation notice | Design docs superseded by codex |
| **SUPERSEDED** | Replaced by newer version; preserved for history | Move to archive/ with version reference | Constitution v1.0 → v1.1 |
| **ARCHIVE** | Cold storage; no longer in working tree | `archive/` with index entry | Action: move from active tree |
| **QUARANTINE** | Blocked; pending investigation | `sovereign/quarantine/` | Invalid records, policy violations |

### 2.2 Current Lifecycle Assignment

| Asset Group | Current State | Target State | Rationale |
|-------------|--------------|--------------|-----------|
| Sovereign documents (15) | ACTIVE | ACTIVE | Authoritative legal corpus |
| Sovereign registries (6) | ACTIVE | ACTIVE (after normalization) | Canonical metadata |
| Codex standards (7) | ACTIVE | ACTIVE | Canonical knowledge doctrine |
| Python code registries (5) | ACTIVE | ACTIVE | Core infrastructure |
| Design docs (6 duplicated) | ACTIVE | SUPERSEDED → ARCHIVE | Superseded by codex standards |
| Design docs (8 unique) | ACTIVE | ACTIVE | No canonical replacement |
| Constitution v1.0 (2 copies) | ACTIVE | SUPERSEDED → ARCHIVE | v1.1 is authoritative |
| Legal registry duplicates (2) | ACTIVE | ARCHIVE | legal_index.yaml is canonical |
| Backups (6) | ARCHIVE (implicit) | ARCHIVE (indexed) | No index exists today |
| Empty directories (10) | ACTIVE (placeholder) | DEPRECATED | Remove from active tree |
| Review packages (12) | ACTIVE | DEPRECATED (phase-appropriate) | Superseded by later phases |
| Interface specs (4) | ACTIVE | ACTIVE | Current design references |

---

## 3. Archive Index Design

### 3.1 Archive Index Schema

Proposed file: `memory/archive_registry/archive_index.yaml`

```yaml
archive_index:
  version: "1.0"
  created_at: "2026-06-07T00:00:00Z"
  last_updated: "2026-06-07T00:00:00Z"
  entries:
    - archive_id: "ARCH-001"
      name: "Legal Reorganization Backup"
      date: "2026-06-07T01:12:03Z"
      source_path: "sovereign/laws/"
      trigger: "legal_reorganization"
      work_package: "WP0"
      file_count: 5
      size_bytes: 80000
      registry_snapshot_hash: "sha256:..."
      status: "PRESERVED"
    - archive_id: "ARCH-002"
      name: "WP0 Bootstrap Backup"
      date: "2026-06-07T01:19:03Z"
      source_path: "sovereign/"
      trigger: "wp0_bootstrap"
      work_package: "WP0"
      file_count: 10
      size_bytes: 50000
      registry_snapshot_hash: "sha256:..."
      status: "PRESERVED"
    # ... (remaining 4 entries)
```

### 3.2 Index Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `archive_id` | string | YES | Unique identifier: ARCH-NNN |
| `name` | string | YES | Human-readable name |
| `date` | string (ISO 8601) | YES | When the archive was created |
| `source_path` | string | YES | Original location of backed-up files |
| `trigger` | string | YES | Why the archive was created |
| `work_package` | string | YES | Which WP caused the archive |
| `file_count` | integer | YES | Number of files in archive |
| `size_bytes` | integer | YES | Total size |
| `registry_snapshot_hash` | string | YES | SHA256 of legal_index.yaml at time of archive |
| `manifest` | list[string] | OPTIONAL | List of archived file paths (relative) |
| `status` | string | YES | PRESERVED, RESTORED, VERIFIED |
| `notes` | string | OPTIONAL | Free-text commentary |

---

## 4. Archive Normalization Strategy

### 4.1 Stage 1: Index Existing Backups

| Step | Action | Detail |
|------|--------|--------|
| 1.1 | Create `memory/archive_registry/` if absent | Ensure directory exists |
| 1.2 | Generate `archive_index.yaml` | Enumerate all 6 existing backups |
| 1.3 | Compute `registry_snapshot_hash` for each archive | SHA256 of legal_index.yaml at time of archive (approximate from backup contents) |
| 1.4 | Add `manifest` for each archive | List all files with relative paths |

### 4.2 Stage 2: Move Superseded Assets to Archive

| Step | Action | Source | Archive Target |
|------|--------|--------|---------------|
| 2.1 | Archive duplicate legal registries | `sovereign/registries/legal_registry.yaml` | `archive/registry_consolidation/backup_<date>/` |
| 2.2 | Archive codex LEGAL_REGISTRY.yaml | `docs/legal/codex/registries/LEGAL_REGISTRY.yaml` | `archive/registry_consolidation/backup_<date>/` |
| 2.3 | Archive superseded design docs | `docs/design/AK_LESSON_QUALITY_MODEL.md` (etc.) | `archive/design_supersession/backup_<date>/` |
| 2.4 | Archive constitution v1.0 copies | `docs/governance/ALKASIK_CONSTITUTION_v1.0.md` + codex copy | `archive/constitution_v1.0/backup_<date>/` |

### 4.3 Stage 3: Deprecate Empty Directories

| Step | Action | Detail |
|------|--------|--------|
| 3.1 | Mark 10 empty directories as deprecated | Add `.deprecated` marker file or update registry |
| 3.2 | Record placeholder intent | Document what each directory was intended for |
| 3.3 | Retain or remove per Sage decision | Option A: remove (clean), Option B: leave with deprecation notice |

---

## 5. Lifecycle Governance

### 5.1 Archive Promotion/Demotion Rules

| Transition | Authority Required | Trigger | Documentation |
|------------|-------------------|---------|---------------|
| ACTIVE → DEPRECATED | Sage review | Superseded by new version | Deprecation notice in file header |
| DEPRECATED → ARCHIVE | Sage review + Janus authorization | No operational need for 30+ days | Archive index entry created |
| ARCHIVE → ACTIVE | Hung Vuong approval | Error correction, historical restoration | Archive index updated |
| ACTIVE → QUARANTINE | Sage + Janus | Policy violation, security finding | Quarantine record created |
| QUARANTINE → ARCHIVE | Sage review | Investigation complete, no action needed | Archive index entry |

### 5.2 Archive Retention Policy

| Asset Type | Minimum Retention | Maximum Retention | Disposal |
|------------|-------------------|-------------------|----------|
| Legal documents | Permanent | Permanent | None |
| Registry files | 1 year post-supersession | 5 years | Sage + Hung Vuong |
| Design docs | 1 year post-supersession | 3 years | Sage |
| Backups | 2 years | 5 years | Janus |
| Quarantine records | Until resolution + 1 year | 3 years | Sage + Janus |

---

## 6. Post-Normalization Archive Directory Structure

```
archive/
├── archive_index.yaml                ← NEW: master index
├── legal_reorganization/             ← EXISTING: preserved
├── wp0_bootstrap_backup/             ← EXISTING: preserved
├── wp1_governance_engine_backup/     ← EXISTING: preserved
├── wp2_agent_framework_backup/       ← EXISTING: preserved
├── wp35_learning_intelligence_design_backup/  ← EXISTING
├── wp35_sage_round2_backup/          ← EXISTING: preserved
├── registry_consolidation/           ← NEW: duplicate registries
├── design_supersession/              ← NEW: superseded design docs
└── constitution_v1.0/               ← NEW: superseded constitution
```

---

## 7. Compliance Verification

| Legal Document | Articles | Archive Compliance |
|----------------|----------|-------------------|
| Retention Decree | Art. on preservation | Archive before delete: PASS |
| Memory Law | Art. on record lifecycle | Lifecycle states defined: PASS |
| Knowledge Governance Decree | Art. on knowledge disposition | Archive strategy documented: PASS |
| Constitution v1.1 | Art. 27, 36–39 | No constitutional content archived: PASS |

---

*End of Archive Normalization Plan.*
