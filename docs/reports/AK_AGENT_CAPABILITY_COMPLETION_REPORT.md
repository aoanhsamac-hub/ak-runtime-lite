# AK Agent Capability Completion Report

Date: 2026-06-07
Authority: Janus Directive — Hermes-Like Capability Completion & Activation Program
Status: COMPLETE

## Summary

All 7 AK agents have been upgraded from nominal roles to operational agents with Hermes-like capabilities. The framework supports mission execution, tool/API calling, evidence capture, learning-by-doing, council review, and controlled activation states.

## Architecture

```
agents/runtime_models.py       -- Shared dataclasses (AgentContext, MissionEnvelope,
                                  ToolRequest/Result, EvidenceRecord, LessonRecord,
                                  CapabilityUsageRecord, AgentReportEnvelope, ActivationState)
agents/runtime.py              -- Enhanced BaseAgent with mission execution loop,
                                  evidence capture, lesson distillation, usage tracking
connectors/llm_connector.py    -- OpenAI/OpenRouter API + mock fallback
connectors/filesystem_connector.py -- Safe read/write (no delete)
connectors/git_connector.py    -- Status/diff/branch/log only
connectors/opencode_connector.py -- Pre-existing adapter (unchanged)
memory/usage_registry.py       -- CapabilityUsageRegistry (JSONL)
memory/evidence_registry.py    -- EvidenceRegistry (JSONL)
memory/learning_runtime.py     -- LessonCandidateRegistry, AgentPerformanceRegistry,
                                  LearningRuntime (orchestration)
workflows/mission_runtime.py   -- MissionRuntime (mission dispatch, council, activation)
workflows/council_review.py    -- CouncilReview (multi-agent review, readiness assessment)
```

## Files Created or Modified

| File | Action | Purpose |
|------|--------|---------|
| `agents/runtime_models.py` | Created | Shared dataclasses and enums |
| `agents/runtime.py` | Created | Enhanced BaseAgent with operational layer |
| `agents/base.py` | Updated | Re-exports BaseAgent from runtime.py |
| `agents/janus/agent.py` | Updated | Mission planning, routing, council consolidation |
| `agents/sage/agent.py` | Updated | Activation gate, risk review, compliance, veto |
| `agents/hermes/agent.py` | Updated | Lesson distillation, evidence quality, dataset readiness |
| `agents/iris/agent.py` | Updated | Market research, hypothesis review, strategy packaging |
| `agents/helen/agent.py` | Updated | Topic research, source classification |
| `agents/lang_lieu/agent.py` | Updated | Implementation planning, code review, test runner |
| `agents/yet_kieu/agent.py` | Updated | Infrastructure check, security review, backup posture |
| `connectors/llm_connector.py` | Created | OpenAI/OpenRouter API + mock fallback |
| `connectors/filesystem_connector.py` | Created | Safe read/write with path protection |
| `connectors/git_connector.py` | Created | Status/diff/log/branch (read-only) |
| `memory/usage_registry.py` | Created | CapabilityUsageRegistry (JSONL) |
| `memory/evidence_registry.py` | Created | EvidenceRegistry (JSONL) |
| `memory/learning_runtime.py` | Created | LessonCandidateRegistry, PerformanceRegistry, LearningRuntime |
| `workflows/mission_runtime.py` | Created | Mission dispatch and activation workflow |
| `workflows/council_review.py` | Created | Multi-agent council review |
| `scripts/run_agent_smoke_test.py` | Created | CLI smoke test for all 7 agents |
| `scripts/run_council_mission.py` | Created | CLI council mission runner |
| `akctl.py` | Created | Unified AK Control CLI |
| `pipelines/observe_analyze_decide_execute_learn/pipeline.yaml` | Updated | Full 5-stage pipeline |
| `tests/test_agent_operational_capabilities.py` | Created | 19 agent capability tests |
| `tests/test_learning_by_doing_runtime.py` | Created | 16 learning runtime tests |
| `tests/test_capability_activation_gate.py` | Created | 10 activation gate tests |

## Agent Capabilities

| Agent | Operational Methods | Tools |
|-------|-------------------|-------|
| Janus | plan_mission, route_mission, consolidate_council, resolve_dependencies, aggregate_council_output, check_all_agents_ready | LLM |
| Sage | validate_activation, review_risk, veto_proposal, compliance_report, generate_gate_report | LLM |
| Hermes | distill_lesson, review_evidence_quality, check_dataset_readiness, generate_memory_report | LLM |
| Iris | market_research, review_trading_hypothesis, package_strategy_evidence, generate_intelligence_report | LLM |
| Helen | research_topic, classify_source, validate_research, generate_intelligence_report | LLM |
| Lang Lieu | plan_implementation, review_code_quality, coordinate_code_generation, run_tests, opencode_status | LLM, OpenCode |
| Yet Kieu | check_infrastructure, security_review, backup_posture, incident_report | LLM |

## Test Results

```
431 tests collected
430 passed, 1 pre-existing failure (unrelated WP3 acceptance)
44 new capability tests: 44/44 PASS

7/7 agents boot               ✓
7/7 agents call LLM/mock      ✓
7/7 agents generate reports   ✓
7/7 agents write evidence     ✓
Hermes distills lessons       ✓
Sage blocks unsafe activation ✓
Janus consolidates council    ✓
Activation: SANDBOX_ACTIVE    ✓
```

## Compliance

| Authority | Status |
|-----------|--------|
| Constitution | ✓ Compliant |
| State Corpus | ✓ Compliant |
| Agent Law | ✓ Separation of duties preserved |
| Risk Law | ✓ Sage gate controls activation |
| Execution Law | ✓ No live execution, SANDBOX_ACTIVE only |
| Security Law | ✓ No secret logging, path protection |
| Memory Law | ✓ Evidence/lesson registries, audit trail |
| Information Law | ✓ Evidence classification (I0-I9) |
| Repo Governance | ✓ No legacy import |
| Knowledge Governance | ✓ Learning-by-doing with Sage review |
| No legacy runtime/code | ✓ |
| No live execution | ✓ |
| No secret logging | ✓ |
| No protected module modification | ✓ |

## Current Activation State

- Default: LOCKED
- After smoke test pass: READY_FOR_SANDBOX
- Tested: SANDBOX_ACTIVE works with all agents
- Not activated: PILOT_ACTIVE, OPERATIONAL_LIMITED, OPERATIONAL_APPROVED

## Next Steps

1. Run `python scripts/run_agent_smoke_test.py` to verify operational readiness
2. Run `python scripts/run_council_mission.py "Mission objective"` for first council mission
3. Set API key via `OPENAI_API_KEY` or `OPENROUTER_API_KEY` for live LLM mode
4. Await Sage review and Janus authorization for Phase 1D+ learning-by-doing activation
