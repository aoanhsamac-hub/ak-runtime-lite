# AK Root Hygiene Gate Report

Directive: WP-REPO-HYGIENE-01 | Date: 2026-06-08

## Gate Description

The Root Hygiene Gate is an automated test suite that verifies the repository root contains only approved files and directories.

## Test Details

| Test | File | Purpose |
|---|---|---|
| test_no_unauthorized_root_directories | tests/test_root_hygiene.py | Fails if any unapproved directory exists at root |
| test_no_unauthorized_root_files | tests/test_root_hygiene.py | Fails if any unapproved file exists at root |
| test_hidden_directories_are_allowed | tests/test_root_hygiene.py | Fails if any hidden directory not in allowlist |

## Allowed Root Structure (Explicit)

### Directories
agents/, archive/, connectors/, data/, docs/, execution/, governance/, learning/, memory/, pipelines/, scripts/, services/, sovereign/, tests/, tools/, workflows/

### Hidden Directories
.venv/, .pytest_cache/, .git/

### Files
README.md, pyproject.toml, requirements.txt, .gitignore, .env.example

## Gate Status

**ACTIVE** — Any new unauthorized root file or directory will cause test failure.

## Command

```powershell
python -m pytest tests/test_root_hygiene.py -v
```
