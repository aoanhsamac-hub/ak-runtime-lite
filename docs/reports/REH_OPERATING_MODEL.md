# Royal Executive House - Operating Model

**Date:** 2026-06-08
**Status:** OPERATIONAL
**Authority:** Constitution v1.1 FINAL, Janus Charter FINAL

## Command Structure

```
King Hung Vuong (Sovereign Authority)
    ↓
Royal Executive House (REH)
    ↓
Janus (President - Coordinator)
    ↓
Directives
    ↓
Tasks
    ↓
Agents (7 Branches)
    ↓
Reports
    ↓
Executive Archive
```

## Operational Principles

1. **Delegation, Not Decision**: Janus coordinates, does not decide
2. **Review Before Action**: All tasks require governance review
3. **Evidence First**: All actions generate audit trail
4. **Soft Freeze Compliant**: No constitutional changes during audit

## Service Integration

| Service | Function | Registry |
|---------|----------|----------|
| reh_directive_manager | Create/approve directives | KINGDOM_DIRECTIVE_REGISTRY.yaml |
| kingdom_task_manager | Manage tasks | KINGDOM_TASK_REGISTRY.yaml |
| kingdom_assignment_manager | Assign tasks to agents | KINGDOM_ASSIGNMENT_REGISTRY.yaml |
| kingdom_progress_tracker | Track completion | All registries |
| kingdom_report_compiler | Generate reports | KINGDOM_REPORT_REGISTRY.yaml |
| kingdom_escalation_manager | Manage escalations | KINGDOM_ESCALATION_REGISTRY.yaml |

## Authority Enforcement

All services respect agent charters and constitutional boundaries.