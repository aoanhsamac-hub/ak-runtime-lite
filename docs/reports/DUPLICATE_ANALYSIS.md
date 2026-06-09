# AK Repository Duplicate & Overlap Analysis

Authority: Janus Directive WP35.4A | Date: 2026-06-08

## Category 1: Legal Document Duplication (>50% overlap)

### 1.1 Constitution Versions
| File | Overlap | Canonical | Action |
|---|---|---|---|
| docs/legal/canon/ALKASIK_CONSTITUTION_v1.1_FINAL.md | 100% | **CANONICAL** | Keep |
| docs/legal/codex/constitution/CONSTITUTION-00_CONSTITUTION_v1.1.md | ~95% | Mirror | Archive codex copy |
| docs/legal/codex/constitution/CONSTITUTION-00_CONSTITUTION_v1.0.md | ~90% | Superseded | Archive |
| docs/governance/ALKASIK_CONSTITUTION_v1.0.md | ~85% | Superseded | Archive |

**Overlap: >50% — CONSOLIDATION REQUIRED**

### 1.2 Legal Canon vs Codex
| Canon File | Codex Mirror | Overlap |
|---|---|---|
| ALKASIK_CONSTITUTION_v1.1_FINAL.md | CONSTITUTION-00_CONSTITUTION_v1.1.md | ~95% |
| ALKASIK_AGENT_LAW_v1.0_FINAL.md | (no direct mirror) | - |
| ALKASIK_MEMORY_LAW_v1.0_FINAL.md | LAW-04_MEMORY_v1.0.md | ~90% |
| ALKASIK_REPO_GOVERNANCE_DECREE_v1.0_FINAL.md | LAW-00_AK_CODEX_GOVERNANCE_CODE_v1.0.md | ~85% |

**Assessment**: Codex/ directory was consolidated from canon but codex files remain as copies. >50% overlap. CONSOLIDATION REQUIRED.

### 1.3 Sovereign Registries vs Governance Registries
| Sovereign Registry | Governance Registry | Overlap |
|---|---|---|
| sovereign/registries/legal_registry.yaml | codex/registries/LEGAL_REGISTRY.yaml | ~60% |
| sovereign/legal_index.yaml | LEGAL_CANON_INDEX.md | ~70% |

**Assessment**: Duplicate registry indexes. >50% overlap. CONSOLIDATION REQUIRED.

## Category 2: Report Duplication (>30% overlap)

### 2.1 WP35 Phase Reports (Sub-reports vs Final)
| Sub-report | Final Report | Overlap |
|---|---|---|
| WP35_1C_01_01_RUNTIME_ARCHITECTURE.md → WP35_1C_01_FINAL_REPORT.md | ~40% |
| WP35_1C_01_02_SIGNAL_EXTRACTION_REPORT.md → WP35_1C_01_FINAL_REPORT.md | ~40% |
| WP35_1C_01_03_INSIGHT_FORMATION_REPORT.md → WP35_1C_01_FINAL_REPORT.md | ~35% |
| WP35_1C_01_04_CANDIDATE_SKILL_CATALOG.md → WP35_1C_01_FINAL_REPORT.md | ~30% |
| WP35_1C_01_05_GOVERNANCE_AUDIT_REPORT.md → WP35_1C_01_FINAL_REPORT.md | ~30% |
| WP35_1C_01_06_TEST_COVERAGE_REPORT.md → WP35_1C_01_FINAL_REPORT.md | ~35% |
| WP35_1C_01_07_RISK_CLASSIFICATION.md → WP35_1C_01_FINAL_REPORT.md | ~30% |
| WP35_1C_01_08_DRY_RUN_VALIDATION.md → WP35_1C_01_FINAL_REPORT.md | ~30% |

**Assessment**: >30% overlap — CONSOLIDATION PROPOSED. Sub-reports are TEMPORARY artifacts.

### 2.2 Capability Pipeline Reports
| Report | Overlap with | Est. Overlap |
|---|---|---|
| AK_CAPABILITY_DISCOVERY_REPORT.md | AK_CAPABILITY_FAMILY_REPORT.md | ~25% |
| AK_CAPABILITY_MATURITY_REPORT.md | AK_CAPABILITY_READINESS_REPORT.md | ~25% |
| AK_CAPABILITY_EVIDENCE_REPORT.md | AK_CAPABILITY_PROMOTION_READINESS_REPORT.md | ~25% |
| AK_CAPABILITY_VALIDATION_BASELINE.md | AK_CAPABILITY_VALIDATION_SCENARIOS.md | ~35% |

**Assessment**: <30% for most, but VALIDATION_BASELINE vs SCENARIOS >30% — CONSOLIDATION PROPOSED.

### 2.3 Knowledge Audit Reports (HERMES-CLEANUP-01)
| Report | Overlap with | Est. Overlap |
|---|---|---|
| AK_KNOWLEDGE_STATE_AUDIT.md | AK_KNOWLEDGE_FOUNDATION_AUDIT.md | ~40% |
| AK_KINGDOM_KNOWLEDGE_INVENTORY.md | AK_DUPLICATE_CONSOLIDATION_PLAN.md | ~35% |
| AK_RETRIEVAL_OPTIMIZATION_REPORT.md | AK_RETRIEVAL_OPTIMIZATION_EXECUTION_REPORT.md | ~45% |
| AK_REGISTRY_NORMALIZATION_PLAN.md | AK_REGISTRY_NORMALIZATION_EXECUTION_REPORT.md | ~40% |

**Assessment**: >30% overlap — CONSOLIDATION PROPOSED.

## Category 3: Obsolete Documents

| File | Superseded By | Reason |
|---|---|---|
| docs/governance/ALKASIK_CONSTITUTION_v1.0.md | canon/ALKASIK_CONSTITUTION_v1.1_FINAL.md | Version upgrade |
| docs/governance/ALKASIK_AGENT_CHARTER_v1.0.md | canon/ALKASIK_AGENT_LAW_v1.0_FINAL.md | Charter → Law |
| docs/governance/ALKASIK_GOVERNANCE_CHARTER_v1.0.md | canon/ (multiple) | Absorbed |
| docs/governance/CONSTITUTIONAL_MAPPING.md | canon/LEGAL_CANON_INDEX.md | Moved |
| docs/specs/AK_WP35_PHASE1A_INTERFACE_SPEC.md | docs/specifications/WP35_DATA_MODEL_SPEC.md | Consolidated |
| docs/specs/AK_WP35_PHASE1B_INTERFACE_SPEC.md | docs/specifications/WP35_DATA_MODEL_SPEC.md | Consolidated |
| docs/specs/AK_WP35_PHASE1C_INTERFACE_SPEC.md | docs/specifications/WP35_IMPLEMENTATION_SPEC.md | Consolidated |
| docs/specs/AK_WP35_PHASE1C_IMPLEMENTATION_CONTRACT.md | docs/specifications/WP35_IMPLEMENTATION_SPEC.md | Consolidated |
| docs/specs/AK_WP35_PHASE1E_INTERFACE_SPEC.md | docs/specifications/WP35_IMPLEMENTATION_SPEC.md | Consolidated |
| codex/reports/AK_CODEX_GOVERNANCE_ACTIVATION_REPORT.md | codex/REPORT-04_FINAL_EXECUTION.md | Phase artifact |
| codex/constitution/CONSTITUTION-00_CONSTITUTION_v1.0.md | codex/constitution/ v1.1 | Version |
| AK_PROJECT_CHARTER.md | sovereign/legal_index.yaml | Registry |
| AK_NO_LEGACY_RUNTIME_POLICY.md | canon/ALKASIK_REPO_GOVERNANCE_DECREE.md | Policy → Decree |

## Category 4: Orphan Documents (Unreferenced)

| File | Estimated Status |
|---|---|
| sovereign/README.md | Empty/placeholder |
| sovereign/legal_registry/LEGAL_INDEX.md | Redundant with LEGAL_CANON_INDEX |
| _pytest_tmp/ (28 temporary dirs) | Test artifacts, orphan |
| governing/ (if exists) | Orphan directory |
| docs/reports/AK_ARCHIVE_NORMALIZATION_PLAN.md | Superseded by execution report |
| docs/reports/AK_APPROVED_DATASET_REPORT.md | Redundant with registry |

## Category 5: Temporary Artifacts

| Path | Reason for Classification | Action |
|---|---|---|
| _pytest_tmp/* | Test temporary output | Archive |
| docs/reports/WP35_1C_01_* (8 sub-reports) | Intermediate phase artifacts | Archive |
| docs/legal/codex/reports/REPORT-01_DISCOVERY.md | Phase artifact | Archive |
| docs/legal/codex/reports/REPORT-01_DISCOVERY_R2.md | Phase artifact | Archive |
| docs/legal/codex/reports/REPORT-02_*.md (3 files) | Phase artifact | Archive |
| docs/legal/codex/reports/REPORT-03_STRUCTURE.md | Phase artifact | Archive |
| docs/legal/codex/reports/REPORT-04_FINAL_EXECUTION.md | Phase artifact | Archive |
| docs/legal/codex/reports/REPORT-05_RELATIONSHIP_MAP.md | Phase artifact | Archive |
| docs/legal/codex/reports/REPORT-06_REGISTRY_CONSOLIDATION.md | Phase artifact | Archive |
| docs/legal/codex/reports/REPORT-07_COMPLIANCE_AUDIT.md | Phase artifact | Archive |
| docs/legal/codex/reports/REPORT-08_NORMALIZATION_AUDIT.md | Phase artifact | Archive |
| docs/reports/AK_LEGACY_LEARNING_INVENTORY.md | One-time scan result | Archive |

## Overlap Heat Map

```
                    Overlap %
                   0  10  20  30  40  50  60  70  80  90 100
                   |  |  |  |  |  |  |  |  |  |  |  |  |  |
canon vs codex      ████████████████████████████████████████ 95%
canon vs gov docs    █████████████████████████████████      85%
WP35 sub vs final    ████████████████                      40%
capability reports   ██████████                            25%
knowledge audits     ████████████████                      40%
sovereign vs gov     ██████████████████████████             60%
registries
specs vs specs       ██████████████████████████████         70%
```

## Summary

| Category | Count | Action Required |
|---|---|---|
| >50% overlap (CONSOLIDATION REQUIRED) | 4 groups | Merge |
| >30% overlap (CONSOLIDATION PROPOSED) | 3 groups | Propose merge |
| Obsolete documents | 12+ | Archive |
| Orphan documents | 5+ | Archive or integrate |
| Temporary artifacts | 20+ | Archive |
