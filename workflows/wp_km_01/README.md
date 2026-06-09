# WP-KM-01 Legacy Knowledge Migration Program

Migrates legacy knowledge artifacts from the AK codebase into 5 governance-controlled candidate registries (decision trace, lesson, dataset, skill, capability).

## Entrypoint

```bash
python workflows/wp_km_01/knowledge_migration.py
```

## Deliverables

- `knowledge_migration.py` — automated migration script
- `docs/reports/AK_LEGACY_KNOWLEDGE_DISCOVERY_REPORT.md`
- `docs/reports/AK_KNOWLEDGE_CLASSIFICATION_REPORT.md`
- `docs/reports/AK_KNOWLEDGE_TRACEABILITY_MAP.md`
- `docs/reports/AK_LEGACY_KNOWLEDGE_MIGRATION_AUDIT.md`
- `docs/reports/WP_KM_01_FINAL_REPORT.md`
- `memory/knowledge_registry/migration_manifest.json`

## Status

COMPLETE — 34 candidates migrated across 5 registries. 134/134 tests pass.
