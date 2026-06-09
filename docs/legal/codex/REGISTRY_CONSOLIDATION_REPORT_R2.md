# REGISTRY CONSOLIDATION REPORT R2

Directive: AK-CODEX-WP01-R2
Phase: 5 - Registry Consolidation
Date: 2026-06-07

## Consolidated Registries

### REG-01_CONSTITUTION.yaml
```yaml
registry: AK-CODEX Constitution Registry
status: LOCKED
authority: Hung Vuong
documents:
  - id: CONSTITUTION-00_CONSTITUTION_v1.0
    path: codex/constitution/CONSTITUTION-00_CONSTITUTION_v1.0.md
    status: FINAL
  - id: CONSTITUTION-00_CONSTITUTION_v1.1
    path: codex/constitution/CONSTITUTION-00_CONSTITUTION_v1.1.md
    status: FINAL
```

### REG-01_LEGAL.yaml
```yaml
registry: AK-CODEX Legal Registry
status: ACTIVE
authority: Hung Vuong
documents:
  - id: LAW-04_MEMORY_v1.0
    path: codex/laws/LAW-04_MEMORY_v1.0.md
    status: FINAL
  - id: POL-01_NO_LEGACY_RUNTIME_v1.0
    path: codex/policies/POL-01_NO_LEGACY_RUNTIME_v1.0.md
    status: ACTIVE
  - id: POL-02_PROJECT_CHARTER_v1.0
    path: codex/policies/POL-02_PROJECT_CHARTER_v1.0.md
    status: ACTIVE
  - id: POL-03_CROSS_AGENT_SHARING_v1.0
    path: codex/policies/POL-03_CROSS_AGENT_SHARING_v1.0.md
    status: ACTIVE
  - id: STD-01_LESSON_QUALITY_v1.0
    path: codex/standards/STD-01_LESSON_QUALITY_v1.0.md
    status: ACTIVE
  - id: STD-02_SKILL_TAXONOMY_v1.0
    path: codex/standards/STD-02_SKILL_TAXONOMY_v1.0.md
    status: ACTIVE
  - id: STD-04_LEARNING_METRICS_v1.0
    path: codex/standards/STD-04_LEARNING_METRICS_v1.0.md
    status: ACTIVE
  - id: STD-05_PROMOTION_GOVERNANCE_v1.0
    path: codex/standards/STD-05_PROMOTION_GOVERNANCE_v1.0.md
    status: ACTIVE
```

### REG-02_AUTHORITY.yaml
```yaml
registry: AK-CODEX Authority Registry
status: ACTIVE
authority: Hung Vuong
hierarchy:
  - level: SOVEREIGN
    authority: Hung Vuong
    can_approve: ALL
  - level: GOVERNANCE
    authority: Sage
    can_approve: Risk, Law, Policy
  - level: TECHNICAL
    authority: Lang Lieu
    can_approve: Implementation, Registry
  - level: REVIEW
    authority: Sage
    can_approve: Review packages
```

### REG-01_APPROVAL_MATRIX.yaml
```yaml
registry: AK-CODEX Approval Matrix
status: ACTIVE
authority: Hung Vuong
approvals:
  - category: Constitution
    required: Hung Vuong
    review: Sage
  - category: Law
    required: Hung Vuong
    review: Sage
  - category: Policy
    required: Lang Lieu
    review: Sage
  - category: Standard
    required: Lang Lieu
    review: Sage
  - category: Specification
    required: Lang Lieu
    review: Sage
  - change_level:
      - LEVEL_0: None
      - LEVEL_1: Janus
      - LEVEL_2: Lang Lieu
      - LEVEL_3: Sage
      - LEVEL_4: Hung Vuong
```

## Registry Fragmentation Status

- BEFORE: Multiple registries across sovereign/, governance/
- AFTER: Unified under docs/legal/codex/registries/
- Status: CONSOLIDATED