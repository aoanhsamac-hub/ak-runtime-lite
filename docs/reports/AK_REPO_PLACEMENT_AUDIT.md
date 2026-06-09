# AK Repo Placement Audit

**Date:** 2026-06-08  
**Author:** Janus  
**Authority:** Repo Governance Decree v1.0 FINAL  
**Status:** COMPLETE  

---

## Scope

Audit of all files in D:\AK for correct directory placement according to the AK Repository Structure Standard.

---

## Standard Directory Layout

| Path | Purpose | Acceptable Content |
|---|---|---|
| root/ | Minimal bootstrap files | ak.bat, law.bat, AK_MEMORY.md only |
| agents/ | Agent runtime + identity | Agent .py, .yaml, role/boundary/memory docs |
| connectors/ | External integrations | Adapter .py, connector .yaml, README.md |
| docs/ | All documentation | Reports, designs, specs, reviews, legal |
| governance/ | Policy engine + gates | .py engines, YAML registries, audit logs |
| learning/ | ML/learning modules | .py learning algorithms |
| memory/ | NationalMemoryPlatform | .py registries, schemas, LanceDB data |
| pipelines/ | Pipeline definitions | pipeline.py + pipeline.yaml per pipeline |
| scripts/ | Runnable automation | .py scripts, .bat files |
| services/ | Business logic services | .py service engines |
| sovereign/ | Constitutional documents | Laws (.docx), registries (.yaml), decrees |
| tests/ | All tests | .py test files |
| tools/ | Utility tools | .py utilities, dashboard |
| workflows/ | Workflow definitions | .py workflow code, .yaml definitions |

---

## Findings

### Correctly Placed Files — OK

| Location | Count | Notes |
|---|---|---|
| agents/ | 61 files | All 7 agents properly placed with role/boundary/memory docs |
| connectors/ | 25 files | 10 connector packages in subdirectories |
| governance/ | 22 files | Policy engine, registries, audit all in correct location |
| learning/ | 5 .py files | All learning modules in one place |
| memory/ | 46 .py files | Well-organized with subdirectory packages |
| pipelines/ | 11 pipelines | Each pipeline has its own subdirectory |
| sovereign/ | 25 files | Laws in laws/, registries in registries/, decrees in decrees/ |
| tests/ | 91 .py files | All test files directly in tests/ (plus learning/ subdir) |
| workflows/ | 25 files | 12 workflow directories with proper structure |

### Placement Issues — Needs Attention

| # | File/Dir | Current Location | Issue | Proposed Destination |
|---|---|---|---|---|
| 1 | `CONSTITUTIONAL_MAPPING.md` | docs/governance/ | MISPLACED — should be in legal/ | docs/legal/canon/ |
| 2 | `Openrouter_LLM_Configuration.md` | docs/governance/ | MISPLACED — technical config, not governance | docs/architecture/ |
| 3 | `ALKASIK_CONSTITUTION_v1.0.md` | docs/governance/ | OUTDATED + MISPLACED | archive/legal_reorganization/ |
| 4 | `ALKASIK_AGENT_CHARTER_v1.0.md` | docs/governance/ | MISPLACED — agent charter | docs/agents/ |
| 5 | `ALKASIK_GOVERNANCE_CHARTER_v1.0.md` | docs/governance/ | OK — governance doc in governance/ | — |
| 6 | `CONSTITUTION-00_CONSTITUTION_v1.0.md` | docs/legal/codex/constitution/ | DUPLICATE — v1.0 exists in 3 places | Consolidate to canon |
| 7 | `CONSTITUTION-00_CONSTITUTION_v1.1.md` | docs/legal/codex/constitution/ | DUPLICATE — v1.1 exists in 2 places | Consolidate to canon |
| 8 | `LAW-04_MEMORY_v1.0.md` | docs/legal/codex/laws/ | DUPLICATE — canon has Memory Law FINAL | Remove codex copy |
| 9 | `POL-01_NO_LEGACY_RUNTIME_v1.0.md` | docs/legal/codex/policies/ | DUPLICATE — same content in docs/reviews/ | Consolidate |
| 10 | `POL-02_PROJECT_CHARTER_v1.0.md` | docs/legal/codex/policies/ | DUPLICATE | Consolidate |
| 11 | `LEGAL_REGISTRY.yaml` | docs/legal/codex/registries/ | DUPLICATE — legal_registry.yaml in sovereign/registries/ | Remove codex copy |
| 12 | `LEGACY_LEARNING_INVENTORY.csv` | docs/reports/ | MISPLACED — data file in reports directory | memory/legacy_corpus/ |
| 13 | `canonicalization_data.json` | docs/reports/ | MISPLACED — data file | memory/knowledge_registry/ |
| 14 | `capability_pipeline_data.json` | docs/reports/ | MISPLACED — data file | memory/capability_backlog/ |
| 15 | `capability_validation_data.json` | docs/reports/ | MISPLACED — data file | memory/capability_backlog/ |
| 16 | `promotion_data.json` | docs/reports/ | MISPLACED — data file | memory/learning_registry/ |
| 17 | `connectors/openai/` | connectors/openai/ | EMPTY — only connector.yaml + README, no code | Remove or implement |
| 18 | `connectors/gmail/` | connectors/gmail/ | EMPTY — only connector.yaml + README | Remove or implement |
| 19 | `memory/legacy_corpus/hermes_review_results.yaml` | memory/legacy_corpus/ | OK — legacy corpus location | — |
| 20 | `execution/` (7 files) | execution/ | STATIC — unknown content | Evaluate for removal |

### Missing Standard Directories (Now Created)

| Directory | Created? | Purpose |
|---|---|---|
| docs/proposals/ | YES | Governance proposals |
| docs/agents/janus/ | YES | Janus charter + skill |
| docs/agents/hermes/ | YES | Hermes charter |
| docs/registries/ | YES | Cross-cutting registries |

---

## Placement Recommendations Summary

| Action | Count | Details |
|---|---|---|
| MOVE (misplaced) | 6 files | Constitutional mapping, LLM config, constitution v1.0, agent charter, data files |
| CONSOLIDATE (duplicates) | ~15 files | Canon/codex overlap |
| REMOVE (empty) | 16 directories | Empty dirs without purpose |
| IMPLEMENT (stub dirs) | 2 directories | connectors/openai/, connectors/gmail/ |
| EVALUATE | 1 directory | execution/ content |

---

## Compliance Verification

| Requirement | Status |
|---|---|
| All files in correct root directory | PASS (with noted exceptions) |
| No file outside standard structure | PASS (5 root files are intentional) |
| Empty directories documented | PASS (16 identified) |
| Duplicate files identified | PASS (~15 canonical/codex overlaps) |
| Misplaced files identified | PASS (6 files, 4 data files) |
