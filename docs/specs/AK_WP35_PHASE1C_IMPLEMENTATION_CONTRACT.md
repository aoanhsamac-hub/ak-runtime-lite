# AK WP3.5 Phase 1C Implementation Contract

Date: 2026-06-07
Module: skill_evidence_policy.py
Status: CONTRACT FREEZE

## 1. Interface Contract

### SkillEvidencePolicy Class

```python
class SkillEvidencePolicy:
    def evaluate(
        self,
        approved_lessons: Sequence[LessonEvaluation],
        governance: GovernanceContext
    ) -> SkillEvidenceEvaluation
    
    def meets_threshold(
        self,
        metrics: SkillEvidenceEvaluation
    ) -> bool
    
    def get_governance_gate(
        self,
        risk_class: RiskClassification
    ) -> GovernanceGateStatus
```

### SkillEvidenceEvaluation Contract

| Field | Type | Contract |
|---|---|---|
| skill_candidate_id | str | Non-empty string; unique identifier |
| evidence_met | bool | True if all thresholds satisfied |
| lesson_count | int | Count of APPROVED lessons |
| source_diversity | float | Range: 0.0-1.0; ratio of distinct sources |
| dataset_diversity | float | Range: 0.0-1.0; ratio of distinct datasets |
| context_diversity | float | Range: 0.0-1.0; ratio of varied contexts |
| reviewer_diversity | float | Range: 0.0-1.0; ratio of distinct reviewers |
| outcome_consistency | float | Range: 0.0-1.0; positive outcome ratio |
| evidence_weight | float | Range: 0.0-5.0; composite score |
| sovereign_asset_impact | bool | True if sovereign assets referenced |
| quality_threshold | float | Threshold value (>= 3.0) |
| coverage_gaps | Sequence[str] | List of missing evidence types |
| risk_classification | RiskClassification | LOW/MEDIUM/HIGH/SOVEREIGN |
| governance_gate_status | GovernanceGateStatus | Current gate status |
| confidence_score | float | Range: 0.0-5.0; final confidence |
| promotion_trace_id | str | Unique trace ID for promotion audit |
| source_lessons | Sequence[str] | Lesson IDs that contributed evidence |
| evidence_snapshot | Mapping[str, object] | Snapshot of evidence at evaluation time |
| decision_reason | str | Reason for pass/fail/blocked status |
| evaluated_by | str | Agent that performed evaluation |
| evaluated_at | str | ISO timestamp of evaluation |
| review_path | str | Governance path (NORMAL or SOVEREIGN) |
| authority_basis | str | Legal authority for decision |

### RiskClassification Contract

```python
class RiskClassification(Enum):
    LOW = "LOW"      # Isolated advisory learning
    MEDIUM = "MEDIUM"  # Cross-agent reuse
    HIGH = "HIGH"    # Protected module recommendation
    SOVEREIGN = "SOVEREIGN"  # Constitutional/sovereign domain
```

### GovernanceGateStatus Contract

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

## 2. Evidence Contract

### Input Requirements

- **approved_lessons**: Sequence of LessonEvaluation with status=APPROVED
- **governance**: Valid GovernanceContext with `governance_valid=True`, non-empty `issue_id`, non-empty `reviewer`

### Evidence Validation Rules

| Metric | LOW Threshold | MEDIUM Threshold | HIGH Threshold | SOVEREIGN Threshold |
|---|---|---|---|---|
| lesson_count | >= 3 | >= 3 | >= 5 | >= 5 |
| source_diversity | >= 0.3 | >= 0.4 | >= 0.5 | >= 0.6 |
| dataset_diversity | >= 0.3 | >= 0.4 | >= 0.5 | >= 0.6 |
| context_diversity | >= 0.4 | >= 0.5 | >= 0.6 | >= 0.7 |
| reviewer_diversity | >= 0.3 | >= 0.4 | >= 0.5 | >= 0.6 |
| outcome_consistency | >= 0.7 | >= 0.8 | >= 0.85 | >= 0.9 |
| evidence_weight | >= 2.5 | >= 3.0 | >= 3.5 | >= 4.0 |

### Evidence Weight Formula Contract

```python
def calculate_evidence_weight(
    source_diversity: float,
    dataset_diversity: float,
    context_diversity: float,
    reviewer_diversity: float,
    outcome_consistency: float
) -> float:
    # Returns value in range 0.0-5.0
    # Weighted average as specified in Evidence Policy Design
```

## 3. Risk Contract

### Risk Classification Rules

| Condition | Risk Level |
|---|---|
| No sovereign assets (constitution, risk kernel, governance) | LOW/MEDIUM/HIGH based on diversity |
| Sovereign asset reference or Constitution/Risk Kernel/Security domain | SOVEREIGN |
| Evidence weight < 2.5 | BLOCKED - cannot promote |

### Approval Authority Mapping

| Risk Level | Authority Required |
|---|---|
| LOW | Sage (Level 3) |
| MEDIUM | Janus (Level 1-2) |
| HIGH | Janus + Sage |
| SOVEREIGN | Hung Vuong (Level 4) |

### Sovereign Asset Check

Skills must be marked SOVEREIGN when evidence touches:
- Constitution
- Risk Kernel
- Security Law
- Execution Law
- State Corpus
- Governance domains

## 4. Registry Contract

### Registry Outputs

| Registry | Update Condition | Authority Required |
|---|---|---|
| skill_registry.yaml | After governance approval | Sage for NORMAL, Hung Vuong for SOVEREIGN |
| audit_log.jsonl | On all evaluations | Automatic |
| governance_gate_registry.yaml | On gate status changes | N/A (tracking only) |

### Registry Schema Requirements

No direct registry modifications by skill_evidence_policy.py. All outputs are advisory. Registry updates occur only through governance-controlled promotion workflow.

### Memory Interface Contract

- **Consumes**: Approved LessonEvaluation records (already-governed)
- **Produces**: SkillEvidenceEvaluation (advisory output)
- **No writes**: No direct registry or database writes
- **No execution**: No autonomous actions

## 5. Legal Mapping

### Contract to Authority References

| Contract Element | Legal Authority |
|---|---|---|
| evidence_met | Constitution Article 37 (Lesson Status) |
| source_diversity | Memory Law Article 15-23 |
| dataset_diversity | Memory Law Article 32-34 |
| context_diversity | State Corpus Article 42-43 |
| reviewer_diversity | Constitution Article 27 (Separation of Duties) |
| outcome_consistency | Information Law Article 9-28 |
| evidence_weight | Knowledge Governance Decree |
| sovereign_asset_impact | Security Law Article 21-23 |
| risk_classification | Risk Law |
| governance_gate_status | Agent Law (Janus coordination) |
| promotion_trace_id | State Corpus Article 35-36 (Governance First) |
| source_lessons | Memory Law Article 32-34 (immutable history) |
| evidence_snapshot | Memory Law (audit trail) |
| decision_reason | Agent Law (accountability) |
| evaluated_by | Agent Law (accountability) |
| evaluated_at | Memory Law (audit trail) |
| review_path | Repo Governance Decree (approval flow) |
| authority_basis | Constitution (legal traceability) |

## 6. Non-Functional Requirements

- Standard library only (no external dependencies)
- No LanceDB/FAISS/SQLite/Chroma imports
- Governance context required for all operations
- Advisory output only - no autonomous behavior
- No production behavior modification
- Archive before modification policy applies

## Contract Freeze Status

Status: FROZEN - AWAITING SAGE REVIEW AND JANUS AUTHORIZATION

Next Steps:
1. Sage review of Contract Package
2. Janus authorization for implementation
3. Phase 1D - Code implementation (contract-only after authorization)