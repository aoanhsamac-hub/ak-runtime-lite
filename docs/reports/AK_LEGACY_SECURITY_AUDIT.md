# AK Legacy Security Audit

**Directive:** WP-LKI-01 Phase 9
**Agent:** Lang Lieu
**Date:** 2026-06-07 06:51:17 UTC
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


## Potentially Sensitive Files Detected (EXCLUDED from migration)

| File | Sensitivity |
|------|-------------|
| config_loader.py | SENSITIVE_CONTENT |
| requirements.lock.txt | SENSITIVE_CONTENT |
| api_gateway/openrouter_gateway.py | SENSITIVE_CONTENT |
| Archive/legacy/app.py | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/config_loader.py | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/api_gateway/openrouter_gateway.py | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/Archive/legacy/app.py | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/agent-security-apex/example_prompts.csv | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/ai-memory-with-cognee/data/copilot_conversations.json | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/kotlin-agent-with-koog/README.md | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/kotlin-agent-with-koog/tutorial.md | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.aionui/FEATURE_CHANNELS_LARK_LARK.md | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.claude/commands/package-assistant.md | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.claude/skills/pr-fix/SKILL.md | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.claude/skills/pr-review/SKILL.md | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.claude/skills/pr-ship/SKILL.md | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.github/CICD_SETUP.md | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.github/actions/call-openai/action.yml | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.github/actions/checkout-pr/action.yml | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.github/workflows/pr-checks.yml | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.github/workflows/release-distribute.yml | SENSITIVE_CONTENT |
| backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/prds/remote/webui/webui.md | SENSITIVE_CONTENT |
| Planning/ALKASIK_Kingdom_Architecture_v6.1.md | SENSITIVE_CONTENT |
| Planning/ALKASIK_Kingdom_v7.0_NEURON.md | SENSITIVE_CONTENT |
| tests/test_aionui_no_legacy_ui.py | SENSITIVE_CONTENT |
| tests/test_telegram_bridge.py | SENSITIVE_CONTENT |
| tools/tailscale_setup.py | SENSITIVE_CONTENT |
| tools/vps_tailscale_sync.py | SENSITIVE_CONTENT |

## Quarantine List

| File | Score | Reason |
|------|-------|--------|
| alkasik_runtime.py | 27 | quarantine |
| config_loader.py | 53 | sensitive_content |
| console_utils.py | 15 | quarantine |
| README.md | 23 | quarantine |
| requirements.lock.txt | 46 | sensitive_content |
| requirements.txt | 15 | quarantine |
| sync_vps_data.py | 29 | quarantine |
| agents/factory.py | 27 | quarantine |
| agents/__init__.py | 15 | quarantine |
| agents/hermes/__init__.py | 15 | quarantine |
| agents/sage/__init__.py | 15 | quarantine |
| agents/shared/__init__.py | 25 | quarantine |
| agents/yet_kieu/__init__.py | 15 | quarantine |
| aionui/requirements.txt | 15 | quarantine |
| alkasik_dependency_audit_package/README.md | 15 | quarantine |
| alkasik_dependency_audit_package/docs/operations/CODEX_PROMPT_DEPENDENCY_AUDIT.md | 15 | quarantine |
| alkasik_phase_c_refactor_intelligence_package/README.md | 15 | quarantine |
| alkasik_vnext_migration_package/README.md | 15 | quarantine |
| api_gateway/openrouter_gateway.py | 70 | sensitive_content |
| api_gateway/__init__.py | 15 | quarantine |
| Archive/db_backups/20260525_205342/__init__.py | 15 | quarantine |
| Archive/legacy/app.py | 38 | sensitive_content |
| Archive/legacy/daily_log.txt | 15 | quarantine |
| Archive/legacy/test.py | 15 | quarantine |
| backups/pre_cleanup/20260606_210352/alkasik_runtime.py | 27 | quarantine |
| backups/pre_cleanup/20260606_210352/config_loader.py | 53 | sensitive_content |
| backups/pre_cleanup/20260606_210352/console_utils.py | 15 | quarantine |
| backups/pre_cleanup/20260606_210352/dashboard.log | 23 | quarantine |
| backups/pre_cleanup/20260606_210352/error.log | 15 | quarantine |
| backups/pre_cleanup/20260606_210352/aionui/requirements.txt | 15 | quarantine |
| ... | (2090 more) | |

## Excluded Binary / Unsafe Files

| Count | Action |
|-------|--------|
| 88503 | Excluded from scan |
| 28 | Detected as sensitive (excluded) |
| 2120 | Quarantined (low score) |
