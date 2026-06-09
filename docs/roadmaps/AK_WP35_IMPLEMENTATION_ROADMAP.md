# Alkasik Kingdom WP3.5 Implementation Roadmap

## Phase 1: Doctrine Approval

Goal: Approve learning intelligence doctrine before code.

Deliverables:

- Lesson Quality Model.
- Skill Discovery Model.
- Capability Evolution Model.
- Cross-Agent Learning Model.
- Learning Metrics Model.
- Behavior Improvement Model.
- Promotion Governance Model.

Acceptance criteria:

- Sage review complete.
- Hung Vuong approval for promotion governance principles.
- No implementation begins before doctrine approval.

## Phase 2: Non-Production Prototype

Goal: Build read-only recommendation prototype using existing memory interfaces.

Allowed:

- Recommendation scoring prototype.
- Offline metrics calculation.
- Draft skill/capability candidate detection.
- Audit trail for recommendations.

Forbidden:

- Production behavior modification.
- New memory backend.
- Direct LanceDB access by agents.
- Execution, trading, MT5, Telegram, dashboard activation.

Acceptance criteria:

- Recommendations are generated from approved records only.
- All outputs are advisory.
- Governance review queue receives promotion candidates.

## Phase 3: Governed Activation

Goal: Allow approved recommendations to improve agent reports and routing suggestions.

Allowed:

- Better prompts for review checklists.
- Better risk warnings.
- Better evidence retrieval.
- Better cross-agent knowledge reuse.

Forbidden:

- Autonomous production behavior changes.
- Self-modifying role boundaries.
- Direct execution.

Acceptance criteria:

- Promotion gates enforced.
- Rollback workflow tested.
- Sage validates protected-domain controls.
- Hung Vuong approves sovereign/highest-risk activation.

## Dependencies

- WP1 Governance Engine.
- WP2 Agent Runtime Framework.
- WP3 Memory Platform and MemoryInterface.
- Hermes distillation role.
- Sage risk review.
- Audit append-only policy.

## Risks

- False pattern discovery.
- Skill inflation from weak evidence.
- Capability overclaim.
- Unsafe cross-agent learning leakage.
- Reviewer bottleneck.
- Stale knowledge reuse.

## Overall Acceptance Criteria

- Doctrine approved.
- Architecture approved.
- Prototype remains recommendation-only.
- No new memory backend.
- No production behavior self-modification.
- Governance Gate controls promotion.
- Audit records exist for promotion decisions.
