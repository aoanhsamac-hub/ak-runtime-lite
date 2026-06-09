# AK Legacy Evidence Scoring Report

**Directive:** WP-LKI-01 Phase 4
**Agent:** Lang Lieu
**Date:** 2026-06-07 06:51:14 UTC
**Status:** COMPLETE

## Scoring Method

Each eligible artifact scored on 6 dimensions (0-5 each) combined into a weighted confidence score (0-100):
- source_quality (×4): based on content line count
- validation_level (×4): based on file size
- outcome_evidence (×5): based on presence of result/keywords
- recency (×2): uniform baseline
- reuse_value (×3): based on word count
- risk_sensitivity (×2): inverted penalty for risk keywords

## Score Distribution

| Range | Count |
|-------|-------|
| 10-19 | 1908 |
| 20-29 | 185 |
| 30-39 | 175 |
| 40-49 | 190 |
| 50-59 | 105 |
| 60-69 | 179 |
| 70-79 | 152 |

## Disposition Summary

| Disposition | Threshold | Count |
|-------------|-----------|-------|
| Candidate Accepted | >= 60 | 331 |
| Archive Only | 30-59 | 470 |
| Quarantine | 10-29 | 2093 |
| Rejected | < 10 | 0 |
