# Alkasik Kingdom Skill Discovery Model

**Status:** PARTIALLY SUPERSEDED
**Superseded By:** `docs/legal/codex/standards/STD-02_SKILL_TAXONOMY_v1.0.md`
**Supersession Date:** 2026-06-07
**Rationale:** Taxonomy content promoted to codex standard. Discovery-specific content retained as active design reference.

## Purpose

This doctrine defines how AK discovers skills from reviewed lessons. A skill must emerge from evidence. A skill is not manually declared by an agent and is not activated by a single lesson.

## Skill Definition

A skill is a reusable, evidence-backed pattern that improves task performance for a bounded class of decisions.

Skill examples:

- Safer protected-path change planning.
- Better incident triage pattern recognition.
- More reliable budget proposal review.

A skill is not:

- A permission expansion.
- A production execution capability.
- A role boundary change.
- A model prompt preference without measured evidence.

## Evidence Requirement

Minimum evidence for skill discovery:

- At least 3 approved lessons.
- At least 2 distinct tasks or incidents.
- At least 1 reviewed decision trace.
- No unresolved quarantine records in the evidence chain.

High-risk domains require stronger evidence:

- Governance, security, execution, risk kernel, credentials, constitution, and state corpus require at least 5 approved lessons and Sage review.

## Qualifying Patterns

Patterns qualify when they show:

- Repeated trigger conditions.
- Similar reasoning path.
- Consistent positive outcome.
- Clear reusable method.
- Stable scope boundaries.
- No contradiction from reviewed evidence.

## Rejected Patterns

Patterns are rejected when they are:

- Based on coincidence or isolated success.
- Only stylistic preferences.
- Dependent on a secret, credential, or unavailable runtime.
- Bypassing Governance Gate.
- Proposing MT5, trading, live execution, deployment, or direct broker calls.
- Dependent on direct LanceDB access by agents.

## Confidence Calculation

Skill confidence is deterministic:

```text
evidence_strength = min(5, approved_lessons / 2)
trace_strength = min(5, reviewed_decision_traces)
consistency = 0..5
scope_clarity = 0..5
risk_inverse = 5 - risk_score

skill_confidence = round(
  evidence_strength * 0.25 +
  trace_strength * 0.20 +
  consistency * 0.25 +
  scope_clarity * 0.15 +
  risk_inverse * 0.15,
  2
)
```

Minimum discovery threshold:

```text
skill_confidence >= 3.5
```

## Governance Involvement

Hermes proposes skill candidates from approved lessons. Sage validates risk. Domain reviewer validates applicability. Janus coordinates cross-agent review where more than one agent will use the skill.

Skill promotion remains manual and governance-controlled:

```text
Draft -> Reviewed -> Approved -> Active
```

Active means recommended for use. Active does not mean autonomous production behavior modification.
