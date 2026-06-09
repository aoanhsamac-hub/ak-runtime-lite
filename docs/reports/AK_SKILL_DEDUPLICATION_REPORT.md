# AK Skill Deduplication Report

## Overview
Deduplication engine analyzed 33 candidate skills for duplicates, overlaps, and conflicts.

## Results

| Status | Count | Description |
|--------|-------|-------------|
| Unique | 12 | No issues detected |
| Superseded | 25 | Name is a subset of another skill |
| Overlapping | 11 | Significant word overlap |
| Duplicate | 0 | Exact name matches |
| Conflicting | 0 | Conflict markers detected |

## Detection Methods

### Duplicate Detection
Exact name match between any two skills.

### Superseded Detection
One skill name is a subset of another (significant words only, stop words filtered).

### Overlap Detection
Skills sharing >= 50% of significant words.

### Conflict Detection
Skills with opposing directive markers (avoid/never vs allow/always).

## No Automatic Merge
All deduplication results are advisory. No skills are automatically merged, deleted, or modified.
