# AK Repository Dependency Map

Authority: Janus Directive WP35.4A

## Knowledge Flow

```
Laws (canon/) → Governance (governance/) → Memory (memory/) → Services (services/) → Pipelines (pipelines/) → Reports (docs/reports/)
                    ↓                           ↗
              Sovereign Registries → AK_MEMORY.md (master index)
```

## Cross-Reference Map

### 1. Legal → Governance Dependencies
| Source | References | Type |
|---|---|---|
| ALKASIK_CONSTITUTION v1.1 | governance/policy_engine.py | Authority chain |
| ALKASIK_AGENT_LAW | agents/identity.py | Agent authority |
| ALKASIK_MEMORY_LAW | memory/*.py | Memory governance |
| ALKASIK_EXECUTION_LAW | connectors/mt5/*.py | Execution prohibition |
| ALKASIK_REPO_GOVERNANCE_DECREE | governance/governance_gate.py | Change control |
| LEGAL_CANON_INDEX | All legal docs | Master index |

### 2. Governance → Runtime Dependencies
| Source | References | Type |
|---|---|---|
| governance/gate.py | agents/runtime.py | Runtime gate call |
| governance/approval_engine.py | agents/role_boundary.py | Role validation |
| governance/audit_engine.py | agents/audit_hook.py | Audit trail |
| protected_modules.yaml | connectors/filesystem_connector.py | Path protection |

### 3. Memory → Service Dependencies
| Source | References | Type |
|---|---|---|
| lancedb_adapter.py | kingdom_memory_platform.py | Backend |
| kingdom_memory_platform.py | All registries | Platform |
| memory_interface.py | agent_memory.py, learning_runtime.py | Interface |
| learning_registry/ (8 registries) | services/*skill*.py | Skill pipeline |
| capability_pipeline/ (4 registries) | services/*capability*.py | Cap pipeline |
| learning_runtime.py | agents/runtime.py | Agent integration |

### 4. Service → Pipeline → Report Dependencies
| Source | References | Type |
|---|---|---|
| services/learning_signal_engine.py | pipelines/skill_discovery/ | Orchestration |
| services/skill_discovery_engine.py | pipelines/skill_discovery/ | Orchestration |
| services/capability_validation_engine.py | pipelines/capability_evolution/ | Orchestration |
| All services | docs/reports/ | Output reports |

### 5. Agent → Runtime Dependencies
| Source | References | Type |
|---|---|---|
| agents/runtime.py → BaseAgent | memory/learning_runtime.py | Mission output |
| agents/iris/agent.py | connectors/mt5/*.py | Market observation |
| agents/hermes/agent.py | memory/*.py | Memory operations |
| agents/janus/agent.py | workflows/*.py | Council/coordination |

### 6. Duplicate/Mirror References
| Original | Mirror(s) | Action |
|---|---|---|
| docs/legal/canon/ (13 files) | docs/legal/codex/constitution/, docs/governance/ | MIRROR |
| docs/design/ (7+ models) | docs/reports/AK_*_MODEL.md | OVERLAP |
| governance/registries/*.yaml | sovereign/registries/*.yaml | OVERLAP (needs merge) |
| LEGAL_CANON_INDEX | sovereign/legal_index.yaml, codex/registries/LEGAL_REGISTRY.yaml | TRIPLE INDEX |

## Dependency Graph Summary

```
canon/ ──→ sovereign/registries/
   │           │
   ↓           ↓
governance/ ─→ codex/
   │
   ↓
agents/ ──→ runtime/ ──→ memory/
   │                        │
   ↓                        ↓
services/ ──────────────→ pipelines/ ──→ docs/reports/
   │
   ↓
connectors/ (mt5, llm, filesystem, git)
```
