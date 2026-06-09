# LEGAL RELATIONSHIP MAP

Directive: AK-CODEX-WP01
Phase: 7 - Legal Graph Preparation
Date: 2026-06-07

## Authority Chain

```
Hung Vuong (Sovereign)
    ├── Constitution v1.1
    ├── Laws (Agent, Risk, Execution, Security, Memory, Information, Economic)
    ├── Decrees (Repo Governance, Knowledge Governance, Retention)
    └── State Corpus v1.0

Janus (Coordination)
    ├── Governance Engine
    ├── Approval Matrix
    └── Agent Coordination

Sage (Governance/Risk)
    ├── Risk Review
    ├── Constitutional Compliance
    └── Gate Approval

Lang Lieu (Technical)
    ├── Implementation
    ├── Code Review
    └── Legal Normalization (AK-CODEX)
```

## Key Relationships

### Constitution → Laws
- Constitution v1.1 is source of authority for all laws
- Article 27 governs separation of duties (applied to all laws)
- Article 36 governs memory operations
- Article 37 governs lesson status
- Article 39 governs information classification

### Laws → Policies
- Memory Law → Lesson Quality Model, Promotion Governance
- Agent Law → Role definitions, boundaries
- Security Law → Audit requirements

### Policies → Standards
- No Legacy Runtime Policy → WP3.5 Implementation (no runtime changes)
- Cross-Agent Sharing Policy → Lesson Deduplication Model

### Standards → Specifications
- Learning Metrics Model → WP3.5 Data Model Spec
- Skill Taxonomy Model → WP3.5 Implementation Spec

## Cross-References

| Document | Depends On | Implements | Approved By |
|---|---|---|---|
| Lesson Status Enum | Article 37 | WP3.5 Phase 1B | Sage |
| Information Classification | Article 39 | WP3.5 Phase 1B | Sage |
| Learning Metrics | Constitution v1.1 | WP3.5 Phase 1A | Sage |
| Lesson Evaluator | Article 27, 36 | WP3.5 Phase 1B | Sage |

## Knowledge Graph Preparation

All relationships mapped for Hermes ingestion:
- Node types: Constitution, Law, Policy, Standard, Specification, Procedure, Registry
- Edge types: depends_on, implements, approved_by, owned_by, supersedes