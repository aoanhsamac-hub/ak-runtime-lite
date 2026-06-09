# AK Skill Registry Architecture v1.0

## Overview

The AK Skill Registry Architecture defines the technical infrastructure for the National Skill Registry, including LanceDB tables, registry classes, API integration, and data flow.

## Core Tables (LanceDB)

| Table | Registry | Purpose |
|-------|----------|---------|
| ak_skills | SkillRegistry | Master skill records (extends NAOP mandatory table) |
| ak_skill_dependencies | SkillDependencyRegistry | Dependency graph edges |
| ak_skill_ownership | SkillOwnershipRegistry | Ownership and access control mappings |
| ak_skill_lifecycle | SkillLifecycleEngine | Lifecycle transition events |
| ak_skill_validations | SkillValidationEngine | Validation results and reports |
| ak_skill_retirement | (embedded in skill record) | Retirement tracking |

## Registry Classes

### SkillRegistry (`memory/skill_registry.py`)

- Manages CRUD operations for SkillRecord
- Supports lifecycle_stage transitions
- Handles ownership updates (primary_users, secondary_users, forbidden_users)
- Manages dependency lists
- Filters by status, lifecycle_stage, owner, category, source
- Backed by `ak_skills` LanceDB table

### SkillDependencyRegistry (`memory/dependency_registry.py`)

- Manages SkillDependencyRecord entries
- Supports 5 target types: skill, dataset, tool, agent, capability
- Circular dependency detection
- Query by source skill, target, relationship type

### SkillOwnershipRegistry (`memory/dependency_registry.py`)

- Manages SkillOwnershipRecord entries
- Query by skill, owner, user with access level filter
- Ownership update and transfer

## Service Layer

### SkillLifecycleEngine (`services/skill_lifecycle_engine.py`)

- Validates and executes lifecycle transitions
- Governance gate enforcement
- Transition audit trail via SkillLifecycleEventRecord
- Historical query by skill

### SkillValidationEngine (`services/skill_validation_engine.py`)

- 6 validation types: unit, integration, governance, risk, performance, audit
- Orchestrates existing validators (IndependentReviewGate, governance gates)
- Batch validation support
- Validation report generation

## Import Adapters

### HermesSkillImporter (`connectors/hermes_import_adapter.py`)

- Parses Hermes skill manifests
- Maps to AK SkillRecord
- Creates PROPOSED skills in registry
- Dry-run mode for pre-import validation

### OpenCodeSkillImporter (`connectors/opencode_import_adapter.py`)

- Detects OpenCode vs OpenHands format
- Maps to AK SkillRecord
- Human Sovereignty Gate enforced
- Dry-run mode

## Data Flow

```
External Source (Hermes/OpenCode)
    |
    v
Import Adapter (parse + map)
    |
    v
SkillRegistry.create_candidate() --> ak_skills (PROPOSED)
    |
    v
SkillLifecycleEngine.transition() --> lifecycle events
    |                                  +--> ak_skill_lifecycle
    v
SkillValidationEngine.validate() --> validation reports
    |                                  +--> ak_skill_validations
    v
Governance Gates --> approval checkpoints
    |
    v
ACTIVE skill in production
```

## Integration Points

| Component | Method | Purpose |
|-----------|--------|---------|
| NationalMemoryPlatform | promote_to_skill() | Knowledge -> Skill promotion |
| AgentMemoryClient | approved_skills() | Agent skill access |
| AgentMemoryClient | (new) register_skill() | Agent skill registration |
| Governance Gate | evaluate_skill() | Governance compliance |
| IndependentReviewGate | validate() | Independent review |
| Human Sovereignty Gate | (external) | Human approval |

## Retention Governance

All skill records follow NAOP retention policies:
- ak_skills: CANONICAL (permanent)
- ak_skill_dependencies: OPERATIONAL (365 days)
- ak_skill_ownership: CANONICAL (permanent)
- ak_skill_lifecycle: CANONICAL (permanent)
- ak_skill_validations: OPERATIONAL (365 days)

## Governance Authority

This architecture is established under Janus Directive AK-WP35.5-001 and governed by:
- Repo Governance Decree v1.0
- Memory Law v1.0
- Knowledge Governance Decree v1.0
- Retention Governance Decree v1.0
- NAOP v1.0
