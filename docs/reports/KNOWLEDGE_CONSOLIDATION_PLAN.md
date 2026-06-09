# AK Knowledge Consolidation Plan

Authority: Janus Directive WP35.4A | Date: 2026-06-08

## Phase 1: Legal Canon Consolidation

### 1.1 Constitution - Single Source of Truth
| Action | Source | Target |
|---|---|---|
| **KEEP** | docs/legal/canon/ALKASIK_CONSTITUTION_v1.1_FINAL.md | Canon (authoritative) |
| **REDIRECT** | codex/constitution/CONSTITUTION-00_CONSTITUTION_v1.1.md | Add redirect to canon |
| **ARCHIVE** | codex/constitution/CONSTITUTION-00_CONSTITUTION_v1.0.md | archive/legal/codex/ |
| **ARCHIVE** | docs/governance/ALKASIK_CONSTITUTION_v1.0.md | archive/legal/ |
| **ARCHIVE** | docs/governance/ALKASIK_AGENT_CHARTER_v1.0.md | archive/legal/ |
| **ARCHIVE** | docs/governance/ALKASIK_GOVERNANCE_CHARTER_v1.0.md | archive/legal/ |
| **ARCHIVE** | docs/governance/CONSTITUTIONAL_MAPPING.md | archive/legal/ |
| **MERGE** | codex/laws/LAW-04_MEMORY_v1.0.md | canon/ALKASIK_MEMORY_LAW_v1.0_FINAL.md |
| **MERGE** | codex/laws/LAW-00_AK_CODEX_GOVERNANCE_CODE_v1.0.md | canon/ALKASIK_REPO_GOVERNANCE_DECREE.md |

### 1.2 Registry - Single Source of Truth
| Action | Source | Target |
|---|---|---|
| **KEEP** | sovereign/registries/legal_registry.yaml | Authoritative |
| **MERGE** | codex/registries/LEGAL_REGISTRY.yaml | sovereign/registries/legal_registry.yaml |
| **KEEP** | LEGAL_CANON_INDEX.md | Authoritative index |
| **MERGE** | sovereign/legal_index.yaml | LEGAL_CANON_INDEX.md |
| **ARCHIVE** | sovereign/legal_registry/LEGAL_INDEX.md | archive/legal/ |

## Phase 2: Report Consolidation

### 2.1 WP35 Phase 1C Sub-reports → Final
| Action | Source | Target |
|---|---|---|
| **ARCHIVE** | WP35_1C_01_01_RUNTIME_ARCHITECTURE.md | archive/reports/wp35_1c_01/ |
| **ARCHIVE** | WP35_1C_01_02_SIGNAL_EXTRACTION_REPORT.md | archive/reports/wp35_1c_01/ |
| **ARCHIVE** | WP35_1C_01_03_INSIGHT_FORMATION_REPORT.md | archive/reports/wp35_1c_01/ |
| **ARCHIVE** | WP35_1C_01_04_CANDIDATE_SKILL_CATALOG.md | archive/reports/wp35_1c_01/ |
| **ARCHIVE** | WP35_1C_01_05_GOVERNANCE_AUDIT_REPORT.md | archive/reports/wp35_1c_01/ |
| **ARCHIVE** | WP35_1C_01_06_TEST_COVERAGE_REPORT.md | archive/reports/wp35_1c_01/ |
| **ARCHIVE** | WP35_1C_01_07_RISK_CLASSIFICATION.md | archive/reports/wp35_1c_01/ |
| **ARCHIVE** | WP35_1C_01_08_DRY_RUN_VALIDATION.md | archive/reports/wp35_1c_01/ |

### 2.2 Codex Phase Artifacts → Archive
| Action | Source | Target |
|---|---|---|
| **ARCHIVE** | codex/reports/REPORT-01_DISCOVERY.md | archive/codex/ |
| **ARCHIVE** | codex/reports/REPORT-01_DISCOVERY_R2.md | archive/codex/ |
| **ARCHIVE** | codex/reports/REPORT-02_TAXONOMY.md | archive/codex/ |
| **ARCHIVE** | codex/reports/REPORT-02_NAMING_NORMALIZATION.md | archive/codex/ |
| **ARCHIVE** | codex/reports/REPORT-03_STRUCTURE.md | archive/codex/ |
| **ARCHIVE** | codex/reports/REPORT-04_FINAL_EXECUTION.md | archive/codex/ |
| **ARCHIVE** | codex/reports/REPORT-05_RELATIONSHIP_MAP.md | archive/codex/ |
| **ARCHIVE** | codex/reports/REPORT-06_REGISTRY_CONSOLIDATION.md | archive/codex/ |
| **ARCHIVE** | codex/reports/REPORT-07_COMPLIANCE_AUDIT.md | archive/codex/ |
| **ARCHIVE** | codex/reports/REPORT-08_NORMALIZATION_AUDIT.md | archive/codex/ |
| **ARCHIVE** | codex/REPORT-01_DISCOVERY.md | archive/codex/ |
| **ARCHIVE** | codex/REPORT-02_NAMING_NORMALIZATION.md | archive/codex/ |

### 2.3 Knowledge Audit Reports → Consolidate
| Action | Source | Target |
|---|---|---|
| **MERGE** | AK_KNOWLEDGE_STATE_AUDIT.md → AK_KNOWLEDGE_FOUNDATION_AUDIT.md |
| **MERGE** | AK_RETRIEVAL_OPTIMIZATION_REPORT.md → AK_RETRIEVAL_OPTIMIZATION_EXECUTION_REPORT.md |
| **MERGE** | AK_REGISTRY_NORMALIZATION_PLAN.md → AK_REGISTRY_NORMALIZATION_EXECUTION_REPORT.md |

## Phase 3: Specification Consolidation

| Action | Source | Target |
|---|---|---|
| **KEEP** | docs/specifications/WP35_DATA_MODEL_SPEC.md | Authoritative |
| **KEEP** | docs/specifications/WP35_IMPLEMENTATION_SPEC.md | Authoritative |
| **ARCHIVE** | docs/specs/AK_WP35_PHASE1A_INTERFACE_SPEC.md | archive/specs/ |
| **ARCHIVE** | docs/specs/AK_WP35_PHASE1B_INTERFACE_SPEC.md | archive/specs/ |
| **ARCHIVE** | docs/specs/AK_WP35_PHASE1C_INTERFACE_SPEC.md | archive/specs/ |
| **ARCHIVE** | docs/specs/AK_WP35_PHASE1C_IMPLEMENTATION_CONTRACT.md | archive/specs/ |
| **ARCHIVE** | docs/specs/AK_WP35_PHASE1E_INTERFACE_SPEC.md | archive/specs/ |

## Phase 4: Governance.md → Governance.py Consolidation

| Action | Source | Target |
|---|---|---|
| **ARCHIVE** | governance/policy_engine/POLICY_ENGINE.md | archive/governance/ |
| **ARCHIVE** | governance/approval_gate/APPROVAL_GATE.md | archive/governance/ |
| **ARCHIVE** | governance/protected_modules/PROTECTED_MODULES.md | archive/governance/ |
| **ARCHIVE** | governance/risk_kernel/RISK_KERNEL_CHARTER.md | archive/governance/ |

## Phase 5: Test Artifact Cleanup

| Action | Source | Target |
|---|---|---|
| **CLEAN** | _pytest_tmp/* | Delete (temp artifacts) |

## Migration Order

```
Phase 1: Legal canon (highest priority, clearest duplication)
    ↓
Phase 2: Reports (medium priority, large volume)
    ↓
Phase 3: Specifications (low priority, already superseded)
    ↓
Phase 4: Governance docs (maintenance)
    ↓
Phase 5: Test artifacts (cleanup)
```

## Risk Assessment

| Risk | Mitigation |
|---|---|
| Archive breaks cross-references | Update LEGAL_CANON_INDEX and AK_MEMORY.md |
| Loss of historical context | Archive preserves original files |
| Merge conflicts in YAML registries | Manual merge, validate schema |
| Orphaned report references | Check AK_MEMORY.md for references |
