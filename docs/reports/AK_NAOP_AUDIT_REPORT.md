# AK NAOP Audit Report

Date: 2026-06-07
Authority: Janus Directive — NAOP Legal & Integration Completion Patch v1.0
Status: COMPLETE

## Repository Inventory

| Directory | .py | .md | .yaml | Description |
|---|---|---|---|---|
| agents/ | 37 | 21 | 22 | 7 agents + runtime, identity, boundaries |
| memory/ | 34 | 0 | 1 | LanceDB adapter, registries, learning runtime |
| governance/ | 10 | 5 | 5 | Gate, policy, audit, classification |
| connectors/ | 5 | 8 | 8 | LLM, filesystem, git, opencode |
| workflows/ | 5 | 9 | 9 | Mission runtime, council review |
| pipelines/ | 5 | 6 | 11 | OADEL, skill, capability pipelines |
| tests/ | 65 | 0 | 0 | All test files |
| docs/ | 0 | 280 | 1 | Reports, design, legal, governance |
| scripts/ | 10 | 0 | 0 | CLI, pipeline runners |
| root | 1 | 0 | 0 | akctl.py |
| **Total** | **172** | **329** | **57** | |

## Existing Capabilities

- 7 operational agents (janus, sage, hermes, iris, helen, lang_lieu, yet_kieu)
- Agent runtime with mission execution, evidence capture, lesson distillation
- LanceDB adapter with insert/search/table management
- Memory interface with lesson, skill, capability, dataset registries
- Learning runtime with NationalMemoryPlatform (13 tables)
- Mission runtime with Sage approval gate
- Council review workflow
- LLM connector with provider routing (9router, openrouter, openai)
- Governance gate with proposal evaluation
- Policy engine with risk classification
- Capability pipelines (discovery→family→canonical→graph→maturity→readiness)
- Skill pipelines (signal→insight→discovery→deduplication→family→canonical)
- NationalMemoryPlatform with retention governance
- Agent boundary tests (13 tests)

## Existing Activation States

- LOCKED (default)
- READY_FOR_SANDBOX
- SANDBOX_ACTIVE
- PILOT_ACTIVE, OPERATIONAL_LIMITED, OPERATIONAL_APPROVED (blocked by Sage)

## Existing Governance Controls

- Governance gate (Sage)
- Policy engine (risk classification)
- Protected module classification (PROTECTED/CONTROLLED/OPEN)
- Agent boundary enforcement (role_boundary)
- Filesystem connector (blocked paths)
- Git connector (read-only)

## Deliverable Status

| Deliverable | Status | Path |
|---|---|---|
| CONSTITUTIONAL_MAPPING.md | ✓ EXISTS | docs/governance/CONSTITUTIONAL_MAPPING.md |
| AK_LEGAL_IMPACT_REPORT.md | ✓ EXISTS | docs/reports/AK_LEGAL_IMPACT_REPORT.md |
| protected_module_classification.yaml | ✓ EXISTS | governance/protected_module_classification.yaml |
| test_agent_boundaries.py | ✓ EXISTS | tests/test_agent_boundaries.py (13 tests) |
| capability_roi_registry.py | ✗ MISSING | memory/capability_roi_registry.py |
| test_human_sovereignty_gate.py | ✗ MISSING | tests/test_human_sovereignty_gate.py |
| test_capability_roi_registry.py | ✗ MISSING | tests/test_capability_roi_registry.py |
| test_lancedb_retention_fields.py | ✗ MISSING | tests/test_lancedb_retention_fields.py |
| AK_KNOWLEDGE_LIFECYCLE_AUDIT.md | ✗ MISSING | docs/reports/AK_KNOWLEDGE_LIFECYCLE_AUDIT.md |
| AK_RETENTION_GOVERNANCE_REPORT.md | ✗ MISSING | docs/reports/AK_RETENTION_GOVERNANCE_REPORT.md |
| AK_AGENT_BOUNDARY_AUDIT.md | ✗ MISSING | docs/reports/AK_AGENT_BOUNDARY_AUDIT.md |
| AK_NAOP_GAP_ANALYSIS.md | ✗ MISSING | docs/reports/AK_NAOP_GAP_ANALYSIS.md |
| AK_NAOP_INTEGRATION_VERIFICATION.md | ✗ MISSING | docs/reports/AK_NAOP_INTEGRATION_VERIFICATION.md |

**7 deliverables present, 7 deliverables missing.**
