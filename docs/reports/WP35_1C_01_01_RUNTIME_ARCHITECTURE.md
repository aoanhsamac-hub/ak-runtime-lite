# WP35-1C-01-01: Learning Foundation Runtime Architecture

## Overview
The Learning Foundation Runtime implements the activated Learning Intelligence pipeline (Phase 1C of WP35). It transforms approved knowledge into signals, aggregates signals into insights, and creates candidate skills — all with strict governance gates and no autonomous promotion.

## Architecture Diagram
```
Approved Knowledge (JSON)
  ├── lessons_approved.json (101)
  ├── skills_approved.json (4)
  ├── datasets_approved.json (10)
  └── decision_traces_approved.json (6)
         │
         ▼
┌─────────────────────────────────┐
│  LearningSignalEngine           │  5 signal types: PATTERN, ANOMALY,
│  services/learning_signal_engine│  REPEATABILITY, GOVERNANCE, DATASET
└──────────────┬──────────────────┘
               │ 323 signals extracted
               ▼
┌─────────────────────────────────┐
│  InsightEngine                  │  5 insight types: PATTERN, CONSOLIDATION,
│  services/insight_engine.py     │  GAP, TREND, RISK
└──────────────┬──────────────────┘
               │ 6 insights formed
               ▼
┌─────────────────────────────────┐
│  CandidateSkillPipeline         │  status=CANDIDATE
│  services/candidate_skill_pipeline│  approval_status=PENDING_REVIEW
│                                │  activation_status=DISABLED
└──────────────┬──────────────────┘
               │ 6 candidate skills
               ▼
┌─────────────────────────────────┐
│  LearningGovernanceGate         │  7 gates per record
│  services/learning_governance_gate│  traceability, evidence, confidence,
│                                │  ownership, review, risk, no-promotion
└──────────────┬──────────────────┘
               │ 335/335 passed
               ▼
┌─────────────────────────────────┐
│  LearningAuditLayer             │  Full audit trail of all operations
│  services/learning_audit_layer.py│
└─────────────────────────────────┘
```

## Registry Layer
- `memory/learning_registry/learning_signal_registry.py`: LearningSignalRegistry
- `memory/learning_registry/insight_registry.py`: InsightRegistry
- `memory/learning_registry/candidate_skill_registry.py`: CandidateSkillRegistry

## Service Layer
- `services/learning_signal_engine.py`: 5 signal types
- `services/insight_engine.py`: 5 insight types
- `services/candidate_skill_pipeline.py`: Candidate skill creation
- `services/learning_governance_gate.py`: 7 governance gates
- `services/learning_audit_layer.py`: Event recording & audit trail

## Constraints
- No autonomous learning
- No skill/capability promotion
- No agent evolution
- All candidate skills: status=CANDIDATE, approval_status=PENDING_REVIEW, activation_status=DISABLED
- Every record has traceability to source knowledge
- 7 governance gates per record
- Full audit trail
