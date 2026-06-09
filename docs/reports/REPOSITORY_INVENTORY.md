# AK Repository Knowledge Inventory

Generated: 2026-06-08 | Authority: Janus Directive WP35.4A

## Total Files Scanned

- `.py`: 172
- `.md`: 329+ 
- `.yaml/.yml`: 57
- **Total**: ~558 source/doc files

## Category Breakdown

### 1. Laws (Canonical Legal Framework)
| File | Authority | Status |
|---|---|---|
| docs/legal/canon/ALKASIK_CONSTITUTION_v1.1_FINAL.md | **CANONICAL** | Active |
| docs/legal/canon/ALKASIK_AGENT_LAW_v1.0_FINAL.md | **CANONICAL** | Active |
| docs/legal/canon/ALKASIK_MEMORY_LAW_v1.0_FINAL.md | **CANONICAL** | Active |
| docs/legal/canon/ALKASIK_INFORMATION_LAW_v1.0_FINAL.md | **CANONICAL** | Active |
| docs/legal/canon/ALKASIK_REPO_GOVERNANCE_DECREE_v1.0_FINAL.md | **CANONICAL** | Active |
| docs/legal/canon/ALKASIK_ECONOMIC_LAW_v1.0_FINAL.md | **CANONICAL** | Active |
| docs/legal/canon/ALKASIK_EXECUTION_LAW_v1.0_FINAL.md | **CANONICAL** | Active |
| docs/legal/canon/ALKASIK_RISK_LAW_v1.0_FINAL.md | **CANONICAL** | Active |
| docs/legal/canon/ALKASIK_SECURITY_LAW_v1.0_FINAL.md | **CANONICAL** | Active |
| docs/legal/canon/ALKASIK_KNOWLEDGE_GOVERNANCE_DECREE_v1.0_FINAL.md | **CANONICAL** | Active |
| docs/legal/canon/ALKASIK_RETENTION_ARCHIVE_GOVERNANCE_DECREE_v1.0_FINAL.md | **CANONICAL** | Active |
| docs/legal/canon/ALKASIK_STATE_CORPUS_v1.0_FINAL.md | **CANONICAL** | Active |
| docs/legal/canon/LEGAL_CANON_INDEX.md | **REGISTRY** | Active |
| docs/legal/canon/LEGAL_COMPLIANCE_AUDIT.md | Supporting | Superseded |
| sovereign/laws/budget/AK_KINGDOM_BUDGET_LAW_v1.0_REVIEW.md | **CANONICAL** | REVIEW PENDING |
| docs/legal/codex/constitution/CONSTITUTION-00_CONSTITUTION_v1.0.md | Supporting | Superseded by v1.1 |
| docs/legal/codex/constitution/CONSTITUTION-00_CONSTITUTION_v1.1.md | Supporting | Mirror of canon |
| docs/legal/codex/laws/LAW-00_AK_CODEX_GOVERNANCE_CODE_v1.0.md | Supporting | Codex mirror |
| docs/legal/codex/laws/LAW-04_MEMORY_v1.0.md | Supporting | Codex mirror |
| docs/governance/ALKASIK_CONSTITUTION_v1.0.md | Supporting | Superseded by v1.1 |
| docs/governance/ALKASIK_AGENT_CHARTER_v1.0.md | Supporting | Superseded by Agent Law |
| docs/governance/ALKASIK_GOVERNANCE_CHARTER_v1.0.md | Supporting | Superseded by canon |

### 2. Governance Documents
| File | Authority | Status |
|---|---|---|
| governance/policy_engine.py | **AUTHORITATIVE** | Active |
| governance/governance_gate.py | **AUTHORITATIVE** | Active |
| governance/approval_engine.py | **AUTHORITATIVE** | Active |
| governance/audit_engine.py | **AUTHORITATIVE** | Active |
| governance/issue_registry.py | **AUTHORITATIVE** | Active |
| governance/__init__.py | Supporting | Active |
| governance/protected_module_classification.yaml | **REGISTRY** | Active |
| governance/policy_engine/POLICY_ENGINE.md | Supporting | Doc mirror |
| governance/approval_gate/APPROVAL_GATE.md | Supporting | Doc mirror |
| governance/protected_modules/PROTECTED_MODULES.md | Supporting | Doc mirror |
| governance/risk_kernel/RISK_KERNEL_CHARTER.md | Supporting | Doc mirror |
| governance/registries/approval_matrix.yaml | **REGISTRY** | Active |
| governance/registries/issue_registry.yaml | **REGISTRY** | Active |
| governance/registries/governance_gate_registry.yaml | **REGISTRY** | Active |
| governance/registries/protected_modules.yaml | **REGISTRY** | Active |
| governance/audit/README.md | Supporting | Active |
| sovereign/registries/legal_registry.yaml | **REGISTRY** | Active |
| sovereign/registries/constitution_registry.yaml | **REGISTRY** | Active |
| sovereign/registries/state_corpus_registry.yaml | **REGISTRY** | Active |
| sovereign/registries/legal_hierarchy.yaml | **REGISTRY** | Active |
| sovereign/registries/directive_registry.yaml | **REGISTRY** | Active |
| sovereign/registries/treasury_registry.yaml | **REGISTRY** | Active |
| sovereign/legal_index.yaml | **REGISTRY** | Active |
| sovereign/legal_registry/LEGAL_INDEX.md | Supporting | Doc mirror |

### 3. Reports (203 files in docs/reports/)
| Category | Count | Note |
|---|---|---|
| WP0-3 completion reports | 15 | Authoritative per WP |
| Capability pipeline reports | 40+ | Sub-reports per phase |
| Skill pipeline reports | 30+ | Sub-reports per phase |
| Market sandbox reports | 5 | Active |
| Legacy/cleanup reports | 20+ | One-time deliverables |
| Knowledge audit reports | 15+ | One-time deliverables |
| Codex reports | 15+ | Codex phase artifacts |

### 4. Reviews (20 files in docs/reviews/)
| File | Authority | Status |
|---|---|---|
| WP35_GOVERNANCE_CONSISTENCY_AUDIT.md | Supporting | One-time |
| WP35_GOVERNANCE_IMPACT_ASSESSMENT.md | Supporting | One-time |
| WP35_HUNG_VUONG_APPROVAL_PACKAGE.md | Supporting | One-time |
| WP35_IMPLEMENTATION_READINESS.md | Supporting | One-time |
| WP35_SAGE_REVIEW_CHECKLIST.md | Supporting | One-time |
| WP35_SAGE_ROUND2_CLOSURE.md | Supporting | One-time |
| WP35_REVIEW_DOSSIER.md | Supporting | One-time |
| AK_WP35_PHASE1* (remaining 12 files) | Supporting | One-time |

### 5. Memory Registries (Python)
| Module | Registry Type | Status |
|---|---|---|
| memory/lancedb_adapter.py | Backend | **AUTHORITATIVE** |
| memory/kingdom_memory_platform.py | Platform | **AUTHORITATIVE** |
| memory/memory_interface.py | Interface | **AUTHORITATIVE** |
| memory/agent_memory.py | Client | **AUTHORITATIVE** |
| memory/learning_runtime.py | Runtime | **AUTHORITATIVE** |
| memory/evidence_registry.py | Registry | **AUTHORITATIVE** |
| memory/lesson_registry.py | Registry | **AUTHORITATIVE** |
| memory/skill_registry.py | Registry | **AUTHORITATIVE** |
| memory/capability_registry/ | Package | **AUTHORITATIVE** |
| memory/capability_pipeline/ | Package | **AUTHORITATIVE** |
| memory/learning_registry/ | Package | **AUTHORITATIVE** |
| memory/capability_roi_registry.py | Registry | **AUTHORITATIVE** |
| memory/decision_trace_registry.py | Registry | **AUTHORITATIVE** |
| memory/dataset_registry.py | Registry | **AUTHORITATIVE** |
| memory/market_forecast_registry.py | Registry | Active |
| memory/zone_validation_registry.py | Registry | Active |
| memory/prompt_registry.py | Registry | Active |
| memory/fine_tuning_registry.py | Registry | Active |
| memory/dual_brain_registry.py | Registry | Active |
| memory/skill_benchmark_registry.py | Registry | Active |
| memory/usage_registry.py | Registry | **AUTHORITATIVE** |
| memory/quarantine_policy.py | Policy | Active |
| memory/knowledge_compression.py | Pipeline | Active |
| memory/distillation_pipeline.py | Pipeline | Active |
| memory/learning_loop.py | Pipeline | Active |
| memory/capability_backlog/ | Package | Active |

### 6. Services (Business Logic)
| File | Purpose | Status |
|---|---|---|
| services/*.py (36 files) | All pipeline engines | **AUTHORITATIVE** |

### 7. Architecture & Design Documents
| File | Authority | Status |
|---|---|---|
| docs/architecture/AK_LEARNING_INTELLIGENCE_ARCHITECTURE.md | **AUTHORITATIVE** | Active |
| docs/design/AK_LESSON_QUALITY_MODEL.md | Supporting | Active |
| docs/design/AK_SKILL_DISCOVERY_MODEL.md | Supporting | Active |
| docs/design/AK_CAPABILITY_EVOLUTION_MODEL.md | Supporting | Active |
| docs/design/AK_CROSS_AGENT_LEARNING_MODEL.md | Supporting | Active |
| docs/design/AK_LEARNING_METRICS_MODEL.md | Supporting | Active |
| docs/design/AK_BEHAVIOR_IMPROVEMENT_MODEL.md | Supporting | Active |
| docs/design/AK_PROMOTION_GOVERNANCE_MODEL.md | Supporting | Active |
| docs/design/AK_KNOWLEDGE_LIFECYCLE_MODEL.md | Supporting | Active |
| docs/design/WP35_* (remaining design files) | Supporting | Active |

### 8. Specifications
| File | Authority | Status |
|---|---|---|
| docs/specifications/WP35_DATA_MODEL_SPEC.md | **AUTHORITATIVE** | Active |
| docs/specifications/WP35_IMPLEMENTATION_SPEC.md | **AUTHORITATIVE** | Active |
| docs/specs/AK_WP35_PHASE1A_INTERFACE_SPEC.md | Supporting | Superseded |
| docs/specs/AK_WP35_PHASE1B_INTERFACE_SPEC.md | Supporting | Superseded |
| docs/specs/AK_WP35_PHASE1C_INTERFACE_SPEC.md | Supporting | Superseded |
| docs/specs/AK_WP35_PHASE1C_IMPLEMENTATION_CONTRACT.md | Supporting | Superseded |
| docs/specs/AK_WP35_PHASE1E_INTERFACE_SPEC.md | Supporting | Superseded |

### 9. Workflows & Pipelines
| File | Authority | Status |
|---|---|---|
| workflows/market_sandbox_loop.yaml | Active | OBSERVE_ONLY |
| workflows/wp2_acceptance.py | Supporting | One-time |
| workflows/wp3_acceptance.py | Supporting | One-time |
| workflows/mission_runtime.py | **AUTHORITATIVE** | Active |
| workflows/council_review.py | **AUTHORITATIVE** | Active |
| workflows/mission_templates/*.yaml (9) | **AUTHORITATIVE** | Active |
| workflows/debate_engine/workflow.yaml | Active | Active |
| pipelines/*/pipeline.py (5) | **AUTHORITATIVE** | Active |
| pipelines/*/pipeline.yaml (10) | **AUTHORITATIVE** | Active |

### 10. Root-Level Documents
| File | Purpose | Status |
|---|---|---|
| AK_MEMORY.md | Master memory record | **AUTHORITATIVE** |
| README.md | Project readme | Supporting |
| akctl.py | CLI tool | **AUTHORITATIVE** |

## Summary Statistics

| Category | Count |
|---|---|
| Laws (canonical) | 13 |
| Governance docs | 20+ |
| Reports | 200+ |
| Reviews | 20+ |
| Registries (Python) | 30+ |
| Registry YAML files | 12+ |
| Services | 36 |
| Architecture/Design | 15+ |
| Specifications | 7+ |
| Workflows | 15+ |
| Pipelines | 10+ |
| Scripts | 16 |
| Tests | 100+ |
