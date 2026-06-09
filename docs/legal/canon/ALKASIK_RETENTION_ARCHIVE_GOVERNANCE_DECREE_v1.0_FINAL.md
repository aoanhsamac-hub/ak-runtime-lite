# ALKASIK RETENTION & ARCHIVE GOVERNANCE DECREE v1.0 FINAL

Source: sovereign/decrees/infrastructure/ALKASIK_RETENTION_ARCHIVE_GOVERNANCE_DECREE_v1.0_FINAL.docx
Status: FINAL
Authority: Hung Vuong
Canonical Format: docs/legal/canon/ALKASIK_RETENTION_ARCHIVE_GOVERNANCE_DECREE_v1.0_FINAL.md

## Note

Original .docx file is binary and not extractable in current environment.

## Key Requirements (from available documentation)

### Retention Classes

| Class | Retention Period | Compaction Policy |
|---|---|---|
| TRANSIENT | 30 days | Auto-delete after expiry |
| OPERATIONAL | 1 year | Archive after 1 year |
| CANONICAL | Permanent | No deletion |
| ARCHIVAL | Permanent | No deletion, compressed |

### Mandatory Fields

Every record must have:
- retention_class: TRANSIENT | OPERATIONAL | CANONICAL | ARCHIVAL
- archive_policy: auto_delete | auto_archive | permanent | compressed
- compaction_policy: 30d | 1y | never | compressed_never
- created_at: ISO timestamp
- retention_until: ISO timestamp or null

### Archive Management

- Archived records must remain queryable
- Archived records must be marked with status=ARCHIVED
- Deletion must follow retention policy
- No early deletion without Sage approval
- Archive index must be maintained

### Compaction Rules

- TRANSIENT: Delete records older than 30 days
- OPERATIONAL: Move records older than 1 year to archive
- CANONICAL: Never compact
- ARCHIVAL: Compress storage, never delete

### Auditing

- All retention policy changes must be audited
- All archive operations must be logged
- Hermes is responsible for archive management
- Sage must review archive policy changes
