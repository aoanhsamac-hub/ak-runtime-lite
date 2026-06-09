# Alkasik Kingdom Capability Evolution Model

## Purpose

This doctrine defines how capabilities emerge from skills. A capability is an operationally meaningful cluster of approved skills, not a manually assigned label.

## Skill Versus Capability

A skill is a reusable method for a bounded task pattern.

A capability is a mature, governed collection of skills that allows an agent or department to perform a broader class of work more reliably.

Example:

- Skill: identify protected module change risk.
- Skill: produce rollback-safe implementation plan.
- Skill: route Sage review.
- Capability: governed protected-change planning.

## Capability Evidence Requirement

Minimum capability creation requirements:

- At least 3 approved or active skills.
- At least 2 agents or 1 department showing repeated benefit.
- At least 5 reviewed decision traces.
- Demonstrated improvement in decision quality or reduced failure rate.
- No unresolved high-risk contradiction.

Constitutional, security, governance, and execution-adjacent capabilities require Sage review and Hung Vuong approval before Active state.

## Maturity Levels

```text
M0 Observed
M1 Candidate
M2 Reviewed
M3 Approved
M4 Active
M5 Retired
```

Maturity meaning:

- M0 Observed: pattern suspected but insufficient evidence.
- M1 Candidate: evidence threshold met for review.
- M2 Reviewed: Hermes and domain reviewer confirm evidence.
- M3 Approved: governance approval granted.
- M4 Active: capability can inform recommendations.
- M5 Retired: capability superseded, unsafe, or no longer useful.

## Capability Confidence

```text
skill_base = min(5, approved_skills)
trace_base = min(5, reviewed_decision_traces / 2)
agent_spread = min(5, benefiting_agents)
performance_delta = 0..5
risk_inverse = 5 - risk_score

capability_confidence = round(
  skill_base * 0.20 +
  trace_base * 0.20 +
  agent_spread * 0.15 +
  performance_delta * 0.30 +
  risk_inverse * 0.15,
  2
)
```

Promotion threshold:

```text
capability_confidence >= 3.75
```

## Promotion Allowed

Promotion is allowed only when:

- Evidence is reviewed.
- Risk is classified.
- Required approvals are present.
- Rollback or retirement path exists.
- Capability only changes recommendations, routing suggestions, or review prompts.

Promotion is blocked when it changes production behavior, grants new authority, bypasses role boundaries, or enables direct execution.
