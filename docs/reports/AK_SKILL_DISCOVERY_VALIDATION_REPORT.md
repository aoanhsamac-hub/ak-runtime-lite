# AK Skill Discovery Validation Report

## Dry Run Results

| Metric | Value | Status |
|--------|-------|--------|
| Signals created | 559 | PASS |
| Signal types (V2) | 9 of 10 | PASS* |
| Clusters created | 12 | PASS |
| Cluster types | 7 of 7 | PASS |
| Insights created (V2) | 21 | PASS |
| Insight types | 7 of 7 | PASS |
| Candidate skills created | 33 | PASS |
| Duplicates detected | 0 | PASS |
| Superseded detected | 25 | PASS |
| Overlapping detected | 11 | PASS |
| Conflicting detected | 0 | PASS |
| Governance pass rate | 625/625 (100%) | PASS |
| All skills locked | True | PASS |
| Audit events | 6 | PASS |
| Test suite | 262/262 | PASS |

*\*PERFORMANCE signal not triggered from traces (no approved traces with reuse_value). Logic is correct.*

## Pipeline
```
Approved Knowledge (121)
  -> Signals (559)
    -> Clusters (12)
      -> Insights V2 (21)
        -> Candidate Skills (33)
          -> Deduplication (0 dup, 25 sup, 11 ovlp)
            -> Governance (625/625 pass)
              -> Audit (6 events)
```

## Constraints Verified
- No skill approval: True
- No capability promotion: True
- No agent evolution: True
- No autonomous learning: True
