# AK Merge Recommendations

Authority: Janus Directive WP35.4A | Date: 2026-06-08

## Merge Group 1: Legal Canon + Codex Consolidation

### Merge 1: ALKASIK_MEMORY_LAW + LAW-04_MEMORY
| Item | Detail |
|---|---|
| **Canonical** | canon/ALKASIK_MEMORY_LAW_v1.0_FINAL.md |
| **Merge Into** | canon/ (already authoritative, add codex content if missing) |
| **Archive** | codex/laws/LAW-04_MEMORY_v1.0.md after merge |
| **Overlap** | ~90% |
| **Action** | Verify codex has no additional content; if so, add to canon then archive |

### Merge 2: ALKASIK_REPO_GOVERNANCE_DECREE + LAW-00_CODEX_GOVERNANCE
| Item | Detail |
|---|---|
| **Canonical** | canon/ALKASIK_REPO_GOVERNANCE_DECREE_v1.0_FINAL.md |
| **Merge Into** | canon/ |
| **Archive** | codex/laws/LAW-00_AK_CODEX_GOVERNANCE_CODE_v1.0.md |
| **Overlap** | ~85% |

### Merge 3: Sovereign Registries + Codex Registries
| Item | Detail |
|---|---|
| **Canonical** | sovereign/registries/legal_registry.yaml |
| **Merge Into** | sovereign/registries/legal_registry.yaml (add codex entries) |
| **Archive** | codex/registries/LEGAL_REGISTRY.yaml |
| **Overlap** | ~60% |

## Merge Group 2: Report Consolidation

### Merge 4: WP35_1C_01 Sub-reports → Final
| Item | Detail |
|---|---|
| **Canonical** | WP35_1C_01_FINAL_REPORT.md |
| **Merge Target** | Final report (already authoritative) |
| **Archive** | All 8 sub-reports |
| **Note** | Sub-reports are TEMPORARY artifacts; final report contains distilled content |

### Merge 5: Knowledge Audit Duplicates
| Item | Detail |
|---|---|
| **Canonical** | AK_KNOWLEDGE_FOUNDATION_AUDIT.md |
| **Merge Into** | Add content from AK_KNOWLEDGE_STATE_AUDIT.md |
| **Archive** | AK_KNOWLEDGE_STATE_AUDIT.md |

| Item | Detail |
|---|---|
| **Canonical** | AK_RETRIEVAL_OPTIMIZATION_EXECUTION_REPORT.md |
| **Merge Into** | Execution report (add plan content) |
| **Archive** | AK_RETRIEVAL_OPTIMIZATION_REPORT.md, AK_RETRIEVAL_OPTIMIZATION_IMPLEMENTATION_PLAN.md |

| Item | Detail |
|---|---|
| **Canonical** | AK_REGISTRY_NORMALIZATION_EXECUTION_REPORT.md |
| **Merge Into** | Execution report (add plan content) |
| **Archive** | AK_REGISTRY_NORMALIZATION_PLAN.md |

### Merge 6: Capability Validation Baseline + Scenarios
| Item | Detail |
|---|---|
| **Canonical** | AK_CAPABILITY_VALIDATION_BASELINE.md |
| **Merge Into** | Baseline (add scenario content) |
| **Archive** | AK_CAPABILITY_VALIDATION_SCENARIOS.md |
| **Overlap** | ~35% |

## Merge Group 3: Specification Consolidation

### Merge 7: Phase Interface Specs → Unified Spec
| Item | Detail |
|---|---|
| **Canonical** | docs/specifications/WP35_DATA_MODEL_SPEC.md |
| **Canonical** | docs/specifications/WP35_IMPLEMENTATION_SPEC.md |
| **Merge Into** | Canonical spec files (add any unique content) |
| **Archive** | All docs/specs/ phase-specific specs |
| **Note** | Phase specs were superseded by unified specs |

## Merge Tracking

| Merge ID | Priority | Overlap | Effort | Risk |
|---|---|---|---|---|
| M1 | HIGH | 90% | Low | Low |
| M2 | HIGH | 85% | Low | Low |
| M3 | HIGH | 60% | Medium | Medium |
| M4 | MEDIUM | 40% | Medium | Low |
| M5 | MEDIUM | 40% | Medium | Low |
| M6 | LOW | 35% | Low | Low |
| M7 | LOW | 70% | Low | Low |
