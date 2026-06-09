# AK WP3.5 Phase 1C Interface Specification

Date: 2026-06-07
Module: Skill Evidence Policy

## Purpose

This specification defines the interface for the Skill Evidence Policy module, which governs when Approved Lessons can become Skills and the evidence thresholds required for skill promotion.

## Public Interfaces

### SkillEvidencePolicy (Class)

Primary interface for evaluating skill evidence requirements.

```python
class SkillEvidencePolicy:
    def evaluate(self, approved_lessons: Sequence[LessonEvaluation]) -> SkillEvidenceEvaluation
    def meets_threshold(self, metrics: LearningMetrics) -> bool
    def get_governance_gate(self, risk_class: str) -> GovernanceGateStatus
```

### SkillEvidenceEvaluation (dataclass, frozen)

| Field | Type | Purpose |
|---|---|---|
| skill_candidate_id | str | Unique identifier for skill candidate |
| evidence_met | bool | Whether evidence threshold is satisfied |
| lesson_count | int | Number of approved lessons provided |
| source_diversity | float | Ratio of distinct sources (0.0-1.0) |
| dataset_diversity | float | Ratio of distinct datasets referenced (0.0-1.0) |
| context_diversity | float | Ratio of varied contexts across lessons (0.0-1.0) |
| reviewer_diversity | float | Ratio of distinct reviewers (0.0-1.0) |
| outcome_consistency | float | Consistency of positive outcomes (0.0-1.0) |
| evidence_weight | float | Combined evidence strength score (0.0-5.0) |
| sovereign_asset_impact | bool | True if touches sovereign assets (constitution, risk kernel, etc.) |
| quality_threshold | float | Minimum quality score required (3.0) |
| coverage_gaps | Sequence[str] | List of missing evidence types |
| risk_classification | RiskClassification | LOW, MEDIUM, HIGH, SOVEREIGN |
| governance_gate_status | GovernanceGateStatus | Required approvals for promotion |
| confidence_score | float | Calculated skill confidence (0.0-5.0) |

### RiskClassification (Enum)

```python
class RiskClassification(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    SOVEREIGN = "SOVEREIGN"
```

### GovernanceGateStatus (Enum)

```python
class GovernanceGateStatus(Enum):
    NOT_READY = "NOT_READY"
    EVIDENCE_REVIEW = "EVIDENCE_REVIEW"
    SAGE_RISK_REVIEW = "SAGE_RISK_REVIEW"
    JANUS_COORDINATION = "JANUS_COORDINATION"
    HUNG_VUONG_APPROVAL = "HUNG_VUONG_APPROVAL"
    APPROVED = "APPROVED"
    BLOCKED = "BLOCKED"
```

### EvidenceThreshold (dataclass)

| Field | Type | Purpose |
|---|---|---|
| minimum_lessons | int | Minimum approved lessons required (per risk class) |
| minimum_source_diversity | float | Minimum distinct source ratio (default 0.4) |
| minimum_dataset_diversity | float | Minimum distinct dataset ratio (default 0.3) |
| minimum_context_diversity | float | Minimum context variation ratio (default 0.5) |
| minimum_reviewer_diversity | float | Minimum reviewer variation ratio (default 0.4) |
| minimum_outcome_consistency | float | Minimum outcome consistency ratio (default 0.8) |
| minimum_evidence_weight | float | Minimum evidence weight score (default 3.0) |
| sovereign_asset_check | bool | Check for sovereign asset impact |
| requires_sage_review | bool | Must pass Sage risk review |
| requires_janus_coordination | bool | Requires Janus coordination |
| requires_hung_vuong_approval | bool | Requires Hung Vuong approval |

### Evidence Weight Formula

```text
source_score = min(5, source_diversity * 5)
dataset_score = min(5, dataset_diversity * 5)
context_score = min(5, context_diversity * 5)
reviewer_score = min(5, reviewer_diversity * 5)
outcome_score = min(5, outcome_consistency * 5)

evidence_weight = round(
    source_score * 0.20 +
    dataset_score * 0.20 +
    context_score * 0.20 +
    reviewer_score * 0.20 +
    outcome_score * 0.20,
    2
)
```

## Governance Approval Flow

### Normal Skill Promotion Flow

```
Hermes Evidence Review
    ↓
Sage Risk Review
    ↓
Janus Coordination
    ↓
Registry Update (Level 0)
```

### Sovereign Skill Promotion Flow

```
Hermes Evidence Review
    ↓
Sage Risk Review
    ↓
Janus Coordination
    ↓
Hung Vuong Approval (Level 4)
```

## Methods

### SkillEvidencePolicy.evaluate(approved_lessons, governance) -> SkillEvidenceEvaluation

- **approved_lessons**: Sequence of `LessonEvaluation` with status=APPROVED
- **governance**: `GovernanceContext` (validated)
- Returns: `SkillEvidenceEvaluation` with computed values
- Raises: `SkillEvidencePolicyError` on invalid input

### SkillEvidencePolicy.blocked_result(reason) -> SkillEvidenceEvaluation

- **reason**: Block reason string
- Returns: `SkillEvidenceEvaluation` with evidence_met=False, governance_gate_status=BLOCKED

## Integration Points

- Consumes: Approved `LessonEvaluation` records
- Produces: Advisory `SkillEvidenceEvaluation` output
- No database writes
- No autonomous actions

## Governance Constraints

- Evidence threshold based on diversity metrics per risk classification
- Risk-based approval flow (Normal vs Sovereign skill paths)
- Evidence-based model replaces fixed lesson-count requirements
- No autonomous skill creation without governance approval