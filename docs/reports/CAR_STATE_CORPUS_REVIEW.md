# CAR: State Corpus Review

**Date:** 2026-06-08
**Phase:** B
**Status:** GAPS_FOUND

---

## 1. Documents Reviewed

| # | Document | Path | Status |
|---|----------|------|--------|
| 1 | ALKASIK_CONSTITUTION_v1.0.md | `docs/governance/` | READ |
| 2 | ALKASIK_STATE_CORPUS_v1.0_FINAL.md | `docs/legal/canon/` *(not at `docs/governance/`)* | READ (truncated — 23 lines, docx source not extractable) |
| 3 | JANUS_CHARTER_v1.0_FINAL.md | `docs/charters/` | READ |
| 4 | HERMES_CHARTER_v1.0_FINAL.md | `docs/charters/` | READ |
| 5 | ALKASIK_AGENT_CHARTER_v1.0.md | `docs/governance/` | READ |
| 6 | ALKASIK_GOVERNANCE_CHARTER_v1.0.md | `docs/governance/` | READ |
| 7 | AK_TREASURY_CHARTER_v1.0_FINAL.md | `docs/charters/` | READ |
| 8 | AK_ROYAL_TREASURY_CHARTER_v1.0_FINAL.md | `docs/charters/` | READ |
| 9 | JANUS_CHARTER_DRAFT_v1.0.md | `docs/agents/janus/` | READ |
| 10 | HERMES_MEMORY_DATASET_CHARTER_DRAFT_v1.0.md | `docs/agents/hermes/` | READ |
| 11 | JANUS_SKILL_PRESIDENTIAL_ORCHESTRATION_DRAFT_v1.0.md | `docs/agents/janus/` | READ |
| 12 | AK_AGENT_ACTIVATION_MATRIX_DRAFT.md | `docs/registries/` | READ |
| 13 | MISSING_ARTIFACTS_REGISTER.md | `docs/registries/` | READ |
| 14 | Agent stub files (agent.py, agent.yaml, role.md, boundaries.md, tools.yaml, workflows.yaml) | `agents/{janus,sage,hermes,iris,helen,lang_lieu,yet_kieu}/` | SCANNED |

---

## 2. Corpus Structure Analysis

### Does the State Corpus properly reflect all 7 agents from Constitution v1.0?

**NO.** The State Corpus at `docs/legal/canon/ALKASIK_STATE_CORPUS_v1.0_FINAL.md` is a minimal placeholder (23 lines). It references the original `.docx` as the source (which is binary and cannot be extracted), and only contains high-level notes from WP3.5 doctrine about lesson structure and knowledge preservation. It does **not** enumerate the 7 agents, their departments, or their authorities.

### Are agent→department→authority mappings complete?

**NO.** The State Corpus does not define agent→department→authority mappings. The Constitution (v1.0, Article 4) does define roles and permissions for all 7 agents. The Agent Charter (`docs/governance/ALKASIK_AGENT_CHARTER_v1.0.md`) provides a concise matrix but lacks department/authority-level detail. Full mappings would need to be reconstructed from the Constitution + individual agent charters, but 5/7 agents lack FINAL charters.

### Does the Agent Charter (governance-level) align with the Constitution?

**YES — partially.** The Agent Charter's role/permission matrix aligns with Constitution Article 4. However, it is a high-level summary (1 table, 23 lines total) and does not include:
- Department names
- Authority levels (COORDINATE, REVIEW, EXECUTE, etc.)
- Escalation paths
- Governance gates per agent

The Governance Charter (`ALKASIK_GOVERNANCE_CHARTER_v1.0.md`) defines change levels (C0–C4) but does not explicitly map agents to these levels beyond mentioning Janus, Sage, Lang Lieu, and Hung Vuong as approvers.

---

## 3. Charter Completeness Check

| Agent | FINAL Charter Exists | Location | Notes |
|-------|---------------------|----------|-------|
| Janus | YES ✓ | `docs/charters/JANUS_CHARTER_v1.0_FINAL.md` | DRAFT also at `docs/agents/janus/` |
| Sage | **NO** ✗ | — | No FINAL or DRAFT charter found anywhere |
| Lang Lieu | **NO** ✗ | — | No FINAL or DRAFT charter found anywhere |
| Hermes | YES ✓ | `docs/charters/HERMES_CHARTER_v1.0_FINAL.md` | DRAFT also at `docs/agents/hermes/` |
| Iris | **NO** ✗ | — | No FINAL or DRAFT charter found anywhere |
| Helen | **NO** ✗ | — | No FINAL or DRAFT charter found anywhere |
| Yet Kieu | **NO** ✗ | — | No FINAL or DRAFT charter found anywhere |

**Supplementary Charters (treasury domain):**

| Charter | Exists | Path |
|---------|--------|------|
| Kingdom Treasury Charter | YES ✓ | `docs/charters/AK_TREASURY_CHARTER_v1.0_FINAL.md` |
| Royal Treasury Charter | YES ✓ | `docs/charters/AK_ROYAL_TREASURY_CHARTER_v1.0_FINAL.md` |

**Missing FINAL charters: 5 of 7 agents (Sage, Lang Lieu, Iris, Helen, Yet Kieu).**

---

## 4. Job Mapping Check

### Agent Implementation Status

| Agent | Agent Code Exists | Skill Files | Skill Directory (`D:\AK\skills\`) |
|-------|------------------|-------------|-----------------------------------|
| Janus | `agents/janus/` | 1 DRAFT skill (`docs/agents/janus/JANUS_SKILL_PRESIDENTIAL_ORCHESTRATION_DRAFT_v1.0.md`) | DOES NOT EXIST |
| Sage | `agents/sage/` | None | DOES NOT EXIST |
| Lang Lieu | `agents/lang_lieu/` | None (but has `dev_orchestrator.py`) | DOES NOT EXIST |
| Hermes | `agents/hermes/` | None | DOES NOT EXIST |
| Iris | `agents/iris/` | None | DOES NOT EXIST |
| Helen | `agents/helen/` | None | DOES NOT EXIST |
| Yet Kieu | `agents/yet_kieu/` | None | DOES NOT EXIST |

### Service-Layer Mapping

The `services/` directory contains numerous Python implementations that map to constitutional roles:

| Service Area | Relevant Services | Maps To |
|-------------|------------------|---------|
| Treasury | `treasury_*.py` (audit, reporting, allocation, revenue, health, impact, evidence) | Iris |
| Knowledge | `knowledge_health_monitor.py`, `knowledge_roi_engine.py` | Hermes |
| Skill | `skill_*.py` (lifecycle, promotion, validation, maturity, discovery, graph, family, dedup) | Hermes |
| Capability | `capability_*.py` (usage, value, roi, adoption, maturity, readiness, evolution, evidence) | Hermes |
| Security | `security_status_monitor.py` | Yet Kieu |
| Trading | `trading_health_monitor.py`, `signal_*.py`, `zone_*.py`, `forecast_*.py` | Iris |
| Governance | `governance_health_monitor.py`, `independent_review_gate.py` | Sage |
| Kingdom | `kingdom_*.py` (status, health, scheduler, program, planning, goal, performance) | Janus |
| Agent | `agent_status_monitor.py` | Janus |
| Audit | `audit_evidence_compiler.py` | Sage |
| Learning | `learning_*.py` (signal, audit, governance) | Hermes |

**Assessment:** While agent Python stubs exist under `agents/{name}/` and service-layer code covers most constitutional domains, there are **no formal skill files** for any agent except Janus (1 DRAFT). The `D:\AK\skills\` directory **does not exist**. The Activation Matrix (DRAFT) enumerates skill counts per agent (Janus: 3, Sage: 2, Hermes: 3, Iris: 2, Helen: 2, Lang Lieu: 3, Yet Kieu: 2) but these skills have not been materialized as files.

---

## 5. Gaps Identified

| # | Gap | Severity | Details |
|---|-----|----------|---------|
| G1 | State Corpus missing from expected path | HIGH | File at `docs/legal/canon/` instead of `docs/governance/`. Original `.docx` at `sovereign/state_corpus/` is binary and unextractable. |
| G2 | State Corpus content is incomplete | HIGH | Only 23 lines; does not define agent→department→authority mappings, does not enumerate agents, does not serve as a functional corpus. |
| G3 | Missing FINAL charters for 5/7 agents | HIGH | Sage, Lang Lieu, Iris, Helen, Yet Kieu have no FINAL charters in `docs/charters/`. Only Janus and Hermes have FINAL charters. |
| G4 | Missing DRAFT charters for 5/7 agents | MEDIUM | Sage, Lang Lieu, Iris, Helen, Yet Kieu have no DRAFT charters either (not even in `docs/agents/`). |
| G5 | No `D:\AK\skills\` directory | HIGH | The skills directory specified in the task does not exist. No shared skill repository. |
| G6 | Skill files missing for 6/7 agents | HIGH | Only Janus has 1 DRAFT skill file. Sage, Lang Lieu, Hermes, Iris, Helen, Yet Kieu have zero skill files. |
| G7 | Activation Matrix is DRAFT | MEDIUM | `docs/registries/AK_AGENT_ACTIVATION_MATRIX_DRAFT.md` is still in DRAFT status, pending Hung Vuong approval. |
| G8 | Agent Charter is too sparse | LOW | At 23 lines, the Agent Charter provides only a high-level table. Lacks department names, authority levels, escalation paths per agent. |
| G9 | State Corpus source binary-locked | MEDIUM | The authoritative source is a `.docx` file that cannot be extracted in the current environment, making the canonical `.md` a thin wrapper. |

---

## 6. Verdict

**GAPS_FOUND**

The State Corpus is structurally incomplete and misplaced. 5 of 7 constitutional agents lack FINAL charters. No skill files exist for 6 of 7 agents, and the shared `skills/` directory does not exist. While agent Python stubs and service-layer implementations exist across the codebase, the governance documentation layer has significant gaps that must be resolved before alignment can be certified.

**Status: GAPS_FOUND** — Not yet ALIGNED. Requires remediation of G1–G6 at minimum to reach CONDITIONALLY_ALIGNED.
