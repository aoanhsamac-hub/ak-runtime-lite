# AK WP3.5 Phase 1B Interface Specification

Date: 2026-06-07
Module: Lesson Evaluator

## Public Interfaces

### LessonStatus (Enum)

```python
class LessonStatus(Enum):
    DRAFT = "DRAFT"
    REVIEWED = "REVIEWED"
    APPROVED = "APPROVED"
    DEPRECATED = "DEPRECATED"
    QUARANTINE = "QUARANTINE"
```

### LessonEvaluation (dataclass, frozen)

| Field | Type | Purpose |
|---|---|---|
| lesson_id | str | Unique lesson identifier |
| status | LessonStatus | Lesson lifecycle status (DRAFT, REVIEWED, APPROVED, DEPRECATED, QUARANTINE) |
| quality_score | float | Average evidence confidence |
| evidence_count | int | Number of evidence records |
| blocked | bool | Advisory blocked flag |
| reason | str | Status reason |
| source | str | Source reference |
| author | str | Author agent name |
| reviewer | str | Reviewer name |
| date | str | Review timestamp |
| validation_result | str | Validation result |
| version | str | Lesson version |
| information_classification | InformationClassification | I0-I9 classification |
| metadata | dict | Additional metadata |

### InformationClassification (Enum)

```python
class InformationClassification(Enum):
    I0_OFFICIAL_VERIFIED = "I0_OFFICIAL_VERIFIED"
    I1_PROBABLE = "I1_PROBABLE"
    I2_HYPOTHESIS = "I2_HYPOTHESIS"
    I3_THEORY = "I3_THEORY"
    I4_SCENARIO = "I4_SCENARIO"
    I5_SPECULATIVE = "I5_SPECULATIVE"
    I6_FICTION = "I6_FICTION"
    I7_LEGEND = "I7_LEGEND"
    I8_RUMOR = "I8_RUMOR"
    I9_REJECTED = "I9_REJECTED"
```

### Methods

#### LessonEvaluator.evaluate(lesson, governance) -> LessonEvaluation

- **lesson**: `Mapping[str, object]` with lesson data
- **governance**: `GovernanceContext` (validated)
- Returns: `LessonEvaluation` with computed values
- Raises: `LessonEvaluationError` on invalid input

#### LessonEvaluator.block_result(lesson_id, reason) -> LessonEvaluation

- **lesson_id**: Lesson identifier
- **reason**: Block reason string
- Returns: `LessonEvaluation` with blocked=True, status=QUARANTINE

## Validation Layer

### LessonValidationLayer.validate_governance(context)

Requires:
- Non-empty `context` dict
- `governance_valid` must be `True`
- Non-empty `issue_id`
- Non-empty `reviewer`

### LessonValidationLayer.validate_lesson(lesson)

Requires:
- `lesson_id`, `context`, `outcome`, `status` present
- Non-empty `lesson_id`

### LessonValidationLayer.validate_status_transition(from_status, to_status)

Enforces valid status transitions:
- DRAFT → DRAFT, REVIEWED, QUARANTINE
- REVIEWED → APPROVED, DRAFT, QUARANTINE
- APPROVED → DEPRECATED, QUARANTINE
- DEPRECATED → (blocked)
- QUARANTINE → DRAFT, REVIEWED

## Integration Points

- Consumes: Lesson records from already-governed sources
- Produces: Advisory `LessonEvaluation` output
- No database writes
- No autonomous actions