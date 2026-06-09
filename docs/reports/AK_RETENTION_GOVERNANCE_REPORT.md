# AK Retention Governance Report

Date: 2026-06-07 | Authority: NAOP Legal & Integration Completion Patch v1.0

## Retention Classes (RETENTION_CLASSES dict)

| Class | retention_days | archive_policy | compaction_policy |
|---|---|---|---|
| TRANSIENT | 30 | auto_delete | 30d |
| OPERATIONAL | 365 | auto_archive | 1y |
| CANONICAL | None | permanent | never |
| ARCHIVAL | None | compressed | compressed_never |

## Field Injection (via _retention_fields)

Every record written through NationalMemoryPlatform methods receives:
- `retention_class` — from the method's default or caller override
- `archive_policy` — from RETENTION_CLASSES lookup
- `compaction_policy` — from RETENTION_CLASSES lookup
- `retention_until` — ISO timestamp computed as `now + retention_days`, or None for permanent classes

## Retention Policy Runtime (apply_retention_policy)

- Scans all 13 MANDATORY_TABLES
- Identifies records where `retention_until < now`
- Supports dry_run mode (default) and live deletion
- Granular per-table action reporting

## Verified Tables

| Table | Retention Class Default | Verified |
|---|---|---|
| ak_evidence | OPERATIONAL | YES |
| ak_lesson_candidates | OPERATIONAL | YES |
| ak_lessons | OPERATIONAL | YES |
| ak_knowledge | CANONICAL | YES |
| ak_skills | CANONICAL | YES |
| ak_capabilities | CANONICAL | YES |
| ak_capability_usage | OPERATIONAL | YES |
| ak_capability_roi | CANONICAL | YES |
| ak_agent_performance | OPERATIONAL | YES |
| ak_missions | OPERATIONAL | YES |
| ak_council_reviews | CANONICAL | YES |
| ak_audit_events | CANONICAL | YES |
| ak_activation_events | CANONICAL | YES |

## Gaps Found

None. Retention fields injected on all 13 tables. Policy enforcement runtime operational.
