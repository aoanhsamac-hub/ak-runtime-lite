# AK Skill Governance Model v1.0

## Overview

The AK Skill Governance Model defines ownership, access control, approval flows, and escalation paths for all skills in the National Skill Registry.

## Agent Ownership Model

### Access Levels

| Level | Label | Description |
|-------|-------|-------------|
| OWNER | Owner Agent | Full control over skill lifecycle, can approve transitions, modify schema, retire |
| PRIMARY_USER | Primary User | Can use skill in operations, recommend changes, request transitions |
| SECONDARY_USER | Secondary User | Can use skill under supervision of PRIMARY_USER or OWNER |
| FORBIDDEN_USER | Forbidden User | Blocked from all access to the skill |

### Ownership Rules

1. Every skill must have exactly one Owner Agent
2. Owner Agent cannot be listed in forbidden_users
3. PRIMARY_USER and SECONDARY_USER sets must be disjoint from FORBIDDEN_USER
4. Ownership changes require Sage approval
5. Ownership transfer requires both current and new owner consent

## Approval Flows

### Lifecycle Transitions

| Transition | Required Approval | Authority |
|------------|-------------------|-----------|
| PROPOSED -> DISCOVERED | Auto | Discovery Pipeline |
| DISCOVERED -> SANDBOXED | Sage Review | Sage Agent |
| SANDBOXED -> VALIDATED | Validation Engine | SkillValidationEngine |
| VALIDATED -> APPROVED | Independent Review | IndependentReviewGate |
| APPROVED -> ACTIVE | Human Sovereignty | Hung Vuong / Human Operator |
| ACTIVE -> SUSPENDED | Risk Kernel | Sage / Risk System |
| ACTIVE -> DEPRECATED | Owner or Sage | Owner Agent or Sage |
| DEPRECATED -> RETIRED | Auto | Retirement conditions |
| RETIRED -> ARCHIVED | Auto | Retention policy |

### Escalation Path

1. Standard: Auto/Engine -> Sage -> Hermes -> Hung Vuong
2. Sovereign Risk: Any agent -> Hung Vuong (bypass)
3. Conflict: Sage + Hermes disagreement -> Hung Vuong resolves

## Audit Requirements

- Every governance action must produce an audit event
- Audit events are stored in ak_audit_events table
- Minimum audit fields: action, agent, skill_id, timestamp, reason
- Non-repudiation: all actions are traceable to an agent identity

## Governance Authority

This model is established under Janus Directive AK-WP35.5-001 and governed by:
- Agent Law v1.0
- Constitution v1.1
- Security Law v1.0
- Information Law v1.0
