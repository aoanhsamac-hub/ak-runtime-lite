# Registry Normalization Plan

**Directive:** HERMES-CLEANUP-01 Phase 2
**Date:** 2026-06-07
**Status:** PLAN ONLY — NO EXECUTION

---

## 1. Registry Inventory

### 1.1 All Known Registries

| # | Registry | File | Lines | Schema Type | Status |
|---|----------|------|-------|-------------|--------|
| R01 | Legal Index | `sovereign/legal_index.yaml` | 167 | Custom: 15 docs × 11 fields | ACTIVE |
| R02 | Legal Registry | `sovereign/registries/legal_registry.yaml` | 165 | Custom: 15 docs × 11 fields | ACTIVE (DUPLICATE) |
| R03 | Codex Legal Registry | `docs/legal/codex/registries/LEGAL_REGISTRY.yaml` | 165 | Custom: 15 docs × 11 fields | ACTIVE (DUPLICATE) |
| R04 | Constitution Registry | `sovereign/registries/constitution_registry.yaml` | 13 | Custom: 5 fields | ACTIVE |
| R05 | State Corpus Registry | `sovereign/registries/state_corpus_registry.yaml` | 13 | Custom: 5 fields | ACTIVE |
| R06 | Legal Hierarchy | `sovereign/registries/legal_hierarchy.yaml` | 26 | Custom: 7 levels | ACTIVE |
| R07 | Directive Registry | `sovereign/registries/directive_registry.yaml` | 13 | Custom: 3 classes | ACTIVE |
| R08 | Treasury Registry | `sovereign/registries/treasury_registry.yaml` | 32 | Custom: 3 sections | ACTIVE |
| R09 | Agent Registry | `agents/registry.yaml` | — | Custom: 7 agents | ACTIVE |
| R10 | Protected Modules | `governance/registries/protected_modules.yaml` | 48 | Custom: module list | ACTIVE |
| R11 | Approval Matrix | `governance/registries/approval_matrix.yaml` | 24 | Custom: role→authority | ACTIVE |
| R12 | Governance Gate Registry | `governance/registries/governance_gate_registry.yaml` | 18 | Custom: gate rules | ACTIVE |
| R13 | Issue Registry | `governance/registries/issue_registry.yaml` | 12 | Custom: issue list | ACTIVE |
| R14 | LessonRegistry | `memory/lesson_registry.py` | 51 | LessonRecord schema | IMPLEMENTED |
| R15 | SkillRegistry | `memory/skill_registry.py` | 64 | SkillRecord schema | IMPLEMENTED |
| R16 | CapabilityRegistry | `memory/capability_registry.py` | 59 | CapabilityRecord schema | IMPLEMENTED |
| R17 | DatasetRegistry | `memory/dataset_registry.py` | 22 | DatasetRecord schema | IMPLEMENTED |
| R18 | DecisionTraceRegistry | `memory/decision_trace_registry.py` | 22 | DecisionTraceRecord schema | IMPLEMENTED |

---

## 2. Duplicate Identification

### 2.1 Registry Duplicates

| Duplicate Group | Registries | Overlap | Recommendation |
|----------------|------------|---------|----------------|
| **Group A** | R01, R02, R03 | 100% identical (15 docs × 11 fields) | Consolidate to R01; retire R02, R03 |

### 2.2 Superseded Registries

| Registry | Superseded By | Rationale |
|----------|---------------|-----------|
| R02 (sovereign/registries/legal_registry.yaml) | R01 (sovereign/legal_index.yaml) | R01 is the master index; R02 is legacy copy |
| R03 (codex LEGAL_REGISTRY.yaml) | R01 (sovereign/legal_index.yaml) | Codex should reference, not duplicate |

### 2.3 Near-Duplicate Registries

| Pair | Potential Overlap | Assessment |
|------|-------------------|------------|
| R04 (Constitution) + R05 (State Corpus) | Both LEVEL_4_CONSTITUTIONAL, both LOCKED | Distinct by type; keep separate |
| R12 (Governance Gate) + R11 (Approval Matrix) | Both involve approval routing | Distinct by purpose; keep separate |

---

## 3. Schema Inconsistency Analysis

### 3.1 Field Name Inconsistencies

| Concept | R01–R03 Field | R04–R05 Field | R14–R18 Field |
|---------|--------------|---------------|---------------|
| Identifier | `document_name` | `document_name` | `lesson_id`, `skill_id`, etc. |
| Owner | `owner_agent` | (absent) | `owner_agent` |
| Reviewer | `reviewer_agent` | (absent) | `reviewer_agent` |
| Status | `status` | `status` | `status` |
| Version | `version` | `version` | `version` |
| Risk level | `protection_level` | `protection_level` | `risk_level` |
| Timestamp | (absent) | (absent) | `created_at` |

### 3.2 Missing Fields Per Registry

| Registry | Missing Fields |
|----------|---------------|
| R04 Constitution Registry | `owner_agent`, `reviewer_agent`, `created_at`, `risk_level` |
| R05 State Corpus Registry | `owner_agent`, `reviewer_agent`, `created_at`, `risk_level` |
| R06 Legal Hierarchy | No standard metadata fields at all |
| R07 Directive Registry | No `created_at`, no `status` per directive |
| R08 Treasury Registry | No `owner_agent`, no `version` |
| R09 Agent Registry | No `version`, no `created_at` |
| R10–R13 Governance Registries | Inconsistent field sets |

### 3.3 Status Taxonomy Inconsistency

| Registry | Status Values Used |
|----------|-------------------|
| R01–R03 | FINAL, DRAFT, REVIEW, ACTIVE |
| R04 | ACTIVE, LOCKED |
| R05 | RATIFIED, LOCKED |
| R14 | DRAFT, REVIEWED, APPROVED, DEPRECATED, QUARANTINE |
| R15 | DRAFT, REVIEWED, APPROVED, ACTIVE, DEPRECATED, QUARANTINE |
| R16 | DRAFT, REVIEWED, APPROVED, ACTIVE, DEPRECATED, QUARANTINE |
| R17 | DRAFT |
| R18 | DRAFT |

**Problem:** 4 different status taxonomies across 18 registries.

---

## 4. Normalization Strategy

### 4.1 Canonical Registry Schema

Define a single `RegistryRecord` schema for all YAML registries:

```yaml
registry_record:
  id: string                # Unique identifier (e.g., "DOC-CONSTITUTION-001")
  name: string              # Display name
  type: string              # Record type from taxonomy
  status: string            # From unified status taxonomy
  version: string           # Semantic version
  owner_agent: string       # Agent responsible
  reviewer_agent: string    # Agent for review
  risk_level: string        # From unified risk taxonomy
  created_at: string        # ISO 8601 UTC
  source_hash: string       # Content integrity hash
```

### 4.2 Unified Status Taxonomy

| Status | Definition | Applicable To |
|--------|------------|---------------|
| DRAFT | Under development | All registry types |
| REVIEWED | Passed review | All registry types |
| APPROVED | Formally approved | All registry types |
| ACTIVE | In operational use | Laws, standards, agents, skills |
| DEPRECATED | Superseded but preserved | Lessons, skills, standards |
| QUARANTINE | Blocked pending investigation | All record types |
| LOCKED | Constitutional-level frozen | Constitution, State Corpus |
| ARCHIVED | Moved to cold storage | All record types |

### 4.3 Unified Risk/Protection Taxonomy

| Level | Scope | Applicable To |
|-------|-------|---------------|
| LEVEL_1_MODERATE | Standard operational | Lessons, traces |
| LEVEL_2_ELEVATED | Agent-internal | Skills, capabilities |
| LEVEL_3_CRITICAL | Kingdom-wide | Laws, policies, standards |
| LEVEL_4_CONSTITUTIONAL | Constitutional | Constitution, State Corpus |

---

## 5. Consolidation Plan

### 5.1 Immediate Consolidation (Stage 1)

| Action | Source | Target | Rationale |
|--------|--------|--------|-----------|
| Retire R02 | `sovereign/registries/legal_registry.yaml` | R01 | 100% duplicate |
| Retire R03 | `docs/legal/codex/registries/LEGAL_REGISTRY.yaml` | R01 | 100% duplicate; codex should reference |
| Add cross-reference | Codex | R01 | Insert `source_registry: sovereign/legal_index.yaml` |

### 5.2 Schema Migration (Stage 2)

| Action | Target Registries | Change |
|--------|-------------------|--------|
| Normalize fields | R04, R05 | Add `owner_agent`, `reviewer_agent`, `created_at` |
| Normalize status | R06–R13 | Map to unified taxonomy |
| Add timestamps | R01–R13 | Add `created_at`, `updated_at` |
| Add versioning | R01–R13 | Add `registry_version` |

### 5.3 Schema Alignment (Stage 3)

| Action | Target | Change |
|--------|--------|--------|
| Align YAML `protection_level` with Python `risk_level` | All YAML registries + Python schemas | Use same taxonomy |
| Align `status` taxonomy | All registries | Single unified set |
| Normalize agent naming | All registries | "Janus", "Sage", "Hermes", etc. |

---

## 6. Post-Normalization Registry Landscape

```
Before:  18 registries (3 duplicates, 4+ status taxonomies, 3+ field schemas)
After:   16 registries (0 duplicates, 1 status taxonomy, 1 field schema)
                ↕
          1 master legal index (R01)
          15 other normalized registries
```

---

## 7. Compliance Verification

| Legal Document | Articles Checked | Normalization Compliance |
|----------------|-----------------|-------------------------|
| Constitution v1.1 | Art. 27, 36, 37, 38, 39 | PASS |
| State Corpus v1.0 | Chapter on governance records | PASS |
| Memory Law | Record-keeping requirements | PASS |
| Information Law | Metadata standards | PASS |
| Knowledge Governance Decree | Registry requirements | PENDING — normalization required |
| Repo Governance Decree | Repository structure | PASS |

---

*End of Registry Normalization Plan.*
