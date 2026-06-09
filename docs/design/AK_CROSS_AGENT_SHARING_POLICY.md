# Alkasik Kingdom Cross-Agent Sharing Policy

**Status:** SUPERSEDED
**Superseded By:** `docs/legal/codex/policies/POL-03_CROSS_AGENT_SHARING_v1.0.md`
**Supersession Date:** 2026-06-07
**Rationale:** Design content promoted to canonical codex policy. This document retained for design traceability.

## Purpose

Define default-deny cross-agent learning sharing and ensure only approved knowledge can move between agents.

## Cross References

- `docs/design/AK_CROSS_AGENT_LEARNING_MODEL.md`
- `docs/design/AK_BEHAVIOR_IMPROVEMENT_MODEL.md`
- `docs/architecture/AK_LEARNING_INTELLIGENCE_ARCHITECTURE.md`
- `agents/role_boundary.py`

## Default Rule

```text
Default = DENY
```

No cross-agent sharing is allowed unless explicitly approved by governance-controlled knowledge status.

## Approved Knowledge Only

Shareable knowledge must be one of:

- Approved Lesson.
- Approved Skill.
- Active Skill.
- Approved Capability.
- Active Capability.
- Approved Recommendation.

Draft, Reviewed-only, Rejected, Retired, Quarantined, or private records are not shareable as operating guidance.

## Ownership

- Originating agent owns draft source.
- Hermes owns distillation quality.
- Sage owns risk review.
- Domain reviewer owns applicability.
- Hung Vuong owns sovereign/highest-risk approval.

## Access Control

Sharing must respect:

- Role boundary.
- Least privilege.
- Protected module rules.
- Agent department scope.
- Governance Gate result.

Agents cannot use shared knowledge to self-expand permission, self-approve, self-promote, modify runtime, or bypass review.

## Auditability

Cross-agent sharing must record:

- Source knowledge id.
- Target agent.
- Sharing reason.
- Reviewer.
- Risk class.
- Approval state.
- Audit event reference.

## Quarantine

Sharing is blocked and record is quarantined when:

- Secret exposure is suspected.
- Credential or `.env` content appears.
- Governance bypass is suggested.
- Direct execution, trading, MT5, deployment, or broker action is suggested.
- Role boundary conflict exists.

## Final Rule

Approved knowledge may advise other agents. It never grants permission or execution power.
