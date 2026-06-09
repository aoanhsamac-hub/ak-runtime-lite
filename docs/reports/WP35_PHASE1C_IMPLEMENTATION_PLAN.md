# WP35_PHASE1C_IMPLEMENTATION_PLAN.md

**Generated:** 2026-06-07T09:30:21Z
**Directive:** WP35-PREP-01 Phase 8 — Phase 1C Implementation Plan
**Status:** Design Complete (No Runtime Activation)

---

## 1. Overview

This plan defines the implementation of WP3.5 Phase 1C: Learning Intelligence Pipeline.
It covers the build, test, and deployment of the Learning Engine, Discovery Engine,
Promotion Engine, and supporting registries.

## 2. Implementation Order

```
WP 1: Foundation (Week 1-2)
WP 2: Learning Engine (Week 3-4)
WP 3: Discovery Engine (Week 5-6)
WP 4: Promotion Engine (Week 7-8)
WP 5: Evolution Engine (Week 9-10)
WP 6: Governance Integration (Week 11-12)
WP 7: Agent Integration (Week 13-14)
WP 8: Testing & Audit (Week 15-16)
```

## 3. Work Packages

### WP 1: Foundation (Weeks 1-2)

| Task | Description | Dependencies | Review Gate |
|------|-------------|--------------|-------------|
| 1.1 | Create learning registries (7 registries) | Registry design doc | Sage |
| 1.2 | Implement registry adapter for LanceDB | Base adapter | Hermes |
| 1.3 | Create audit layer foundation | Registry adapter | Sage |
| 1.4 | Implement schema validation | Registry adapter | Hermes |
| 1.5 | Write unit tests for registries | 1.1-1.4 | Hermes |
| **Deliverable:** | Working registry system with audit | | |

### WP 2: Learning Engine (Weeks 3-4)

| Task | Description | Dependencies | Review Gate |
|------|-------------|--------------|-------------|
| 2.1 | Implement Signal Extractor | Approved Knowledge Base | Hermes |
| 2.2 | Implement Pattern Recognizer | Signal Extractor | Hermes |
| 2.3 | Implement Insight Generator | Pattern Recognizer | Sage |
| 2.4 | Implement Dataset Learner | Approved Datasets | Hermes |
| 2.5 | Implement Trace Analyzer | Approved Traces | Sage |
| 2.6 | Write learning engine tests | 2.1-2.5 | Hermes |
| **Deliverable:** | Learning Engine processing pipeline | | |

### WP 3: Discovery Engine (Weeks 5-6)

| Task | Description | Dependencies | Review Gate |
|------|-------------|--------------|-------------|
| 3.1 | Implement Skill Detector | Insights | Hermes |
| 3.2 | Implement Capability Detector | Active Skills | Sage |
| 3.3 | Implement Cross-Domain Matcher | Skill Detector | Sage |
| 3.4 | Implement Gap Analyzer | Registry state | Hermes |
| 3.5 | Write discovery engine tests | 3.1-3.4 | Hermes |
| **Deliverable:** | Discovery Engine detecting candidates | | |

### WP 4: Promotion Engine (Weeks 7-8)

| Task | Description | Dependencies | Review Gate |
|------|-------------|--------------|-------------|
| 4.1 | Implement Evidence Evaluator | Evidence model | Sage |
| 4.2 | Implement Governance Gate | Governance model | Sage |
| 4.3 | Implement Status Manager | Registry adapter | Hermes |
| 4.4 | Implement Promotion Workflow | 4.1-4.3 | Sage + Hermes |
| 4.5 | Write promotion engine tests | 4.1-4.4 | Hermes |
| **Deliverable:** | Promotion Engine with governance gates | | |

### WP 5: Evolution Engine (Weeks 9-10)

| Task | Description | Dependencies | Review Gate |
|------|-------------|--------------|-------------|
| 5.1 | Implement Maturity Tracker | Approved Capabilities | Hermes |
| 5.2 | Implement Agent Inheritor | Agent model | Sage |
| 5.3 | Implement Retirement Monitor | Evolution registry | Hermes |
| 5.4 | Implement Evolution Recorder | Audit layer | Sage |
| 5.5 | Write evolution engine tests | 5.1-5.4 | Hermes |
| **Deliverable:** | Evolution Engine with maturity lifecycle | | |

### WP 6: Governance Integration (Weeks 11-12)

| Task | Description | Dependencies | Review Gate |
|------|-------------|--------------|-------------|
| 6.1 | Integrate Risk Classifier | Governance model | Sage |
| 6.2 | Implement Approval Workflows | Promotion Engine | Sage + Hermes |
| 6.3 | Implement Emergency Stop | All engines | Hung Vuong |
| 6.4 | Implement Rollback Process | Registry adapter | Hermes |
| 6.5 | Write governance integration tests | 6.1-6.4 | Sage |
| **Deliverable:** | Fully governed learning pipeline | | |

### WP 7: Agent Integration (Weeks 13-14)

| Task | Description | Dependencies | Review Gate |
|------|-------------|--------------|-------------|
| 7.1 | Implement capability inheritance per agent | Agent model | Sage |
| 7.2 | Implement learning budget enforcement | Budget model | Hermes |
| 7.3 | Implement agent learning permissions | Agent model | Sage |
| 7.4 | Implement agent feedback loop | Capability usage | Hermes |
| 7.5 | Write agent integration tests | 7.1-7.4 | Sage |
| **Deliverable:** | Agent learning integration complete | | |

### WP 8: Testing & Audit (Weeks 15-16)

| Task | Description | Dependencies | Review Gate |
|------|-------------|--------------|-------------|
| 8.1 | End-to-end pipeline integration tests | WP 1-7 | Hermes |
| 8.2 | Security and penetration testing | All WPs | Sage |
| 8.3 | Governance compliance testing | All WPs | Sage |
| 8.4 | Performance benchmarking | All WPs | Hermes |
| 8.5 | Audit report generation | All WPs | Hung Vuong |
| **Deliverable:** | Fully tested learning pipeline | | |

## 4. Dependencies

| Dependency | Required For | Risk if Delayed |
|------------|-------------|-----------------|
| Approved Knowledge Base | WP 2 | Cannot extract signals |
| LanceDB Adapter | WP 1 | Cannot persist registries |
| Governance Module | WP 4, 6 | Cannot gate promotions |
| Agent Runtime | WP 7 | Cannot inherit capabilities |
| Evidence Model | WP 4 | Cannot evaluate promotion readiness |

## 5. Risk Controls

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| LanceDB unavailable | Medium | High | JSON fallback adapter |
| Agent integration complexity | Medium | Medium | Phased agent rollout |
| Governance gate performance | Low | Medium | Async review gates |
| Learning pipeline performance | Medium | Medium | Batch processing |
| Security vulnerability | Low | High | Penetration testing in WP 8 |

## 6. Testing Requirements

| Test Level | Coverage Target | Tooling |
|------------|----------------|---------|
| Unit tests | >= 90% | pytest |
| Integration tests | >= 80% | pytest + fixtures |
| E2E tests | >= 70% | pytest + mock runtime |
| Security tests | 100% of gates | Custom test suite |
| Performance tests | < 100ms per gate | pytest-benchmark |

## 7. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Signal extraction accuracy | >= 85% | Manual review sample |
| Skill detection precision | >= 75% | Confirmed / total candidates |
| Promotion gate accuracy | >= 95% | Correct / total decisions |
| Pipeline throughput | >= 100 signals/hour | Monitoring |
| Review cycle time | <= 5 days | Average from DRAFT to APPROVED |
| Agent adoption rate | >= 80% | Adopted / available capabilities |

## 8. Rollback Procedures

| Scenario | Rollback Action | Authority |
|----------|----------------|-----------|
| Registry corruption | Restore from backup | Hermes |
| Engine failure | Fall back to manual pipeline | Sage |
| Governance bypass | Emergency stop all learning | Hung Vuong |
| Data integrity issue | Restore registries from audit trail | Hermes |
