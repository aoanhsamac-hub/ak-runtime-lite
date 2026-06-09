# AK WP3 Hermes-Native Memory Platform Report

## Summary

WP3 creates an AK-native learning layer instead of importing Hermes,
OpenHands, LightAgent, or OpenCode runtime code. The implementation defines a
LanceDB-only memory adapter, registries for lessons, skills, capabilities,
datasets, and decision traces, plus an adapter-only OpenCode connector for
Lang Lieu. The hardening pass adds first-insert table creation for real LanceDB
compatibility, Arrow-based text-table fallback, OpenCode governance metadata,
Windows path protection, and a memory client that lets AK agents route through
`MemoryInterface`. The final acceptance pass adds a runnable WP3 gate at
`workflows.wp3_acceptance`, with a workflow package under
`workflows/wp3_memory_platform/`.

## Hermes Capabilities Extracted

- Memory persistence: represented by `LanceDBAdapter`.
- Lesson distillation: represented by `LearningLoop` and `DistillationPipeline`.
- Knowledge compression: represented by `KnowledgeCompressionEngine`.
- Skill creation: skills require approved source lessons.
- Capability creation: capabilities require active or approved skills.
- Decision trace: decisions store reasoning, evidence, outcome, and optional generated lesson.
- Learning lifecycle: observe, review, approve, skill candidate, capability promotion.
- Quarantine: incomplete or invalid records are marked `QUARANTINE`.
- Agent memory access: agents receive `AgentMemoryClient` wrappers and do not
  receive direct LanceDB backend handles.

## Architecture Decisions

- No Hermes framework dependency.
- No OpenCode runtime dependency.
- No SQLite, Chroma, FAISS, or JSON memory fallback.
- LanceDB is imported lazily so the repo can be tested before the package is installed.
- Tests use an injected fake backend only to validate the adapter contract.
- Runtime acceptance is machine-checkable through `python -m workflows.wp3_acceptance`.

## LanceDB Design

All runtime memory access goes through `memory.lancedb_adapter.LanceDBAdapter`.
The adapter exposes `insert`, `search`, and `table`. First insert creates a
table using the first batch of rows instead of creating an empty schema-less
table. Search against a missing table returns an empty result without creating
storage. For text-only tables without vector columns, the adapter falls back to
Arrow row scan before trying Pandas. If LanceDB is not installed, runtime
connection fails closed with `LanceDBUnavailableError`.

## Learning Layer Design

Agents must use `MemoryInterface` instead of writing to LanceDB directly.
Lessons begin as `DRAFT`. Skills can only be created from `APPROVED` lessons.
Capabilities can only be created from `ACTIVE` or `APPROVED` skills. Promotion
is never automatic.

## OpenCode Integration Design

OpenCode is adapter-only for Lang Lieu. Protected paths are blocked unless both
Sage review and approval gate are supplied. The connector prepares task
metadata, includes governance gate metadata, normalizes Windows paths, and never
performs direct execution.

## Risks

- LanceDB and its `pylance` runtime reader dependency are listed in requirements.
- AK agents are currently bootstrap-level; WP3 records interfaces and evidence paths but does not pretend full agent reasoning is implemented.
- OpenCode executable may be unavailable; the connector reports `UNAVAILABLE` safely.

## Pending Reviews

- Sage review of WP3 memory lifecycle.
- Governance review before connecting WP3 to execution or protected modules.
- Formal Sage approval before using the memory platform in protected workflows.

## Verification Evidence

- `D:\AK\.venv\Scripts\python.exe -m pytest ...`: 37 passed.
- `D:\AK\.venv\Scripts\python.exe -m workflows.wp3_acceptance`: PASS, score 1.0.
- Acceptance gate confirms required files, banned backend scan, runtime dependencies,
  runtime boundaries, OpenCode safety, report readiness, and LanceDB runtime smoke.

## Readiness Score

Readiness: 0.96

WP3 is runtime verified for local LanceDB insert/search smoke, lifecycle
contracts, governance regression, and OpenCode adapter safety. Remaining
production work is formal Sage review and long-running operational integration.
