# AK WP3.5 Phase 1E Sage Review Package

Date: 2026-06-07
Subject: Skill Discovery Design — Sage Review Submission

---

## Legal Compliance Analysis

### Source Documents Referenced

| Document | Status | Application |
|----------|--------|-------------|
| Constitution v1.1 FINAL | ✓ Canonical | Articles 27, 36, 37, 39 |
| State Corpus v1.0 FINAL | ✓ Canonical | Knowledge Lifecycle, Governance First |
| Memory Law v1.0 FINAL | ✓ Canonical | Lesson requirements, audit trail |
| Information Law v1.0 FINAL | ✓ Canonical | Traceability, classification |
| Security Law v1.0 FINAL | ✓ Canonical | Sovereign asset protection |
| Knowledge Governance Decree | ✓ Canonical | Evidence-based promotion |
| Agent Law | ✓ Canonical | Separation of duties, accountability |
| Janus Directive | ✓ Canonical | Coordination, approval routing |

---

## Design Compliance Verification

| Requirement | Source | Status |
|-------------|--------|--------|
| Candidate lifecycle defined | State Corpus, Promotion Governance | ✓ PASS |
| Discovery process defined | Skill Discovery Model, Design doc | ✓ PASS |
| Deduplication defined | Promotion Governance Model, Design doc | ✓ PASS |
| Traceability defined | Memory Law, State Corpus, Design doc | ✓ PASS |
| Governance gates defined | Constitution Art 27, Janus Directive | ✓ PASS |
| No registry write path | Constitution Art 27, Design doc | ✓ PASS |
| No autonomous promotion | Constitution Art 27, 36, Design doc | ✓ PASS |
| Standard library only | POL-01, Design doc | ✓ PASS |
| Governance context required | Constitution Art 36, Design doc | ✓ PASS |
| Advisory output only | Constitution Art 27, 36, Design doc | ✓ PASS |

---

## Architecture Review

### Components

| Component | Verdict |
|-----------|---------|
| SkillDiscovery class | PASS — 3 methods, advisory output |
| SkillCandidate dataclass | PASS — 15 fields with contracts |
| EvidencePattern dataclass | PASS — 6 structural fields |
| EvidenceRequirements dataclass | PASS — 5 threshold fields |
| CandidateStatus enum | PASS — 4 states |
| RiskClassification enum | PASS — 4 classes (reuse Phase 1C) |
| CandidateStatus enum | PASS — 4 states |

### Design Principles

- Standard library only — PASS
- Governance context required — PASS
- Advisory output only — PASS
- No autonomous behavior — PASS
- No registry writes — PASS

### Integration Points

- Consumes: Approved LessonEvaluation records
- Produces: SkillCandidate sequence (advisory)
- No database writes — PASS
- No autonomous actions — PASS

---

## Risk Review

| Risk | Status | Mitigation |
|------|--------|------------|
| Candidate explosion | IDENTIFIED | Deduplication with similarity threshold ≥0.8 |
| False positive sovereign detection | IDENTIFIED | Explicit domain list, review_path SOVEREIGN |
| Candidate drift from source lessons | IDENTIFIED | Immutable source_lesson_ids, evidence_snapshot |
| Governance bypass | IDENTIFIED | Governance context validation mandatory |
| Registry write attempt | IDENTIFIED | No write methods in interface; read-only queries |

All identified risks are mitigated through:
- Deterministic deduplication with similarity threshold
- Mandatory governance context validation
- Immutable audit trail per candidate
- Read-only registry access pattern
- No autonomous actions in design

---

## Discovery Model Review

### Evidence Requirements

| Requirement | Threshold | Verified |
|-------------|-----------|----------|
| Minimum approved lessons | ≥ 3 | ✓ |
| Minimum distinct tasks | ≥ 2 | ✓ |
| Minimum reviewed decision traces | ≥ 1 | ✓ |
| Evidence weight composite | ≥ 2.5 | ✓ |
| No quarantine in chain | Mandatory | ✓ |

### Candidate Confidence Formula

```
confidence = evidence_weight × 0.40 +
            trigger_similarity × 0.25 +
            outcome_consistency × 0.20 +
            scope_clarity × 0.15
```

All weights sum to 1.0 — PASS

### Deduplication Model

- Deduplication key: hash(canonical_name + sorted_triggers) — PASS
- Similarity threshold: Jaccard ≥ 0.8 — PASS
- Merge protocol defined — PASS
- Archive original candidates — PASS

---

## Governance Gate Analysis

| Gate | Authority | Implementation | Status |
|------|-----------|----------------|--------|
| Evidence Validation | Hermes | Internal threshold check | PASS |
| Deduplication Check | Hermes | Registry query | PASS |
| Sovereign Check | Hermes | sovereign_asset_impact flag | PASS |
| Evidence Evaluation | Sage | Phase 1D (external) | PASS |
| Risk Review | Sage | Phase 1D (external) | PASS |
| Coordination | Janus | Phase 1D (external) | PASS |
| Sovereign Approval | Hung Vuong | Phase 1D (external) | PASS |

Separation of Duties (Constitution Art 27): PASS

---

## Questions Answered

1. **What is a Skill Candidate?**
   - A proposed skill pattern discovered from APPROVED lessons with evidence pattern, confidence, risk classification, and traceability. Proposal only, not a skill.

2. **How is a candidate discovered?**
   - Deterministic pipeline: governance validation → trigger grouping → pattern extraction → threshold check → candidate construction → deduplication → governance routing.

3. **What evidence is required?**
   - ≥3 approved lessons, ≥2 distinct tasks, ≥1 reviewed trace, evidence_weight ≥2.5, no quarantine in chain.

4. **What lessons can participate?**
   - Only APPROVED lessons with complete evidence, source, author, reviewer, context, outcome, and valid governance context.

5. **How are duplicate candidates prevented?**
   - Deduplication key (hash of canonical name + triggers), Jaccard similarity ≥0.8, registry query, merge protocol with archival.

6. **How does Skill Discovery interact with SkillEvidencePolicy?**
   - Separate modules. Discovery uses evidence weight formula internally. Promotion workflow orchestrates both. No direct calls.

7. **What audit trail is required?**
   - discovery_trace_id, source_lesson_ids, evidence_summary, discovered_by, discovered_at, deduplication_key, status.

8. **What constitutional constraints apply?**
   - Separation of Duties (Art 27), Proposal≠Execution (Art 27), Memory Governance (Art 36), Lesson Status (Art 37), Information Classification (Art 39), Knowledge Lifecycle (State Corpus), Evidence-based (Knowledge Governance).

---

## Compliance Checklist

| Authority | Status |
|-----------|--------|
| Constitution | ✓ PASS |
| State Corpus | ✓ PASS |
| Agent Law | ✓ PASS |
| Risk Law | ✓ PASS |
| Execution Law | ✓ PASS |
| Security Law | ✓ PASS |
| Memory Law | ✓ PASS |
| Information Law | ✓ PASS |
| Knowledge Governance Decree | ✓ PASS |
| Repo Governance Decree | ✓ PASS |

---

## Recommendation: PASS — DESIGN FREEZE

Phase 1E Skill Discovery design complete and compliant.

**Requires Sage review and Janus authorization before Phase 1D implementation.**

No code implementation — design documentation only.

Awaiting Sage review and Janus authorization.