# WP3.5 Review Dossier

## Executive Summary

WP3.5 Learning Intelligence Layer is a governance-controlled planning package for turning AK's existing memory platform into a recommendation-oriented learning system. It does not implement runtime code, create new databases, create new registries, or modify agents, governance, memory, or LanceDB architecture.

WP3.5 proposes doctrine and future implementation boundaries for:

- Lesson quality evaluation.
- Skill discovery from evidence.
- Capability evolution from approved skills.
- Cross-agent learning through Hermes distillation.
- Learning metrics.
- Behavior improvement recommendations.
- Promotion governance.

## Objectives

- Prepare Sage and Hung Vuong review materials before implementation begins.
- Define implementation scope without code.
- Identify governance, risk, agent, memory, learning, and promotion impacts.
- Confirm that future learning remains recommendation-only.
- Preserve fail-closed governance and no autonomous production behavior change.

## Expected Benefits

- Better decision quality through reviewed lessons and capabilities.
- Safer cross-agent knowledge reuse.
- Clear scoring for lesson value and danger.
- Evidence-based skill discovery.
- Governed capability growth.
- Auditable recommendations and promotion decisions.

## Governance Impact

WP3.5 increases the importance of Governance Gate, Sage review, audit logging, promotion criteria, and rollback workflow. It must not reduce or bypass existing governance controls.

## Risk Impact

Primary risks:

- False learning from weak evidence.
- Overgeneralized lessons.
- Unsafe recommendations for protected surfaces.
- Cross-agent leakage of unreviewed knowledge.
- Skill or capability inflation.

Risk controls:

- Deterministic scoring.
- Hermes distillation.
- Sage risk review.
- Quarantine for unsafe records.
- Promotion gates.
- Recommendation-only output.

## Agent Impact

Agents may benefit from approved recommendations. Agents must not self-promote lessons, skills, or capabilities. Agents must not self-modify role boundaries or production behavior.

## Memory Impact

WP3.5 uses existing AK memory interfaces only. No new backend or registry is proposed. Agents continue to access memory through `MemoryInterface` or `AgentMemoryClient` only.

## Learning Impact

WP3.5 defines the transition:

```text
Experience -> Lesson -> Skill -> Capability -> Recommendation -> Better Decision
```

Learning output is advisory and requires governance review before promotion.

## Promotion Impact

Promotion becomes more structured:

- Lessons: Draft, Reviewed, Approved.
- Skills: Draft, Reviewed, Approved, Active.
- Capabilities: Draft, Reviewed, Approved, Active.

No promotion grants new authority or changes production behavior.

## Approval Requirements

- Sage review: doctrine, scoring, risk controls, promotion gates.
- Hung Vuong approval: promotion governance principle and any sovereign/high-risk activation.
- Janus coordination: cross-agent rollout sequencing.
- Hermes review: distillation and evidence quality.

## Open Questions

- What minimum score should Sage require for first non-production prototype?
- Should cross-agent recommendations start with one pilot domain?
- What audit schema should future recommendation records use?
- How should stale or contradicted capabilities be retired?
- Which domains require Hung Vuong approval by default?

## Review Checklist

- Doctrine complete.
- Architecture complete.
- Roadmap complete.
- Implementation specification complete.
- Data model specification complete.
- Governance impact assessed.
- Sage checklist complete.
- Hung Vuong approval package complete.
- Implementation remains not started.
