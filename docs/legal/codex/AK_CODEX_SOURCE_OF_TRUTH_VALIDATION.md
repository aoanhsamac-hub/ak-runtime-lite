# AK CODEX SOURCE OF TRUTH VALIDATION

Directive: AK-CODEX-ACCEPTANCE-GATE
Requirement: 4 - Source of Truth Validation
Date: 2026-06-07

## Source Audit

| Location | Active | Deprecated | Archived |
|---|---|---|---|
| `docs/legal/codex/` | ✓ 27 documents | - | - |
| `docs/legal/canon/` | - | - | 8 files (redirect to codex) |
| `sovereign/` | - | - | 11 .docx files (binary archive) |
| `docs/design/` | - | ✓ migrated | - |
| `docs/specifications/` | - | ✓ migrated | - |

## Active Source Determination

**ACTIVE SOURCE: `docs/legal/codex/`**
- All canonical legal documents
- All naming compliant
- All registry documentation

**ARCHIVED SOURCES:**
- `docs/legal/canon/` - Redirect to codex, marked for deprecation
- `sovereign/` - Binary .docx files preserved as historical archive
- `docs/design/`, `docs/specifications/` - Migrated, no longer active

## Evidence

- All text-based legal documents unified in codex/
- No conflicting legal meanings
- Binary files preserved with canonical representations
- Redirect created for legacy paths

## Result

**PASS** - Exactly one active legal source exists (`docs/legal/codex/`).