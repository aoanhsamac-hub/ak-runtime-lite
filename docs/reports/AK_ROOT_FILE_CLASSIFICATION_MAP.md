# AK Root File Classification Map

Directive: WP-REPO-HYGIENE-01 | Date: 2026-06-08

## Classification Categories

| Code | Category | Destination |
|---|---|---|
| REPORT | Report/Memory | docs/reports/ |
| REVIEW | Review/Audit | docs/reviews/ |
| SCRIPT | Runnable script | scripts/ |
| TOOL | CLI tool | tools/ |
| SERVICE | Service/business logic | services/ |
| CONNECTOR | Connector/adapter | connectors/ |
| TEMPORARY | Temp/scratch file | archive/root_hygiene/ |
| ARCHIVE | Empty/superseded dir | archive/ |
| CACHE | Cache | Keep in place |

## File Classification

| Path | Classification | Target Destination | Risk |
|---|---|---|---|
| .pytest_cache/ | CACHE | Keep (hidden cache) | NONE |
| .venv/ | CACHE | Keep (virtual environment) | NONE |
| .env.example | CONFIG | Keep (approved config template) | LOW |
| .gitignore | CONFIG | ALLOWED (approved root file) | NONE |
| ak.bat | SCRIPT | scripts/ | LOW |
| akctl.py | TOOL | tools/ | LOW |
| AK_MEMORY.md | REPORT | docs/reports/ | MEDIUM |
| ARCHIVE_RECOMMENDATIONS.md | REPORT | docs/reports/ | LOW |
| DUPLICATE_ANALYSIS.md | REPORT | docs/reports/ | LOW |
| FINAL_CONSOLIDATION_REPORT.md | REPORT | docs/reports/ | LOW |
| KNOWLEDGE_CONSOLIDATION_PLAN.md | REPORT | docs/reports/ | LOW |
| law.bat | SCRIPT | scripts/ | LOW |
| MERGE_RECOMMENDATIONS.md | REPORT | docs/reports/ | LOW |
| pyproject.toml | CONFIG | ALLOWED (approved root file) | NONE |
| README.md | DOC | ALLOWED (approved root file) | NONE |
| REPOSITORY_DEPENDENCY_MAP.md | REPORT | docs/reports/ | LOW |
| REPOSITORY_HEALTH_SCORE.md | REPORT | docs/reports/ | LOW |
| REPOSITORY_INVENTORY.md | REPORT | docs/reports/ | LOW |
| requirements.txt | CONFIG | ALLOWED (approved root file) | NONE |
| test.txt | TEMPORARY | archive/root_hygiene/ | LOW |
| UPDATED_REGISTRY_STRUCTURE.md | REPORT | docs/reports/ | LOW |

## Directory Classification

| Path | Classification | Target Destination | Risk |
|---|---|---|---|
| _pytest_tmp/ | TEMPORARY | archive/root_hygiene/20260608_120000/ | LOW |
| audit_output/ | TEMPORARY | archive/root_hygiene/20260608_120000/ | LOW |
| backups/ | ARCHIVE | archive/ | LOW |
| infrastructure/ | CONNECTOR | connectors/mt5/ | LOW |
| intelligence/ | SERVICE | services/iris/ | **HIGH** (imports) |
| interface/ | TOOL | tools/dashboard/ | LOW |
| logs/ | ARCHIVE | archive/ | LOW |
