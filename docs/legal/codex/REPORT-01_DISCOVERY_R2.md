# CODEX DISCOVERY REPORT R2

Directive: AK-CODEX-WP01-R2
Phase: 1 - Legal Discovery Revalidation
Date: 2026-06-07

## Complete Legal Inventory

### Current Legal Sources

#### 1. Primary Source - sovereign/
| Path | Document | Type | Owner | Authority | Status | Migration |
|---|---|---|---|---|---|---|
| sovereign/constitution/ALKASIK_CONSTITUTION_v1.1_FINAL.docx | Constitution v1.1 | Constitution | Hung Vuong | Hung Vuong | FINAL | PENDING (.docx) |
| sovereign/state_corpus/ALKASIK_STATE_CORPUS_v1.0 FINAL.docx | State Corpus v1.0 | State Corpus | Hung Vuong | Hung Vuong | FINAL | PENDING (.docx) |
| sovereign/laws/agent/ALKASIK_AGENT_LAW_v1.0 FINAL.docx | Agent Law | Law | Hung Vuong | Hung Vuong | FINAL | PENDING (.docx) |
| sovereign/laws/risk/ALKASIK RISK LAW v1.0 FINAL.docx | Risk Law | Law | Hung Vuong | Hung Vuong | FINAL | PENDING (.docx) |
| sovereign/laws/execution/ALKASIK EXECUTION LAW v1.0 FINAL.docx | Execution Law | Law | Hung Vuong | Hung Vuong | FINAL | PENDING (.docx) |
| sovereign/laws/security/ALKASIK_SECURITY_LAW_v1.0 FINAL.docx | Security Law | Law | Hung Vuong | Hung Vuong | FINAL | PENDING (.docx) |
| sovereign/laws/memory/ALKASIK_MEMORY_LAW_v1.0 FINAL.docx | Memory Law | Law | Hung Vuong | Hung Vuong | FINAL | PENDING (.docx) |
| sovereign/laws/intelligence/ALKASIK_INFORMATION_LAW_v1.0 FINAL.docx | Information Law | Law | Hung Vuong | Hung Vuong | FINAL | PENDING (.docx) |
| sovereign/laws/Economic/ALKASIK Economic Law v1.0 FINAL.docx | Economic Law | Law | Hung Vuong | Hung Vuong | FINAL | PENDING (.docx) |
| sovereign/decrees/infrastructure/ALKASIK_REPO_GOVERNANCE_DECREE_v1.0_FINAL.docx | Repo Governance Decree | Decree | Hung Vuong | Hung Vuong | FINAL | PENDING (.docx) |
| sovereign/decrees/knowledge/ALKASIK_KNOWLEDGE_GOVERNANCE_DECREE_v1.0_FINAL.docx | Knowledge Governance Decree | Decree | Hung Vuong | Hung Vuong | FINAL | PENDING (.docx) |
| sovereign/decrees/retention/ALKASIK_RETENTION_DECREE_v1.0_FINAL.docx | Retention Decree | Decree | Hung Vuong | Hung Vuong | FINAL | PENDING (.docx) |

#### 2. Secondary Source - docs/
| Path | Document | Type | Owner | Authority | Status | Migration |
|---|---|---|---|---|---|---|
| docs/governance/ALKASIK_CONSTITUTION_v1.0.md | Constitution v1.0 | Constitution | Hung Vuong | Hung Vuong | FINAL | MIGRATED |
| docs/legal/codex/constitution/ALKASIK_CONSTITUTION_v1.1_FINAL.md | Constitution v1.1 | Constitution | Hung Vuong | Hung Vuong | FINAL | CANONICAL |
| docs/legal/canon/ALKASIK_CONSTITUTION_v1.1_FINAL.md | Constitution v1.1 | Constitution | Hung Vuong | Hung Vuong | FINAL | DUPLICATE |
| docs/legal/canon/*.md | Legal Canon files | Canonical | Hung Vuong | Hung Vuong | FINAL | CANONICAL |
| docs/legal/codex/* | CODEX files | CODEX | Lang Lieu | Sage | ACTIVE | CANONICAL |
| docs/design/*.md | Design Models | Design | Lang Lieu | Sage | ACTIVE | MIGRATE TO STANDARDS |
| docs/specifications/*.md | Specifications | Specification | Lang Lieu | Sage | ACTIVE | MIGRATED |
| docs/reviews/*.md | Review Packages | Review | Sage | Hung Vuong | ACTIVE | MIGRATED |
| docs/reports/*.md | Reports | Report | Lang Lieu | Sage | ACTIVE | PRESERVE |
| sovereign/registries/*.yaml | Registries | Registry | Lang Lieu | Sage | ACTIVE | CONSOLIDATE |

#### 3. Archive Source - archive/
| Path | Document | Type | Status | Migration |
|---|---|---|---|---|
| archive/wp0_bootstrap_backup/ | WP0 Backup | Archive | BACKUP | PRESERVE |
| archive/wp1_governance_engine_backup/ | WP1 Backup | Archive | BACKUP | PRESERVE |
| archive/wp2_agent_framework_backup/ | WP2 Backup | Archive | BACKUP | PRESERVE |
| archive/wp35_learning_intelligence_design_backup/ | WP3.5 Backup | Archive | BACKUP | PRESERVE |
| archive/wp35_sage_round2_backup/ | WP3.5 Sage Round 2 | Archive | BACKUP | PRESERVE |
| archive/legal_reorganization/ | Legal Reorg | Archive | BACKUP | PRESERVE |

## Duplicate Analysis

| Duplicate | Canonical Source | Action |
|---|---|---|
| docs/legal/canon/ALKASIK_CONSTITUTION_v1.1_FINAL.md | docs/legal/codex/constitution/ALKASIK_CONSTITUTION_v1.1_FINAL.md | Redirect/Remove |
| docs/legal/canon/*.md | docs/legal/codex/ | Migrate and remove |

## Migration Priority

1. HIGH: .docx files (binary, inaccessible)
2. MEDIUM: docs/design/*.md → standards/
3. LOW: Archive preservation

## Coverage Status

- Total legal artifacts: ~50
- Migrated to AK-CODEX: ~23
- Requires migration: ~27 (.docx + design files)
- Status: PARTIAL COVERAGE