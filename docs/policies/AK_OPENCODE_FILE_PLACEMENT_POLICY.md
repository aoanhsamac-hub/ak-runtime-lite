# AK OpenCode File Placement Policy

Directive: WP-REPO-HYGIENE-01 | Date: 2026-06-08
Authority: Repo Governance Decree, Knowledge Governance Decree

## Purpose

Prevent root pollution and enforce canonical file placement when OpenCode creates files.

## Mandatory Rules

### 1. Root Creation Prohibited
OpenCode may NOT create new files or directories in the repository root. Only the following may exist at root:
- README.md, pyproject.toml, requirements.txt, .gitignore, .env.example
- Directories: agents/, archive/, connectors/, data/, docs/, execution/, governance/, learning/, memory/, pipelines/, scripts/, services/, sovereign/, tests/, tools/, workflows/

### 2. Canonical Placement
| File Type | Destination | Legal Basis |
|---|---|---|
| Reports | docs/reports/ | Knowledge Governance Decree |
| Reviews | docs/reviews/ | Knowledge Governance Decree |
| Designs | docs/design/ | Knowledge Governance Decree |
| Architecture | docs/architecture/ | Knowledge Governance Decree |
| Roadmaps | docs/roadmaps/ | Knowledge Governance Decree |
| Scripts | scripts/ | Repo Governance Decree |
| Tools | tools/ | Repo Governance Decree |
| Tests | tests/ | Repo Governance Decree |
| Services | services/ | Repo Governance Decree |
| Pipelines | pipelines/ | Repo Governance Decree |
| Memory registries | memory/ | Memory Law |
| Governance registries | governance/registries/ | Repo Governance Decree |
| Audit logs | governance/audit/ | Audit Governance |
| Archives | archive/ | Retention Governance Decree |
| Legal documents | docs/legal/canon/ | Constitution |
| Policies | docs/policies/ | Knowledge Governance Decree |
| Workflows | workflows/ | Repo Governance Decree |

### 3. Temporary Files
Temporary files must go to `archive/tmp/` or an approved workspace directory. They must not remain at root.

### 4. Classification Required
Before creating any file, OpenCode must:
1. Classify the file type
2. Verify target directory exists
3. Confirm no equivalent file already exists
4. Create in the approved destination only

### 5. Uncertain Files
If a file cannot be classified into any category above, OpenCode MUST stop and request classification. Do not create unclassified files at root.

### 6. Governance Gate
Root hygiene test (`tests/test_root_hygiene.py`) will fail if unauthorized root files or directories exist. This gate runs automatically.

## Enforcement

| Check | How |
|---|---|
| Automated test | tests/test_root_hygiene.py |
| File placement rules | This policy |
| Registry update | memory/archive_registry/archive_index.yaml |

## Violation Consequences

Violation of this policy requires:
1. Immediate relocation to approved destination
2. Archive of any temporary artifacts
3. Update of archive registry
4. Root hygiene test re-verification
