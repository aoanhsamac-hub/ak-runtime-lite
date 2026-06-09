# AK Legacy Knowledge Traceability Map

**Directive:** WP-LKI-01 Phase 8
**Agent:** Lang Lieu
**Date:** 2026-06-07 06:51:15 UTC
**Status:** COMPLETE

## Traceability Model

Candidate → Source Path → Source Hash → Domain → Evidence → Owner Agent → Reviewer Agent → Governance Authority

## Candidates

| Candidate ID | Type | Source Path | Source Hash | Domain | Confidence | Owner | Reviewer | Authority |
|-------------|------|-------------|-------------|--------|-----------|-------|----------|-----------|
| LKI-F3B0F47FE700 | lesson_candidate | hungvuong.py | 484122bbf9e03707... | Agent Knowledge | 72 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-ACD7015302C9 | lesson_candidate | agents/helen_controller.py | 1ca4c79a16b54db7... | Agent Knowledge | 63 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-3F38891862DA | lesson_candidate | agents/iris_agent.py | 349b1948a3aab707... | Market Knowledge | 67 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-3A5ACF2AA508 | lesson_candidate | agents/janus_core.py | 9a54be1d80653e83... | Trading Knowledge | 72 | Iris | Sage | AK-CODEX v1.0 |
| LKI-675AC43452D1 | lesson_candidate | agents/lang_lieu_agent.py | e0c6301ebdfa2292... | Execution Knowledge | 63 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-6E794C901D23 | lesson_candidate | agents/hermes/hermes_agent.py | ffd2671da7243e46... | Agent Knowledge | 73 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-CD53B4C973B9 | lesson_candidate | agents/sage/sage_agent.py | d1256282713c0314... | Risk Knowledge | 63 | Sage | Sage | ALKASIK RISK LAW v1.0 |
| LKI-133245D3377B | lesson_candidate | agents/shared/base_agent.py | 0846ea1a83e9fbc0... | Risk Knowledge | 72 | Sage | Sage | ALKASIK RISK LAW v1.0 |
| LKI-C44EFDB740B2 | lesson_candidate | aionui/main.py | 00e39fc7f2d84e7e... | Trading Knowledge | 72 | Iris | Sage | AK-CODEX v1.0 |
| LKI-15CDF251CA0B | lesson_candidate | aionui/static/index.html | f456981acea13136... | Execution Knowledge | 67 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-95BDB01EBB1F | skill_candidate | alkasik_dependency_audit_package/scripts/analysis/build_dependency_graph.py | d815dbca2feb78ed... | Memory Knowledge | 60 | Hermes | Sage | ALKASIK_MEMORY_LAW_v1.0 |
| LKI-3D6E1D13B0F4 | lesson_candidate | alkasik_vnext_migration_package/scripts/migration/alkasik_vnext_phase_ab.py | e7cd0b27ffb9219d... | Execution Knowledge | 66 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-81240C6D92C0 | dataset_candidate | api_gateway/llm_router_gateway.py | 42b7b5b06b04150d... | Engineering Knowledge | 73 | Lang Lieu | Sage | ALKASIK_REPO_GOVERNANCE_DECREE_v1.0 |
| LKI-2F5FA07C545F | lesson_candidate | backups/pre_cleanup/20260606_210352/DATA_GOVERNANCE_MIGRATION_PLAN.md | 402d932782a7ae0f... | Trading Knowledge | 72 | Iris | Sage | AK-CODEX v1.0 |
| LKI-259CF21671F4 | lesson_candidate | backups/pre_cleanup/20260606_210352/memory.md | af0d6c4bdcdf1508... | Execution Knowledge | 72 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-83D959E6ED5E | lesson_candidate | backups/pre_cleanup/20260606_210352/MEMORY_COMPACTION_IMPLEMENTATION_REPORT.md | 64caff87c2b39412... | Execution Knowledge | 72 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-7C05B165575A | lesson_candidate | backups/pre_cleanup/20260606_210352/alkasik_root_cleanup_package/scripts/migration/reorganize_root_safe.py | a85cd60dba415d96... | Agent Knowledge | 62 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-9FAB040B2E53 | lesson_candidate | backups/pre_cleanup/20260606_210352/configs/agents/skill_registry.yaml | 658bc31c3bb0f177... | Market Knowledge | 72 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-07F18F61215D | lesson_candidate | backups/pre_cleanup/20260606_210352/Data/inventory_backtest/XAUUSDm_M5_202604010000_202606020655.csv | 582964e2ad09545d... | Market Knowledge | 66 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-3E590962471E | lesson_candidate | backups/pre_cleanup/20260606_210352/Data/raw_indicators/batch_20260530_100710.json | 906d6cf6be2568ee... | Trading Knowledge | 66 | Iris | Sage | AK-CODEX v1.0 |
| LKI-7544255696F8 | lesson_candidate | backups/pre_cleanup/20260606_210352/Data/raw_indicators/foundation_20260530_100850.json | 8e326b17f550fe1e... | Trading Knowledge | 63 | Iris | Sage | AK-CODEX v1.0 |
| LKI-EABD6C42CBA5 | skill_candidate | backups/pre_cleanup/20260606_210352/database/db_manager.py | cae6f61bf69a1bfb... | Memory Knowledge | 63 | Hermes | Sage | ALKASIK_MEMORY_LAW_v1.0 |
| LKI-D9BF12C216AD | lesson_candidate | backups/pre_cleanup/20260606_210352/database/migration.py | f578bbe4050159bc... | Agent Knowledge | 63 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-B67B4E45100D | dataset_candidate | backups/pre_cleanup/20260606_210352/dataset_pipeline/dataset_pipeline.py | 68c65a57df3d7353... | Engineering Knowledge | 72 | Lang Lieu | Sage | ALKASIK_REPO_GOVERNANCE_DECREE_v1.0 |
| LKI-0C88AE8F668F | lesson_candidate | backups/pre_cleanup/20260606_210352/decision_trace/decision_trace.py | 8dc7fb3f418ed8e4... | Trading Knowledge | 69 | Iris | Sage | AK-CODEX v1.0 |
| LKI-415B9657AD3F | lesson_candidate | backups/pre_cleanup/20260606_210352/deploy/yet_kieu_vps/yet_kieu_collector.py | 2b10d843fd8b15fc... | Trading Knowledge | 69 | Iris | Sage | AK-CODEX v1.0 |
| LKI-4269C1ABBFA2 | lesson_candidate | backups/pre_cleanup/20260606_210352/event_bus/event_bus.py | 42c25751a220249d... | Market Knowledge | 67 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-C6A5B34B78D5 | lesson_candidate | backups/pre_cleanup/20260606_210352/evolution_sandbox/sandbox.py | f7fde5223922ed3e... | Risk Knowledge | 72 | Sage | Sage | ALKASIK RISK LAW v1.0 |
| LKI-77003E4264B4 | lesson_candidate | backups/pre_cleanup/20260606_210352/execution_intelligence/execution_intelligence.py | a270d769fedca0b5... | Trading Knowledge | 76 | Iris | Sage | AK-CODEX v1.0 |
| LKI-24D18E468840 | lesson_candidate | backups/pre_cleanup/20260606_210352/execution_planner/execution_planner.py | c14f4d10faa08219... | Trading Knowledge | 72 | Iris | Sage | AK-CODEX v1.0 |
| LKI-BA810E924030 | lesson_candidate | backups/pre_cleanup/20260606_210352/hermes/memory_hygiene.py | f0343fa17aed5e06... | Agent Knowledge | 69 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-26FFD34AB119 | lesson_candidate | backups/pre_cleanup/20260606_210352/inventory_bot/backtest.py | b8b69f1da41b9b7b... | Trading Knowledge | 72 | Iris | Sage | AK-CODEX v1.0 |
| LKI-435A77AB3D2E | lesson_candidate | backups/pre_cleanup/20260606_210352/inventory_bot/engine.py | c1e3c5acb9dfa05b... | Market Knowledge | 62 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-374554D7F26C | lesson_candidate | backups/pre_cleanup/20260606_210352/inventory_bot/runner.py | 0f11de35a4feec59... | Trading Knowledge | 67 | Iris | Sage | AK-CODEX v1.0 |
| LKI-AE8D874DB344 | lesson_candidate | backups/pre_cleanup/20260606_210352/knowledge_trust/knowledge_trust.py | 657a6bbe3fa79bc6... | Trading Knowledge | 72 | Iris | Sage | AK-CODEX v1.0 |
| LKI-2CD6EC39B8FB | lesson_candidate | backups/pre_cleanup/20260606_210352/learning/cognitive_market_intelligence.py | f6aeb21c2e46d960... | Execution Knowledge | 66 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-F368C9EACB73 | lesson_candidate | backups/pre_cleanup/20260606_210352/learning/progress_tracker.md | 93189bf2ee4032f2... | Agent Knowledge | 62 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-E110EE0C49F5 | lesson_candidate | backups/pre_cleanup/20260606_210352/learning/behavior_forecasting/behavior_forecaster.py | 86cc82ce7672a8a4... | Market Knowledge | 76 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-7CB7915894BA | lesson_candidate | backups/pre_cleanup/20260606_210352/learning/execution_adaptation/execution_adapter.py | 7f24bcca7f3f102c... | Trading Knowledge | 72 | Iris | Sage | AK-CODEX v1.0 |
| LKI-0B1760436B12 | lesson_candidate | backups/pre_cleanup/20260606_210352/learning/explainability/explainability.py | 8ad472a833143e95... | Trading Knowledge | 72 | Iris | Sage | AK-CODEX v1.0 |
| LKI-BD825DDB5353 | lesson_candidate | backups/pre_cleanup/20260606_210352/learning/liquidity_intelligence/liquidity_intelligence.py | 79a006261c81bd92... | Market Knowledge | 73 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-F002D55D69CB | skill_candidate | backups/pre_cleanup/20260606_210352/learning/memory_engine/memory_engine.py | 6a439a4f85123a23... | Memory Knowledge | 73 | Hermes | Sage | ALKASIK_MEMORY_LAW_v1.0 |
| LKI-69DDDC563415 | lesson_candidate | backups/pre_cleanup/20260606_210352/learning/multi_timeframe_cognition/multi_timeframe_cognition.py | e4f3eb75e240a7d7... | Execution Knowledge | 70 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-8FC69E1F8176 | lesson_candidate | backups/pre_cleanup/20260606_210352/learning/narrative_tracker/narrative_tracker.py | 83733ab01c45c588... | Market Knowledge | 60 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-D9DC4CCEEF16 | lesson_candidate | backups/pre_cleanup/20260606_210352/learning/pattern_encoder/pattern_encoder.py | c1174c94bf179775... | Market Knowledge | 62 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-A3CC8A9634B6 | lesson_candidate | backups/pre_cleanup/20260606_210352/learning/regime_classifier/regime_classifier.py | 0737b18254b0143e... | Market Knowledge | 76 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-E4F9E4F38808 | lesson_candidate | backups/pre_cleanup/20260606_210352/learning/similarity_search/similarity_search.py | bf4d5e6317038900... | Execution Knowledge | 73 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-6D310AF33BAA | lesson_candidate | backups/pre_cleanup/20260606_210352/learning/structure_encoder/structure_encoder.py | 0a639e276efc2a3f... | Market Knowledge | 60 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-0AA6240F8FE1 | skill_candidate | backups/pre_cleanup/20260606_210352/learning/structure_memory/structure_memory.py | 249b9e2c91c46d64... | Memory Knowledge | 70 | Hermes | Sage | ALKASIK_MEMORY_LAW_v1.0 |
| LKI-DCEBA395DB62 | lesson_candidate | backups/pre_cleanup/20260606_210352/learning_budget/budget_governor.py | 620a70bb837ed3b8... | Market Knowledge | 73 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-24EE0307108B | lesson_candidate | backups/pre_cleanup/20260606_210352/lesson_distillation/pipeline.py | 1ea772065b49c8db... | Trading Knowledge | 72 | Iris | Sage | AK-CODEX v1.0 |
| LKI-3CA1D9797718 | lesson_candidate | backups/pre_cleanup/20260606_210352/lightgate/mcp/kingdom_mcp_server.py | af68e4bfa1f7f133... | Agent Knowledge | 72 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-8755E3224CC7 | skill_candidate | backups/pre_cleanup/20260606_210352/memory_lifecycle/stages.py | 9a38956ad1ca921c... | Memory Knowledge | 63 | Hermes | Sage | ALKASIK_MEMORY_LAW_v1.0 |
| LKI-DBB6780CE451 | dataset_candidate | backups/pre_cleanup/20260606_210352/observability_stack/observability.py | 844a72d0d62a4201... | Engineering Knowledge | 67 | Lang Lieu | Sage | ALKASIK_REPO_GOVERNANCE_DECREE_v1.0 |
| LKI-ABA948317F59 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/CONTRIBUTING.md | 74ba2bda6bd89abb... | Market Knowledge | 70 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-0992B5C716CC | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/README.md | 9c98f085d531a2b9... | Execution Knowledge | 62 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-41987F549336 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/agent-security-apex/model_testing_tools.py | 6da7fa944673074f... | Agent Knowledge | 70 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-757B77C8B7A4 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/agent-security-apex/prompt_manipulation_tools.py | 3a7464f31caf116a... | Trading Knowledge | 60 | Iris | Sage | AK-CODEX v1.0 |
| LKI-598FA0011B55 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/agent-with-tavily-web-access/supplemental/docs/amazon.pdf | a4aada1fc5c24099... | Market Knowledge | 63 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-8B422F93EE67 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/agent-with-tavily-web-access/supplemental/docs/apple.pdf | 1812024b17774763... | Market Knowledge | 63 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-604F9AA415D6 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/agent-with-tavily-web-access/supplemental/docs/google.pdf | fbc486c32d058a96... | Market Knowledge | 63 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-F28B2DC32FD4 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/agent-with-tavily-web-access/supplemental/docs/meta.pdf | 6c02d200ef1b0329... | Market Knowledge | 63 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-4BA25B9C3DD3 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/agent-with-tavily-web-access/supplemental/docs/microsoft.pdf | aac8804de0a3c0cd... | Market Knowledge | 63 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-453DACEA8ACA | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/agent-with-tavily-web-access/supplemental/docs/tesla.pdf | 3bafc476a8e2ff80... | Trading Knowledge | 63 | Iris | Sage | AK-CODEX v1.0 |
| LKI-A140FDC28636 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/ai-memory-with-cognee/guido_contributions.html | 2e3ce1459bd5eed7... | Trading Knowledge | 76 | Iris | Sage | AK-CODEX v1.0 |
| LKI-3FDE2D7EA581 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/ai-memory-with-cognee/data/guido_contributions.json | f20b302c12b7ca7c... | Trading Knowledge | 76 | Iris | Sage | AK-CODEX v1.0 |
| LKI-2309B80B1491 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/docker-intro/README.md | 76b359b5f7a4c6f6... | Execution Knowledge | 72 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-A0400B02D7C7 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/runpod-gpu-deploy/README.md | 93dbc5a68a4396aa... | Trading Knowledge | 76 | Iris | Sage | AK-CODEX v1.0 |
| LKI-21C772FD0275 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/runpod-gpu-deploy/crew-ai-ollama-runpod-tutorial/handler.py | 3fa63b68b089256a... | Execution Knowledge | 70 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-A920DBEB0475 | dataset_candidate | backups/pre_cleanup/20260606_210352/Open source/agents-towards-production/tutorials/runpod-gpu-deploy/crew-ai-ollama-runpod-tutorial/README.md | 30199baa9337ba85... | Engineering Knowledge | 76 | Lang Lieu | Sage | ALKASIK_REPO_GOVERNANCE_DECREE_v1.0 |
| LKI-E52CDDDFE1A0 | dataset_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/AGENTS.md | 25d2671ff8d59519... | Engineering Knowledge | 73 | Lang Lieu | Sage | ALKASIK_REPO_GOVERNANCE_DECREE_v1.0 |
| LKI-E37E8A130851 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/CONTRIBUTING.md | a3ac90fccdb6a8c5... | Trading Knowledge | 62 | Iris | Sage | AK-CODEX v1.0 |
| LKI-8E9AEE136D22 | dataset_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/package.json | 0e242f3b1b134d5f... | Engineering Knowledge | 60 | Lang Lieu | Sage | ALKASIK_REPO_GOVERNANCE_DECREE_v1.0 |
| LKI-C5E85271295E | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/readme.md | a1f172bd7ec4e689... | Market Knowledge | 76 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-E20B7D2AC455 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.aionui/FEATURE_CHANNELS.md | 085c5d21db0d2199... | Trading Knowledge | 66 | Iris | Sage | AK-CODEX v1.0 |
| LKI-21E4B0144DA5 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.aionui/FEATURE_DEV_TEMPLATE.md | 121aca4fb9a6192a... | Agent Knowledge | 76 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-E61842CA75B8 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.claude/skills/architecture/SKILL.md | 54c1456a2f69f6a3... | Execution Knowledge | 70 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-11767B637838 | dataset_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.claude/skills/architecture/references/renderer.md | 6a11676180ac3378... | Engineering Knowledge | 63 | Lang Lieu | Sage | ALKASIK_REPO_GOVERNANCE_DECREE_v1.0 |
| LKI-5E195C66C9A6 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.claude/skills/fix-issues/SKILL.md | cc95fe0c56a7b022... | Trading Knowledge | 76 | Iris | Sage | AK-CODEX v1.0 |
| LKI-621E568DFB9E | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.claude/skills/fix-issues/references/triage-rules.md | 6d4f8df285497175... | Execution Knowledge | 76 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-51D301AAF036 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.claude/skills/fix-sentry/SKILL.md | 952c105355589c6d... | Trading Knowledge | 76 | Iris | Sage | AK-CODEX v1.0 |
| LKI-5C37525C7DFD | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.claude/skills/fix-sentry/references/triage-rules.md | 5e492ce66f19826e... | Market Knowledge | 69 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-BC37DB16705B | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.claude/skills/i18n/SKILL.md | e27b1d3ec003270d... | Execution Knowledge | 72 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-0155B3DB2475 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.claude/skills/pr-automation/SKILL.md | 0347b3b53d47a3ab... | Execution Knowledge | 72 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-65B07724F5A6 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.claude/skills/pr-verify/SKILL.md | aff58498b43e75f1... | Trading Knowledge | 72 | Iris | Sage | AK-CODEX v1.0 |
| LKI-D2EE76D0CEFA | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.github/workflows/build-and-release.yml | 5c4ba2eeebc60864... | Execution Knowledge | 76 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-038996B85D8F | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.github/workflows/gpt-pr-assessment.yml | 45d00a777e0f5d7c... | Execution Knowledge | 72 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-9BD733A5FEEF | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.github/workflows/gpt-review.yml | 9329cd60c76457f3... | Execution Knowledge | 72 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-9C81CB6A0B1A | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.github/workflows/pack-web-cli.yml | 801125b70d0ef4ca... | Trading Knowledge | 70 | Iris | Sage | AK-CODEX v1.0 |
| LKI-58D970DC1292 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.github/workflows/project-automation.yml | 72fbe4d12fd688cf... | Market Knowledge | 73 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-FF8B4A63DC38 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.github/workflows/_build-reusable.yml | 741b969f1c8cb78b... | Execution Knowledge | 72 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-2B7699425086 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/.specify/templates/plan-template.md | e8e36ad2e2d7b81a... | Trading Knowledge | 66 | Iris | Sage | AK-CODEX v1.0 |
| LKI-E5F97EB8D62B | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/contributing/development.md | 7aebc2c1b85e1944... | Execution Knowledge | 76 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-3FA069660727 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/contributing/file-structure.md | 8fad1af22aa62ca1... | Execution Knowledge | 76 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-A58E26917A5D | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/guides/deploy-server.md | b8119c328bcbefa4... | Execution Knowledge | 72 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-3EA1E8902DDF | dataset_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/guides/hub-testing.md | 789c5576e766b979... | Engineering Knowledge | 60 | Lang Lieu | Sage | ALKASIK_REPO_GOVERNANCE_DECREE_v1.0 |
| LKI-126D6271DC08 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/guides/webui.md | 15ad861d02f616bc... | Market Knowledge | 72 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-318EBDE65C45 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/prds/conversations/acp/README.md | b2129ce46f3d17b3... | Market Knowledge | 63 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-0F84EF46DBFF | skill_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/prds/conversations/custom/custom-agent.md | a2528b1603329cc7... | Memory Knowledge | 76 | Hermes | Sage | ALKASIK_MEMORY_LAW_v1.0 |
| LKI-2BD6D5CBCD0D | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/prds/conversations/remote/remote-agent.md | cd0a00f69a2baab5... | Trading Knowledge | 76 | Iris | Sage | AK-CODEX v1.0 |
| LKI-B686F22461E3 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/prds/remote/channels/channels.md | 5249bc135d1cde97... | Trading Knowledge | 76 | Iris | Sage | AK-CODEX v1.0 |
| LKI-56FB6DE7B126 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/prds/settings/about/about-update.md | 4c9a9139a0a236ea... | Trading Knowledge | 76 | Iris | Sage | AK-CODEX v1.0 |
| LKI-29256DA439DE | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/readme/readme_ch.md | d31548bad2cc758c... | Market Knowledge | 66 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-827D71E4000C | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/readme/readme_es.md | 98068c592cc1a904... | Market Knowledge | 76 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-8B2142FC9FDE | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/readme/readme_jp.md | afc14891bf4f6567... | Market Knowledge | 66 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-6A61EE3861DD | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/readme/readme_ko.md | cb5c4a2104e0dd74... | Market Knowledge | 66 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-8129939350FD | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/readme/readme_pt.md | 82210d567206536a... | Market Knowledge | 76 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-333BA6C34563 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/readme/readme_ru.md | 360c28ab9ac99d6e... | Market Knowledge | 66 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-191A7D2C7A21 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/readme/readme_tr.md | 78eb29f3b6b8c3dd... | Market Knowledge | 66 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-D1121965A664 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/readme/readme_tw.md | 53937ec9ac8c5259... | Market Knowledge | 66 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-4F3CBA95E47F | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/docs/readme/readme_uk.md | 404745c6be08f624... | Market Knowledge | 66 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-C330D19939B8 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/mobile/src/i18n/locales/ru-RU.json | 4b2374e4ad41f8c9... | Trading Knowledge | 67 | Iris | Sage | AK-CODEX v1.0 |
| LKI-6632DDCF8432 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/mobile/src/i18n/locales/uk-UA.json | 2111ef8a34171d98... | Trading Knowledge | 67 | Iris | Sage | AK-CODEX v1.0 |
| LKI-CAD80B81D476 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/pages/conversation/Preview/README.cn.md | 2b339f31288627e9... | Market Knowledge | 66 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-B3EFEF54CFC1 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/pages/conversation/Preview/README.en.md | a8574800840b2fd6... | Market Knowledge | 66 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-C6C30197A756 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/pages/conversation/Workspace/README.cn.md | 133e6dc0055628b2... | Trading Knowledge | 73 | Iris | Sage | AK-CODEX v1.0 |
| LKI-AC0C38171DB8 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/pages/conversation/Workspace/README.en.md | 66366cb6ecc9c85c... | Market Knowledge | 76 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-38A3E622147D | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/en-US/codex.json | 9e8ee00afac57eec... | Risk Knowledge | 70 | Sage | Sage | ALKASIK RISK LAW v1.0 |
| LKI-1038D3B617B6 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/en-US/conversation.json | ed501f5e7054cb57... | Market Knowledge | 76 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-95FD5FE19BB9 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/en-US/cron.json | ca15ce018dd6d5d3... | Execution Knowledge | 70 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-4B4C62F10D25 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/en-US/preview.json | 1379b4510adfaa9e... | Market Knowledge | 67 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-5CA45888B0BE | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/en-US/settings.json | 722e890c5664741a... | Market Knowledge | 72 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-0C88D3BC3D87 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/ja-JP/codex.json | 8d104cef570d3b23... | Execution Knowledge | 64 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-65F63414318A | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/ja-JP/conversation.json | fd489e1530c6786f... | Market Knowledge | 70 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-5B615D99D564 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/ja-JP/cron.json | bb507b51aa3e3eef... | Execution Knowledge | 64 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-994EA23284E5 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/ja-JP/preview.json | fab73e1f2d354244... | Market Knowledge | 64 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-54EFA9F00F81 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/ja-JP/settings.json | 68e942bba4a71045... | Market Knowledge | 76 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-F0F0083C550F | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/ko-KR/codex.json | 3bce00f39325a59d... | Execution Knowledge | 70 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-88DEBE45A5E2 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/ko-KR/conversation.json | 498783de8b45ca5c... | Market Knowledge | 76 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-23BE7113973A | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/ko-KR/cron.json | bbdf8306f30c67ed... | Execution Knowledge | 67 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-B8C63B9C73EB | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/ko-KR/preview.json | 9a77af30097a766c... | Market Knowledge | 67 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-F3E8A9C4B40C | dataset_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/ko-KR/settings.json | 718bb90cc0643d27... | Engineering Knowledge | 76 | Lang Lieu | Sage | ALKASIK_REPO_GOVERNANCE_DECREE_v1.0 |
| LKI-B7B135675654 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/ru-RU/codex.json | 708f6f84e315a136... | Market Knowledge | 70 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-C74D468FE2E2 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/ru-RU/conversation.json | b30f35ed880c8ad4... | Market Knowledge | 76 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-684204D197E2 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/ru-RU/cron.json | bed7d336755961e1... | Execution Knowledge | 67 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-4D2D52EA0888 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/ru-RU/preview.json | 01a495f3c9090c55... | Market Knowledge | 67 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-9AFB2951C6AA | dataset_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/ru-RU/settings.json | bb984bd0bd67ba5b... | Engineering Knowledge | 76 | Lang Lieu | Sage | ALKASIK_REPO_GOVERNANCE_DECREE_v1.0 |
| LKI-04B6FBC5456F | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/tr-TR/codex.json | 066f1de88a18d900... | Trading Knowledge | 70 | Iris | Sage | AK-CODEX v1.0 |
| LKI-4C95284CB8D0 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/tr-TR/conversation.json | b2e05b1cb1b7fe53... | Market Knowledge | 76 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-4900A76814E9 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/tr-TR/cron.json | 48127605d713b188... | Execution Knowledge | 70 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-2477D58DCD0D | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/tr-TR/preview.json | 629dcfa6cfab77dc... | Market Knowledge | 67 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-6558D7CCC36B | dataset_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/tr-TR/settings.json | 28d192895f32750a... | Engineering Knowledge | 76 | Lang Lieu | Sage | ALKASIK_REPO_GOVERNANCE_DECREE_v1.0 |
| LKI-8D9876522414 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/uk-UA/codex.json | 6fef10d06a810f16... | Market Knowledge | 70 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-AACECA16832D | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/uk-UA/conversation.json | 96b072bade59c13b... | Market Knowledge | 76 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-499C287619B6 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/uk-UA/cron.json | ec3d221500bfebfd... | Execution Knowledge | 67 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-18F4BBF2F370 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/uk-UA/preview.json | 4a4c62825bb752e5... | Market Knowledge | 67 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-79E9AAFEAF34 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/uk-UA/settings.json | f5806e2cda8a8e61... | Market Knowledge | 76 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-C2AD09C05492 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/zh-CN/codex.json | 9644d01eab4b54ef... | Execution Knowledge | 64 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-8E8E9077C064 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/zh-CN/conversation.json | 90927a2c9fa2377f... | Market Knowledge | 70 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-F669266D60C2 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/zh-CN/cron.json | 33f4f628886b5633... | Execution Knowledge | 64 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-EEFD08DF0C9A | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/zh-CN/preview.json | 8fab2581c73be649... | Trading Knowledge | 64 | Iris | Sage | AK-CODEX v1.0 |
| LKI-B9463736AA42 | dataset_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/zh-CN/settings.json | dd9e7f34f0be2554... | Engineering Knowledge | 76 | Lang Lieu | Sage | ALKASIK_REPO_GOVERNANCE_DECREE_v1.0 |
| LKI-1D2125AB3AFC | dataset_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/zh-TW/codex.json | 2dc81e083fbecbf2... | Engineering Knowledge | 64 | Lang Lieu | Sage | ALKASIK_REPO_GOVERNANCE_DECREE_v1.0 |
| LKI-7BEC905D00DE | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/zh-TW/conversation.json | 98d2199414455925... | Market Knowledge | 70 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-BD77D7EBF516 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/zh-TW/cron.json | bd092d33cb056a33... | Execution Knowledge | 64 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-AA6B6EE86434 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/zh-TW/preview.json | efa0b69b028067e7... | Trading Knowledge | 64 | Iris | Sage | AK-CODEX v1.0 |
| LKI-133D5F12BDA6 | lesson_candidate | backups/pre_cleanup/20260606_210352/Open source/AionUi-2.1.0/packages/desktop/src/renderer/services/i18n/locales/zh-TW/settings.json | 9f2b09a8c114c69c... | Market Knowledge | 76 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-95A11ECC75BC | lesson_candidate | Data/system_maps/import_graph.json | e712a2f0900b584f... | Agent Knowledge | 62 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-F8886861EC5A | lesson_candidate | Data/system_maps/phase_c_import_graph.json | 5f8c1f1f01a63816... | Agent Knowledge | 62 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-62FA379EB60F | decision_trace_candidate | docs/ALKASIK_CONSTITUTION_v1.1_FINAL.docx | 84a3d9c61967d572... | Governance Knowledge | 66 | Sage | Sage | ALKASIK_CONSTITUTION_v1.1_FINAL |
| LKI-0BD8FF988644 | lesson_candidate | docs/ALKASIK_Kingdom_Cockpit_v2.0_Plan.md | 576087f36eb54c70... | Agent Knowledge | 72 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-965622F33001 | decision_trace_candidate | docs/ALKASIK_KNOWLEDGE_GOVERNANCE_DECREE_v1.0_FINAL.docx | 4489195b30281a9c... | Governance Knowledge | 66 | Sage | Sage | ALKASIK_CONSTITUTION_v1.1_FINAL |
| LKI-AC350CEE0DA2 | decision_trace_candidate | docs/ALKASIK_REPO_GOVERNANCE_DECREE_v1.0_FINAL.docx | e4dc55679c5419cc... | Governance Knowledge | 66 | Sage | Sage | ALKASIK_CONSTITUTION_v1.1_FINAL |
| LKI-BCD4A7A230CA | decision_trace_candidate | docs/ALKASIK_RETENTION_DECREE_v1.0_FINAL.docx | 76bc8e9aa004cd2a... | Governance Knowledge | 66 | Sage | Sage | ALKASIK_CONSTITUTION_v1.1_FINAL |
| LKI-56B4E4CCB168 | lesson_candidate | docs/architecture/ALKASIK_YetKieu.md | 2b5443bfc39c1adf... | Agent Knowledge | 72 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-4CEC41B0A4B0 | decision_trace_candidate | docs/governance/ALKASIK CONSTITUTION v1.1 DRAFT.pdf | 3960df81ad6688d6... | Governance Knowledge | 66 | Sage | Sage | ALKASIK_CONSTITUTION_v1.1_FINAL |
| LKI-89F50BEA84E8 | lesson_candidate | docs/governance/ALKASIK_CONSTITUTION_v1.0.md | 2ecfcd2914c0febf... | Trading Knowledge | 62 | Iris | Sage | AK-CODEX v1.0 |
| LKI-E5682A0D31A3 | lesson_candidate | docs/memory/archive/memory_archive_2026-05-26_pre_compact.md | 73d2eead509433a2... | Agent Knowledge | 72 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-11FA7E109A5E | lesson_candidate | docs/memory/archive/memory_archive_2026-05-30_pre_phaseA.md | 3a5e6cf3c0151762... | Execution Knowledge | 72 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-5BB875BCD06E | lesson_candidate | docs/reports/Report 1A.md | 5d8dc064f666bdfd... | Agent Knowledge | 72 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-362D46295DA2 | lesson_candidate | docs/reports/Report 1B.md | 25460f00c059a202... | Agent Knowledge | 62 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-0B862C8CBDF6 | lesson_candidate | docs/reports/STRUCTURE_AUDIT_REPORT.md | 3bf66024ad8de10a... | Execution Knowledge | 62 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-025A3489367E | decision_trace_candidate | docs/reports/VNEXT_PHASE_AB_REPORT_20260606_214751.md | bb2de8defbe438ea... | Governance Knowledge | 62 | Sage | Sage | ALKASIK_CONSTITUTION_v1.1_FINAL |
| LKI-E4728B154B84 | lesson_candidate | docs/reports/VNEXT_PHASE_AB_REPORT_20260606_214903.md | 4ffb0a8590083433... | Execution Knowledge | 62 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-65307D6D0584 | lesson_candidate | hermes/memory_hygiene.py | 7e63e388eaebfe37... | Agent Knowledge | 69 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-60BEF4C4F65D | lesson_candidate | logs/9router.out.log | 9dd3042d59f65b53... | Trading Knowledge | 66 | Iris | Sage | AK-CODEX v1.0 |
| LKI-C85FFD79D472 | lesson_candidate | logs/aionui_8000.log | bbf24863f6972547... | Execution Knowledge | 66 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-E8C0DE4B1061 | lesson_candidate | logs/dashboard_8501.log | f79120584bb36a71... | Execution Knowledge | 67 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-B2D197EF2B2A | lesson_candidate | Planning/ALKASIK Agent Learning & Evolution Master Plan.docx | 5b1d0c09ef5e759f... | Agent Knowledge | 66 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-A76B96672749 | lesson_candidate | Planning/Alkasik Learning.md | a6daca040a75eac5... | Agent Knowledge | 72 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-FCE4EC7FAFAB | lesson_candidate | Planning/Alkasik MARKET LEARNING SYSTEM.md | a384fdc8afeacc6a... | Agent Knowledge | 72 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-C6BD995EB9D0 | lesson_candidate | Planning/ALKASIK_Kingdom_v4.docx | 893f5ceddb78647a... | Trading Knowledge | 66 | Iris | Sage | AK-CODEX v1.0 |
| LKI-02572FB85B65 | lesson_candidate | Planning/alkasik_master_training_architecture_plan_v_1.md | db0227a3af321c93... | Agent Knowledge | 72 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-A309B4360D67 | lesson_candidate | Planning/ALKASIK_ProjectLIGHTGATE_v1.docx | c9c74217eb031fc7... | Trading Knowledge | 66 | Iris | Sage | AK-CODEX v1.0 |
| LKI-2A8442303DEE | lesson_candidate | Planning/ALKASIK_ProjectNEURON_v1.docx | 3978e28ceff20596... | Trading Knowledge | 66 | Iris | Sage | AK-CODEX v1.0 |
| LKI-6059386EEF84 | lesson_candidate | Planning/ALKASIK_Report_V3_Unified.docx | 083104ed70e8b789... | Trading Knowledge | 63 | Iris | Sage | AK-CODEX v1.0 |
| LKI-F0DE79CFCBD7 | lesson_candidate | Planning/ALKASIK_Report_V4_Dashboard.docx | 0fbdbec9419b9846... | Trading Knowledge | 66 | Iris | Sage | AK-CODEX v1.0 |
| LKI-C0BD0F32EF8D | lesson_candidate | portfolio_governor/portfolio_governor.py | 1d082656ce2e02d7... | Risk Knowledge | 69 | Sage | Sage | ALKASIK RISK LAW v1.0 |
| LKI-3856BEC64011 | lesson_candidate | reporting/dashboard_snapshot.py | 5aced89399e50c0e... | Agent Knowledge | 72 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-7069EFBC6B03 | lesson_candidate | reporting/metrics.py | 104d88afb4b6f57d... | Agent Knowledge | 66 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-E2A2F214A92B | lesson_candidate | reporting/report_writer.py | 7b435ec911541d01... | Agent Knowledge | 69 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-8014C29055FE | lesson_candidate | Reports/aionui_dashboard_snapshot.html | dc2dc15fe2619df3... | Trading Knowledge | 68 | Iris | Sage | AK-CODEX v1.0 |
| LKI-FCAE8051C1B2 | lesson_candidate | Reports/dashboard_snapshot.html | 70eece077d1a94f0... | Trading Knowledge | 72 | Iris | Sage | AK-CODEX v1.0 |
| LKI-56E881D5DC67 | lesson_candidate | Reports/skills/agent_skill_matrix_2026-06-02_220436.md | ba18e8b8b3d6cea7... | Market Knowledge | 61 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-B86AF965618F | lesson_candidate | Reports/skills/agent_skill_matrix_2026-06-03_230127.md | 2a668061884d2ca8... | Market Knowledge | 61 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-4E1F93902867 | lesson_candidate | risk_kernel/gate0_formal_run.py | e12d379b7e2509da... | Agent Knowledge | 67 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-DBF2AB776F51 | lesson_candidate | scripts/migrate_sqlite_to_lancedb.py | f9bb1d4737bbce9c... | Market Knowledge | 67 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-321C19C25F9C | lesson_candidate | strategy_genome/components.py | 8fe15dac570ed372... | Trading Knowledge | 72 | Iris | Sage | AK-CODEX v1.0 |
| LKI-EC6A7A92E85E | lesson_candidate | tests/test_capability_router.py | 79aea1cb7d76f064... | Agent Knowledge | 60 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-773628970022 | lesson_candidate | tests/test_codex_agent_collaboration.py | 3fedceac20ca9e29... | Agent Knowledge | 60 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-A6329863DE40 | lesson_candidate | tests/test_inventory_bot.py | 4732ff82c8f2d4af... | Market Knowledge | 72 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-88DED5A9CC2C | lesson_candidate | tests/test_lightgate.py | 3d763e4c9b70886f... | Execution Knowledge | 66 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-8E154C1EA445 | skill_candidate | tests/test_national_registry_population.py | cf77cf772fe962f9... | Memory Knowledge | 66 | Hermes | Sage | ALKASIK_MEMORY_LAW_v1.0 |
| LKI-7269762752AD | lesson_candidate | tools/agent_skill_registry.py | 945b657a17be01fd... | Trading Knowledge | 72 | Iris | Sage | AK-CODEX v1.0 |
| LKI-7CC811424C54 | lesson_candidate | tools/capability_router.py | 12435c023fe70390... | Execution Knowledge | 72 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-0554162910B8 | lesson_candidate | tools/ci_tools.py | f032a52da19c6406... | Execution Knowledge | 67 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-3E0D35F1E9C1 | lesson_candidate | tools/inventory_backtest_report.py | 632e8cd6feea9e14... | Trading Knowledge | 73 | Iris | Sage | AK-CODEX v1.0 |
| LKI-63E0A7006319 | lesson_candidate | tools/inventory_data_ingestion.py | c91abdd3973985ca... | Agent Knowledge | 72 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-3B06622CC5D2 | lesson_candidate | tools/liquidity_intelligence.py | da273d0ab268374e... | Market Knowledge | 63 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-5AF5FDA3D4C3 | lesson_candidate | tools/multi_timeframe.py | cc8082b37a8b610a... | Trading Knowledge | 67 | Iris | Sage | AK-CODEX v1.0 |
| LKI-185D38C97285 | skill_candidate | tools/national_registry.py | c18000466d3e470c... | Memory Knowledge | 62 | Hermes | Sage | ALKASIK_MEMORY_LAW_v1.0 |
| LKI-77A195A750F5 | lesson_candidate | tools/source_learning.py | 635ca9f203d7a666... | Trading Knowledge | 72 | Iris | Sage | AK-CODEX v1.0 |
| LKI-8505839B4DA2 | lesson_candidate | tools/structure_brain.py | 1096ef696146776f... | Market Knowledge | 67 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-3E58649D90FC | lesson_candidate | tools/telegram_bridge.py | f284637d672a2626... | Trading Knowledge | 76 | Iris | Sage | AK-CODEX v1.0 |
| LKI-9941A21ADAF7 | lesson_candidate | tools/vps_data_ingestion.py | b18271650ffe3120... | Agent Knowledge | 72 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-3419389FC3C7 | lesson_candidate | tools/yet_kieu_scout.py | ff359abfeca0a466... | Trading Knowledge | 66 | Iris | Sage | AK-CODEX v1.0 |
| LKI-5E002B299EF9 | lesson_candidate | Trading data/alkasik_bot_events.csv | 1b37522c6b27d71c... | Trading Knowledge | 72 | Iris | Sage | AK-CODEX v1.0 |
| LKI-6FB9975091B5 | lesson_candidate | Trading data/alkasik_bot_eventss.csv | fae67c1795be0d3c... | Trading Knowledge | 72 | Iris | Sage | AK-CODEX v1.0 |
| LKI-8D3515591499 | lesson_candidate | Trading data/bot_20260519.log | cc2e41eca85485d1... | Trading Knowledge | 66 | Iris | Sage | AK-CODEX v1.0 |
| LKI-D0379C7F3BB3 | lesson_candidate | Trading data/bot_20260524.log | 67dbd2c9cdd40238... | Trading Knowledge | 62 | Iris | Sage | AK-CODEX v1.0 |
| LKI-4733D5EC8408 | lesson_candidate | Trading data/bot_20260525.log | 2c76cd69060db20a... | Trading Knowledge | 62 | Iris | Sage | AK-CODEX v1.0 |
| LKI-69100E4DFDA7 | lesson_candidate | Trading data/bot_20260528.log | caf857b2272de88e... | Trading Knowledge | 62 | Iris | Sage | AK-CODEX v1.0 |
| LKI-23E2B37162EF | lesson_candidate | Trading data/bot_20260529.log | 4ab8302f3d210e44... | Trading Knowledge | 62 | Iris | Sage | AK-CODEX v1.0 |
| LKI-8CB2499BD9F5 | lesson_candidate | Trading data/bot_20260530.log | 5cb9c4c0a3a9f5d7... | Trading Knowledge | 62 | Iris | Sage | AK-CODEX v1.0 |
| LKI-A35196DE8E31 | lesson_candidate | Trading data/bot_20260531.log | 1e4bb98b30de5632... | Trading Knowledge | 62 | Iris | Sage | AK-CODEX v1.0 |
| LKI-13CCA29C1CF4 | lesson_candidate | Trading data/bot_20260601.log | a409cf238493f024... | Trading Knowledge | 62 | Iris | Sage | AK-CODEX v1.0 |
| LKI-E2399030E43F | lesson_candidate | Trading data/bot_20260602.log | 4351a34ad9b04f23... | Trading Knowledge | 62 | Iris | Sage | AK-CODEX v1.0 |
| LKI-20ED6758F935 | lesson_candidate | Trading data/pending_orders_20260527.csv | 04dfe84d3adde475... | Trading Knowledge | 63 | Iris | Sage | AK-CODEX v1.0 |
| LKI-E0F2A4939F59 | lesson_candidate | Trading data/alkasik_logs/market_state.csv | 6e83ab3c0c54a25d... | Trading Knowledge | 63 | Iris | Sage | AK-CODEX v1.0 |
| LKI-8254D6101E07 | lesson_candidate | Trading data/alkasik_logs/portfolio_state.csv | ae8498360d91fdf6... | Trading Knowledge | 62 | Iris | Sage | AK-CODEX v1.0 |
| LKI-2CE5B911DC36 | lesson_candidate | Trading data/alkasik_logs/symbol_health.csv | 545e77fe88163fd7... | Trading Knowledge | 66 | Iris | Sage | AK-CODEX v1.0 |
| LKI-8F5A9340F173 | lesson_candidate | workflows/agent_status.py | 6c3ba1a63a951fea... | Agent Knowledge | 76 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-4F8336102E62 | lesson_candidate | workflows/codex_agent_collaboration.py | b81dbb37072e24c9... | Agent Knowledge | 72 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-70E4DA32E38D | lesson_candidate | workflows/dashboard.py | 3445ad78e9f5d7b2... | Trading Knowledge | 70 | Iris | Sage | AK-CODEX v1.0 |
| LKI-8CBCB2A1837D | lesson_candidate | workflows/janus_core.py | 9987613a557b3c1c... | Agent Knowledge | 63 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-8D21C3921F0C | lesson_candidate | workflows/kingdom_workflows.py | cf74cfe083371cba... | Execution Knowledge | 72 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-C4FA03DCD667 | lesson_candidate | workflows/market_intelligence_workflow.py | 938354760f68b8df... | Market Knowledge | 63 | Iris | Hermes | AK-CODEX v1.0 |
| LKI-1FDA6BBE9DEE | lesson_candidate | workflows/offline_code_optimization.py | 7002b4f3bf4b4054... | Execution Knowledge | 64 | Yet Kieu | Sage | ALKASIK EXECUTION LAW v1.0 |
| LKI-C62F058AE4BD | lesson_candidate | workflows/offline_learning_cycle.py | 7eee54f42dc0b731... | Agent Knowledge | 63 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |
| LKI-FBE9403876A6 | lesson_candidate | workflows/realtime_agent_learning.py | 9791a6dee88d9024... | Agent Knowledge | 66 | Janus | Sage | ALKASIK_AGENT_LAW_v1.0 |

## Completeness

| Requirement | Status |
|-------------|--------|
| Source path present | 240/240 |
| Source hash present | 240/240 |
| Domain present | 240/240 |
| Owner agent present | 240/240 |
| Reviewer agent present | 240/240 |
| Traceability % | 100% |
