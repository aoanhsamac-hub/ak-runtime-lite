# AK_LEARNING_INTELLIGENCE_ARCHITECTURE.md

**Generated:** 2026-06-07T09:30:21Z
**Directive:** WP35-PREP-01 Phase 1 — Learning Intelligence Architecture
**Status:** Design Complete (No Runtime Activation)

---

## 1. Architecture Overview

The Learning Intelligence Architecture defines how AK transforms approved knowledge
into learned skills, capabilities, and agent evolution through a controlled,
governance-gated pipeline.

```
                    +---------------------+
                    |   Approved National  |
                    |   Knowledge Base     |
                    | 101L / 6DT / 10DS / |
                    |   4S / 3C           |
                    +----------+----------+
                               |
                    +----------v----------+
                    |   LEARNING ENGINE    |
                    | Signal Extraction   |
                    | Pattern Recognition |
                    | Insight Generation  |
                    +----------+----------+
                               |
                    +----------v----------+
                    |  DISCOVERY ENGINE    |
                    | Skill Candidate     |
                    | Detection           |
                    | Cross-Domain        |
                    | Pattern Matching    |
                    +----------+----------+
                               |
                    +----------v----------+
                    |  PROMOTION ENGINE   |
                    | Evidence Evaluation |
                    | Governance Gating   |
                    | Status Promotion    |
                    +----------+----------+
                               |
                    +----------v----------+
                    |  EVOLUTION ENGINE   |
                    | Capability Assembly |
                    | Maturity Tracking   |
                    | Agent Inheritance   |
                    +----------+----------+
                               |
                    +----------v----------+
                    |   AGENT LAYER       |
                    | 7 Agents with       |
                    | Learned Capabilities|
                    +---------------------+
```

## 2. Core Components

### 2.1 Learning Engine

The Learning Engine processes approved knowledge and extracts learning signals.

| Component | Responsibility | Input | Output |
|-----------|---------------|-------|--------|
| Signal Extractor | Identifies learning signals from approved lessons | Approved Lesson | LearningSignal |
| Pattern Recognizer | Detects repeated patterns across lessons | Multiple Signals | PatternRecord |
| Insight Generator | Produces candidate insights for skill formation | PatternRecord | CandidateInsight |
| Dataset Learner | Extracts knowledge from approved datasets | Approved Dataset | DatasetInsight |
| Trace Analyzer | Learns from decision trace outcomes | Approved Trace | DecisionPattern |

### 2.2 Discovery Engine

The Discovery Engine identifies skill and capability candidates from insights.

| Component | Responsibility | Input | Output |
|-----------|---------------|-------|--------|
| Skill Detector | Detects skill-shaped knowledge clusters | CandidateInsight[] | SkillCandidate |
| Capability Detector | Detects multi-skill capability patterns | SkillCandidate[] | CapabilityCandidate |
| Cross-Domain Matcher | Matches patterns across domain boundaries | Multiple Domains | CrossDomainPattern |
| Gap Analyzer | Identifies missing knowledge areas | Registry State | KnowledgeGapReport |

### 2.3 Promotion Engine

The Promotion Engine manages the lifecycle of skill and capability promotion.

| Component | Responsibility |
|-----------|---------------|
| Evidence Evaluator | Scores evidence quality against promotion thresholds |
| Governance Gate | Enforces review gates before promotion |
| Status Manager | Transitions registry status (DRAFT->REVIEWED->APPROVED->ACTIVE) |
| Audit Recorder | Records all promotion decisions for audit trail |

### 2.4 Evolution Engine

The Evolution Engine tracks capability maturity and agent adoption.

| Component | Responsibility |
|-----------|---------------|
| Maturity Tracker | Monitors capability maturity levels (Emerging->Advanced) |
| Agent Inheritor | Assigns capabilities to agents based on role boundaries |
| Retirement Monitor | Detects deprecated or superseded skills/capabilities |
| Evolution Recorder | Maintains evolution history per capability |

### 2.5 Governance Gate

| Component | Responsibility |
|-----------|---------------|
| Policy Enforcer | Verifies constitutional, legal, and regulatory compliance |
| Risk Classifier | Assigns risk level (LOW/MEDIUM/HIGH/SOVEREIGN) |
| Authority Resolver | Routes to correct approval authority |
| Block Detector | Identifies conditions requiring immediate stop |

### 2.6 Audit Layer

| Component | Responsibility |
|-----------|---------------|
| Event Recorder | Logs all learning events with timestamps |
| Trace Linker | Maintains provenance from knowledge->skill->capability |
| Compliance Verifier | Checks every promotion against governance policy |
| Report Generator | Produces learning audit reports |

### 2.7 Registry Layer

| Registry | Purpose |
|----------|---------|
| learning_signal_registry | Raw learning signals extracted from knowledge |
| insight_registry | Processed insights ready for skill discovery |
| skill_candidate_registry | Skill candidates awaiting review |
| approved_skill_registry | Skills that passed governance review |
| capability_candidate_registry | Capability candidates awaiting review |
| approved_capability_registry | Capabilities ready for agent inheritance |
| evolution_registry | Evolution history and maturity tracking |

## 3. Design Principles

1. **Governance-first** — Every learning transition requires review gate passage
2. **Traceability** — Every artifact links to its source knowledge
3. **No autonomous promotion** — All status changes require explicit agent action
4. **Risk-gated** — Higher risk knowledge requires higher approval authority
5. **Auditable** — Every operation produces audit records
6. **Reversible** — Capability revocation and rollback must be supported
7. **Domain-aware** — Learning respects domain boundaries and agent jurisdictions

## 4. Component Interactions

```
ApprovedLesson --> LearningEngine --> CandidateInsight
CandidateInsight --> DiscoveryEngine --> SkillCandidate
SkillCandidate --> PromotionEngine + GovernanceGate --> ApprovedSkill
ApprovedSkill --> EvolutionEngine --> CapabilityCandidate
CapabilityCandidate --> PromotionEngine + GovernanceGate --> ApprovedCapability
ApprovedCapability --> AgentLayer --> AgentInheritance
All layers --> AuditLayer (continuous logging)
All layers --> RegistryLayer (persistence)
```

## 5. Architecture Constraints

- No runtime agent behavior modification without governance approval
- No autonomous learning loop without human (Hung Vuong) oversight
- All learning must be pausable via emergency stop
- Learning cannot exceed predefined budget (tokens, compute, time)
- Cross-domain learning requires Sage review
- Sovereign domain learning requires Hung Vuong approval
