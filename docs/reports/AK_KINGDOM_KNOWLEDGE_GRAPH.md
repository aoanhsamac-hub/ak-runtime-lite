# AK_NATIONAL_KNOWLEDGE_GRAPH.md

**Generated:** 2026-06-07T09:11:51Z
**Directive:** WP-KM-03 Phase 4 — National Knowledge Graph

## Graph Structure

```
Decision Trace ──> Lesson ──> Skill Recommendation ──> Capability Recommendation
     Dataset    ──> Lesson ──> Skill Recommendation ──> Capability Recommendation
          Skill ──> Capability Recommendation
```

## 1. Decision Trace -> Lesson Mapping

| Decision Trace | Linked Lessons (by domain) | Domain |
|---------------|---------------------------|--------|
| Alkasik Constitution V1.1 Final | 0 lessons in Governance | Governance |
| Alkasik Knowledge Governance Decree V1.0 Final | 0 lessons in Governance | Governance |
| Alkasik Repo Governance Decree V1.0 Final | 0 lessons in Governance | Governance |
| Alkasik Retention Decree V1.0 Final | 0 lessons in Governance | Governance |
| Alkasik Constitution V1.1 Draft | 0 lessons in Governance | Governance |
| ALKASIK vNext Phase A+B Report | 0 lessons in Governance | Governance |

## 2. Dataset -> Lesson Mapping

| Dataset | Linked Lessons (by domain) | Domain |
|---------|---------------------------|--------|
| Llm Router Gateway | 0 lessons in Engineering | Engineering |
| Dataset Pipeline | 0 lessons in Engineering | Engineering |
| Observability | 0 lessons in Engineering | Engineering |
| CrewAI + Ollama on RunPod: Serverless AI Agents | 0 lessons in Engineering | Engineering |
| AionUi - Project Guide | 0 lessons in Engineering | Engineering |
| Package | 0 lessons in Engineering | Engineering |
| Renderer Layer (`packages/desktop/src/renderer/`) | 0 lessons in Engineering | Engineering |
| Hub Backend 测试指南 | 0 lessons in Engineering | Engineering |
| Settings | 0 lessons in Engineering | Engineering |
| Settings | 0 lessons in Engineering | Engineering |
| Settings | 0 lessons in Engineering | Engineering |
| Settings | 0 lessons in Engineering | Engineering |
| Codex | 0 lessons in Engineering | Engineering |

## 3. Lesson -> Skill Recommendation Edges

| Lesson (cluster) | Proposed Skill | Confidence |
|-----------------|---------------|------------|
| development.md (+1 more) | Contributing | 83 |
| README.cn.md (+1 more) | Workspace | 81 |
| build-and-release.yml (+5 more) | Workflows | 79 |
| DATA_GOVERNANCE_MIGRATION_PLAN.md (+2 more) | 20260606 210352 | 79 |
| deploy-server.md (+1 more) | Guides | 79 |
| memory_archive_2026-05-26_pre_compact.md (+1 more) | Archive | 79 |
| codex.json (+4 more) | En Us | 78 |
| codex.json (+4 more) | Uk Ua | 78 |
| FEATURE_CHANNELS.md (+1 more) | .Aionui | 78 |
| codex.json (+3 more) | Ko Kr | 77 |
| codex.json (+3 more) | Ru Ru | 77 |
| codex.json (+3 more) | Tr Tr | 77 |
| aionui_dashboard_snapshot.html (+1 more) | Reports | 77 |
| agent_skill_registry.py (+11 more) | Tools | 76 |
| readme_ch.md (+8 more) | Readme | 75 |
| conversation.json (+3 more) | Zh Tw | 75 |
| dashboard_snapshot.py (+2 more) | Reporting | 75 |
| CONTRIBUTING.md (+1 more) | Aionui 2.1.0 | 75 |
| ALKASIK Agent Learning & Evolution Master Plan.doc (+8 more) | Planning | 74 |
| agent_status.py (+8 more) | Workflows | 74 |
| codex.json (+4 more) | Ja Jp | 74 |
| backtest.py (+2 more) | Inventory Bot | 73 |
| ru-RU.json (+1 more) | Locales | 73 |
| helen_controller.py (+3 more) | Agents | 72 |
| codex.json (+3 more) | Zh Cn | 72 |
| 9router.out.log (+2 more) | Logs | 72 |
| CONTRIBUTING.md (+1 more) | Agents Towards Production | 72 |
| README.cn.md (+1 more) | Preview | 72 |
| model_testing_tools.py (+1 more) | Agent Security Apex | 71 |
| alkasik_bot_events.csv (+11 more) | Trading Data | 70 |

## 4. Skill -> Capability Edges

| (skills pending) | Trading Operations |
| (skills pending) | Market Intelligence |
| (skills pending) | Risk Management |
| (skills pending) | Memory Management |
| (skills pending) | Governance Review |
| (skills pending) | Agent Coordination |
| (skills pending) | Engineering Pipeline |
| (skills pending) | Knowledge Systems |

## 5. Full Knowledge Graph (Text Representation)

```
ROOT: National Knowledge Corpus (240 candidates)
  +-- TRADING DOMAIN
  |   +-- LESSON CLUSTER (12 lessons) --> Skill: Tools (conf 76)
  |   +-- LESSON CLUSTER (12 lessons) --> Skill: Trading Data (conf 70)
  |   +-- LESSON CLUSTER (9 lessons) --> Skill: Planning (conf 74)
  |   +-- LESSON CLUSTER (9 lessons) --> Skill: Workflows (conf 74)
  |   +-- LESSON CLUSTER (6 lessons) --> Skill: Docs (conf 69)
  |   +-- LESSON CLUSTER (6 lessons) --> Skill: Workflows (conf 79)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Agents (conf 72)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Tr Tr (conf 77)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Zh Cn (conf 72)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Zh Tw (conf 75)
  |   +-- LESSON CLUSTER (3 lessons) --> Skill: 20260606 210352 (conf 79)
  |   +-- LESSON CLUSTER (3 lessons) --> Skill: Inventory Bot (conf 73)
  |   +-- LESSON CLUSTER (3 lessons) --> Skill: Logs (conf 72)
  |   +-- LESSON CLUSTER (3 lessons) --> Skill: Alkasik Logs (conf 70)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Raw Indicators (conf 70)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Agent Security Apex (conf 71)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Aionui 2.1.0 (conf 75)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: .Aionui (conf 78)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Locales (conf 73)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Workspace (conf 81)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Reports (conf 77)
  +-- MARKET DOMAIN
  |   +-- LESSON CLUSTER (12 lessons) --> Skill: Tools (conf 76)
  |   +-- LESSON CLUSTER (9 lessons) --> Skill: Readme (conf 75)
  |   +-- LESSON CLUSTER (9 lessons) --> Skill: Workflows (conf 74)
  |   +-- LESSON CLUSTER (6 lessons) --> Skill: Docs (conf 69)
  |   +-- LESSON CLUSTER (6 lessons) --> Skill: Workflows (conf 79)
  |   +-- LESSON CLUSTER (5 lessons) --> Skill: En Us (conf 78)
  |   +-- LESSON CLUSTER (5 lessons) --> Skill: Ja Jp (conf 74)
  |   +-- LESSON CLUSTER (5 lessons) --> Skill: Uk Ua (conf 78)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Agents (conf 72)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Ko Kr (conf 77)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Ru Ru (conf 77)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Tr Tr (conf 77)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Zh Cn (conf 72)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Zh Tw (conf 75)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Tests (conf 70)
  |   +-- LESSON CLUSTER (3 lessons) --> Skill: Inventory Bot (conf 73)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Agents Towards Production (conf 72)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Aionui 2.1.0 (conf 75)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Guides (conf 79)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Preview (conf 72)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Workspace (conf 81)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Skills (conf 67)
  +-- EXECUTION DOMAIN
  |   +-- LESSON CLUSTER (12 lessons) --> Skill: Tools (conf 76)
  |   +-- LESSON CLUSTER (9 lessons) --> Skill: Workflows (conf 74)
  |   +-- LESSON CLUSTER (6 lessons) --> Skill: Workflows (conf 79)
  |   +-- LESSON CLUSTER (5 lessons) --> Skill: En Us (conf 78)
  |   +-- LESSON CLUSTER (5 lessons) --> Skill: Ja Jp (conf 74)
  |   +-- LESSON CLUSTER (5 lessons) --> Skill: Uk Ua (conf 78)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Agents (conf 72)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Ko Kr (conf 77)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Ru Ru (conf 77)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Tr Tr (conf 77)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Zh Cn (conf 72)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Zh Tw (conf 75)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Reports (conf 70)
  |   +-- LESSON CLUSTER (4 lessons) --> Skill: Tests (conf 70)
  |   +-- LESSON CLUSTER (3 lessons) --> Skill: 20260606 210352 (conf 79)
  |   +-- LESSON CLUSTER (3 lessons) --> Skill: Logs (conf 72)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Learning (conf 70)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Agents Towards Production (conf 72)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Contributing (conf 83)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Guides (conf 79)
  |   +-- LESSON CLUSTER (2 lessons) --> Skill: Archive (conf 79)
  +-- OTHER DOMAINS
      +-- LESSON CLUSTER (9 lessons) --> Skill: Planning (conf 74)
      +-- LESSON CLUSTER (9 lessons) --> Skill: Workflows (conf 74)
      +-- LESSON CLUSTER (5 lessons) --> Skill: En Us (conf 78)
      +-- LESSON CLUSTER (4 lessons) --> Skill: Agents (conf 72)
      +-- LESSON CLUSTER (4 lessons) --> Skill: Reports (conf 70)
      +-- LESSON CLUSTER (4 lessons) --> Skill: Tests (conf 70)
      +-- LESSON CLUSTER (3 lessons) --> Skill: Reporting (conf 75)
      +-- LESSON CLUSTER (2 lessons) --> Skill: Agent Security Apex (conf 71)
      +-- LESSON CLUSTER (2 lessons) --> Skill: System Maps (conf 68)
      +-- LESSON CLUSTER (2 lessons) --> Skill: Archive (conf 79)
```

- 8 existing skill candidates
- 38 recommended skills from lesson clusters
- 8 proposed capability clusters
