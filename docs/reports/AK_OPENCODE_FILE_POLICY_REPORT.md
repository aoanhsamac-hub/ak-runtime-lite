# AK OpenCode File Policy Report

Directive: WP-REPO-HYGIENE-01 | Date: 2026-06-08

## Policy Created

docs/policies/AK_OPENCODE_FILE_PLACEMENT_POLICY.md

## Policy Coverage

| Requirement | Status |
|---|---|
| OpenCode may not create files in root | ✅ Enforced |
| Reports go to docs/reports/ | ✅ Enforced |
| Reviews go to docs/reviews/ | ✅ Enforced |
| Designs go to docs/design/ | ✅ Enforced |
| Scripts go to scripts/ | ✅ Enforced |
| Tools go to tools/ | ✅ Enforced |
| Tests go to tests/ | ✅ Enforced |
| Pipelines go to pipelines/ | ✅ Enforced |
| Services go to services/ | ✅ Enforced |
| Temporary files go to archive/tmp/ | ✅ Enforced |
| Uncertain files require classification | ✅ Enforced |
| Legal basis required | ✅ Enforced |
| Root hygiene gate enforced | ✅ Automated test |

## Enforcement Mechanism

- **Automated test**: `tests/test_root_hygiene.py` (3 tests)
- **Governance gate**: Built into test suite
- **Archive registry**: `memory/archive_registry/archive_index.yaml`
