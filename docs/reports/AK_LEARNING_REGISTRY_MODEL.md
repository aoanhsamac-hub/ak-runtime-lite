# AK_LEARNING_REGISTRY_MODEL.md

**Generated:** 2026-06-07T09:30:21Z
**Directive:** WP35-PREP-01 Phase 7 — Registry Design
**Status:** Design Complete (No Runtime Activation)

---

## 1. Registry Architecture

```
learning_signal_registry
    |-- Stores raw learning signals from approved knowledge
    |-- Write: Learning Engine
    |-- Read: Discovery Engine
    v
insight_registry
    |-- Stores processed candidate insights
    |-- Write: Learning Engine
    |-- Read: Discovery Engine
    v
skill_candidate_registry
    |-- Stores skill candidates awaiting review
    |-- Write: Discovery Engine
    |-- Read: Promotion Engine, Reviewers
    v
approved_skill_registry
    |-- Stores approved/active skills
    |-- Write: Promotion Engine (after review)
    |-- Read: Evolution Engine, Agents
    v
capability_candidate_registry
    |-- Stores capability candidates awaiting review
    |-- Write: Evolution Engine
    |-- Read: Promotion Engine, Reviewers
    v
approved_capability_registry
    |-- Stores approved capabilities for agent inheritance
    |-- Write: Promotion Engine (after review)
    |-- Read: Agent Layer
    v
evolution_registry
    |-- Stores evolution history and maturity tracking
    |-- Write: Evolution Engine
    |-- Read: Reviewers, Auditors
```

## 2. Registry Schemas

### 2.1 learning_signal_registry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| signal_id | UUID | YES | Unique signal identifier |
| source_type | enum | YES | lesson, dataset, decision_trace |
| source_id | string | YES | ID of source approved record |
| signal_type | enum | YES | pattern, outcome, procedure, method |
| signal_content | text | YES | Extracted signal content |
| confidence | float | YES | 0-100 confidence score |
| domain | string | YES | Knowledge domain |
| extracted_at | datetime | YES | When signal was extracted |
| ttl | datetime | YES | Signal expiration (configurable) |
| status | enum | YES | active, expired, consumed |

### 2.2 insight_registry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| insight_id | UUID | YES | Unique insight identifier |
| signal_ids | UUID[] | YES | Source signal IDs |
| insight_type | enum | YES | skill_pattern, cross_domain, gap |
| title | string | YES | Human-readable title |
| description | text | YES | Detailed insight description |
| confidence | float | YES | 0-100 aggregated confidence |
| domain | string | YES | Primary domain |
| cross_domains | string[] | NO | Related domains |
| pattern_frequency | int | YES | Number of signal occurrences |
| created_at | datetime | YES | When insight was formed |
| status | enum | YES | active, consumed, expired |

### 2.3 skill_candidate_registry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| candidate_id | UUID | YES | Unique candidate ID |
| insight_ids | UUID[] | YES | Source insight IDs |
| title | string | YES | Proposed skill name |
| description | text | YES | Skill description |
| domain | string | YES | Primary domain |
| confidence | float | YES | 0-100 score |
| evidence_score | float | YES | 0-5 evidence quality |
| risk_level | enum | YES | LOW, MEDIUM, HIGH, SOVEREIGN |
| status | enum | YES | DRAFT, REVIEWED, APPROVED, REJECTED |
| owner_agent | string | YES | Agent responsible |
| reviewer_agent | string | YES | Assigned reviewer |
| created_at | datetime | YES | Creation timestamp |
| reviewed_at | datetime | NO | Review timestamp |
| review_notes | text | NO | Reviewer notes |

### 2.4 approved_skill_registry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| skill_id | UUID | YES | Unique skill ID |
| candidate_id | UUID | YES | Source candidate ID |
| title | string | YES | Skill name |
| description | text | YES | Skill description |
| domain | string | YES | Primary domain |
| status | enum | YES | APPROVED, ACTIVE, DEPRECATED |
| confidence | float | YES | Final confidence score |
| approved_by | string | YES | Approving agent |
| approved_at | datetime | YES | Approval timestamp |
| activated_by | string | NO | Activating agent |
| activated_at | datetime | NO | Activation timestamp |
| superseded_by | UUID | NO | Newer skill ID (if superseded) |

### 2.5 capability_candidate_registry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| candidate_id | UUID | YES | Unique candidate ID |
| skill_ids | UUID[] | YES | Source active skill IDs |
| title | string | YES | Proposed capability name |
| description | text | YES | Capability description |
| domains | string[] | YES | All domains covered |
| maturity_target | enum | YES | EMERGING, DEVELOPING, ESTABLISHED, ADVANCED |
| confidence | float | YES | 0-100 score |
| status | enum | YES | DRAFT, REVIEWED, APPROVED, REJECTED |
| created_at | datetime | YES | Creation timestamp |

### 2.6 approved_capability_registry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| capability_id | UUID | YES | Unique capability ID |
| candidate_id | UUID | YES | Source candidate ID |
| title | string | YES | Capability name |
| domains | string[] | YES | Covered domains |
| maturity_level | enum | YES | Current maturity level |
| status | enum | YES | APPROVED, ACTIVE, DEPRECATED |
| approved_by | string | YES | Approving agent |
| approved_at | datetime | YES | Approval timestamp |
| agent_assignments | string[] | NO | Agents with inheritance |

### 2.7 evolution_registry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| evolution_id | UUID | YES | Unique evolution event ID |
| entity_type | enum | YES | skill, capability |
| entity_id | UUID | YES | ID of evolved entity |
| event_type | enum | YES | created, reviewed, approved, activated, deprecated, superseded, maturity_change |
| previous_status | string | NO | Previous status |
| new_status | string | YES | New status |
| previous_maturity | string | NO | Previous maturity (capabilities) |
| new_maturity | string | NO | New maturity (capabilities) |
| actor | string | YES | Agent that triggered evolution |
| reason | text | YES | Reason for evolution |
| timestamp | datetime | YES | When evolution occurred |

## 3. Registry Lifecycle

### 3.1 Data Flow

```
Signal Registry -> Insight Registry -> Skill Candidate Registry
    -> Approved Skill Registry -> Capability Candidate Registry
    -> Approved Capability Registry
All transitions -> Evolution Registry (audit trail)
```

### 3.2 Retention

| Registry | Active Retention | Archive | Purge |
|----------|-----------------|---------|-------|
| learning_signal | 90 days | 1 year | After TTL |
| insight | 180 days | 2 years | After consumption |
| skill_candidate | Until resolved | 5 years | After resolution |
| approved_skill | Permanent | Never | Never |
| capability_candidate | Until resolved | 5 years | After resolution |
| approved_capability | Permanent | Never | Never |
| evolution | Permanent | Never | Never |

## 4. Registry Ownership

| Registry | Write Owner | Read Owner | Governance |
|----------|-------------|------------|------------|
| learning_signal | Helen | All agents | Hermes |
| insight | Helen | Discovery Engine | Hermes |
| skill_candidate | Discovery Engine | Hermes, Sage | Sage |
| approved_skill | Sage, Hung Vuong | All agents | Sage |
| capability_candidate | Evolution Engine | Hermes, Sage | Sage |
| approved_capability | Hung Vuong | All agents | Hung Vuong |
| evolution | All engines | Auditors | Hermes |

## 5. Versioning

All registries support:

- **Immutable records** — Existing records are never modified
- **Status transitions** — New status creates new record version
- **Full history** — Evolution registry maintains complete timeline
- **Point-in-time queries** — Ability to query registry state at any date
