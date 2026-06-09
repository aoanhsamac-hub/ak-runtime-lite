# National Knowledge Inventory

**Directive:** HERMES-CLEANUP-01 Phase 4
**Date:** 2026-06-07
**Status:** INVENTORY COMPLETE — NO EXECUTION

---

## 1. Knowledge Asset Classification

### 1.1 Lessons

**Count:** 0 persisted records
**Storage:** LanceDB `lessons` table (0 rows)
**Schema:** `LessonRecord` (frozen dataclass, 14 fields)
**Backing registry:** `memory/lesson_registry.py` — in-memory `_records: dict`
**States defined:** DRAFT → REVIEWED → APPROVED → DEPRECATED / QUARANTINE
**Doctrine:** `docs/legal/codex/standards/STD-01_LESSON_QUALITY_v1.0.md`
**Dedup model:** `docs/design/AK_LESSON_DEDUPLICATION_MODEL.md`

*No lessons have been created. The lesson pipeline is structurally complete but empty.*

### 1.2 Skills

**Count:** 0 persisted records
**Storage:** LanceDB `skills` table (0 rows)
**Schema:** `SkillRecord` (frozen dataclass, 15 fields)
**Backing registry:** `memory/skill_registry.py` — in-memory `_records: dict`
**States defined:** DRAFT → REVIEWED → APPROVED → ACTIVE → DEPRECATED / QUARANTINE
**Doctrine:** `docs/legal/codex/standards/STD-02_SKILL_TAXONOMY_v1.0.md`
**Discovery design:** `docs/design/AK_SKILL_DISCOVERY_MODEL.md`

*No skills have been created. Skills require approved source lessons first.*

### 1.3 Capabilities

**Count:** 0 persisted records
**Storage:** LanceDB `capabilities` table (0 rows)
**Schema:** `CapabilityRecord` (frozen dataclass, 13 fields)
**Backing registry:** `memory/capability_registry.py` — in-memory `_records: dict`
**States defined:** DRAFT → REVIEWED → APPROVED → ACTIVE → DEPRECATED / QUARANTINE
**Maturity levels:** Not yet defined in code; referenced in design docs
**Doctrine:** `docs/design/AK_CAPABILITY_EVOLUTION_MODEL.md`, `docs/design/AK_CAPABILITY_LIFECYCLE_MODEL.md`

*No capabilities have been created. Capabilities require approved/active skills.*

### 1.4 Datasets

**Count:** 0 persisted records
**Storage:** LanceDB `datasets` table (0 rows)
**Schema:** `DatasetRecord` (frozen dataclass, 10 fields + metadata dict)
**Backing registry:** `memory/dataset_registry.py` — in-memory `_records: dict`
**States defined:** DRAFT (no state machine implemented)
**Physical storage:** `data/datasets/` (empty)

*No datasets have been created or registered.*

### 1.5 Decision Traces

**Count:** 0 persisted records
**Storage:** LanceDB `decision_traces` table (0 rows)
**Schema:** `DecisionTraceRecord` (frozen dataclass, 14 fields)
**Backing registry:** `memory/decision_trace_registry.py` — in-memory `_records: dict`
**States defined:** DRAFT (hardcoded default)
**Lesson generation:** Optional `lesson_generated` field links trace→lesson

*No decision traces have been recorded.*

---

## 2. Learning Artifacts

### 2.1 Design Doctrine (docs/design/)

| Artifact | Lines | Status | Relation to Knowledge |
|----------|-------|--------|----------------------|
| AK_LESSON_QUALITY_MODEL.md | 106 | SUPERSEDED by STD-01 | Lesson quality standards |
| AK_LESSON_DEDUPLICATION_MODEL.md | 105 | CURRENT | Dedup rules |
| AK_SKILL_DISCOVERY_MODEL.md | 96 | SUPERSEDED (partial) by STD-02 | Skill emergence |
| AK_SKILL_TAXONOMY_MODEL.md | 87 | SUPERSEDED by STD-02 | Skill classification |
| AK_CAPABILITY_EVOLUTION_MODEL.md | 87 | CURRENT | Capability progression |
| AK_CAPABILITY_LIFECYCLE_MODEL.md | 115 | CURRENT | Lifecycle management |
| AK_CROSS_AGENT_LEARNING_MODEL.md | 86 | CURRENT | Cross-agent knowledge sharing |
| AK_CROSS_AGENT_SHARING_POLICY.md | 81 | SUPERSEDED by POL-03 | Sharing rules |
| AK_LEARNING_METRICS_MODEL.md | 73 | SUPERSEDED by STD-04 | Measurement framework |
| AK_BEHAVIOR_IMPROVEMENT_MODEL.md | 125 | CURRENT | Behavior learning |
| AK_PROMOTION_GOVERNANCE_MODEL.md | 130 | SUPERSEDED by STD-05 | Promotion gates |
| AK_WP35_PHASE1A_LEARNING_METRICS_NOTES.md | — | HISTORICAL | Phase 1A notes |
| AK_WP35_PHASE1C_EVIDENCE_POLICY_DESIGN.md | 239 | CURRENT | Evidence policy |
| AK_WP35_PHASE1E_SKILL_DISCOVERY_DESIGN.md | 347 | CURRENT | Phase 1E design |

### 2.2 Codex Standards (docs/legal/codex/)

| Artifact | Lines | Status | Relation to Knowledge |
|----------|-------|--------|----------------------|
| STD-01_LESSON_QUALITY_v1.0.md | 106 | CANONICAL | Lesson quality |
| STD-02_SKILL_TAXONOMY_v1.0.md | 87 | CANONICAL | Skill taxonomy |
| STD-04_LEARNING_METRICS_v1.0.md | 73 | CANONICAL | Learning metrics |
| STD-05_PROMOTION_GOVERNANCE_v1.0.md | 130 | CANONICAL | Promotion governance |
| POL-03_CROSS_AGENT_SHARING_v1.0.md | 81 | CANONICAL | Cross-agent sharing |
| SPEC-00_WP35_IMPLEMENTATION_v1.0.md | 129 | CANONICAL | Implementation spec |
| SPEC-01_WP35_DATA_MODEL_v1.0.md | 131 | CANONICAL | Data model spec |

### 2.3 Architecture

| Artifact | Lines | Description |
|----------|-------|-------------|
| AK_LEARNING_INTELLIGENCE_ARCHITECTURE.md | 171 | Full learning intelligence architecture |

### 2.4 Interface Specifications

| Artifact | Lines | Description |
|----------|-------|-------------|
| AK_WP35_PHASE1A_INTERFACE_SPEC.md | 129 | Learning Metrics interface |
| AK_WP35_PHASE1B_INTERFACE_SPEC.md | 99 | Lesson Evaluator interface |
| AK_WP35_PHASE1C_INTERFACE_SPEC.md | 153 | Skill Evidence Policy interface |
| AK_WP35_PHASE1E_INTERFACE_SPEC.md | 157 | Skill Discovery interface |

### 2.5 Learning Implementation Code

| Artifact | Description |
|----------|-------------|
| `learning/learning_metrics.py` | EvidenceRecord, GovernanceContext, EvidenceProvider |
| `learning/lesson_evaluator.py` | LessonEvaluator, LessonStatus, InformationClassification |
| `learning/skill_evidence_policy.py` | SkillEvidencePolicy, RiskClassification, promotion audits |

---

## 3. Governance Artifacts

### 3.1 Policy Engine

| Artifact | Description |
|----------|-------------|
| `governance/policy_engine.py` | Policy enforcement |
| `governance/approval_engine.py` | Approval routing |
| `governance/governance_gate.py` | Default-deny gate |
| `governance/audit_engine.py` | Append-only audit |
| `governance/issue_registry.py` | Issue tracking |

### 3.2 Governance Registries

| Artifact | Description |
|----------|-------------|
| `governance/registries/protected_modules.yaml` | Protected module list |
| `governance/registries/approval_matrix.yaml` | Approval authority matrix |
| `governance/registries/governance_gate_registry.yaml` | Gate rules |
| `governance/registries/issue_registry.yaml` | Issues |
| `governance/audit/audit_log.jsonl` | Append-only audit log |

---

## 4. Registry Assets

### 4.1 Legal/Knownledge Registries

| Registry | File | Purpose |
|----------|------|---------|
| Legal Index | `sovereign/legal_index.yaml` | Master index of 15 sovereign documents |
| Constitution Registry | `sovereign/registries/constitution_registry.yaml` | Constitution metadata |
| State Corpus Registry | `sovereign/registries/state_corpus_registry.yaml` | State corpus metadata |
| Legal Hierarchy | `sovereign/registries/legal_hierarchy.yaml` | 7-level legal hierarchy |
| Directive Registry | `sovereign/registries/directive_registry.yaml` | Directive classes |
| Treasury Registry | `sovereign/registries/treasury_registry.yaml` | Revenue/reserve tracking |

### 4.2 Agent Registry

| Registry | File | Content |
|----------|------|---------|
| Agent Registry | `agents/registry.yaml` | 7 agents: Janus, Sage, Hermes, Iris, Helen, Lang Lieu, Yet Kieu |

### 4.3 Code Registries (Empty)

| Registry | File | Knowledge Type | Record Count |
|----------|------|---------------|--------------|
| LessonRegistry | `memory/lesson_registry.py` | Lessons | 0 |
| SkillRegistry | `memory/skill_registry.py` | Skills | 0 |
| CapabilityRegistry | `memory/capability_registry.py` | Capabilities | 0 |
| DatasetRegistry | `memory/dataset_registry.py` | Datasets | 0 |
| DecisionTraceRegistry | `memory/decision_trace_registry.py` | Decision traces | 0 |

---

## 5. Sovereign Documents

| # | Document | Type | Version | Format | Status |
|---|----------|------|---------|--------|--------|
| 1 | Constitution | Constitution | v1.1 | .docx | FINAL |
| 2 | State Corpus | State Corpus | v1.0 | .docx | FINAL |
| 3 | Governance Charter | Governance Charter | v1.1 | .docx | FINAL |
| 4 | Agent Law | Agent Law | v1.0 | .docx | FINAL |
| 5 | Risk Law | Risk Law | v1.0 | .docx | FINAL |
| 6 | Execution Law | Execution Law | v1.0 | .docx | FINAL |
| 7 | Economic Law | Economic Law | v1.0 | .docx | FINAL |
| 8 | Information Law | Information Law | v1.0 | .docx | FINAL |
| 9 | Memory Law | Memory Law | v1.0 | .docx | FINAL |
| 10 | Security Law | Security Law | v1.0 | .docx | FINAL |
| 11 | National Budget Law | Budget Law | v0.1 | .docx | DRAFT |
| 12 | National Budget Law | Budget Law | v1.0 | .md | REVIEW |
| 13 | Repo Governance Decree | Decree | v1.0 | .docx | FINAL |
| 14 | Knowledge Governance Decree | Decree | v1.0 | .docx | FINAL |
| 15 | Retention Decree | Decree | v1.0 | .docx | FINAL |

---

## 6. Archived Knowledge

| Archive | Date | Contents | Size |
|---------|------|----------|------|
| `archive/legal_reorganization/` | 2026-06-07 | Legal directory backup | ~5 files |
| `archive/wp0_bootstrap_backup/` | 2026-06-07 | WP0 complete backup | ~10 files |
| `archive/wp1_governance_engine_backup/` | 2026-06-07 | Governance engine | ~8 files |
| `archive/wp2_agent_framework_backup/` | 2026-06-07 | Agent framework | ~15 files |
| `archive/wp35_learning_intelligence_design_backup/` | 2026-06-07 | Learning design | ~12 files |
| `archive/wp35_sage_round2_backup/` | 2026-06-07 | Sage round 2 | ~5 files |

---

## 7. Knowledge Map Summary

```
KNOWLEDGE INFRASTRUCTURE
│
├── Memory Platform (memory/)
│   ├── LanceDBAdapter (persistence)
│   ├── 5 Registries (empty)
│   ├── LearningLoop (orchestration)
│   ├── KnowledgeCompressionEngine (defined)
│   ├── DistillationPipeline (defined)
│   └── QuarantinePolicy (defined)
│
├── Learning Layer (learning/)
│   ├── LearningMetrics (Phase 1A)
│   ├── LessonEvaluator (Phase 1B)
│   └── SkillEvidencePolicy (Phase 1C)
│
├── Governance Layer (governance/)
│   ├── PolicyEngine
│   ├── ApprovalEngine
│   ├── GovernanceGate
│   └── AuditEngine
│
├── Doctrine (docs/design/ + docs/legal/codex/)
│   ├── 14 Design Documents
│   ├── 7 Codex Standards/Specifications
│   ├── 4 Interface Specifications
│   └── 1 Architecture Document
│
├── Legal Framework (sovereign/)
│   ├── 1 Constitution (v1.1)
│   ├── 1 State Corpus (v1.0)
│   ├── 10 Laws (FINAL)
│   ├── 3 Decrees (FINAL)
│   └── 6 Registries
│
├── Agent Layer (agents/)
│   ├── 7 Agents (operational)
│   └── AgentRegistry
│
└── Archives (archive/)
    └── 6 Backups (unindexed)
```

---

## 8. Key Metrics

| Asset Category | Total Assets | Populated | Empty | Population % |
|---------------|-------------|-----------|-------|-------------|
| Knowledge records (lessons) | ∞ capacity | 0 | — | 0% |
| Knowledge records (skills) | ∞ capacity | 0 | — | 0% |
| Knowledge records (capabilities) | ∞ capacity | 0 | — | 0% |
| Knowledge records (datasets) | ∞ capacity | 0 | — | 0% |
| Knowledge records (traces) | ∞ capacity | 0 | — | 0% |
| Design documents | 14 | 14 | 0 | 100% |
| Codex standards | 7 | 7 | 0 | 100% |
| Legal documents | 15 | 15 | 0 | 100% |
| YAML registries | 13 | 13 | 0 | 100% |
| Python registries | 5 | 0 | 5 | 0% |
| Archive backups | 6 | 6 | 0 | 100% |
| Empty data dirs | 10 | 0 | 10 | 0% |

**National Knowledge Maturity:** STRUCTURAL (Layer 3 of 5)
- Layer 1: Infrastructure ✓
- Layer 2: Doctrine ✓
- Layer 3: Registries ✓
- Layer 4: Population ✗ (0 records)
- Layer 5: Evolution ✗ (no capabilities)

---

*End of National Knowledge Inventory.*
