# AK_LEARNING_INTELLIGENCE_DESIGN_PACKAGE.md

**Generated:** 2026-06-07T09:30:21Z
**Directive:** WP35-PREP-01 Phase 9 — Final Design Package
**Status:** Design Complete (No Runtime Activation)

---

## 1. Architecture Summary

The Learning Intelligence Architecture defines a controlled, governance-gated pipeline
from approved knowledge to agent capabilities. Seven core components work together:
Learning Engine, Discovery Engine, Promotion Engine, Evolution Engine, Governance Gate,
Audit Layer, and Registry Layer.

## 2. Pipeline Summary

```
Approved Knowledge -> Learning Signal -> Candidate Insight -> Skill Candidate
    -> Review Gate -> Approved Skill -> Active Skill -> Capability Candidate
    -> Review Gate -> Approved Capability -> Agent Inheritance
```

10 stages, 5 review gates, 4 possible outcomes per gate (APPROVED, REJECTED, NEEDS_EVIDENCE, QUARANTINE).

## 3. Skill Evolution Summary

6 lifecycle stages (DRAFT -> REVIEWED -> APPROVED -> ACTIVE -> DEPRECATED -> ARCHIVED).
Skills require minimum confidence and evidence depending on risk level.
Supersession supported with explicit linking.

## 4. Capability Evolution Summary

5 maturity levels (EMERGING -> DEVELOPING -> ESTABLISHED -> ADVANCED -> SOVEREIGN).
Capabilities require minimum 2 active skills. Maturity progresses automatically based on
operational metrics and agent adoption.

## 5. Agent Learning Summary

| Agent | Domain | Max Skills | Max Capabilities | Prohibited Domains |
|-------|--------|-----------|-----------------|-------------------|
| Janus | Orchestration | 5 | 3 | Trading, Risk |
| Sage | Risk, Governance | 3 | 2 | Trading |
| Hermes | Memory, Quality | 4 | 3 | Trading, Risk |
| Iris | Trading, Market | 6 | 4 | Governance |
| Helen | Learning | 3 | 2 | Governance, Risk |
| Lang Lieu | Engineering | 4 | 2 | Trading |
| Yet Kieu | Execution | 3 | 2 | Strategy, Risk |

## 6. Governance Summary

Risk classification: LOW / MEDIUM / HIGH / SOVEREIGN based on domain, confidence,
evidence, cross-domain reach, agent impact, and economic impact.
Approval authority escalates with risk level.

## 7. Registry Summary

7 registries with defined schemas, retention policies, and ownership.
Immutable records with status transitions creating version history.
Permanent retention for approved skills and capabilities.

## 8. Implementation Plan Summary

8 work packages over 16 weeks:
- Foundation (2 weeks)
- Learning Engine (2 weeks)
- Discovery Engine (2 weeks)
- Promotion Engine (2 weeks)
- Evolution Engine (2 weeks)
- Governance Integration (2 weeks)
- Agent Integration (2 weeks)
- Testing & Audit (2 weeks)

## 9. Strategic Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Learning pipeline complexity | Delays Phase 1C | Medium | Phased WP approach |
| Agent adoption resistance | Low capability utilization | Low | Mandatory inheritance for critical capabilities |
| Governance overhead | Slow learning cycles | Medium | Risk-based gate automation |
| Registry scalability | Performance degradation | Low | LanceDB horizontal scaling |
| Emergency stop abuse | Learning stagnation | Low | Clear escalation criteria |

## 10. Open Questions

1. Should learning signals expire, and if so, what is the default TTL?
2. Should agents have differing learning budgets, or a shared pool?
3. How is cross-domain capability inheritance enforced across agent boundaries?
4. Should there be a capability capacity limit per domain, not just per agent?
5. How are capability conflicts resolved when two capabilities overlap?
6. Should there be a learning sandbox for experimental skills before formal promotion?
7. How does the system handle concurrent promotion requests for the same skill/capability?

## 11. Design Package Contents

| Document | Description |
|----------|-------------|
| AK_LEARNING_INTELLIGENCE_ARCHITECTURE.md | Core architecture blueprint |
| AK_LEARNING_PIPELINE_MODEL.md | End-to-end pipeline stages |
| AK_SKILL_EVOLUTION_MODEL.md | Skill lifecycle and promotion |
| AK_CAPABILITY_EVOLUTION_MODEL.md | Capability lifecycle and maturity |
| AK_AGENT_LEARNING_MODEL.md | Per-agent learning permissions |
| AK_LEARNING_GOVERNANCE_MODEL.md | Governance, risk, and audit |
| AK_LEARNING_REGISTRY_MODEL.md | Registry schemas and retention |
| WP35_PHASE1C_IMPLEMENTATION_PLAN.md | Implementation work packages |
| AK_LEARNING_INTELLIGENCE_DESIGN_PACKAGE.md | This consolidated package |
