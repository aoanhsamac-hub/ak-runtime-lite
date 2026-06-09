# NCP-R Wave 1 — Governance Finalization Report

**Date:** 2026-06-08
**Authority:** Janus Directive — NCP-R
**Status:** COMPLETE
**Reviewer:** Janus

---

## Classification Summary

| Decision | Count |
|----------|-------|
| APPROVE | 24 |
| REQUIRE_REVISION | 3 |
| MISSING | 5 |
| SUPERSEDED | 47 |
| ARCHIVE | 3 |
| REJECT | 0 |
| **Total** | **82** |

---

## Constitution & State Corpus

| Artifact | Decision | Authority | Legal Basis |
|----------|----------|-----------|-------------|
| Constitution v1.1 FINAL | APPROVE | Hung Vuong | Sovereignty |
| State Corpus v1.0 FINAL | APPROVE | Hung Vuong | Sovereignty |
| Constitution Registry | APPROVE | Hung Vuong | Constitution Art 1 |
| State Corpus Registry | APPROVE | Hung Vuong | State Corpus Art 1 |

---

## FINAL Laws

| Artifact | Decision | Authority | Legal Basis |
|----------|----------|-----------|-------------|
| Agent Law v1.0 | APPROVE | Hung Vuong | Constitution Art 27 |
| Economic Law v1.0 | APPROVE | Hung Vuong | Constitution |
| Execution Law v1.0 | APPROVE | Hung Vuong | Constitution Art 27 |
| Information Law v1.0 | APPROVE | Hung Vuong | Constitution Art 39 |
| Memory Law v1.0 | APPROVE | Hung Vuong | Constitution Art 36 |
| Risk Law v1.0 | APPROVE | Hung Vuong | Constitution |
| Security Law v1.0 | APPROVE | Hung Vuong | Constitution |

---

## FINAL Decrees

| Artifact | Decision | Authority | Legal Basis |
|----------|----------|-----------|-------------|
| Knowledge Governance Decree v1.0 | APPROVE | Hung Vuong | State Corpus |
| Repo Governance Decree v1.0 | APPROVE | Hung Vuong | Constitution |
| Retention & Archive Decree v1.0 | APPROVE | Hung Vuong | Memory Law |

---

## Charters

| Artifact | Decision | Authority | Legal Basis |
|----------|----------|-----------|-------------|
| Governance Charter v1.1 | APPROVE | Hung Vuong | Constitution Art 27 |
| Agent Charter v1.0 | APPROVE | Hung Vuong | Agent Law |
| Janus Charter (DRAFT) | REQUIRE_REVISION | Janus | Agent Law — needs FINAL status, activation gate |
| Hermes Charter (DRAFT) | REQUIRE_REVISION | Janus | Agent Law — needs FINAL status, lifecycle ownership |
| Treasury Charter | MISSING | Janus | Economic Law — required by Approved Economic Model |
| Risk Kernel Charter | APPROVE | Hung Vuong | Risk Law |

---

## Registries

| Artifact | Decision | Authority | Legal Basis |
|----------|----------|-----------|-------------|
| Sovereign Legal Registry | APPROVE | Hung Vuong | Repo Governance Decree |
| Sovereign Constitution Registry | APPROVE | Hung Vuong | Repo Governance Decree |
| Sovereign State Corpus Registry | APPROVE | Hung Vuong | Repo Governance Decree |
| Sovereign Treasury Registry | APPROVE | Hung Vuong | Economic Law |
| Sovereign Skill Registry | APPROVE | Hung Vuong | Knowledge Governance Decree |
| Sovereign Skill Dependency Registry | APPROVE | Hung Vuong | Knowledge Governance Decree |
| Sovereign Skill Lifecycle Registry | APPROVE | Hung Vuong | Knowledge Governance Decree |
| Sovereign Skill Owner Registry | APPROVE | Hung Vuong | Knowledge Governance Decree |
| Sovereign Skill Retirement Registry | APPROVE | Hung Vuong | Knowledge Governance Decree |
| Sovereign Skill Validation Registry | APPROVE | Hung Vuong | Knowledge Governance Decree |
| Governance Approval Matrix | APPROVE | Janus | Risk Law |
| Governance Gate Registry | APPROVE | Janus | Risk Law |
| Governance Issue Registry | APPROVE | Janus | Risk Law |
| Governance Protected Modules | APPROVE | Janus | Risk Law |
| Legal Index YAML | APPROVE | Hung Vuong | Repo Governance Decree |

---

## Codex Documents — SUPERSEDED

All 47 files in `docs/legal/codex/` are **SUPERSEDED** by canon equivalents.

| Codex File | Superseded By | Reason |
|------------|--------------|--------|
| CONSTITUTION-00_CONSTITUTION_v1.0.md | docs/legal/canon/ALKASIK_CONSTITUTION_v1.1_FINAL.md | Canon is authoritative. v1.0 superseded by v1.1. |
| CONSTITUTION-00_CONSTITUTION_v1.1.md | docs/legal/canon/ALKASIK_CONSTITUTION_v1.1_FINAL.md | Canon is authoritative |
| LAW-04_MEMORY_v1.0.md | docs/legal/canon/ALKASIK_MEMORY_LAW_v1.0_FINAL.md | Canon is authoritative |
| LAW-00_AK_CODEX_GOVERNANCE_CODE_v1.0.md | docs/governance/ALKASIK_GOVERNANCE_CHARTER_v1.0.md | Superseded by Governance Charter |
| POL-01_NO_LEGACY_RUNTIME_v1.0.md | AK_PROJECT_CHARTER.md | Same content, codex copy |
| POL-02_PROJECT_CHARTER_v1.0.md | AK_PROJECT_CHARTER.md | Duplicate |
| POL-03_CROSS_AGENT_SHARING_v1.0.md | Security Law | Subsumed by canon law |
| POL-04_AK_CODEX_INTEGRATION_POLICY_v1.0.md | Retired | Codex is maintenance mode |
| All validation reports (AK_CODEX_*) | N/A | Codex phase complete, archive |
| All reports (REPORT-01 through REPORT-08) | N/A | Codex phase complete, archive |
| All reviews (REV-01, REV-02) | N/A | Codex phase complete, archive |
| All specifications (SPEC-*) | N/A | Codex phase complete, archive |
| All standards (STD-*) | N/A | Codex phase complete, archive |

---

## Skills & SOPs

All skill registries under `sovereign/registries/skill_*.yaml` are APPROVED.

No formal SOPs found in the repository. SOP-related governance is handled through:
- Workflow definitions in `workflows/`
- Pipeline definitions in `pipelines/`
- Agent role boundaries in `agents/*/boundaries.md`

---

## Items Requiring Revision

| Artifact | Missing Elements | Required Additions | Blocking Issues |
|----------|-----------------|-------------------|-----------------|
| Janus Charter DRAFT | FINAL status, activation authority | Add Hung Vuong approval block, activation gate conditions | DRAFT status |
| Hermes Charter DRAFT | FINAL status, full lifecycle ownership | Document all 9 domains (Memory, Knowledge, Dataset, Lessons, Skills, Capabilities, Maturity, Adoption, Archive) | DRAFT status |
| Budget Law | FINAL status, authority assignment | Upgrade from REVIEW or DRAFT to FINAL with clear revenue allocation | DRAFT/REVIEW status |

---

## Items Marked for Archive

| Artifact | Reason |
|----------|--------|
| LEGAL_DISCOVERY_RAW.csv.2026-06-07 (archive/) | Raw discovery output, task complete |
| .env.2026-06-07 (archive/) | Environment backup, no longer needed |
| ALL_REPORT.7z (root) | Root-level archive, move to archive/ |
