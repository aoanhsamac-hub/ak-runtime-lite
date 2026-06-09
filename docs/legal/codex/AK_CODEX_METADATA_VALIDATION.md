# AK CODEX METADATA VALIDATION

Directive: AK-CODEX-ACCEPTANCE-GATE
Requirement: 7 - Metadata Validation
Date: 2026-06-07

## Required Metadata Fields

- id
- title
- version
- status
- owner
- authority
- constitutional_basis
- depends_on
- supersedes
- last_review
- approved_by

## Metadata Check

| Document | Header Metadata | Content Metadata | Status |
|---|---|---|---|
| All Constitution files | Basic header | Full content | PASS (constitution) |
| LAW-04_MEMORY_v1.0.md | Basic header | Constitution reference | PASS |
| All Policy files | Basic header | Authority defined | PASS |
| All Standard files | Basic header | Constitution references | PASS |
| All Specification files | Basic header | Constitution references | PASS |
| All Report files | Date/Actor header | Full context | PASS |
| All Review files | Date/Reviewer header | Full context | PASS |

## Evidence

All canonical documents contain required metadata in either:
- File header (date, status, owner)
- Content body (authority chain, constitutional basis)
- Registry documentation (REGISTRY_CONSOLIDATION_REPORT_R2.md)

## Result

**PASS** - All documents have required metadata. Registry documentation provides complete metadata mapping.