# AK WP3.5 Phase 1E Interface Specification

Date: 2026-06-07
Module: Skill Discovery
Status: DESIGN FREEZE

## Purpose

This specification defines the interface for the Skill Discovery module, which discovers Skill Candidates from Approved Lessons. Skill Discovery proposes candidates but does NOT create skills, write to the registry, or bypass SkillEvidencePolicy.

## Public Interfaces

### SkillDiscovery (Class)

Primary interface for discovering skill candidates from approved lessons.

```python
class SkillDiscovery:
    def discover(
        self,
        approved_lessons: Sequence[LessonEvaluation],
        governance: GovernanceContext,
    ) -> Sequence[SkillCandidate]
    
    def get_deduplication_threshold(self) -> float
    
    def get_candidate_evidence_requirements(self) -> EvidenceRequirements
```

### SkillCandidate (dataclass, frozen)

Represents a proposed skill candidate discovered from approved lessons.

| Field | Type | Purpose |
|-------|------|---------|
| candidate_id | str | Unique identifier for this candidate |
| name | str | Proposed skill name (canonical) |
| description | str | Human-readable description |
| source_lesson_ids | Sequence[str] | IDs of contributing approved lessons |
| evidence_pattern | EvidencePattern | Discovered pattern structure |
| confidence_score | float | Candidate confidence [0.0, 1.0] |
| risk_classification | RiskClassification | LOW/MEDIUM/HIGH/SOVEREIGN |
| deduplication_key | str | Key used for deduplication |
| discovery_trace_id | str | Unique trace ID for this discovery |
| discovered_by | str | Agent that performed discovery |
| discovered_at | str | ISO timestamp of discovery |
| evidence_summary | Mapping[str, object] | Summary of supporting evidence |
| status | CandidateStatus | DISCOVERED / VALIDATED / REJECTED / MERGED |

### EvidencePattern (dataclass, frozen)

Structured representation of the discovered pattern.

| Field | Type | Purpose |
|-------|------|---------|
| trigger_conditions | Sequence[str] | Repeated trigger conditions observed |
| reasoning_path | Sequence[str] | Similar reasoning steps across lessons |
| outcome_pattern | str | Consistent outcome description |
| scope_boundaries | Mapping[str, object] | Applicable agents, tasks, contexts |
| method_summary | str | Reusable method extracted from lessons |
| limitations | Sequence[str] | Known limits and counterexamples |

### EvidenceRequirements (dataclass)

Minimum evidence requirements for candidate discovery.

| Field | Type | Purpose |
|-------|------|---------|
| minimum_lessons | int | Minimum approved lessons (default: 3) |
| minimum_distinct_tasks | int | Minimum distinct task types (default: 2) |
| minimum_evidence_weight | float | Minimum composite evidence weight (default: 2.5) |
| require_sage_review | bool | Whether Sage review required before proposal |
| require_janus_coordination | bool | Whether Janus coordination required |

### CandidateStatus (Enum)

```python
class CandidateStatus(Enum):
    DISCOVERED = "DISCOVERED"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"
    MERGED = "MERGED"
```

### GovernanceContext (TypedDict)

```python
class GovernanceContext(TypedDict, total=False):
    issue_id: str
    actor: str
    reviewer: str
    risk_level: str
    governance_valid: bool
    source: str
    timestamp: str
```

### LessonEvaluation (TypedDict)

```python
class LessonEvaluation(TypedDict, total=False):
    lesson_id: str
    status: str
    quality_score: float
    evidence_count: int
    source: str
    author: str
    reviewer: str
    date: str
    context: str
    outcome: str
    evidence: Sequence[Mapping[str, object]]
```

## Methods

### SkillDiscovery.discover(approved_lessons, governance) -> Sequence[SkillCandidate]

- **approved_lessons**: Sequence of `LessonEvaluation` with status=APPROVED
- **governance**: `GovernanceContext` (validated)
- Returns: Sequence of `SkillCandidate` (may be empty)
- Raises: `SkillDiscoveryError` on invalid input

### SkillDiscovery.get_candidate_evidence_requirements() -> EvidenceRequirements

- Returns: Current evidence requirements for discovery

### SkillDiscovery.blocked_result(reason) -> Sequence[SkillCandidate]

- **reason**: Block reason string
- Returns: Empty sequence with audit metadata in metadata field

## Integration Points

- Consumes: Approved `LessonEvaluation` records from governed sources
- Produces: Advisory `SkillCandidate` sequence
- **Does NOT**: Write to skill registry
- **Does NOT**: Call SkillEvidencePolicy directly (policy used by promotion workflow)
- **Does NOT**: Execute any autonomous actions
- No database writes

## Governance Constraints

- Governance context required before discovery
- Minimum 3 approved lessons from at least 2 distinct tasks
- Evidence weight >= 2.5 per SkillEvidencePolicy thresholds
- No autonomous promotion to skill
- Deduplication required before candidate emission
- All candidates traceable to source lessons
- No direct registry modifications

## Error Handling

```python
class SkillDiscoveryError(ValueError):
    """Raised when skill discovery violates AK governance contracts."""
```