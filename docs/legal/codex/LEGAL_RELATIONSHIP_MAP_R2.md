# LEGAL RELATIONSHIP MAP R2

Directive: AK-CODEX-WP01-R2
Phase: 8 - Legal Graph Preparation
Date: 2026-06-07

## Relationships

| Document | depends_on | implements | approved_by | owned_by | related_to |
|---|---|---|---|---|---|
| STD-01_LESSON_QUALITY_v1.0 | LAW-04_MEMORY_v1.0 | WP3.5 Phase 1 | Sage | Lang Lieu | STD-05_PROMOTION_GOVERNANCE_v1.0 |
| STD-02_SKILL_TAXONOMY_v1.0 | LAW-04_MEMORY_v1.0 | WP3.5 Phase 2 | Sage | Lang Lieu | STD-01_LESSON_QUALITY_v1.0 |
| STD-04_LEARNING_METRICS_v1.0 | Article 37, Article 39 | WP3.5 Phase 1A | Sage | Lang Lieu | STD-01_LESSON_QUALITY_v1.0 |
| STD-05_PROMOTION_GOVERNANCE_v1.0 | CONSTITUTION-00_CONSTITUTION_v1.1 | WP3.5 Phase 3 | Sage | Lang Lieu | STD-01_LESSON_QUALITY_v1.0 |
| LAW-04_MEMORY_v1.0 | CONSTITUTION-00_CONSTITUTION_v1.1 | Article 37 | Hung Vuong | Hung Vuong | POL-01_NO_LEGACY_RUNTIME_v1.0 |
| POL-01_NO_LEGACY_RUNTIME_v1.0 | CONSTITUTION-00_CONSTITUTION_v1.1 | Implementation | Sage | Lang Lieu | - |
| POL-02_PROJECT_CHARTER_v1.0 | CONSTITUTION-00_CONSTITUTION_v1.1 | Foundation | Sage | Lang Lieu | - |
| POL-03_CROSS_AGENT_SHARING_v1.0 | LAW-04_MEMORY_v1.0 | WP3.5 Architecture | Sage | Lang Lieu | - |
| SPEC-00_WP35_IMPLEMENTATION_v1.0 | STD-01..05 | WP3.5 Implementation | Sage | Lang Lieu | - |
| SPEC-01_WP35_DATA_MODEL_v1.0 | LAW-04_MEMORY_v1.0, LAW-05_INFORMATION | WP3.5 Data Model | Sage | Lang Lieu | - |
| CONSTITUTION-00_CONSTITUTION_v1.0 | - | State Constitution | Hung Vuong | Hung Vuong | CONSTITUTION-00_CONSTITUTION_v1.1 |
| CONSTITUTION-00_CONSTITUTION_v1.1 | Article 27-39 | Constitutional Update | Hung Vuong | Hung Vuong | - |
| REV-01_WP35_PHASE1A_v1.0 | STD-04_LEARNING_METRICS_v1.0 | Phase 1A Review | Hung Vuong | Sage | - |
| REV-02_WP35_PHASE1B_v1.0 | STD-01, LAW-04, POL-01 | Phase 1B Review | Hung Vuong | Sage | - |

## Graph Node Types

- **Con: Constitution**
- **Law: Law**
- **Pol: Policy**
- **Std: Standard**
- **Spec: Specification**
- **Rev: Review**

## Graph Edge Types

- **depends_on**: Legal prerequisite
- **implements**: Operational implementation
- **approved_by**: Approval authority
- **owned_by**: Document owner
- **related_to**: Related documents

Ready for Hermes graph ingestion.