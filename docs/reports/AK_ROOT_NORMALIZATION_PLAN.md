# AK Root Normalization Plan

## Current Location -> Canonical Destination Mapping

| Current Location | Canonical Destination | Reason | Action |
|------------------|----------------------|--------|--------|
| .env | archive/.env.2026-06-07 | Contains potential secrets; should be .env.example template if needed | MOVE to archive/ with lineage metadata |
| LEGAL_DISCOVERY_RAW.csv | archive/LEGAL_DISCOVERY_RAW.csv.2026-06-07 | Raw discovery data should be preserved in archive | MOVE to archive/ with lineage metadata |
| Openrouter LLM.md | docs/governance/Openrouter_LLM_Configuration.md | LLM configuration belongs in governance documentation | MOVE to docs/governance/ |
| _pytest_tmp/ | (to be cleaned) | Temporary pytest cache directory | CONTENTS: DELETE after verifying no active processes use it; DIRECTORY: KEEP in .gitignore |
| Project_docs/ | docs/legacy/ or archive/Project_docs.2026-06-07/ | Legacy documentation - evaluate for consolidation or archiving | EVALUATE: If useful content exists, MOVE to docs/legacy/; if obsolete, ARCHIVE entirely |

## Detailed Migration Procedures

### 1. Environment File Handling
- **Current**: .env (root)
- **Analysis**: File appears to contain environment variables, potentially including secrets
- **Action**: 
  - If contains actual secrets: Move to archive/ with timestamp and create .env.example template
  - If is template: Rename to .env.example and keep in root
  - Lineage metadata: Record original location, date moved, and reason

### 2. Legal Discovery Data
- **Current**: LEGAL_DISCOVERY_RAW.csv (root)
- **Analysis**: Raw CSV data from legal discovery process
- **Action**: 
  - Move to archive/ with timestamp suffix
  - Create README.md in archive directory explaining the data origin
  - Preserve original filename for auditability

### 3. LLM Configuration Documentation
- **Current**: Openrouter LLM.md (root)
- **Analysis**: Documentation about LLM configuration
- **Action**:
  - Move to docs/governance/ directory
  - Rename to be more descriptive: Openrouter_LLM_Configuration.md
  - Ensure proper markdown formatting and links

### 4. pytest Temporary Directory
- **Current**: _pytest_tmp/ (root)
- **Analysis**: Temporary directory created by pytest
- **Action**:
  - Verify no active testing processes are using this directory
  - If safe: Delete contents
  - Ensure _pytest_tmp/ is listed in .gitignore to prevent future accumulation
  - Keep directory structure but empty

### 5. Legacy Project Documentation
- **Current**: Project_docs/ (root)
- **Analysis**: Directory containing legacy project documentation
- **Action**:
  - Survey contents for value and duplication with existing docs/
  - If contains unique valuable content: 
    - Create docs/legacy/ directory if it doesn't exist
    - Move valuable files to docs/legacy/ preserving subdirectory structure
  - If contents are obsolete or duplicated:
    - Archive entire directory to archive/Project_docs.2026-06-07/
    - Create README.md in archive explaining origin and date

## Implementation Order
1. Handle _pytest_tmp/ (safest, lowest risk)
2. Move Openrouter LLM.md to docs/governance/
3. Archive LEGAL_DISCOVERY_RAW.csv
4. Process .env file (careful with potential secrets)
5. Evaluate and process Project_docs/ (requires content analysis)

## Verification Checklist
- [ ] No unauthorized files remain in root after migration
- [ ] All moved files have proper lineage metadata in archive/
- [ ] No data loss during migration
- [ ] Root directory contains only canonical items:
  - README.md, LICENSE, pyproject.toml, requirements.txt
  - .env.example (if applicable)
  - .gitignore
  - AK entrypoint files (ak.bat, law.bat)
  - Approved governance root files
  - Approved system directories (agents, archive, docs, governance, memory, scripts, tests, etc.)

## Lineage Metadata Template for Archive Items
For each item moved to archive/, create accompanying metadata:
```
# Archive Lineage Metadata
Original Location: [relative path from repo root]
Move Date: [YYYY-MM-DD]
Moved By: [OpenCode/auto-normalization]
Reason: [brief explanation]
Contents Description: [summary of what was moved]
Access Instructions: [how to retrieve if needed]
```