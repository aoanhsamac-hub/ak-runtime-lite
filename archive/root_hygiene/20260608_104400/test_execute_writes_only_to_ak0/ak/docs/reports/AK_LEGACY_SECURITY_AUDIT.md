# AK Legacy Security Audit

**Directive:** WP-LKI-01 Phase 9
**Agent:** Lang Lieu
**Date:** 2026-06-07 12:12:47 UTC
**Status:** PASS

## Security Checks

| Check | Result |
|-------|--------|
| Secrets migrated into candidates | NO - 0 secrets in candidates |
| Credentials migrated | NO |
| Broker login migrated | NO |
| Runtime link created | NO |
| Legacy code imported into AK runtime | NO |
| Unsafe binaries ingested | NO |
| Excluded sensitive files listed | YES |


## Quarantine List

| File | Score | Reason |
|------|-------|--------|
| code.py | 15 | quarantine |
| config.yaml | 15 | quarantine |
| data.csv | 15 | quarantine |
| normal.txt | 15 | quarantine |
| README.md | 15 | quarantine |
| docs/report.md | 15 | quarantine |

## Excluded Binary / Unsafe Files

| Count | Action |
|-------|--------|
| 0 | Excluded from scan |
| 0 | Detected as sensitive (excluded) |
| 6 | Quarantined (low score) |
