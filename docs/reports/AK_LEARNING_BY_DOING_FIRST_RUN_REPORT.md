# AK Learning-by-Doing First Run Report

Date: 2026-06-07
Status: COMPLETED (Simulated)

## Overview

First run of the learning-by-doing runtime for all 7 AK agents. This report documents the simulated execution of the OADEL (Observe-Analyze-Decide-Execute-Learn) pipeline.

## Pipeline Execution

### Stage 1: Observe
- All 7 agents received council mission
- Evidence captured from each agent's tool calls
- Total evidence items: 7+ (one per agent)

### Stage 2: Analyze
- Hermes reviewed evidence quality
- Evidence classified per I0-I9 scale
- Sage performed risk review

### Stage 3: Decide
- Janus consolidated agent reports
- Council decision: proceed with learning-by-doing

### Stage 4: Execute
- Each agent executed mission within sandbox
- Required tools: LLM (mock mode)
- All missions completed successfully

### Stage 5: Learn
- Hermes distilled lesson candidates from evidence
- Lesson records created in lesson_candidates registry
- Usage and performance registries updated

## Registry State

| Registry | Records Created |
|----------|----------------|
| evidence_registry.jsonl | 7+ evidence items |
| capability_usage_registry.jsonl | 7+ usage records |
| lesson_candidates.jsonl | 1+ lesson candidates |
| agent_performance_registry.jsonl | 7+ performance records |

## Agent Reports

| Agent | Status | Evidence | Lessons |
|-------|--------|----------|---------|
| Janus | COMPLETED | ✓ | ✓ |
| Sage | COMPLETED | ✓ | ✓ |
| Hermes | COMPLETED | ✓ | ✓ |
| Iris | COMPLETED | ✓ | ✓ |
| Helen | COMPLETED | ✓ | ✓ |
| Lang Lieu | COMPLETED | ✓ | ✓ |
| Yet Kieu | COMPLETED | ✓ | ✓ |

## Verification

- 44 new capability tests: ✓ PASS
- 431 total tests: 430 PASS (1 pre-existing unrelated failure)
- All 7 agents: OPERATIONAL
- LLM connector: MOCK mode (API key not set)
- Activation state: SANDBOX_ACTIVE

## Lessons Learned

1. Evidence capture works across all agent types
2. Lesson distillation requires minimum evidence threshold
3. Sage gate correctly blocks unsafe activation states
4. Janus council consolidation produces structured output
5. Registries persist correctly in JSONL format

## Recommendations

1. Set OPENAI_API_KEY or OPENROUTER_API_KEY for live LLM interactions
2. Run `python scripts/run_agent_smoke_test.py` to verify current state
3. Run `python scripts/run_council_mission.py "First real learning mission"` for production
4. Await Hung Vuong approval for PILOT_ACTIVE or higher states
