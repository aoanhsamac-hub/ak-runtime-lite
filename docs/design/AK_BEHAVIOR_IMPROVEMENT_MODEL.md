# Alkasik Kingdom Behavior Improvement Model

## Purpose

This doctrine defines how AK turns decision traces into recommendations without autonomous production behavior changes.

Core flow:

```text
Decision Trace
Lesson
Skill
Capability
Recommendation
```

## Recommendation Generation

Recommendations are generated from reviewed evidence only.

Inputs:

- Decision traces with reasoning, evidence, outcome.
- Approved lessons.
- Approved or active skills.
- Approved or active capabilities.
- Current task context.
- Governance classification.

Output:

- A bounded recommendation.
- Confidence score.
- Evidence references.
- Required reviewers.
- Risk classification.
- Explicit statement that recommendation is not autonomous execution.

## Ranking Model

Recommendations are ranked deterministically:

```text
evidence_match = 0..5
capability_confidence = 0..5
impact = 0..5
risk_inverse = 5 - risk_score
recency = 0..5
cross_agent_reuse = 0..5

recommendation_rank = round(
  evidence_match * 0.25 +
  capability_confidence * 0.20 +
  impact * 0.20 +
  risk_inverse * 0.15 +
  recency * 0.10 +
  cross_agent_reuse * 0.10,
  2
)
```

Recommendations with high risk can be ranked but must be review-required or blocked.

## Confidence Measurement

Confidence is separate from rank.

```text
confidence = round(
  evidence_quality * 0.35 +
  pattern_consistency * 0.25 +
  reviewed_outcome_strength * 0.25 +
  reviewer_agreement * 0.15,
  2
)
```

Minimum confidence for recommendation display:

```text
confidence >= 3.0
```

Minimum confidence for governance review queue:

```text
confidence >= 3.5
```

## Governance Review

Governance classifies every recommendation:

- Low-risk recommendation: may be shown as advisory.
- Moderate/high-risk recommendation: Sage review required.
- Protected module recommendation: Sage review required.
- Constitutional/state corpus/risk kernel recommendation: Hung Vuong approval required after Sage review.

## Forbidden Behavior

Recommendations must never:

- Modify role boundaries.
- Modify production behavior.
- Enable execution, trading, MT5, deployment, or broker calls.
- Change governance policy without review.
- Promote a lesson, skill, or capability automatically.
- Bypass Sage, Janus, Yet Kieu, or Hung Vuong approval gates.

## Safe Behavior Improvement

Safe improvement means:

- Better task framing.
- Better risk warnings.
- Better review checklists.
- Better routing suggestions.
- Better evidence retrieval.
- Better failure avoidance.

Final principle:

```text
AK recommends. Governance approves. Runtime remains fail-closed.
```
