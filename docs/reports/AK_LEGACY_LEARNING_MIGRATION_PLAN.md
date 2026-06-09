# AK Legacy Learning Migration Plan

Date: 2026-06-07 | Authority: Janus Directive — AK-SANDBOX-READINESS & LEGACY LEARNING MIGRATION AUDIT v1.0

## Migration Strategy

Phase 1: Dry-run audit (completed by `scripts/audit_legacy_learning.py`)
Phase 2: Quarantine import (safe knowledge artifacts only)
Phase 3: Sage review of imported artifacts
Phase 4: Hermes distillation into AK-native lessons
Phase 5: Promotion through standard lifecycle

## Phase 2 — Quarantine Import Candidates

| Recommendation | Count | Description |
|---|---|---|
| APPROVED_FOR_REVIEW | 16 | Markdown docs, JSON data, YAML configs — safe for direct review |
| QUARANTINE_IMPORT | 27 | Python/PS1 scripts — knowledge must be extracted, code discarded |
| REQUIRES_SAGE_REVIEW | 24 | Mixed content requiring governance assessment |
| DO_NOT_IMPORT | 0 | None rejected |

## Import Rules

### Allowed imports (to quarantine):
- Normalized knowledge artifacts (markdown, JSON, YAML)
- Skill templates
- Governance rules (as reference)
- Market intelligence reports

### Forbidden imports:
- Python runtime code (must NOT be placed in `agents/`, `execution/`, `connectors/`, `governance/`, `sovereign/`)
- Scripts containing executable trading logic
- Any file containing credential patterns

## Target Registry Mapping

| Category | Target AK Registry |
|---|---|
| GOVERNANCE | governance/registries/ (as reference) |
| LESSON | memory/lesson_registry (via Hermes distillation) |
| SKILL | memory/skill_registry (templates only) |
| CAPABILITY | memory/capability_registry (metadata only) |
| MEMORY | memory/legacy_corpus/quarantine/ |
| DATASET | memory/dataset_registry (as reference) |
| DECISION_TRACE | memory/decision_trace_registry |
| MARKET_INTELLIGENCE | memory/legacy_corpus/quarantine/ |
| ENGINEERING_KNOWLEDGE | memory/legacy_corpus/quarantine/ |
| INFRASTRUCTURE_KNOWLEDGE | memory/legacy_corpus/quarantine/ |

## Execution

Run: `python scripts/audit_legacy_learning.py --import-quarantine`

Legacy Learning Migration: **DRY_RUN_COMPLETE**
