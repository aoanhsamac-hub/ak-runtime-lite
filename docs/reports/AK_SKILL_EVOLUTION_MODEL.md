# AK_SKILL_EVOLUTION_MODEL.md

**Generated:** 2026-06-07T09:30:21Z
**Directive:** WP35-PREP-01 Phase 3 — Skill Evolution Model
**Status:** Design Complete (No Runtime Activation)

---

## 1. Skill Lifecycle

```
                    +-----------+
                    |   DRAFT   |
                    +-----+-----+
                          |
                    +-----v-----+
              +-----+  REVIEWED +------+
              |     +-----+-----+      |
        (Reject)          |      (Needs Evidence)
              |     +-----v-----+      |
              +---->+ APPROVED  +<-----+
                    +-----+-----+
                          |
                    +-----v-----+
                    |  ACTIVE   |
                    +-----+-----+
                          |
                    +-----v-----+
              +-----+DEPRECATED+-----+
              |     +-----------+     |
        (Superseded)           (Retired)
```

## 2. Lifecycle Stages

| Stage | Status | Description | Allowed Transitions |
|-------|--------|-------------|-------------------|
| 1 | DRAFT | Initial candidate discovered from insights | -> REVIEWED |
| 2 | REVIEWED | Passed evidence review and governance gate | -> APPROVED, -> QUARANTINE |
| 3 | APPROVED | Final approval granted | -> ACTIVE, -> DEPRECATED |
| 4 | ACTIVE | Available for capability formation and agent use | -> DEPRECATED |
| 5 | DEPRECATED | Superseded by newer skill or no longer relevant | -> ARCHIVED |
| 6 | QUARANTINE | Blocked due to governance or risk violation | -> REVIEWED, -> DEPRECATED |

## 3. Skill Discovery

### 3.1 Discovery Triggers

- **Pattern threshold met:** >= 3 learning signals from the same domain
- **Cross-domain pattern:** >= 2 signals from different domains converging
- **Manual nomination:** Agent explicitly nominates a skill candidate
- **Scheduled discovery:** Periodic batch discovery (daily/weekly)

### 3.2 Discovery Criteria

| Criterion | Weight | Minimum |
|-----------|--------|---------|
| Source lesson confidence | 30% | >= 65 |
| Evidence outcome quality | 25% | >= 2/5 |
| Pattern repetition count | 20% | >= 2 occurrences |
| Reuse value | 15% | >= 3/5 |
| Domain coverage | 10% | >= 1 domain |

## 4. Skill Validation

### 4.1 Evidence Requirements

| Risk Level | Min Evidence | Min Confidence | Min Sources | Review Authority |
|------------|-------------|----------------|-------------|-----------------|
| LOW | 2/5 | 65 | 2 | Hermes |
| MEDIUM | 3/5 | 70 | 3 | Sage |
| HIGH | 4/5 | 80 | 5 | Hung Vuong |
| SOVEREIGN | 5/5 | 90 | 7 | Hung Vuong + Council |

### 4.2 Validation Process

1. Evidence evaluator scores candidate against criteria
2. Risk classifier determines risk level
3. Governance gate routes to correct reviewer
4. Reviewer approves, rejects, or requests more evidence
5. Audit trail recorded in evolution_registry

## 5. Skill Promotion

### 5.1 Promotion Sequence

```
DRAFT -> mark_reviewed(reviewer) -> REVIEWED
REVIEWED -> approve(reviewer) -> APPROVED
APPROVED -> activate(owner) -> ACTIVE
```

### 5.2 Promotion Constraints

- Skills cannot skip stages (DRAFT must pass through REVIEWED)
- Skills cannot be promoted without approved source lessons
- Skills with SOVEREIGN risk require Council approval
- Promotion creates permanent audit record

## 6. Skill Retirement

| Reason | Action | Authority |
|--------|--------|-----------|
| Superseded by newer skill | Mark as SUPERSEDED, link to replacement | Sage |
| No longer operationally relevant | Mark as DEPRECATED | Sage |
| Evidence of harm or error | Mark as QUARANTINE immediately | Hung Vuong |
| Retention period expired | Move to ARCHIVED | Hermes |

## 7. Skill Supersession

When a newer skill replaces an older one:

1. New skill is created and promoted normally
2. Old skill is marked SUPERSEDED
3. Supersession link is recorded (old -> new)
4. Capabilities using old skill are notified
5. Old skill remains readable but not usable for new capabilities

## 8. Confidence Requirements

| Stage | Minimum Confidence | Calculation |
|-------|------------------|-------------|
| DRAFT creation | 60 | Automated score |
| REVIEWED | 65 | After evidence evaluation |
| APPROVED | 70 | After governance review |
| ACTIVE | 75 | After operational validation |
