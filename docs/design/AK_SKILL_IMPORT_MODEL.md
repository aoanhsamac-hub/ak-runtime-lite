# AK Skill Import Model v1.0

## Overview

The AK Skill Import Model defines the pathways for importing skills from external sources into the National Skill Registry. This model supports Hermes Framework skills and OpenCode/OpenHands workforce skills.

## Design Principles

1. **No Activation**: Imported skills enter the registry as PROPOSED and require full lifecycle governance before activation
2. **Source Traceability**: Every imported skill records its origin, author, and source ID
3. **Schema Mapping**: External skill formats are mapped to the AK Skill Schema Standard
4. **Governance Compliance**: Imported skills must pass all validation gates before reaching ACTIVE state
5. **Human Sovereignty**: No external skill may reach ACTIVE without human approval

## Hermes Import Pathway

```
Hermes Skill Manifest
    |
    v
HermesSkillImporter.parse_manifest()
    |
    v
HermesSkillImporter.import_skill()
    |
    v
AKSkillRecord (source=hermes, category=imported, lifecycle_stage=PROPOSED)
    |
    v
Standard Lifecycle Gates (PROPOSED -> DISCOVERED -> SANDBOXED -> ... -> ACTIVE)
```

### Hermes Manifest Mapping

| Hermes Field | AK Field | Notes |
|-------------|----------|-------|
| skill_id | audit_requirements.hermes_id | Preserved for traceability |
| name | name | Direct mapping |
| description | description | Direct mapping |
| version | version | Integer conversion |
| owner | owner_agent | Direct mapping |
| status | lifecycle_stage | Mapped via HERMES_SKILL_STATES map |
| category | category | Always "imported" |
| dependencies | dependencies | Direct mapping |
| risk_level | risk_level | Direct mapping |

## OpenCode / OpenHands Import Pathway

```
Workflow Skill Manifest
    |
    v
OpenCodeSkillImporter.parse_manifest()
    |
    v
OpenCodeSkillImporter.import_skill()
    |
    v
AKSkillRecord (source=opencode/openhands, category=imported, lifecycle_stage=PROPOSED)
    |
    v
Standard Lifecycle Gates (max stage: READY_FOR_SANDBOX without human approval)
```

### OpenCode Manifest Mapping

| OpenCode Field | AK Field | Notes |
|---------------|----------|-------|
| skill_id | audit_requirements.source_id | Preserved |
| name | name | Direct mapping |
| description | description | Direct mapping |
| version | version | Integer conversion |
| author | audit_requirements.source_author | Preserved |
| dependencies | dependencies | Direct mapping |
| tools | required_tools | Direct mapping |

## Governance Restrictions

- OpenCode imports: max lifecycle_stage = SANDBOXED without Hung Vuong approval
- Hermes imports: full lifecycle available but all gates apply
- All imported skills: category = "imported", source = origin system
- Import log maintained for audit trail

## Governance Authority

This model is established under Janus Directive AK-WP35.5-001 and governed by:
- Janus Directive
- Agent Law v1.0
- Execution Law v1.0
- Security Law v1.0
- Human Sovereignty Gate (NAOP v1.0)
