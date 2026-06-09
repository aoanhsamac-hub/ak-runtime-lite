# Constitutional Mapping

Date: 2026-06-07
Authority: Janus Directive — NAOP v1.0
Status: FINAL

## Purpose

Map every new NAOP component to its constitutional and legal basis.

---

## 1. Unified LanceDB Platform

### Constitution
- Article 36 — Memory Governance: All memory operations require governance context
- Article 37 — Lesson Status: Defines mandatory lesson lifecycle

### Laws
- Memory Law: Lesson requirements, governance controls
- Information Law: Evidence classification (I0-I9)
- Knowledge Governance Decree: Knowledge lifecycle Evidence→Lesson→Knowledge→Skill→Capability
- Retention & Archive Governance Decree: Retention classes, compaction policies

### State Corpus
- Section on National Memory: LanceDB is the canonical operational memory platform

### Protected Module Classification
- `memory/lancedb` — CONTROLLED

---

## 2. Agent Operational Runtime (receive_mission, call_tool, capture_evidence, distill_lesson)

### Constitution
- Article 27 — Separation of Duties: Distinct roles for proposal, review, approval
- Article 38 — Knowledge Compression Doctrine: Learning must produce compressed knowledge

### Laws
- Agent Law: Role boundaries, governance-before-execution
- Risk Law: Risk classification before execution
- Execution Law: Audit trail for all execution
- Security Law: Least privilege, fail closed

### State Corpus
- Agent role definitions (Janus coordination, Sage governance, Hermes memory, etc.)

### Protected Module Classification
- `agents/runtime.py` — CONTROLLED
- `agents/` (agent-specific files) — CONTROLLED

---

## 3. Mission Runtime & Council Review

### Constitution
- Article 27 — Separation of Duties: Council requires distinct roles (Janus coordinates, Sage reviews)

### Laws
- Agent Law: Coordination through Janus, risk review through Sage
- Execution Law: Approval chain before execution
- Risk Law: Sage mandatory for ACTIVATION/GOVERNANCE missions

### Protected Module Classification
- `workflows/mission_runtime.py` — CONTROLLED
- `workflows/council_review.py` — CONTROLLED

---

## 4. Connectors (LLM, Filesystem, Git)

### Laws
- Security Law: No secrets in code, least privilege
- Execution Law: Read-only git, blocked filesystem paths
- Information Law: LLM output classification (I5_SPECULATIVE default)

### Protected Module Classification
- `connectors/filesystem_connector.py` — CONTROLLED (blocked paths enforced)
- `connectors/git_connector.py` — CONTROLLED (read-only enforced)
- `connectors/llm_connector.py` — CONTROLLED (mock fallback, no API key in code)

---

## 5. Activation States (LOCKED→READY_FOR_SANDBOX→SANDBOX_ACTIVE)

### Constitution
- Article 27 — Separation of Duties: Activation requires Sage gate + Janus authorization

### Laws
- Agent Law: No autonomous activation
- Risk Law: Sage must validate each state transition
- Execution Law: Human Sovereignty Gate — OpenCode only reaches READY_FOR_SANDBOX
- Security Law: LOCKED default, no self-escalation

### Protected Module Classification
- `agents/runtime_models.py` (ActivationState enum) — CONTROLLED

---

## 6. Capability ROI Registry (ak_capability_roi)

### Laws
- Economic Law: Every capability must track usage, value, cost, ROI
- Knowledge Governance Decree: Capability as final knowledge lifecycle stage

### Protected Module Classification
- `memory/kingdom_memory_platform.py` (ak_capability_roi table) — CONTROLLED

---

## 7. Retention Governance

### Laws
- Retention & Archive Governance Decree: TRANSIENT/OPERATIONAL/CANONICAL/ARCHIVAL classes
- Memory Law: No unbounded memory growth

### Protected Module Classification
- Retention logic within `memory/kingdom_memory_platform.py` — CONTROLLED

---

## 8. Agent Boundary Tests

### Laws
- Agent Law: No agent may exceed authority, self-escalate, modify law, or modify risk
- Security Law: Self-escalation prohibited

### Protected Module Classification
- `tests/test_agent_boundaries.py` — OPEN

---

## Classification Summary

| Component | Classification | Legal Basis |
|---|---|---|
| memory/kingdom_memory_platform.py | CONTROLLED | Memory Law, Knowledge Gov Decree, Retention Decree |
| agents/runtime.py | CONTROLLED | Agent Law, Risk Law, Execution Law |
| agents/runtime_models.py | CONTROLLED | Agent Law, Execution Law |
| connectors/llm_connector.py | CONTROLLED | Security Law, Information Law |
| connectors/filesystem_connector.py | CONTROLLED | Security Law, Repo Gov Decree |
| connectors/git_connector.py | CONTROLLED | Security Law, Repo Gov Decree |
| workflows/mission_runtime.py | CONTROLLED | Agent Law, Execution Law, Risk Law |
| workflows/council_review.py | CONTROLLED | Agent Law, Risk Law |
| tests/test_agent_boundaries.py | OPEN | Agent Law, Security Law |
| docs/governance/CONSTITUTIONAL_MAPPING.md | OPEN | None |
| docs/reports/AK_LEGAL_IMPACT_REPORT.md | OPEN | None |
| governance/protected_module_classification.yaml | CONTROLLED | Risk Law, Repo Gov Decree |
