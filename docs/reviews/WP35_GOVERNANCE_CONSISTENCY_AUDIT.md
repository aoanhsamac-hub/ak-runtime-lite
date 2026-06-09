# WP3.5 Governance Consistency Audit

Status: READY FOR SAGE ROUND 2 REVIEW
Actor: Lang Lieu
Scope: WP3.5 Learning Intelligence doctrine and governance consistency

## Audit Scope

Reviewed documents found:

- `docs/architecture/AK_LEARNING_INTELLIGENCE_ARCHITECTURE.md`
- `docs/design/AK_PROMOTION_GOVERNANCE_MODEL.md`
- `docs/design/AK_LEARNING_METRICS_MODEL.md`
- `docs/design/AK_BEHAVIOR_IMPROVEMENT_MODEL.md`
- `docs/design/AK_CAPABILITY_EVOLUTION_MODEL.md`
- `docs/reviews/AK_AUTONOMOUS_PROPOSAL_POLICY.md`

Referenced scope documents not found:

- `AK_CAPABILITY_LIFECYCLE_MODEL.md`
- `AK_LESSON_DEDUPLICATION_MODEL.md`
- `AK_SKILL_TAXONOMY_MODEL.md`
- `AK_CROSS_AGENT_SHARING_POLICY.md`

Missing documents are treated as governance gaps, not assumed approvals.

## Findings

### Capability Governance

Finding: existing capability doctrine is directionally consistent.

Evidence:

- Capability creation requires at least 3 approved or active skills, at least 5 reviewed decision traces, and no unresolved high-risk contradiction.
- Capability promotion requires reviewed evidence, classified risk, required approvals, rollback or retirement path, and recommendation-only scope.
- Architecture defines rollback/retirement as a governance control.
- Promotion model states rollback removes active recommendation use without deleting source records.

Consistency result:

- Capability Creation: consistent.
- Capability Promotion: consistent.
- Capability Decay: partially specified through stale knowledge and retirement metrics, but no dedicated lifecycle document exists.
- Capability Retirement: consistent at principle level, incomplete at detailed lifecycle level.

### Lesson Governance

Finding: lesson governance preserves traceability in existing doctrine, but deduplication/merge/compression are not fully specified.

Evidence:

- Architecture requires Decision Trace before Draft Lesson Candidate.
- Promotion model requires source trace, complete evidence, audit trail preservation, and rollback without deleting source records.
- Behavior improvement model requires evidence references and reviewed evidence.

Consistency result:

- Decision Trace: preserved in current doctrine.
- Auditability: preserved in promotion and architecture.
- Lineage: preserved by source trace and evidence references.
- Deduplication, Merge, Compression: governance gap because `AK_LESSON_DEDUPLICATION_MODEL.md` is missing.

### Skill Governance

Finding: skill promotion and confidence controls reduce skill inflation, but taxonomy/normalization/merge governance is incomplete.

Evidence:

- Promotion model requires at least 3 approved lessons before skill review.
- Architecture identifies Skill inflation as a failure mode controlled by evidence threshold and confidence scoring.
- Behavior improvement uses approved or active skills only.

Consistency result:

- Skill Explosion: mitigated by evidence thresholds.
- Skill Fragmentation: not fully controlled because `AK_SKILL_TAXONOMY_MODEL.md` is missing.
- Normalization/Merge/Taxonomy: governance gap pending taxonomy model.

### Cross-Agent Governance

Finding: default-deny is implied but not explicitly codified in a dedicated sharing policy.

Evidence:

- Architecture states agents can search approved memory and use approved recommendations in reports.
- Agent restrictions prohibit approving own lessons, promoting own skills, activating own capabilities, bypassing Sage/Governance Gate, or self-modifying role boundaries.
- Behavior improvement requires reviewed evidence and governance classification.

Consistency result:

- Approved knowledge only: consistent in existing architecture.
- Role Boundary: preserved.
- Least Privilege: preserved in principle.
- Default = DENY: not explicitly codified because `AK_CROSS_AGENT_SHARING_POLICY.md` is missing.

### Autonomous Proposal Governance

Finding: autonomous proposal policy is consistent with WP3.5 recommendation-only doctrine, but remains draft for Hung Vuong decision.

Evidence:

- Policy allows proposal drafts and suggestions only.
- Policy forbids task creation, action execution, governance/runtime/memory/role/risk modification, deploy code, trade, and broker access.
- Constitutional principle states Proposal is not Execution, Recommendation is not Authority, Knowledge is not Permission, Capability is not Power.
- Behavior improvement model states AK recommends, Governance approves, Runtime remains fail-closed.

Consistency result:

- Proposal != Task: consistent.
- Proposal != Execution: consistent.
- No bypass of Governance Gate: consistent in principle.
- No bypass of Approval Engine: consistent in proposal flow.
- No bypass of Audit Engine: requires explicit audit mention in autonomous proposal policy before final approval.

## Conflicts

No direct doctrinal conflict was found among existing documents.

Governance gaps found:

- Missing capability lifecycle doctrine prevents full audit of decay and detailed retirement.
- Missing lesson deduplication doctrine prevents full audit of merge/compression lineage preservation.
- Missing skill taxonomy doctrine prevents full audit of normalization/merge and fragmentation controls.
- Missing cross-agent sharing policy prevents explicit confirmation that Default = DENY is codified.
- Autonomous proposal policy is still `DRAFT FOR HUNG VUONG DECISION` and does not explicitly name Audit Engine in Proposal Flow.

## Resolutions

Required before implementation unlock:

- Create or approve `AK_CAPABILITY_LIFECYCLE_MODEL.md` with decay, retirement, rollback, and dependency confidence recomputation rules.
- Create or approve `AK_LESSON_DEDUPLICATION_MODEL.md` with deduplication, merge, compression, lineage, source trace, and audit preservation rules.
- Create or approve `AK_SKILL_TAXONOMY_MODEL.md` with normalization, merge, canonical naming, anti-fragmentation, and anti-explosion rules.
- Create or approve `AK_CROSS_AGENT_SHARING_POLICY.md` with explicit `Default = DENY` and `APPROVED KNOWLEDGE ONLY` rules.
- Update or ratify `docs/reviews/AK_AUTONOMOUS_PROPOSAL_POLICY.md` to include Audit Engine in the proposal governance path and confirm Hung Vuong decision.

Interim resolution:

- Treat implementation as conditionally approved for planning only.
- Do not start runtime implementation until Sage Round 2 review closes these gaps.

## Remaining Risks

- Capability decay may be inconsistently applied without a lifecycle model.
- Lesson compression may accidentally obscure lineage unless deduplication doctrine is approved.
- Skill taxonomy gaps may cause duplicate or fragmented skill candidates.
- Cross-agent sharing may be interpreted too broadly without explicit default-deny policy.
- Autonomous proposals may be mistaken for issue creation unless the Proposal != Task rule is enforced in future specs.
- Audit Engine involvement must be explicit in any future autonomous proposal flow.

## Sage Review Items

- Confirm that existing architecture and promotion governance are internally consistent.
- Decide whether the four missing scope documents are mandatory blockers or conditional pre-implementation items.
- Review autonomous proposal policy for audit-path completeness.
- Confirm Default = DENY requirement for cross-agent learning.
- Confirm whether capability lifecycle must include decay score thresholds before implementation.
- Confirm lineage requirements for lesson deduplication, merge, and compression.
- Confirm canonical taxonomy requirements for skill normalization.

## Hung Vuong Decision Items

- Ratify or reject `docs/reviews/AK_AUTONOMOUS_PROPOSAL_POLICY.md`.
- Decide whether autonomous proposals are allowed only as proposal drafts and suggestions.
- Confirm that Capability remains recommendation power only, not authority.
- Confirm that implementation cannot unlock until Sage Round 2 closes missing doctrine gaps.

## Final Recommendation

```text
IMPLEMENTATION APPROVED WITH CONDITIONS
```

Conditions:

- Sage Round 2 review must approve or require creation of the four missing scope documents.
- Hung Vuong must decide the autonomous proposal policy.
- Audit Engine must be explicitly included in any future autonomous proposal governance flow.
- No runtime implementation begins until these conditions are closed.

## Target State

```text
WP3.5
READY FOR SAGE ROUND 2 REVIEW
```
