# AK_LEARNING_PIPELINE_MODEL.md

**Generated:** 2026-06-07T09:30:21Z
**Directive:** WP35-PREP-01 Phase 2 — Learning Pipeline Model
**Status:** Design Complete (No Runtime Activation)

---

## 1. Pipeline Overview

The Learning Pipeline transforms approved knowledge into agent capabilities through
controlled stages, each with defined inputs, outputs, triggers, and review gates.

```
Stage 1: SIGNAL EXTRACTION
  Input:  ApprovedLesson / ApprovedDataset / ApprovedTrace
  Process: Extract learning signals, patterns, and insights
  Output: LearningSignal
  Trigger: New approved knowledge in registry
  Gate:   None (automated extraction)

Stage 2: INSIGHT FORMATION
  Input:  LearningSignal[]
  Process: Aggregate signals, detect patterns, form candidate insights
  Output: CandidateInsight
  Trigger: Sufficient signal mass (configurable threshold)
  Gate:   None (automated formation)

Stage 3: SKILL CANDIDATE DISCOVERY
  Input:  CandidateInsight[]
  Process: Match insights to skill patterns, compute confidence
  Output: SkillCandidate (status=DRAFT)
  Trigger: Insight confidence >= minimum threshold
  Gate:   Automated detection

Stage 4: SKILL REVIEW
  Input:  SkillCandidate (status=DRAFT)
  Process: Evidence evaluation, risk classification, governance check
  Output: SkillCandidate (status=REVIEWED or QUARANTINE)
  Trigger: Agent submits for review
  Gate:   Sage (Medium risk) / Hung Vuong (High/Sovereign risk)

Stage 5: SKILL APPROVAL
  Input:  SkillCandidate (status=REVIEWED)
  Process: Final approval by authorized agent
  Output: ApprovedSkill (status=APPROVED)
  Trigger: Review complete with PASS result
  Gate:   Sage / Hung Vuong

Stage 6: SKILL ACTIVATION
  Input:  ApprovedSkill (status=APPROVED)
  Process: Mark skill as available for capability formation
  Output: ActiveSkill (status=ACTIVE)
  Trigger: Owner agent activation
  Gate:   Skill owner agent

Stage 7: CAPABILITY CANDIDATE DISCOVERY
  Input:  ActiveSkill[]
  Process: Detect multi-skill patterns for capability formation
  Output: CapabilityCandidate (status=DRAFT)
  Trigger: Sufficient active skills in related domains
  Gate:   Automated detection

Stage 8: CAPABILITY REVIEW
  Input:  CapabilityCandidate (status=DRAFT)
  Process: Organizational value, strategic impact, sustainability check
  Output: CapabilityCandidate (status=REVIEWED)
  Trigger: Agent submits for review
  Gate:   Sage + Hermes

Stage 9: CAPABILITY APPROVAL
  Input:  CapabilityCandidate (status=REVIEWED)
  Process: Final approval
  Output: ApprovedCapability (status=APPROVED)
  Trigger: Review complete
  Gate:   Hung Vuong

Stage 10: AGENT ADOPTION
  Input:  ApprovedCapability (status=APPROVED)
  Process: Assign capability to eligible agents
  Output: AgentCapabilityInheritance
  Trigger: Capability approved + agent eligible
  Gate:   Agent role boundary enforcement
```

## 2. Pipeline States

```
LearningSignal --> CandidateInsight --> SkillCandidate[DRAFT]
  --> SkillCandidate[REVIEWED] --> ApprovedSkill[APPROVED]
  --> ActiveSkill[ACTIVE] --> CapabilityCandidate[DRAFT]
  --> CapabilityCandidate[REVIEWED] --> ApprovedCapability[APPROVED]
  --> AgentCapabilityInheritance
```

## 3. Review Gates Detail

| Gate | Stage | Reviewer | Criteria | Duration |
|------|-------|----------|----------|----------|
| G1 | Skill Review (Low Risk) | Hermes | Evidence >= 3, Confidence >= 70 | 1 day |
| G2 | Skill Review (Medium Risk) | Sage | Evidence >= 4, Confidence >= 75 | 3 days |
| G3 | Skill Review (High Risk) | Hung Vuong | Full governance review | 7 days |
| G4 | Capability Review | Sage + Hermes | Multi-skill validation | 5 days |
| G5 | Capability Approval | Hung Vuong | Strategic impact assessment | 7 days |

## 4. Failure Modes

| Failure Mode | Symptom | Resolution |
|-------------|---------|------------|
| Stale signal | Insight not generated within TTL | Expire and re-extract |
| Low confidence insight | Confidence < threshold | Increase evidence requirements |
| Review timeout | Candidate in REVIEWED > max days | Escalate to Sage |
| Governance conflict | Policy violation detected | Route to Hung Vuong |
| Registry inconsistency | Missing provenance chain | Manual reconciliation |
| Skill supersession | Newer skill duplicates older | Mark old as SUPERSEDED |

## 5. Pipeline Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Signal extraction latency | < 1 hour | Time from approval to signal |
| Insight formation rate | >= 70% | Insights / signals ratio |
| Skill promotion rate | >= 60% | Approved / candidates ratio |
| Capability promotion rate | >= 50% | Approved / candidates ratio |
| Review cycle time | < 5 days | Time from DRAFT to APPROVED |
| Agent adoption rate | >= 80% | Adopted / approved capabilities |
