# AK-WP37 National Evolution & Learning System — Reviewer Loop Audit Report

**Date:** 2026-06-08
**Status:** AUDIT COMPLETE — 60+ source files reviewed, 20+ test files reviewed

## Audit Scope

Capability infrastructure, learning pipeline, evolution systems, agent profiles, automation, governance, maturity tracking, terminal autonomy, Hermes integration, ROI tracking.

## Executive Summary

**No component needs to be built from scratch.** Every WP37 requirement maps to existing infrastructure that can be EXTENDED. Two exceptions: a scheduler module for daily/weekly/monthly automation, and the evolution loop itself (which is currently gated LOCKED).

## 1. Capability Infrastructure — EXTEND

| Registry | What It Has | WP37 Extension |
|----------|-------------|----------------|
| `OfficialCapabilityRegistry` | activation_status, adoption_stage, evolution_status (LOCKED) | Add evolution_cycle, evolution_history[], last_evolved_at |
| `CapabilityEvidenceRegistry` | EvidenceRecord with confidence/metrics/risk | Add usage_evidence type |
| `CapabilityBacklog` | 6 activation states, dependency tracking | Add evolution-triggered state transitions |
| `CapabilityROIRegistry` | record_roi, record_usage, summary | Add evolution_cost, evolution_value tracking |

**All registries are extend-only. No new registries required.**

## 2. Learning Pipeline — EXTEND

| Module | Current | Extension |
|--------|---------|-----------|
| `LearningLoop` (`memory/learning_loop.py`) | Lesson→Skill only | Add Skill→Capability evolution loop |
| `LearningGovernanceGate` (`services/learning_governance_gate.py`) | 20 gates, no_evolution LOCKED | Unlock evolution gate with sandbox constraints |
| `SkillDiscovery` (`learning/skill_discovery.py`) | Group→Weight→Confidence→Risk→Candidate | Add evolution-triggered rediscovery |
| `LessonRegistry` | Draft→Reviewed→Approved→Deprecated | No changes needed |

**No new learning modules required.**

## 3. Agent Profiles — EXTEND

| File | Current | Extension |
|------|---------|-----------|
| `agents/identity.py` | AgentIdentity (role, department, authority) | Add capabilities[], skills[], maturity_level |
| `agents/role_boundary.py` | RoleBoundary (allowed/forbidden actions) | Add autonomy_level (READ_ONLY/SANDBOX_WRITE/BRANCH_WRITE/PROMOTION_CANDIDATE) |
| `agents/runtime_models.py` | ActivationState (LOCKED→OPERATIONAL_APPROVED) | Add CapabilityUsageRecord integration |
| 7 agent classes in `agents/{name}/agent.py` | Per-agent methods | Add standardized profile fields |

**AgentIdentity and RoleBoundary are the extension points. No new identity system.**

## 4. National Automation — CREATE (Scheduler), EXTEND (Pipelines)

**Gap found:** No scheduler/cron/daily/weekly/monthly system exists.

| Component | Action |
|-----------|--------|
| Scheduler module | **CREATE** `services/kingdom_scheduler.py` with DAILY/WEEKLY/MONTHLY cadences |
| Existing pipelines | EXTEND: `run_capability_pipeline.py`, `run_capability_validation_pipeline.py` as scheduled tasks |
| `MissionRuntime` (workflows/mission_runtime.py) | EXTEND: support scheduled mission execution |

## 5. Governed Terminal Autonomy — EXTEND (RoleBoundary)

Current state: autonomy is implicitly encoded as `forbidden_actions` in role_boundary.py and hardcoded `execution_enabled: False`.

| Level | Current | Extension |
|-------|---------|-----------|
| READ_ONLY | Default (observe only) | Formalize in RoleBoundary |
| SANDBOX_WRITE | Exists implicitly | Add explicit sandbox_write permission |
| BRANCH_WRITE | Not supported | Add branch_write permission |
| PROMOTION_CANDIDATE | Exists in pipeline | Add promotion_candidate flag |

**No new autonomy module needed — extend RoleBoundary with autonomy_level.**

## 6. Hermes Integration — EXTEND

| Component | Current | Extension |
|-----------|---------|-----------|
| `HermesAgent.distill_lesson()` | Extracts lessons from evidence | Add evolution-context distillation |
| `HermesAgent.review_evidence_quality()` | Scores I0-I9 | Add evolution-readiness scoring |
| `LearningGovernanceGate.hermes_review_gate` | Present | Add evolution-stage review |
| `HermesSkillImporter` | Imports Hermes skills to AK | No changes needed |

**No autonomous Hermes — AK governance remains authoritative.**

## 7. Capability ROI — EXTEND

`CapabilityROIRegistry` exists at `memory/capability_roi_registry.py` as a thin proxy. Needs:
- Evolution cost tracking (value/cost per evolution cycle)
- Usage→ROI correlation
- Adoption-stage ROI recalculation

## 8. National Maturity Tracking — EXTEND

5 engines already exist at `services/capability_maturity_engine.py`, `services/capability_maturity_reassessment_engine.py`, `services/skill_maturity_engine.py`, etc.

| Engine | Extension |
|--------|-----------|
| `CapabilityMaturityEngine` | Add evolution-cycle-aware scoring (compound maturity over cycles) |
| `CapabilityMaturityReassessmentEngine` | Add evolution-trace support |
| `CapabilityPromotionReadinessEngine` | Add evolution readiness decision path |

**No new maturity engine required.**

## 9. Evolution Engine — CREATE (Core Logic), EXTEND (Registry)

**Gap found:** No evolution engine exists. Evolution is entirely LOCKED by governance gates.

| Component | Action |
|-----------|--------|
| Evolution state machine | **CREATE** `services/capability_evolution_loop.py` |
| Evolution audit events | **EXTEND** audit layer with EVOLVED/MATURITY_PROGRESSED events |
| OfficialCapabilityRegistry evolution_status | EXTEND: LOCKED→UNLOCKED→EVOLVING→EVOLVED |
| LearningLoop | EXTEND: add capability evolution methods |

## 10. Duplication Analysis

| Risk | Check | Result |
|------|-------|--------|
| Duplicate registries | No new registries created | ✅ PASS |
| Duplicate lifecycle systems | All use existing lifecycle | ✅ PASS |
| Duplicate validation systems | All use LearningGovernanceGate | ✅ PASS |
| Duplicate governance systems | All use governance/* | ✅ PASS |
| Overlap with existing files | All changes are EXTEND | ✅ PASS |

## 11. Compliance Checklist

| Law/Decree | Status |
|------------|--------|
| Constitution v1.1 | Compliant — evolution governed, not autonomous |
| State Corpus | Compliant — no law modification |
| Agent Law | Compliant — agent profiles extend existing identity |
| Risk Law | Compliant — sandbox-first, no production modification |
| Execution Law | Compliant — no MT5/execution changes |
| Security Law | Compliant — protected modules unchanged |
| Memory Law | Compliant — all learning recorded and traceable |
| Information Law | Compliant — no new data classification needed |
| Economic Law | Compliant — ROI tracking extends existing |
| Knowledge Governance Decree | Compliant — UPDATE > CREATE |
| Repo Governance Decree | Compliant — no root pollution |
| Retention Governance Decree | Compliant — all new tables follow retention policy |

## 12. Implementation Strategy

PHASE 1: Evolution Loop + Scheduler (core infrastructure)
PHASE 2: Agent Profiles + Terminal Autonomy (agent layer)
PHASE 3: ROI + Maturity Integration (measurement layer)
PHASE 4: Integration + Tests
PHASE 5: Final Report + Exit Criteria

**All phases avoid:** MT5 modification, runtime mutation, Risk Kernel changes, governance law changes, credential access, protected module modification, uncontrolled self-modification, unauthorized deletion.
