# AK Proposed Registry Structure

Authority: Janus Directive WP35.4A | Date: 2026-06-08

## Current State (Before Consolidation)

```
sovereign/
  legal_index.yaml
  registries/
    legal_registry.yaml
    constitution_registry.yaml
    state_corpus_registry.yaml
    legal_hierarchy.yaml
    directive_registry.yaml
    treasury_registry.yaml

legal/
  canon/LEGAL_CANON_INDEX.md

legal/codex/
  registries/LEGAL_REGISTRY.yaml    ← DUPLICATE of sovereign/legal_registry.yaml

sovereign/
  legal_registry/LEGAL_INDEX.md    ← ORPHAN
```

## Proposed Structure (Single Source of Truth)

### Authoritative Registry Hierarchy

```
sovereign/                                          ← SINGLE SOURCE OF TRUTH
  legal_index.yaml                                  ← Master canonical index
  registries/
    legal_registry.yaml                             ← All legal documents
    constitution_registry.yaml                      ← Constitution versions
    state_corpus_registry.yaml                      ← State corpus
    legal_hierarchy.yaml                            ← Legal hierarchy
    directive_registry.yaml                         ← Directives
    treasury_registry.yaml                          ← Treasury

governance/
  registries/
    approval_matrix.yaml                            ← Approval authority
    issue_registry.yaml                             ← Issue tracking
    governance_gate_registry.yaml                   ← Gate records
    protected_modules.yaml                          ← Protected paths

memory/
  (All registries remain)                           ← Operational registries
  learning_registry/                                  (8 registries)
  capability_pipeline/                                (4 registries)
  capability_registry/                                (3 registries)
  capability_backlog/                                 (1 registry)
```

### Documentation Index (Registry Role)

```
docs/legal/canon/
  LEGAL_CANON_INDEX.md                              ← Human-readable index, references sovereign/
  ALKASIK_CONSTITUTION_v1.1_FINAL.md                ← Canonical law
  ALKASIK_AGENT_LAW_v1.0_FINAL.md                   ← Canonical law
  ... (13 canonical laws)
```

### Consolidated AK_MEMORY.md
```
./AK_MEMORY.md                                      ← Single master knowledge index
```

## Registry-to-Source Mapping

| Registry | Source of Truth | Backup/Archive |
|---|---|---|
| Legal documents | sovereign/legal_index.yaml | LEGAL_CANON_INDEX.md (human readable) |
| Governance | governance/registries/*.yaml | N/A (code is source) |
| Memory (operational) | memory/*.py | LanceDB tables |
| Skills | memory/learning_registry/*.py | LanceDB tables |
| Capabilities | memory/capability_registry/*.py | LanceDB tables |
| Market forecasts | memory/market_forecast_registry.py | LanceDB tables |
| Test results | N/A (ephemeral) | _pytest_tmp → archive or delete |

## What Changes

| Change | Action |
|---|---|
| Remove codex/registries/LEGAL_REGISTRY.yaml | Archive (merge content into sovereign/) |
| Remove sovereign/legal_registry/LEGAL_INDEX.md | Archive (redundant with LEGAL_CANON_INDEX) |
| Ensure LEGAL_CANON_INDEX.md is the ONLY legal index | Keep in canon/ |
| Ensure sovereign/legal_index.yaml is the ONLY YAML registry index | Keep in sovereign/ |
| Remove duplicate constitution mirrors | Archive to archive/legal/ |

## Single Source of Truth Ownership

| Domain | Owner | Registry Type | Update Authority |
|---|---|---|---|
| Legal Framework | Sage | YAML + Markdown | Constitution requires council |
| Governance | Sage | Python + YAML | Governance gate |
| Memory Platform | Hermes | Python + LanceDB | Learning runtime |
| Agent Identities | Janus | Python | Council mission |
| Market Observation | Iris | Python | OBSERVE_ONLY |
| Engineering | Lang Lieu | Python | Development |
| Security | Yet Kieu | Python | Infrastructure |
