# AK Governance Consolidation Proposal

**Date:** 2026-06-08  
**Proposer:** Janus  
**Status:** DRAFT — Pending Sage Review  
**Authority:** Constitution v1.1 FINAL, Knowledge Governance Decree v1.0 FINAL  

---

## 1. Problem Statement

The Alkasik Kingdom governance repository has grown organically across multiple work packages, resulting in:

- **Document fragmentation**: Same legal content exists in 2-3 locations (canon .md, sovereign .docx, codex copies)
- **Registry duplication**: `legal_registry.yaml` exists in both `sovereign/registries/` and `docs/legal/codex/registries/`
- **Empty directories**: 16 empty directories add noise without value
- **No centralized document registry**: No single source of truth for what documents exist and their status
- **Pending items untracked**: No consolidated register of pending governance actions

---

## 2. Proposed Actions

### 2.1 Canon Consolidation (Phase 1)

Consolidate all legal documents into `docs/legal/canon/` as the single source of truth:

| Action | Detail | Owner | Timeline |
|---|---|---|---|
| Remove codex constitution copies | CONSTITUTION-00_CONSTITUTION_v1.0.md + v1.1 from codex/constitution/ | Hermes | Sprint 1 |
| Remove codex law copies | LAW-04_MEMORY_v1.0.md, LEGAL_REGISTRY.yaml from codex/ | Hermes | Sprint 1 |
| Remove codex policy copies | POL-01 through POL-04 from codex/policies/ | Hermes | Sprint 1 |
| Archive docs/governance/ v1.0 constitution | Move to archive/ | Janus | Sprint 1 |
| Move CONSTITUTIONAL_MAPPING.md to canon | docs/governance/ → docs/legal/canon/ | Janus | Sprint 1 |

### 2.2 Empty Directory Cleanup (Phase 2)

| Action | Directory | Owner |
|---|---|---|
| Remove empty directory | docs/operations/ | Janus |
| Remove empty directory | sovereign/directives/ | Janus |
| Remove empty directory | sovereign/quarantine/ | Janus |
| Remove empty directory | memory/dataset_registry/ | Janus |
| Remove empty directory | memory/skill_registry/ | Janus |
| Remove empty directory | memory/lessons/ | Janus |
| Remove empty directory | governance/policy/ | Janus |
| Remove empty directory | governance/sage/ | Janus |
| Remove empty directory | governance/tests/ | Janus |
| Remove empty directories | tools/archive/, audit/, backup/, refactor/, validators/ | Janus |
| Keep as placeholder | sovereign/laws/digital_assets/, sovereign/laws/infrastructure/ | — |
| Populate or remove | connectors/openai/, connectors/gmail/ | Lang Lieu |

### 2.3 Registry Standardization (Phase 2)

| Action | Detail | Owner |
|---|---|---|
| Create AK_DOCUMENT_REGISTRY_DRAFT.md | Central document registry | Janus (DONE) |
| Integrate existing YAML registries | Cross-reference sovereign + governance registries | Janus |
| Archive codex LEGAL_REGISTRY.yaml | Remove duplicate | Hermes |

### 2.4 Pending Items Resolution (Phase 3)

| Priority | Item | Owner | Target |
|---|---|---|---|
| HIGH | Budget Law FINAL approval | Hung Vuong | Next council |
| HIGH | WP35.5 + WP36 Sage review | Sage | Next sprint |
| HIGH | Agent activation to PILOT | Hung Vuong | After reviews |
| MEDIUM | Retention policy execution | Hermes | Next sprint |
| MEDIUM | Market sandbox 30-day start | Janus | After activation |

---

## 3. Governance Impact Assessment

### Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Removing codex files breaks references | Low | Medium | Codex is in maintenance mode; no active references |
| Empty directory removal confuses history | Medium | Low | Git history preserves structure |
| Canon consolidation creates merge conflicts | Low | Medium | Files are identical content, no conflicts |

### Compliance

| Requirement | Status |
|---|---|
| Constitution checked | PASS |
| State Corpus checked | PASS |
| Agent Law checked | PASS |
| Knowledge Governance Decree checked | PASS |
| Repo Governance Decree checked | PASS |
| Retention/Archive checked | PASS |
| No protected path modified | PASS |
| No credential accessed | PASS |
| No runtime/live execution changed | PASS |

---

## 4. Approval Path

```
Janus (Proposer)
  → Sage (Governance Review)
    → Hung Vuong (Final Approval)
```

## 5. Exit Criteria

- [ ] Canon contains all 12 FINAL laws + constitution + state corpus
- [ ] Codex duplicates removed
- [ ] Empty directories cleaned
- [ ] Document registry operational
- [ ] Pending items register reviewed
- [ ] All compliance checks passed
