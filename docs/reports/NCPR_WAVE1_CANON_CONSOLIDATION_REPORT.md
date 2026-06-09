# NCP-R Wave 1 — Canon Consolidation Report

**Date:** 2026-06-08
**Authority:** Janus Directive — NCP-R
**Status:** COMPLETE
**Reviewer:** Janus

---

## Canonical Source of Truth

| Governance Domain | Source of Truth | Location |
|------------------|----------------|----------|
| Constitution | Constitution Registry | sovereign/registries/constitution_registry.yaml → sovereign/constitution/ |
| State Corpus | State Corpus Registry | sovereign/registries/state_corpus_registry.yaml → sovereign/state_corpus/ |
| Laws | Legal Registry | sovereign/registries/legal_registry.yaml → docs/legal/canon/ |
| Decrees | Legal Registry | sovereign/registries/legal_registry.yaml → docs/legal/canon/ |
| Charters | Charter Registry | MISSING — needs creation |
| Capabilities | Official Capability Registry | memory/capability_registry/official_capability_registry.py |
| Skills | Sovereign Skill Registry | sovereign/registries/skill_registry.yaml |
| Treasury | Treasury Registry | sovereign/registries/treasury_registry.yaml |
| Memory | NationalMemoryPlatform | memory/kingdom_memory_platform.py → LanceDB |
| Datasets | DatasetRegistry | memory/dataset_registry.py → LanceDB |
| Agents | AgentRegistry | agents/registry.py |
| Governance Runtime | Governance Engine | governance/*.py + governance/registries/*.yaml |

---

## Duplicate Analysis

| Domain | Duplicate Pair | Action |
|--------|---------------|--------|
| Constitution | canon (FINAL) + codex (CONSTITUTION-00_v1.0 + v1.1) | ARCHIVE codex copies |
| State Corpus | canon (FINAL) + no codex copy | No action |
| Memory Law | canon (FINAL) + codex (LAW-04_MEMORY_v1.0.md) | ARCHIVE codex copy |
| Governance Code | Governance Charter + codex (LAW-00) | ARCHIVE codex copy |
| Legal Registry | sovereign/registries/legal_registry.yaml + codex/registries/LEGAL_REGISTRY.yaml | ARCHIVE codex copy |
| Project Charter | root-level + codex/policies/POL-02 | ARCHIVE codex copy |
| Legal Index | sovereign/legal_index.yaml + codex index references | ARCHIVE codex copy |

---

## Conflict Analysis

| Domain | Conflict | Resolution |
|--------|----------|------------|
| Constitution | canon v1.1 has Article 27/36/37/38/39 only; v1.0 has full text | Canon SSOT = v1.1 FINAL; v1.0 is informative baseline |
| Budget Law | v0.1 DRAFT and v1.0 REVIEW coexist | v1.0 REVIEW supersedes v0.1 DRAFT |
| Governance Levels | Governance Charter has 5 levels (0-4); Risk Law has 5 levels (LEVEL_0 through LEVEL_4) | Consistent — no conflict |

---

## Obsolete Content

| Path | Reason | Action |
|------|--------|--------|
| docs/legal/codex/ (entire directory, 47 files) | Codex was Phase 1 of legal reorganization; canon is now the authoritative source | Recommend ARCHIVE status — move to archive/legal/codex/ |
| ALL_REPORT.7z (root) | Root-level artifact from earlier consolidation | Move to archive/ |

---

## Superseded Content

| Superseded Item | Replaced By | Date |
|----------------|-------------|------|
| ALKASIK_CONSTITUTION_v1.0.md | ALKASIK_CONSTITUTION_v1.1_FINAL.md | 2026-06-07 |
| codex standards, specs, procedures | Canon laws + governance engine | 2026-06-07 |

---

## Single Legal Authority Recommendation

**For every governance domain, there must be exactly one registry and one path.**

| Domain | Recommended SSOT Registry |
|--------|--------------------------|
| Constitution | sovereign/registries/constitution_registry.yaml |
| State Corpus | sovereign/registries/state_corpus_registry.yaml |
| Laws & Decrees | sovereign/registries/legal_registry.yaml |
| Charters | docs/registries/AK_DOCUMENT_REGISTRY_DRAFT.md (upgrade to FINAL) |
| Capabilities | memory/capability_registry/official_capability_registry.py |
| Skills | sovereign/registries/skill_registry.yaml (parent) + 5 sub-registries |
| Treasury | sovereign/registries/treasury_registry.yaml |
| Memory | NationalMemoryPlatform (ak_* tables in LanceDB) |
| Datasets | memory/dataset_registry.py (DatasetRecord → LanceDB) |
| Agents | agents/registry.py + agents/*/agent.yaml |
| Governance Runtime | governance/registries/*.yaml |

---

## Archive Recommendations

| Item | Destination |
|------|-------------|
| docs/legal/codex/ | archive/legal/codex/ |
| ALL_REPORT.7z | archive/ALL_REPORT.7z |
| archive/root_hygiene/ test outputs | Compress or clean up test artifacts |

No deletion. Archive only per Retention & Archive Governance Decree.
