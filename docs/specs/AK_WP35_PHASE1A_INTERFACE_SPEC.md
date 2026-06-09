# AK WP3.5 Phase 1A Interface Specification

Date: 2026-06-07
Module: Learning Metrics

## Public Interfaces

### EvidenceRecord (TypedDict)

```python
class EvidenceRecord(TypedDict, total=False):
    evidence_id: str
    context: str
    outcome: str
    success: bool
    confidence: float
    dataset_refs: Sequence[str]
```

Fields:
- `evidence_id`: Unique identifier for evidence
- `context`: Learning context description
- `outcome`: Outcome or conclusion
- `success`: Boolean success indicator
- `confidence`: Confidence score [0.0, 1.0]
- `dataset_refs`: Optional sequence of dataset references

### GovernanceContext (TypedDict)

```python
class GovernanceContext(TypedDict, total=False):
    issue_id: str
    actor: str
    reviewer: str
    risk_level: str
    governance_valid: bool
    source: str
```

Required fields for `MetricsCalculator.calculate()`:
- `governance_valid`: Must be `True`
- `issue_id`: Non-empty string
- `reviewer`: Non-empty string

### EvidenceProvider (Protocol)

```python
class EvidenceProvider(Protocol):
    def evidence_records(self) -> Sequence[EvidenceRecord]:
        """Return already-governed evidence records without backend access."""
```

## Core Classes

### MetricsCalculatorConfig (dataclass)

| Field | Type | Default | Purpose |
|---|---|---|---|
| minimum_evidence | int | 3 | Minimum evidence threshold |
| precision | int | 4 | Rounding precision for scores |

### LearningMetrics (dataclass, frozen)

| Field | Type | Purpose |
|---|---|---|
| confidence_score | float | Composite learning score |
| success_rate | float | Success ratio |
| recurrence_count | int | Total evidence record count |
| evidence_count | int | Unique evidence count |
| context_diversity | float | Context variation ratio |
| outcome_stability | float | Most common outcome ratio |
| dataset_support | float | Dataset reference ratio |
| blocked | bool | Advisory blocked flag |
| reason | str | Status reason |
| metadata | dict | Calculation metadata |

### Methods

#### MetricsCalculator.calculate(evidence, governance) -> LearningMetrics

- **evidence**: `Sequence[EvidenceRecord]` or `EvidenceProvider`
- **governance**: `GovernanceContext` (validated)
- Returns: `LearningMetrics` with computed scores
- Raises: `LearningMetricsValidationError` on invalid input

#### MetricsCalculator.blocked_result(reason) -> LearningMetrics

- **reason**: Status reason string
- Returns: `LearningMetrics` with blocked=True, all scores=0.0

## Validation Layer

### MetricsValidationLayer.validate_governance(context)

Requires:
- Non-empty `context` dict
- `governance_valid` must be `True`
- Non-empty `issue_id`
- Non-empty `reviewer`

### MetricsValidationLayer.validate_records(records)

Requires:
- Non-empty sequence
- Each record has: `evidence_id`, `context`, `outcome`, `success`, `confidence`
- `confidence` in [0, 1]
- `success` is boolean
- Text fields non-empty after trim

## Confidence Score Formula

```
score = success_rate * 0.25
      + evidence_strength * 0.20
      + context_diversity * 0.15
      + outcome_stability * 0.15
      + dataset_support * 0.15
      + avg_confidence * 0.10
```

Where:
- `evidence_strength = min(1.0, evidence_count / minimum_evidence)`

## Integration Points

- Consumes: Evidence records from already-governed sources
- Produces: Advisory `LearningMetrics` output
- No database writes
- No autonomous actions