# Alkasik Kingdom Capability Lifecycle Model

Status: READY FOR SAGE ROUND 2 REVIEW

## Purpose

Define capability creation, promotion, decay, retirement, rollback, and dependency confidence recomputation without granting runtime authority or production behavior changes.

## Cross References

- `docs/design/AK_CAPABILITY_EVOLUTION_MODEL.md`
- `docs/design/AK_PROMOTION_GOVERNANCE_MODEL.md`
- `docs/architecture/AK_LEARNING_INTELLIGENCE_ARCHITECTURE.md`
- `docs/reviews/AK_AUTONOMOUS_PROPOSAL_POLICY.md`

## Lifecycle States

```text
Observed
Candidate
Reviewed
Approved
Active
Decaying
Retired
Quarantined
```

## Capability Creation

Creation is allowed only when evidence shows an emergent property from approved skills.

Minimum creation conditions:

- At least 3 approved or active skills.
- At least 5 reviewed decision traces.
- Clear scope and limits.
- No unresolved high-risk contradiction.
- Source lessons and skills remain linked.

Creation produces a Candidate only. It does not create authority, runtime behavior, or execution power.

## Capability Promotion

Promotion path:

```text
Candidate
Reviewed
Approved
Active
```

Promotion requirements:

- Hermes validates evidence lineage.
- Sage validates risk classification.
- Domain reviewer validates usefulness.
- Hung Vuong approves constitutional, sovereign, governance, security, risk-kernel, or execution-adjacent capability activation.
- Rollback path exists before Active.

## Capability Decay

Capability decay begins when evidence weakens.

Decay triggers:

- Stale evidence.
- Reduced reuse success rate.
- Contradictory decision traces.
- Retired source skill.
- Increased risk score.
- Better replacement capability exists.

Decay result:

- Capability remains visible for audit.
- Recommendation confidence is reduced.
- Active use requires review.
- Capability may move to Retired or Quarantined.

## Capability Retirement

Retirement removes the capability from active recommendation use.

Retirement requires:

- Retirement reason.
- Reviewer.
- Audit record.
- Dependency impact review.
- Notification to Hermes, Sage, owner agents, and affected agents.

Retirement never deletes source records.

## Dependency Confidence Recalculation

When a lesson, skill, or capability is rejected, retired, or quarantined:

- Recompute dependent skill confidence.
- Recompute dependent capability confidence.
- Mark affected recommendations for review.
- Preserve original lineage.

## Governance Controls

- Highest Risk Wins.
- No self-promotion.
- No self-approval.
- No production behavior modification.
- No direct execution, trading, MT5, deployment, or broker access.

## Final Rule

Capability is recommendation power only. Capability is not authority.
