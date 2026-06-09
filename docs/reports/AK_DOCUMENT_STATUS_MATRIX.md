# AK Document Status Matrix

**Date:** 2026-06-08  
**Author:** Janus  
**Status:** COMPLETE  

---

## Legend

| Status | Meaning |
|---|---|
| FINAL | Approved, no further changes expected |
| DRAFT | Working document, not yet approved |
| REVIEW | Under review, awaiting signature |
| PENDING | Identified as needed, not yet created |
| DUPLICATE | Content mirrored in another location |
| OUTDATED | Superseded by newer version |
| MISPLACED | Located in wrong directory |
| CHARTER | Informational charter, not executable code |

---

## Legal Documents

### Constitution & State Corpus

| Document | Path | Status | Notes |
|---|---|---|---|
| ALKASIK_CONSTITUTION_v1.1_FINAL.md | docs/legal/canon/ | FINAL | Current constitution |
| ALKASIK_CONSTITUTION_v1.0.md | docs/governance/ | OUTDATED | v1.0 superseded by v1.1 |
| CONSTITUTION-00_CONSTITUTION_v1.0.md | docs/legal/codex/constitution/ | DUPLICATE | Mirror of v1.0 |
| CONSTITUTION-00_CONSTITUTION_v1.1.md | docs/legal/codex/constitution/ | DUPLICATE | Mirror of v1.1 |
| ALKASIK_CONSTITUTION_v1.1_FINAL.docx | sovereign/constitution/ | FINAL | Original signed version |
| ALKASIK_STATE_CORPUS_v1.0_FINAL.md | docs/legal/canon/ | FINAL | Current state corpus |
| ALKASIK_STATE_CORPUS_v1.0 FINAL.docx | sovereign/state_corpus/ | FINAL | Original signed version |

### Laws

| Document | Path | Status | Notes |
|---|---|---|---|
| ALKASIK_AGENT_LAW_v1.0_FINAL.md | docs/legal/canon/ | FINAL | |
| ALKASIK_AGENT_LAW_v1.0 FINAL.docx | sovereign/laws/agent/ | FINAL | Original signed |
| ALKASIK_ECONOMIC_LAW_v1.0_FINAL.md | docs/legal/canon/ | FINAL | |
| ALKASIK Economic Law v1.0 FINAL.docx | sovereign/laws/Economic/ | FINAL | Original signed |
| ALKASIK_EXECUTION_LAW_v1.0_FINAL.md | docs/legal/canon/ | FINAL | |
| ALKASIK EXECUTION LAW v1.0 FINAL.docx | sovereign/laws/execution/ | FINAL | Original signed |
| ALKASIK_INFORMATION_LAW_v1.0_FINAL.md | docs/legal/canon/ | FINAL | |
| ALKASIK_INFORMATION_LAW_v1.0 FINAL.docx | sovereign/laws/intelligence/ | FINAL | Original signed |
| ALKASIK_MEMORY_LAW_v1.0_FINAL.md | docs/legal/canon/ | FINAL | |
| ALKASIK_MEMORY_LAW_v1.0 FINAL.docx | sovereign/laws/memory/ | FINAL | Original signed |
| ALKASIK_MEMORY_LAW_v1.0.md | docs/legal/codex/laws/ | DUPLICATE | Codex copy |
| ALKASIK_RISK_LAW_v1.0_FINAL.md | docs/legal/canon/ | FINAL | |
| ALKASIK RISK LAW v1.0 FINAL.docx | sovereign/laws/risk/ | FINAL | Original signed |
| ALKASIK_SECURITY_LAW_v1.0_FINAL.md | docs/legal/canon/ | FINAL | |
| ALKASIK_SECURITY_LAW_v1.0 FINAL.docx | sovereign/laws/security/ | FINAL | Original signed |

### Decrees

| Document | Path | Status | Notes |
|---|---|---|---|
| ALKASIK_KNOWLEDGE_GOVERNANCE_DECREE_v1.0_FINAL.md | docs/legal/canon/ | FINAL | |
| ALKASIK_KNOWLEDGE_GOVERNANCE_DECREE_v1.0_FINAL.docx | sovereign/decrees/knowledge/ | FINAL | Original signed |
| ALKASIK_REPO_GOVERNANCE_DECREE_v1.0_FINAL.md | docs/legal/canon/ | FINAL | |
| ALKASIK_REPO_GOVERNANCE_DECREE_v1.0_FINAL.docx | sovereign/decrees/infrastructure/ | FINAL | Original signed |
| ALKASIK_RETENTION_ARCHIVE_GOVERNANCE_DECREE_v1.0_FINAL.md | docs/legal/canon/ | FINAL | |
| ALKASIK_RETENTION_DECREE_v1.0_FINAL.docx | sovereign/decrees/retention/ | FINAL | Original signed |

### Budget Law

| Document | Path | Status | Notes |
|---|---|---|---|
| AK_KINGDOM_BUDGET_LAW_v1.0_REVIEW.md | sovereign/laws/budget/ | REVIEW | Awaiting Sage + Hung Vuong |
| AK_NATIONAL_BUDGET_LAW_v0.1_DRAFT.docx | sovereign/laws/budget/ | DRAFT | Working draft |

### Governance Charters

| Document | Path | Status | Notes |
|---|---|---|---|
| ALKASIK_CONSTITUTION_v1.0.md | docs/governance/ | OUTDATED | v1.0, superseded |
| ALKASIK_GOVERNANCE_CHARTER_v1.0.md | docs/governance/ | CHARTER | Governance charter |
| ALKASIK_AGENT_CHARTER_v1.0.md | docs/governance/ | CHARTER | Agent charter |
| CONSTITUTIONAL_MAPPING.md | docs/governance/ | FINAL | Constitutional mapping |
| Openrouter_LLM_Configuration.md | docs/governance/ | CHARTER | LLM configuration doc |

---

## Agent Documents

| Document | Path | Status | Notes |
|---|---|---|---|
| 7x agent.py | agents/{name}/agent.py | OPERATIONAL | Each agent has operational code |
| 7x role.md | agents/{name}/role.md | CHARTER | Role definition |
| 7x boundaries.md | agents/{name}/boundaries.md | CHARTER | Boundary definition |
| 7x memory_policy.md | agents/{name}/memory_policy.md | CHARTER | Memory policy |
| 7x tools.yaml | agents/{name}/tools.yaml | CHARTER | Tool definitions |
| 7x workflows.yaml | agents/{name}/workflows.yaml | CHARTER | Workflow definitions |
| 7x src/agent.py | agents/{name}/src/agent.py | OPERATIONAL | Agent source implementation |
| JANUS_CHARTER_DRAFT_v1.0.md | docs/agents/janus/ | DRAFT | Created in this directive |
| HERMES_MEMORY_DATASET_CHARTER_DRAFT_v1.0.md | docs/agents/hermes/ | DRAFT | Created in this directive |

---

## Reports (~202 files in docs/reports/)

| Report Category | Count | Status Notes |
|---|---|---|
| WP35.4A reports | 9 | COMPLETE |
| WP35 Phase 1C-05 reports | 15 | COMPLETE |
| Capability pipeline reports (WP35-1C-04) | 13 | COMPLETE |
| NAOP Patch reports | 6 | COMPLETE |
| AK-CODEX reports | 27+ | COMPLETE (codex closed) |
| Market sandbox reports | 5 | COMPLETE |
| Legacy migration reports | 5 | COMPLETE |
| Skill pipeline reports (WP35-1C-02) | 9 | COMPLETE |
| WP36 report | 1 | COMPLETE |
| Various audit/review reports | ~112 | COMPLETE |
| **TOTAL** | **~202** | |

---

## Design Documents (26 files in docs/design/)

| Document | Status | Notes |
|---|---|---|
| AK knowledge lifecycle model | FINAL | Pipeline design |
| AK capability lifecycle model | FINAL | Pipeline design |
| AK skill lifecycle/registry/taxonomy models | FINAL | 4 skill design docs |
| AK lesson quality/deduplication models | FINAL | Lesson design |
| AK cross-agent learning/sharing models | FINAL | Agent design |
| AK promotion governance model | FINAL | Governance design |
| AK learning metrics model | FINAL | Metrics design |
| WP35 Phase 1A/1C/1E design notes | FINAL | Phase designs |
| AK pipeline designs (5) | FINAL | Pipeline docs |

---

## Summary Statistics

| Status | Count (estimate) |
|---|---|
| FINAL | ~200+ |
| DRAFT | 6 |
| REVIEW | 1 |
| CHARTER | ~30+ |
| DUPLICATE | ~15 |
| OUTDATED | 2 |
| OPERATIONAL | ~100+ (.py files) |
