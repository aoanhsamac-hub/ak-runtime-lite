# Alkasik Kingdom Learning Intelligence Architecture

## System Overview

The AK Learning Intelligence Layer turns memory records into governed recommendations. It does not create new memory backends, production behavior changes, or autonomous execution.

Purpose:

```text
Experience
Lesson
Skill
Capability
Better Decisions
Better Agent Performance
```

Boundary:

```text
Recommendation only
Governance-controlled promotion
No autonomous production modification
```

## Data Flow

```text
Agent Task / Incident / Review
Decision Trace
Draft Lesson Candidate
Hermes Distillation
Sage Risk Review
Approved Lesson
Skill Discovery Candidate
Skill Review
Approved / Active Skill
Capability Candidate
Capability Review
Approved / Active Capability
Recommendation
Governance Review
Agent Report / Better Decision
```

## Promotion Flow

Lesson:

```text
Draft -> Reviewed -> Approved
```

Skill:

```text
Draft -> Reviewed -> Approved -> Active
```

Capability:

```text
Draft -> Reviewed -> Approved -> Active
```

Promotion flow is blocked by missing evidence, secret exposure, governance bypass, unresolved contradiction, or insufficient reviewer authority.

## Governance Flow

Governance controls:

- Risk classification.
- Reviewer assignment.
- Promotion approval.
- Quarantine decisions.
- Rollback/retirement.

Required reviewers:

- Hermes: distillation and evidence quality.
- Sage: risk and governance review.
- Domain reviewer: applicability.
- Hung Vuong: constitutional, sovereign, or highest-risk approval.

Highest Risk Wins applies to all learning promotions.

## LanceDB Integration

LanceDB remains the AK-native memory backend for existing memory storage.

Learning Intelligence uses existing access paths only:

- `MemoryInterface`
- `AgentMemoryClient`
- Existing lesson, skill, capability, and decision trace registries

Forbidden:

- New memory backend.
- SQLite, Chroma, FAISS, or JSON fallback.
- Direct LanceDB backend handle access by agents.
- Direct production behavior modification based on LanceDB search results.

## Agent Integration

Agent responsibilities:

- Create draft lesson candidates from experience.
- Record decision traces.
- Search approved memory.
- Use approved recommendations in reports.

Agent restrictions:

- Cannot approve own lessons.
- Cannot promote own skills.
- Cannot activate own capabilities.
- Cannot bypass Sage or Governance Gate.
- Cannot self-modify role boundary.

Hermes responsibilities:

- Distill lessons.
- Detect evidence patterns.
- Propose skill/capability candidates.
- Maintain cross-agent knowledge quality.

Sage responsibilities:

- Classify risk.
- Reject unsafe learning.
- Require rollback.
- Gate protected learning.

## Failure Modes

| Failure mode | Control |
|---|---|
| Overgeneralized lesson | Minimum evidence threshold and reviewer challenge |
| Unsafe promotion | Governance Gate and Sage review |
| Secret exposure | Quarantine and `SECURITY_FINDING_REDACTED` reporting |
| Autonomous behavior drift | Recommendation-only architecture |
| Direct backend access | AgentMemoryClient-only rule |
| Skill inflation | Evidence threshold and confidence scoring |
| Capability overclaim | Maturity levels and promotion gates |
| Stale knowledge | Retirement and rollback workflow |

## Security Controls

- No secret or credential content in reports.
- Quarantine suspicious records.
- Protected module learning requires Sage review.
- Constitutional learning requires Hung Vuong approval.
- No direct execution, MT5, trading, broker, or deployment action.
- Audit all promotion decisions.

## Scalability Considerations

Learning can scale by separating:

- Evidence collection.
- Hermes distillation.
- Sage risk review.
- Domain review.
- Recommendation retrieval.

Indexes and vector search support retrieval. Promotion remains human/governance controlled even if discovery becomes automated.

## Architecture Conclusion

AK Learning Intelligence improves decision quality by converting reviewed experience into governed recommendations. It preserves fail-closed runtime behavior and keeps production change authority outside the learning layer.
