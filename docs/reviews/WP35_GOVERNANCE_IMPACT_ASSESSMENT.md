# WP3.5 Governance Impact Assessment

## Governance

WP3.5 strengthens governance by formalizing learning promotion gates. It must not weaken existing Governance Gate controls.

Risks:

- Learning recommendations could be mistaken for approvals.
- Capability labels could imply authority expansion.

Safeguards:

- Recommendation-only language.
- Promotion states require review.
- Highest Risk Wins.

## Approval Engine

Impact: future promotion decisions will require approval routing by risk level.

Risks:

- Missing approver for cross-agent or protected-domain learning.
- Inconsistent approval matrix interpretation.

Safeguards:

- Use existing approval matrix.
- Sage review for protected/risk domains.
- Hung Vuong approval for sovereign/highest-risk domains.

## Issue Registry

Impact: implementation and promotion actions may need issue tracking.

Risks:

- Learning promotions without issue trace.
- Rejection/rollback not linked to issue history.

Safeguards:

- Promotion candidates require issue_id when non-trivial.
- Audit records reference issue_id.

## Audit Engine

Impact: audit becomes mandatory for recommendations, promotion, rejection, and rollback.

Risks:

- Missing audit event.
- Ambiguous recommendation outcome.

Safeguards:

- Append-only audit.
- Record actor, action, target, result, issue_id.

## Protected Modules

Impact: learning related to constitution, state corpus, governance, risk kernel, execution, security, or credentials must be treated as high risk.

Risks:

- Recommendation accidentally targets protected path.
- Protected learning reused by unauthorized agent.

Safeguards:

- Protected-domain recommendations require Sage review.
- Constitutional/risk-kernel records require Hung Vuong approval.

## Role Boundaries

Impact: recommendations may improve agent decision support but cannot change role boundaries.

Risks:

- Agent uses learning to self-expand authority.
- Cross-agent recommendation violates target role.

Safeguards:

- Role boundary validation remains mandatory.
- No self-approval or self-promotion.

## Memory Platform

Impact: WP3.5 uses existing memory records and interfaces only.

Risks:

- Direct backend access.
- New unapproved storage pattern.

Safeguards:

- MemoryInterface and AgentMemoryClient only.
- No new databases, registries, or backends.

## Agent Runtime

Impact: agent reports may include approved recommendations in future implementation.

Risks:

- Recommendation treated as executable instruction.
- Dry-run boundary weakened.

Safeguards:

- No direct execution path.
- Runtime remains fail-closed.
- Recommendations require governance review.

## Overall Risk Register

- False pattern discovery.
- Skill inflation.
- Capability overclaim.
- Cross-agent leakage.
- Stale recommendation reuse.
- Reviewer bottleneck.

## Overall Safeguards

- Deterministic scoring.
- Evidence thresholds.
- Hermes distillation.
- Sage risk review.
- Hung Vuong approval where required.
- Audit append-only.
- Quarantine and rollback workflow.
