# NCP-R Wave 1 — Remediation Plan

**Date:** 2026-06-08
**Authority:** Janus Directive — NCP-R
**Status:** PROPOSAL (pending Sage review)
**Owner:** Janus
**Reviewer:** Sage

---

## Executive Summary

NCP-R Wave 1 reviewed 82 artifacts across 6 domains. Key findings:
- **24** artifacts APPROVED (existing FINAL documents, registries, agents)
- **3** artifacts REQUIRE_REVISION (Janus Charter, Hermes Charter, Budget Law)
- **5** artifacts MISSING (Treasury Charter, Emergency Reserve Framework, Agent/Dataset/Memory registries)
- **47** artifacts SUPERSEDED (entire codex/ directory)
- **3** artifacts marked for ARCHIVE
- **0** artifacts REJECTED

Total remediation items: **8** (3 revisions + 5 missing artifacts, excluding superseded/archive)

---

## Remediation Items

### Priority 1: Critical (Blocking Governance)

| # | Item | Type | Current State | Target State | Effort | Dependencies |
|---|------|------|-------------|-------------|--------|-------------|
| R1 | Budget Law → FINAL | Revision | REVIEW | FINAL | 1 session | None |
| R2 | Treasury Charter | Creation | MISSING | FINAL charter | 1 session | Economic Law reference |

### Priority 2: High (Blocking Formalization)

| # | Item | Type | Current State | Target State | Effort | Dependencies |
|---|------|------|-------------|-------------|--------|-------------|
| R3 | Janus Charter → FINAL | Revision | DRAFT | FINAL | 1 session | None |
| R4 | Hermes Charter → FINAL | Revision | DRAFT | FINAL | 1 session | None |
| R5 | Emergency Reserve Framework | Creation | MISSING | FINAL | 1 session | Budget Law |

### Priority 3: Medium (Quality of Governance)

| # | Item | Type | Current State | Target State | Effort | Dependencies |
|---|------|------|-------------|-------------|--------|-------------|
| R6 | Agent Registry YAML | Creation | PARTIAL | FINAL | 0.5 session | None |
| R7 | Dataset Registry YAML | Creation | PARTIAL | FINAL | 0.5 session | None |
| R8 | Memory Registry YAML | Creation | MISSING | FINAL | 0.5 session | None |

---

## Execution Sequence

```
Phase 1 (Priority 1):
  R1: Budget Law FINAL
  R2: Treasury Charter
  │
Phase 2 (Priority 2):
  R3: Janus Charter FINAL
  R4: Hermes Charter FINAL
  R5: Emergency Reserve Framework
  │
Phase 3 (Priority 3):
  R6: Agent Registry YAML
  R7: Dataset Registry YAML
  R8: Memory Registry YAML
  │
Phase 4: Codex archive migration
  Move docs/legal/codex/ → archive/legal/codex/
  Remove ALL_REPORT.7z from root → archive/
```

---

## Archive Migration Plan

| Item | Source | Destination | Method |
|------|--------|-------------|--------|
| codex/ | docs/legal/codex/ | archive/legal/codex/ | Move directory |
| ALL_REPORT.7z | .\ALL_REPORT.7z | archive/ALL_REPORT.7z | Move file |
| root_hygiene test outputs | archive/root_hygiene/ | archive/root_hygiene/ (compress) | Compress subdirectories |

---

## Agent Activation Plan

| Agent | Current | Target | Gate | Status |
|-------|---------|--------|------|--------|
| Janus | SANDBOX_ACTIVE | PILOT_ACTIVE | Sage → Hung Vuong | RECOMMENDED |
| Sage | SANDBOX_ACTIVE | PILOT_ACTIVE | Sage self-certify → Janus | RECOMMENDED |
| Hermes | SANDBOX_ACTIVE | PILOT_ACTIVE | Sage → Hung Vuong | RECOMMENDED |
| Iris | SANDBOX_ACTIVE | PILOT_ACTIVE | Sage → Janus | RECOMMENDED |
| Lang Lieu | SANDBOX_ACTIVE | PILOT_ACTIVE | Sage → Janus | RECOMMENDED |
| Yet Kieu | SANDBOX_ACTIVE | PILOT_ACTIVE | Sage → Janus | RECOMMENDED |
| Helen | SANDBOX_ACTIVE | CONDITIONAL_ACTIVE | Complete agent.py → Sage → Janus | CONDITIONAL |

---

## Resource Estimate

| Phase | Items | Estimated Sessions |
|-------|-------|-------------------|
| 1 | 2 | 2 |
| 2 | 3 | 2 |
| 3 | 3 | 1 |
| 4 | Archive migration | 1 |
| **Total** | **8** | **6** |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Budget Law FINAL conflicts with Royal Economic Architecture | LOW | HIGH | Already approved by Royal Economic Architecture Approval |
| Agent PILOT_ACTIVE leads to scope creep | LOW | MEDIUM | Agent Law constraints + propose_only default mode |
| Codex archive breaks references | MEDIUM | LOW | All codex content is duplicated in canon or superseded |
| Treasury Charter conflicts with existing registry | LOW | MEDIUM | treasury_registry.yaml is ACTIVE — charter must align |
