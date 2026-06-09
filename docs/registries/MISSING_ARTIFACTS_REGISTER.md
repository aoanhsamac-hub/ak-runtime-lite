# NCP-R Wave 1 — Missing Artifacts Register

**Date:** 2026-06-08
**Authority:** Janus Directive — NCP-R
**Status:** COMPLETE
**Reviewer:** Janus

---

## Purpose

This register documents all artifacts identified as MISSING during NCP-R Wave 1 review.
Per directive: "Do NOT create them. Only document them."

---

## Missing Artifacts

| # | Artifact | Domain | Priority | Required Action | Legal Basis |
|---|----------|--------|----------|----------------|-------------|
| 1 | Treasury Charter | Economic | HIGH | Create charter defining treasury governance structure, authority chain, operational model, and reporting requirements | Economic Law — treasury impact assessment required; Approved Economic Model |
| 2 | Emergency Reserve Framework | Economic | HIGH | Define governance for emergency reserve activation, funding source, authority chain, and maximum allocation | Economic Law — only strategic reserve exists; emergency reserve missing |
| 3 | Agent Registry (dedicated YAML) | Governance | MEDIUM | Create human-readable agent index with status, authority, capabilities, dependencies for all 7 agents | Agent Law — all agents must have registry entry |
| 4 | Dataset Registry (YAML index) | Governance | MEDIUM | Create YAML index of all datasets with schema, retention, owner, status, and lifecycle tracking | Knowledge Governance Decree — retention classes required |
| 5 | Memory Registry (dedicated) | Governance | MEDIUM | Create index of all memory tables (14 NMP tables) with retention policies, compaction schedules, and access controls | Memory Law + Retention & Archive Decree |
| 6 | Revenue Registry (dedicated) | Economic | LOW | Create separate registry for revenue tracking and classification beyond treasury_registry.yaml | Economic Law — 9 revenue sources identified |
| 7 | Budget Registry (dedicated) | Economic | LOW | Create budget allocation tracking registry with program-level detail | Budget Law REVIEW references budget workflow |
| 8 | SOPs (formal) | Governance | LOW | Create standard operating procedures for common workflows (activation, charter creation, registry updates) | Repo Governance Decree — working practices defined but no formal SOPs |
| 9 | National Treasury Governance Charter | Economic | LOW | Subset of Treasury Charter — may be combined | Economic Law |
| 10 | Royal Treasury Charter | Economic | LOW | Subset of Treasury Charter — may be combined | Approved Economic Model — 8% Royal Treasury allocation requires governance |

---

## Summary by Domain

| Domain | Missing Count | Critical (HIGH) |
|--------|--------------|-----------------|
| Economic | 5 | 2 |
| Governance | 4 | 0 |
| Memory | 1 | 0 |
| **Total** | **10** | **2** |

---

## Priority Rationale

### HIGH Priority
- **Treasury Charter**: Without it, the Approved Economic Model (92/8 split, surplus distribution) has no governance framework to operate within.
- **Emergency Reserve Framework**: Without it, the kingdom has no mechanism to handle financial emergencies, violating the prudent governance principle in Economic Law.

### MEDIUM Priority
- Agent/Dataset/Memory registries: The registries function through Python code (AgentRegistry, DatasetRegistry, NationalMemoryPlatform) but lack human-readable YAML indices. These are quality-of-governance improvements.

### LOW Priority
- Revenue/Budget/SOP charters and registries: Nice-to-have refinements that can be deferred.
