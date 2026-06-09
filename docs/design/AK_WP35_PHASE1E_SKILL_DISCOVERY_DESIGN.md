# AK WP3.5 Phase 1E Skill Discovery Design

Date: 2026-06-07
Module: Skill Discovery
Status: DESIGN FREEZE

---

## Legal Analysis

### Question 1: What is a Skill Candidate?

A Skill Candidate is a proposed skill pattern discovered from Approved Lessons. It is NOT a skill. It is a structured proposal containing:

- Discovered pattern from repeated lesson evidence
- Confidence score based on evidence diversity and consistency
- Risk classification per SkillEvidencePolicy model
- Traceability to source lessons
- Governance path identifier (NORMAL/SOVEREIGN)

Per Constitution: "Capability ≠ Authority" and "Proposal ≠ Execution" — a candidate is a proposal only.

### Question 2: How is a candidate discovered?

Discovery follows a deterministic pipeline:

1. **Input Filter**: Accept only APPROVED lessons with complete evidence
2. **Pattern Mining**: Group lessons by trigger similarity, context overlap, reasoning alignment
3. **Pattern Validation**: Verify minimum lessons (≥3), distinct tasks (≥2), evidence weight (≥2.5)
4. **Candidate Construction**: Build SkillCandidate with canonical name, pattern, confidence
5. **Deduplication**: Compare against existing candidates via deduplication_key
5. **Audit Trail**: Record discovery_trace_id, source lessons, evidence snapshot
6. **Governance Routing**: Assign review_path (NORMAL/SOVEREIGN) based on sovereign_asset_impact

Discovery is advisory only — no registry writes, no autonomous actions.

### Question 3: What evidence is required?

Per SkillEvidencePolicy contract and Promotion Governance Model:

| Requirement | Threshold | Source |
|-------------|-----------|--------|
| Minimum approved lessons | ≥ 3 | STD-05, Memory Law |
| Minimum distinct tasks | ≥ 2 | Skill Discovery Model |
| Minimum reviewed decision traces | ≥ 1 | Skill Discovery Model |
| Evidence weight composite | ≥ 2.5 | SkillEvidencePolicy |
| No quarantine in evidence chain | Mandatory | State Corpus |

Each lesson must have: source, author, reviewer, status=APPROVED, evidence[], context, outcome.

### Question 4: What lessons can participate?

Only lessons meeting ALL criteria:
- Status = APPROVED (validated by SkillEvidenceValidationLayer)
- Complete evidence array with confidence, success, dataset_refs
- Source, author, reviewer, context, outcome populated
- No quarantine or rejected status in evidence chain
- Governance context valid (issue_id, reviewer, governance_valid=true)

### Question 5: How are duplicate candidates prevented?

Deduplication uses a multi-layer approach:

1. **Deduplication Key**: Canonical name + trigger conditions hash
2. **Similarity Threshold**: Jaccard similarity ≥ 0.8 on trigger sets triggers merge
3. **Registry Check**: Query existing candidates and active skills before emission
4. **Merge Protocol**: If duplicate detected, merge evidence, update confidence, status=MERGED
5. **Audit Trail**: Record original candidates, merge decision, merged evidence

Per Promotion Governance: "Skill merge is allowed when candidates share same domain, task pattern, compatible triggers, compatible evidence, same risk class."

### Question 6: How does Skill Discovery interact with SkillEvidencePolicy?

SkillDiscovery and SkillEvidencePolicy are separate but complementary:

| Aspect | SkillDiscovery | SkillEvidencePolicy |
|--------|----------------|---------------------|
| **Role** | Propose candidates from lessons | Evaluate evidence against thresholds |
| **Input** | Approved lessons | Approved lessons or candidate evidence |
| **Output** | SkillCandidate (proposal) | SkillEvidenceResult (evaluation) |
| **Registry Write** | No | No (advisory only) |
| **Promotion Decision** | No | No (governance gates decide) |

SkillDiscovery uses SkillEvidencePolicy's evidence weight formula and thresholds internally for candidate confidence calculation, but does not call SkillEvidencePolicy directly. The promotion workflow orchestrates both.

### Question 7: What audit trail is required?

Every SkillCandidate must include:

| Field | Purpose |
|-------|---------|
| discovery_trace_id | Unique UUID for this discovery event |
| source_lesson_ids | IDs of all contributing lessons |
| evidence_summary | Snapshot of evidence metrics at discovery |
| discovered_by | Agent identifier (Hermes) |
| discovered_at | ISO timestamp |
| deduplication_key | Key used for duplicate detection |
| status | DISCOVERED/VALIDATED/REJECTED/MERGED |

Per State Corpus: "No deletion of source records. Archive before modification."

### Question 8: What constitutional constraints apply?

| Constraint | Application |
|------------|-------------|
| Constitution Art 27 — Separation of Duties | Discovery ≠ Evaluation ≠ Promotion; Hermes discovers, Sage evaluates, Janus coordinates, Hung Vuong approves sovereign |
| Constitution Art 27 — Proposal ≠ Execution | SkillCandidate is proposal only; no registry write |
| Constitution Art 36 — Memory Governance | Governance context required; no autonomous modifications |
| Constitution Art 37 — Lesson Status | Only APPROVED lessons eligible |
| Constitution Art 39 — Information Classification | Candidates classified by evidence confidence (I0-I9) |
| State Corpus — Knowledge Lifecycle | Candidate lifecycle: DISCOVERED → VALIDATED → (promotion) → Skill |
| Knowledge Governance Decree | Evidence-based; no autonomous promotion |

---

## Candidate Discovery Model

### Discovery Pipeline

```
Approved Lessons (APPROVED only)
        ↓
[Governance Validation]
        ↓
[Group by Trigger Similarity]
        ↓
[Pattern Extraction]
   - Trigger conditions
   - Reasoning path
   - Outcome consistency
   - Scope boundaries
        ↓
[Evidence Threshold Check]
   - lessons ≥ 3
   - distinct_tasks ≥ 2
   - evidence_weight ≥ 2.5
        ↓
[Candidate Construction]
   - Canonical name
   - EvidencePattern
   - Confidence score
   - Risk classification
        ↓
[Deduplication]
   - Registry query
   - Similarity check (≥0.8)
   - Merge or emit new
        ↓
[Governance Routing]
   - review_path: NORMAL/SOVEREIGN
   - authority_basis assignment
        ↓
SkillCandidate (advisory output)
```

### Pattern Extraction Algorithm

1. **Trigger Extraction**: Extract trigger conditions from lesson.context and lesson.outcome
2. **Reasoning Alignment**: Compare evidence.confidence and reasoning patterns across lessons
3. **Outcome Clustering**: Group by outcome consistency (success/fail patterns)
4. **Scope Inference**: Identify applicable agents, tasks, contexts from lesson metadata
5. **Canonical Naming**: Generate skill name from domain + task pattern + trigger

### Confidence Calculation

```
candidate_confidence = round(
    evidence_weight * 0.40 +
    trigger_similarity * 0.25 +
    outcome_consistency * 0.20 +
    scope_clarity * 0.15,
    4
)
```

Where:
- `evidence_weight` = from SkillEvidencePolicy formula
- `trigger_similarity` = Jaccard similarity of trigger sets across lessons
- `outcome_consistency` = fraction of lessons with same outcome pattern
- `scope_clarity` = 1.0 if scope boundaries clearly defined, 0.5 otherwise

---

## Candidate Deduplication

### Deduplication Key

```
deduplication_key = hash(canonical_name + sorted(trigger_conditions))
```

### Merge Criteria

Two candidates merge if ALL true:
- Same domain
- Jaccard(trigger_set_A, trigger_set_B) ≥ 0.8
- Compatible risk classification
- No contradictory evidence

### Merge Protocol

1. Combine source lessons (union, no duplicates)
2. Recalculate confidence with merged evidence
3. Update candidate status = MERGED
4. Archive original candidates
4. Emit single merged candidate

---

## Candidate Traceability

### Traceability Chain

```
SkillCandidate
    ├── discovery_trace_id (UUID)
    ├── source_lesson_ids [LESSON-001, LESSON-002, ...]
    │   └── Each lesson traces to:
    │       ├── source (agent/system)
    │       ├── author, reviewer
    │       ├── evidence[] → dataset_refs
    │       └── validation_result
    ├── evidence_snapshot (metrics at discovery)
    ├── discovered_by (agent)
    ├── discovered_at (timestamp)
    └── authority_basis (legal reference)
```

### Audit Requirements

- Immutable discovery trace
- No candidate deletion (archive only)
- Full lineage to source lessons
- Governance context preserved

---

## Registry Interaction Model

### Read-Only Access

SkillDiscovery MAY:
- Query existing candidates for deduplication
- Query active skills for scope conflict check
- Read promotion governance thresholds

SkillDiscovery MUST NOT:
- Write to skill_registry.yaml
- Write to audit_log.jsonl (handled by caller)
- Modify any registry directly

### Caller Responsibility

The promotion workflow (Phase 1D+) is responsible for:
- Calling SkillDiscovery.discover()
- Passing candidates to SkillEvidencePolicy.evaluate()
- Routing through governance gates
- Registry updates after approval

---

## Governance Gates

### Discovery Gates

| Gate | Authority | Trigger |
|------|-----------|---------|
| Evidence Validation | Hermes (discovery) | Internal threshold check |
| Deduplication Check | Hermes | Registry query |
| Sovereign Check | Hermes | sovereign_asset_impact flag |

### Promotion Gates (Post-Discovery)

| Gate | Authority | Candidate Requirement |
|------|-----------|----------------------|
| Evidence Evaluation | Sage | SkillEvidencePolicy pass |
| Risk Review | Sage | Risk classification |
| Coordination | Janus | Cross-agent review |
| Sovereign Approval | Hung Vuong | SOVEREIGN candidates only |

---

## Risk Classification

Skill Candidates inherit risk classification from SkillEvidencePolicy:

| Risk Level | Discovery Criteria |
|------------|-------------------|
| LOW | No sovereign assets, evidence_weight 2.5-3.5, lessons 3+ |
| MEDIUM | No sovereign assets, evidence_weight 3.5-4.0, lessons 3+ |
| HIGH | No sovereign assets, evidence_weight ≥4.0, lessons 5+ |
| SOVEREIGN | Any sovereign asset reference (constitution, risk_kernel, security_law, execution_law, state_corpus, governance) |

### Risk-Based Discovery Constraints

| Risk Level | Additional Discovery Requirements |
|------------|-----------------------------------|
| SOVEREIGN | Immediate flag, review_path=SOVEREIGN, no emission without sovereign_check |
| HIGH | Minimum 5 lessons, Janus coordination flag |
| MEDIUM | Standard deduplication, Janus coordination |
| LOW | Standard deduplication |

---

## Failure Modes

| Failure Mode | Detection | Response |
|--------------|-----------|----------|
| Insufficient lessons | lessons < 3 | Return empty sequence, log reason |
| Evidence weight < 2.5 | _check_evidence_met false | Return empty sequence, log gaps |
| No distinct tasks | distinct_tasks < 2 | Return empty sequence |
| Governance invalid | validation error | Raise SkillDiscoveryError |
| Duplicate detected | dedup_key exists | Merge or suppress |
| Sovereign without check | sovereign_asset_impact true | Force SOVEREIGN path, block emission |
| Registry unavailable | Read error | Return partial results, flag degradation |

---

## Design Constraints

### Non-Functional Requirements

- Standard library only (no external dependencies)
- No LanceDB/FAISS/SQLite/Chroma imports
- Governance context required for all operations
- Advisory output only — no autonomous actions
- No registry writes
- No direct SkillEvidencePolicy invocation
- Archive before modification

### Implementation Boundaries

```
SkillDiscovery (this module)
    ├── Reads: Approved lessons, existing candidates, active skills
    ├── Computes: Patterns, confidence, deduplication
    ├── Emits: SkillCandidate sequence (advisory)
    └── Does NOT: Write registry, call SkillEvidencePolicy, execute promotion
```

---

## Design Freeze Status

**Status: DESIGN FREEZE — AWAITING SAGE REVIEW AND JANUS AUTHORIZATION**

No implementation until authorized. All contracts frozen.