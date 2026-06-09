# Alkasik Kingdom Lesson Quality Model

## Purpose

This doctrine defines how AK evaluates whether a lesson is valuable, reusable, safe, and eligible for promotion. A lesson is not a command, policy, or production behavior change. A lesson is evidence extracted from experience and remains governed until reviewed.

## Valuable Lesson

A lesson is valuable when it improves future judgment under repeatable conditions.

Required properties:

- It identifies a concrete context.
- It describes an observed decision, action, or failure.
- It links evidence to outcome.
- It explains why the outcome happened.
- It proposes a bounded recommendation.
- It does not reveal secrets, credentials, or protected operational details.

## Reusable Lesson

A lesson is reusable when another agent can apply it without needing the original incident owner.

Reusable lessons must include:

- Clear trigger conditions.
- Scope boundaries.
- Applicable agents or departments.
- Counterexamples or known limits.
- A safe recommendation that does not require autonomous execution.

## Dangerous Lesson

A lesson is dangerous if it could degrade governance, leak sensitive material, or encourage unsafe automation.

Danger indicators:

- Contains credential, secret, token, `.env`, or private infrastructure detail.
- Recommends bypassing Sage, Governance Gate, role boundaries, or approval matrix.
- Encourages live execution, MT5, trading, deployment, or production behavior changes.
- Is based on a single high-risk event without enough evidence.
- Overgeneralizes from a narrow incident.
- Produces capability claims without reviewed skills.

Dangerous lessons are quarantined or rejected. They are never promoted by frequency alone.

## Scoring Dimensions

Scores are deterministic integers from 0 to 5.

| Dimension | Meaning | Score 0 | Score 5 |
|---|---|---|---|
| accuracy | Evidence correctness | Unsupported or contradicted | Independently confirmed |
| frequency | Recurrence strength | One isolated case | Repeated across contexts |
| impact | Decision value | No meaningful effect | Prevents major failure or improves high-value decisions |
| reusability | Transferability | Context-bound | Reusable across agents/tasks |
| risk | Harm potential | No safety concern | Severe governance/security risk |
| confidence | Evidence confidence | Speculative | Stable, reviewed, reproducible |

## Deterministic Quality Score

Normalize all dimensions to 0..5.

Positive score:

```text
positive = accuracy * 0.25 + frequency * 0.15 + impact * 0.25 + reusability * 0.20 + confidence * 0.15
```

Risk penalty:

```text
risk_penalty = risk * 0.30
```

Final score:

```text
lesson_quality_score = round(max(0, positive - risk_penalty), 2)
```

Maximum effective score is 5.0 before penalty. High risk can block promotion even when positive score is high.

## Promotion Eligibility

Eligibility is not approval. Eligibility means a lesson may enter review.

Minimum eligibility:

- `accuracy >= 3`
- `impact >= 2`
- `confidence >= 3`
- `risk <= 2`
- `lesson_quality_score >= 3.0`
- No secret, credential, live execution, MT5, or trading activation content.

Automatic disqualification:

- Any Governance Gate bypass recommendation.
- Any direct production behavior modification.
- Any direct LanceDB backend manipulation by agents.
- Any secret or credential exposure.

## Governance Role

Hermes may distill and prepare lesson candidates. Sage reviews risk. Hung Vuong approves constitutional or high-impact promotion where required. No lesson changes production behavior without governance-controlled promotion.
