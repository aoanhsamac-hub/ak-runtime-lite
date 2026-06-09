# AK Skill Lifecycle Model v1.0

## Overview

The AK Skill Lifecycle Model defines the 10-stage lifecycle for all skills registered in the National Skill Registry, including transition rules, governance gates, and audit requirements.

## Lifecycle Stages

```
PROPOSED --> DISCOVERED --> SANDBOXED --> VALIDATED --> APPROVED --> ACTIVE
  ^            |               |             |             |          |  |
  |            v               v             v             v          v  v
  +------- PROPOSED <---- DISCOVERED <-- SANDBOXED <-- VALIDATED <--+  |
                                                                       |  |
ACTIVE --> SUSPENDED --> ACTIVE                                        |  |
ACTIVE --> DEPRECATED --> RETIRED --> ARCHIVED                        |  |
APPROVED --> SUSPENDED --> DEPRECATED --> RETIRED --> ARCHIVED <------+  |
SUSPENDED --> DEPRECATED --> RETIRED --> ARCHIVED                        |
SUSPENDED --> RETIRED --> ARCHIVED                                       |
DEPRECATED --> ACTIVE (reversal)                                         |
DEPRECATED --> SUSPENDED                                                  |
```

## Stage Definitions

| Stage | Description | Entry Gate | Exit Gate |
|-------|-------------|------------|-----------|
| PROPOSED | Initial state; skill idea identified | Creation | Discovery pipeline |
| DISCOVERED | Skill pattern detected from signals/insights | Auto-detection | Sage review |
| SANDBOXED | Skill isolated for safe testing | Sage approval | Validation engine |
| VALIDATED | All validations passed | Validation engine | Independent review |
| APPROVED | Governance approved, ready for activation | Independent review | Human sovereignty |
| ACTIVE | Operational in production | Human sovereignty | Risk/Sage |
| SUSPENDED | Temporarily halted due to risk/issue | Risk kernel/gate | Remediation review |
| DEPRECATED | Marked for retirement; no new adoptions | Owner/Sage decision | N/A |
| RETIRED | Removed from active use | Auto/Manual | Retention period |
| ARCHIVED | Preserved for audit/reference only | Auto after retention | N/A |

## Transition Rules

| From | To | Gate | Requires |
|------|----|------|----------|
| PROPOSED | DISCOVERED | auto | - |
| DISCOVERED | SANDBOXED | sage_review | Sage approval |
| SANDBOXED | VALIDATED | validation_engine | All validation types pass |
| VALIDATED | APPROVED | independent_review_gate | IndependentReview approval |
| APPROVED | ACTIVE | human_sovereignty_gate | Human operator approval |
| ACTIVE | SUSPENDED | risk_kernel | Risk detection or Sage order |
| SUSPENDED | ACTIVE | remediation_review | Issues resolved |
| ACTIVE | DEPRECATED | owner_or_sage | Owner/Sage decision |
| DEPRECATED | RETIRED | auto | Time/conditions met |
| RETIRED | ARCHIVED | auto | Retention period elapsed |

## Audit Trail

Every transition produces a SkillLifecycleEventRecord with:
- event_id, skill_id, from_stage, to_stage
- triggered_by, reason, evidence
- governance_approval_ref
- timestamp

## Governance Authority

This model is established under Janus Directive AK-WP35.5-001 and governed by:
- Knowledge Governance Decree v1.0
- Retention Governance Decree v1.0
- Execution Law v1.0
- Memory Law v1.0
