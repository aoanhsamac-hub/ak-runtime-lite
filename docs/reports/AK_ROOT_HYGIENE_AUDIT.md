# AK Repository Root Hygiene Audit

## Inventory of Repository Root

### Files Located at Root

| File | Ownership | Purpose | Recommended Destination | Action |
|------|-----------|---------|-------------------------|--------|
| README.md | Project | Project overview and instructions | Root (CANONICAL) | KEEP |
| .gitignore | Git | Specifies intentionally untracked files to ignore | Root (CANONICAL) | KEEP |
| ak.bat | AK Entrypoint | AK batch script entrypoint | Root (CANONICAL) | KEEP |
| law.bat | AK Entrypoint | Law batch script entrypoint | Root (CANONICAL) | KEEP |
| pyproject.toml | Python | Poetry project configuration | Root (CANONICAL) | KEEP |
| requirements.txt | Python | Python package dependencies | Root (CANONICAL) | KEEP |
| .env | Environment | Environment variables (contains secrets) | Should be .env.example (template) or moved | MOVE to archive/ with lineage metadata |
| LEGAL_DISCOVERY_RAW.csv | Legal Discovery | Raw legal discovery data | archive/ | MOVE to archive/ with lineage metadata |
| Openrouter LLM.md | LLM Configuration | Openrouter LLM configuration | docs/governance/ or scripts/ | MOVE to docs/governance/ |

### Directories Located at Root

| Directory | Ownership | Purpose | Canonical Compliance | Action |
|-----------|-----------|---------|----------------------|--------|
| .pytest_cache | Python/Pytest | Pytest cache directory | Temporary - should be in .gitignore | KEEP (but should be ignored) |
| .venv | Python | Virtual environment | Temporary - should be in .gitignore | KEEP (but should be ignored) |
| agents | AK System | AI agent implementations | Root (APPROVED) | KEEP |
| archive | AK System | Archived materials | Root (APPROVED) | KEEP |
| backups | AK System | Backup files | Root (questionable) | KEEP (but review for archive eligibility) |
| connectors | AK System | External service connectors | Root (APPROVED) | KEEP |
| data | AK System | Data files | Root (APPROVED) | KEEP |
| docs | Documentation | Project documentation | Root (CANONICAL) | KEEP |
| execution | AK System | Execution logs/traces | Root (APPROVED) | KEEP |
| governance | Governance | Governance documents and policies | Root (CANONICAL) | KEEP |
| infrastructure | AK System | Infrastructure configurations | Root (APPROVED) | KEEP |
| intelligence | AK System | Intelligence components | Root (APPROVED) | KEEP |
| interface | AK System | Interface definitions | Root (APPROVED) | KEEP |
| learning | AK System | Learning systems | Root (APPROVED) | KEEP |
| logs | AK System | Log files | Root (APPROVED) | KEEP |
| memory | AK System | Memory storage | Root (CANONICAL) | KEEP |
| pipelines | AK System | Pipeline definitions | Root (APPROVED) | KEEP |
| Project_docs | Documentation | Legacy project documentation | docs/ or archive/ | EVALUATE for MOVE |
| scripts | AK System | Utility scripts | Root (CANONICAL) | KEEP |
| services | AK System | Service implementations | Root (APPROVED) | KEEP |
| sovereign | AK System | Sovereign capabilities | Root (APPROVED) | KEEP |
| tests | Testing | Test files | Root (CANONICAL) | KEEP |
| tools | AK System | Tools and utilities | Root (APPROVED) | KEEP |
| workflows | AK System | Workflow definitions | Root (APPROVED) | KEEP |
| _pytest_tmp | Python/Pytest | Temporary pytest files | Temporary - should be cleaned | MOVE to archive/ or DELETE after verification |

## Root Governance Compliance Assessment

### Compliant Items (Canonically Permitted)
- README.md ✓
- .gitignore ✓
- ak.bat (AK entrypoint) ✓
- law.bat (AK entrypoint) ✓
- pyproject.toml ✓
- requirements.txt ✓
- agents directory (approved system directory) ✓
- archive directory (approved system directory) ✓
- backups directory (questionable but currently permitted) ✓
- connectors directory (approved system directory) ✓
- data directory (approved system directory) ✓
- docs directory (canonical documentation) ✓
- execution directory (approved system directory) ✓
- governance directory (canonical governance) ✓
- infrastructure directory (approved system directory) ✓
- intelligence directory (approved system directory) ✓
- interface directory (approved system directory) ✓
- learning directory (approved system directory) ✓
- logs directory (approved system directory) ✓
- memory directory (canonical memory artifacts) ✓
- pipelines directory (approved system directory) ✓
- scripts directory (canonical scripts) ✓
- services directory (approved system directory) ✓
- sovereign directory (approved system directory) ✓
- tests directory (canonical tests) ✓
- tools directory (approved system directory) ✓
- workflows directory (approved system directory) ✓

### Non-Compliant Items Requiring Action
1. .env - Should be .env.example if template, or contain no secrets
2. LEGAL_DISCOVERY_RAW.csv - Raw data should be archived
3. Openrouter LLM.md - Configuration should be in docs/governance/
4. _pytest_tmp - Temporary directory that should be cleaned
5. Project_docs - Legacy documentation that should be evaluated for proper placement

### Forbidden Patterns Check
- No *_REPORT.md files directly in root ✓
- No *_AUDIT.md files directly in root ✓
- No *_PLAN.md files directly in root ✓
- No *_DESIGN.md files directly in root ✓
- No *_SPEC.md files directly in root ✓
- No *_REVIEW.md files directly in root ✓
- No temp/ directory directly in root ✓
- No tmp/ directory directly in root ✓
- No test/ directory directly in root ✓
- No sandbox/ directory directly in root ✓
- No new_folder/ directory directly in root ✓
- No misc/ directory directly in root ✓
- No output/ directory directly in root ✓
- No results/ directory directly in root ✓

## Recommendations
1. Move .env to archive/ with lineage metadata (or replace with .env.example if it's a template)
2. Move LEGAL_DISCOVERY_RAW.csv to archive/ with lineage metadata
3. Move Openrouter LLM.md to docs/governance/
4. Clean _pytest_tmp directory (contents are temporary)
5. Evaluate Project_docs directory for consolidation into docs/ or archiving