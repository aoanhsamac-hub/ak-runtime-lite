# Directive Lifecycle

**Version:** 1.0
**Authority:** Royal Executive House
**Status:** Operational

## Lifecycle Flow

```
Hung Vuong → REH Intake
    ↓
DIRECTIVE_CREATED (PROPOSED)
    ↓
Janus Review → Tasks Generated
    ↓
DIRECTIVE_APPROVED
    ↓
Tasks Assigned to Agents
    ↓
Task Execution (IN_PROGRESS)
    ↓
Tasks COMPLETE → DIRECTIVE_REVIEW
    ↓
Sage Review
    ↓
DIRECTIVE_CLOSED
    ↓
Archive + Audit
```

## States

| State | Description | Authority |
|-------|-------------|-----------|
| PROPOSED | Submitted for review | Hung Vuong |
| APPROVED | Tasks generated | Janus |
| IN_PROGRESS | Agents executing | Assigned agents |
| BLOCKED | Cannot proceed | System |
| REVIEW | Awaiting final review | Sage |
| CLOSED | Complete and archived | Hung Vuong |

## Audit Requirements

Every state transition must record:
- timestamp
- actor
- previous_state
- new_state
- reason (if applicable)

## Integration Points

- Links to KINGDOM_TASK_REGISTRY.yaml
- Links to KINGDOM_ASSIGNMENT_REGISTRY.yaml
- Generates entries in ak_audit_events table