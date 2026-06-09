# AK WP3.5 Phase 1C Evidence Policy Design

Date: 2026-06-07
Module: Skill Evidence Policy

## Legal Analysis

### Question 1: When can Approved Lessons become a Skill?

**Constitutional Basis**: Article 37 (Lesson Status) and Article 36 (Memory Governance)

**Answer**: Approved Lessons may become Skill candidates only when:

1. **Status Requirement**: All contributing lessons have `status = APPROVED` (not DRAFT or REVIEWED)
2. **Pattern Recognition**: Hermes identifies repeated trigger conditions across approved lessons
3. **Evidence Threshold**: Minimum evidence requirements are satisfied per risk classification
4. **Governance Gate**: Appropriate approval level is reached for the risk domain

### Question 2: What evidence threshold is required?

**Evidence-Based Threshold Model**:

Skills require evidence threshold based on eight dimensions:

1. **lesson_count**: Number of approved lessons (normalized 0-5 scale)
2. **source_diversity**: Ratio of distinct sources (identifies multiple origin evidence)
3. **dataset_diversity**: Ratio of distinct datasets referenced (cross-data validation)
4. **context_diversity**: Ratio of varied contexts across lessons (generalizability)
5. **reviewer_diversity**: Ratio of distinct reviewers (independent validation)
6. **outcome_consistency**: Consistency of positive outcomes (reliability)
7. **evidence_weight**: Combined evidence strength score (composite of 5 diversity metrics)
8. **sovereign_asset_impact**: Boolean flag for sovereign asset touch

### Question 3: What metrics are mandatory?

**Mandatory Metrics (STD-04 Learning Metrics Model)**:

1. **Evidence-based Metrics**:
   - `lesson_count`: Number of approved lessons (0-5 normalized)
   - `source_diversity`: Distinct sources ratio
   - `dataset_diversity`: Distinct datasets ratio
   - `context_diversity`: Varied contexts ratio
   - `reviewer_diversity`: Distinct reviewers ratio
   - `outcome_consistency`: Positive outcome consistency ratio
   - `evidence_weight`: Combined evidence strength score
   - `sovereign_asset_impact`: Sovereign asset impact flag

2. **Risk Metrics**:
   - `risk_classification`: LOW/MEDIUM/HIGH/SOVEREIGN
   - `risk_score`: Numerical risk assessment

3. **Confidence Metrics**:
   - `skill_confidence`: Deterministic composite score

### Question 4: What governance gates are required?

**Governance Gate Flow**:

| Risk Level | Required Gates | Approving Bodies |
|---|---|---|
| LOW | Evidence Review → Sage Review | Sage |
| MEDIUM | Evidence Review → Sage Review → Janus | Janus |
| HIGH | Evidence Review → Sage Review → Janus | Janus, Sage |
| SOVEREIGN | Evidence Review → Sage Review → Janus → Hung Vuong | Hung Vuong |

**Gate Requirements**:
1. Hermes confirms evidence pattern
2. Sage confirms risk classification
3. Domain reviewer confirms applicability  
4. Janus coordinates cross-agent review where >1 agent uses skill
5. Hung Vuong approves constitutional domains

### Question 5: What constitutional constraints apply?

**Constitution Article 27 - Separation of Duties**:
- Proposal, review, and approval must be distinct roles
- No single agent may self-promote knowledge to skill
- Cross-agent skills require Janus coordination

**Constitution Article 36 - Memory Governance**:
- Governance context required for all operations
- No autonomous memory modifications
- Preservation of source records

**Constitution Article 39 - Information Classification**:
- Skills must be classified per evidence confidence
- I0-I9 classification applied to skill output
- Classification determines promotion path

**State Corpus Requirements**:
- Every skill must trace to approved lessons
- Source traceability mandatory
- No deletion of source records

**Memory Law Requirements**:
- Evidence required for all lessons
- No unverified errors become official skills
- Archive before modification

## Risk Classification Model

### Risk Classes

| Risk Level | Evidence Threshold | Review Authority | Promotion Requirements |
|---|---|---|---|
| LOW | 3+ lessons, moderate diversity | Sage | Hermes → Sage → Janus → Registry |
| MEDIUM | 3+ lessons, higher diversity | Janus | Hermes → Sage → Janus → Registry |
| HIGH | 5+ lessons, high diversity | Sage + Janus | Hermes → Sage → Janus → Registry |
| SOVEREIGN | 5+ lessons, full diversity | Hung Vuong | Hermes → Sage → Janus → Hung Vuong |

### Evidence Chain Requirements

1. Each lesson must have source trace
2. Each lesson must have validation outcome
3. Lessons must be from governed sources (MemoryInterface)
4. No quarantine or rejected lessons in chain

## Evidence-Based Threshold Model

### Evidence Model Fields

| Field | Purpose |
|---|---|---|
| source_diversity | Ratio of distinct sources (identifies multiple origin evidence) |
| dataset_diversity | Ratio of distinct datasets referenced (cross-data validation) |
| context_diversity | Ratio of varied contexts across lessons (generalizability) |
| reviewer_diversity | Ratio of distinct reviewers (independent validation) |
| outcome_consistency | Consistency of positive outcomes (reliability) |
| evidence_weight | Combined strength score (0.0-5.0) |
| sovereign_asset_impact | True if touches sovereign assets |

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

### Risk-Class Thresholds

| Metric | LOW | MEDIUM | HIGH | SOVEREIGN |
|---|---|---|---|---|
| lesson_count | >= 3 | >= 3 | >= 5 | >= 5 |
| source_diversity | >= 0.3 | >= 0.4 | >= 0.5 | >= 0.6 |
| dataset_diversity | >= 0.3 | >= 0.4 | >= 0.5 | >= 0.6 |
| context_diversity | >= 0.4 | >= 0.5 | >= 0.6 | >= 0.7 |
| reviewer_diversity | >= 0.3 | >= 0.4 | >= 0.5 | >= 0.6 |
| outcome_consistency | >= 0.7 | >= 0.8 | >= 0.85 | >= 0.9 |
| evidence_weight | >= 2.5 | >= 3.0 | >= 3.5 | >= 4.0 |

## Risk Controls

1. **Default Deny**: Skills without proper evidence are blocked
2. **Highest Risk Wins**: Any SOVEREIGN risk overrides lower concerns
3. **No Self-Promotion**: Agents cannot promote their own lessons to skills
4. **No Autonomous Execution**: Skills are recommendations only

## Governance Analysis

### Gate Sequence

#### Normal Skill Promotion Flow

```
Hermes Evidence Review
    ↓
Sage Risk Review
    ↓
Janus Coordination
    ↓
Registry Update (Level 0)
```

#### Sovereign Skill Promotion Flow

```
Hermes Evidence Review
    ↓
Sage Risk Review
    ↓
Janus Coordination
    ↓
Hung Vuong Approval (Level 4)
```

### Governance Roles per Agent Law

| Agent | Role in Skill Promotion |
|---|---|---|
| Hermes | Evidence validation, pattern confirmation |
| Sage | Risk classification, safety assurance |
| Domain Reviewer | Applicability validation |
| Janus | Coordination, approval routing |
| Hung Vuong | Sovereign domain approval |

### Approval Matrix

| Risk Level | Evidence | Risk Review | Coordination | Final Approval |
|---|---|---|---|---|
| LOW | Required | Required | Required | Sage |
| MEDIUM | Required | Required | Required | Janus |
| HIGH | Required | Required | Required | Janus + Sage |
| SOVEREIGN | Required | Required | Required | Hung Vuong |

## Design Constraints

### Non-Functional Requirements

1. **No Database Access**: Uses MemoryInterface abstraction only
2. **No Autonomous Actions**: All outputs advisory
3. **Standard Library Only**: No external dependencies
4. **Governance Context Required**: All operations require valid context

### Interface Contracts

- `SkillEvidencePolicy` depends on: `LessonEvaluation`, `GovernanceContext`
- Outputs: `SkillEvidenceEvaluation` (advisory)
- No production behavior modification

## Phase 1C Design Freeze R2

Status: DESIGN COMPLETE - AWAITING SAGE REVIEW

Next Steps:
1. Sage review per Janus Directive
2. Janus authorization for implementation
3. Phase 1D - Implementation (code only after authorization)