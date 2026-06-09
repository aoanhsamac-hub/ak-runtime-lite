# WP35-1C-01-02: Learning Signal Extraction Report

## Overview
Extracted learning signals from 121 approved knowledge records (101 lessons, 4 skills, 10 datasets, 6 traces).

## Signal Distribution

| Signal Type | Count | Percentage |
|-------------|-------|-----------|
| DATASET     | 111   | 34.4%     |
| PATTERN     | 105   | 32.5%     |
| GOVERNANCE  | 101   | 31.3%     |
| REPEATABILITY | 6    | 1.9%      |
| ANOMALY     | 0     | 0.0%      |
| **Total**   | **323** | **100%** |

## Extraction Rules
- **PATTERN**: Lessons/skills with confidence_score >= 70
- **GOVERNANCE**: Lessons with source_quality >= 4 AND validation_level >= 3
- **DATASET**: Per-domain lessons (each tagged with domain) + all approved datasets
- **REPEATABILITY**: Decision traces with successful outcomes
- **ANOMALY**: Decision traces with failed/error outcomes

## Status Verification
- 323/323 signals: status=CANDIDATE
- 323/323 signals: governance pass
- 0 signals attempted autonomous promotion

## Signal Sources
| Source Kind | Signals Extracted |
|-------------|------------------|
| lesson      | 307 (PATTERN+GOVERNANCE+DATASET) |
| skill       | 4 (PATTERN) |
| dataset     | 10 (DATASET) |
| trace       | 6 (REPEATABILITY+ANOMALY) |
