# Alkasik Kingdom Cross-Agent Learning Model

## Purpose

This doctrine defines how learning moves from one agent to the kingdom without violating role boundaries or governance.

Target flow:

```text
Agent learns
Hermes distills
Approved Knowledge
Other agents benefit
```

## Sharing Rules

- Agents may create draft lesson candidates through `AgentMemoryClient` or `MemoryInterface`.
- Hermes distills cross-agent patterns from approved lessons and reviewed decision traces.
- Other agents may use only approved or active lessons, skills, and capabilities.
- Sharing is recommendation-only and cannot modify production behavior.

## Isolation Rules

- Agent-private draft lessons remain owned by the originating agent until review.
- Security, credential, incident, governance, and protected-module records remain isolated until Sage or Yet Kieu review.
- Agent role boundary data is not self-editable.
- No agent receives another agent's unreviewed lessons as operating guidance.

## Quarantine Rules

Quarantine is required when records contain:

- Secret, credential, `.env`, API key, or password material.
- Direct execution, MT5, trading, deployment, broker, or live-mode recommendations.
- Governance bypass or role-boundary bypass.
- Unsupported capability claims.
- Contradictory evidence with unresolved risk.

Quarantined records cannot produce skill or capability candidates.

## Ownership Rules

- Originating agent owns the draft lesson.
- Hermes owns distillation quality.
- Sage owns risk review.
- Domain reviewer owns domain applicability.
- Hung Vuong owns constitutional or sovereign approval.

## Review Requirements

Review path:

```text
Draft Lesson
Hermes Distillation
Sage Risk Review
Domain Reviewer Confirmation
Approved Knowledge
Cross-Agent Recommendation
```

Cross-agent learning is blocked if:

- Ownership is missing.
- Evidence is insufficient.
- Risk classification is missing.
- Required reviewer is absent.
- Governance Gate rejects the record.

## Allowed Outcomes

Allowed:

- Better recommendations.
- Better routing suggestions.
- Better risk warnings.
- Better review checklists.
- Better lesson reuse.

Forbidden:

- Autonomous production behavior changes.
- Self-expanded authority.
- Direct LanceDB backend access by agents.
- Direct execution, trading, MT5, or broker action.
