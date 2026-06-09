# Reviewer Runtime Architecture

**Date:** 2026-06-08

## Architecture Overview

```
Implementation
    ↓
Coding Queue Manager (add_to_queue)
    ↓
Reviewer Runtime (run_review)
    ↓
Build Validation Runtime (validate_implementation)
    ↓
Sandbox Workflow Manager (run_sandbox_workflow)
    ↓
HUMAN APPROVAL REQUIRED
    ↓
Production Deploy (if approved)
```

## Key Components

### Coding Queue Manager
- Manages capability implementation queue
- Status: PROPOSED → QUEUED → APPROVED

### Reviewer Runtime  
- Evaluates implementations
- FORBIDDEN: self_approve, auto_promote, bypass_review
- Always requires human approval

### Build Validation Runtime
- Validates code for forbidden patterns
- Checks test coverage
- Returns validation results

### Sandbox Workflow Manager
- Manages sandbox deployment workflow
- States: SANDBOX_PENDING → VALIDATION → TESTING → REVIEW → RETURNED

## Governance Constraints

- All implementations require human approval
- No autonomous promotion
- Forbidden patterns detected and blocked
- Full audit trail maintained