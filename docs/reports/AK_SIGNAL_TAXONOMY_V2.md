# AK Signal Taxonomy V2

## Overview
Expanded from 5 to 10 signal types for comprehensive knowledge extraction.

## Signal Types

| # | Type | Source | Description |
|---|------|--------|-------------|
| 1 | PATTERN | lessons, skills | High-confidence recurring patterns (score >= 70) |
| 2 | ANOMALY | traces | Failed/error outcomes |
| 3 | REPEATABILITY | traces | Successful, repeatable outcomes |
| 4 | GOVERNANCE | lessons | High-quality validated lessons (quality >= 4, validation >= 3) |
| 5 | DATASET | lessons, datasets | Domain-specific knowledge |
| 6 | DECISION | lessons, traces | Decision-making evidence (outcome_evidence >= 3) |
| 7 | EXECUTION | lessons, traces | Execution-related knowledge (source_path contains "exec") |
| 8 | RISK | lessons | Risk/Security knowledge (source_path contains "risk"/"security") |
| 9 | TRADING | lessons | Trading/Market knowledge (source_path contains "trade"/"market") |
| 10 | PERFORMANCE | lessons, skills | High-reuse knowledge (reuse_value >= 4) |

## Extraction Rules
| Signal Type | Condition | Source Kind |
|-------------|-----------|-------------|
| PATTERN | confidence_score >= 70 | lesson, skill |
| ANOMALY | outcome contains "fail" or "error" | trace |
| REPEATABILITY | outcome is successful | trace |
| GOVERNANCE | source_quality >= 4 AND validation_level >= 3 | lesson |
| DATASET | domain present OR source_kind == "dataset" | lesson, dataset |
| DECISION | outcome_evidence >= 3 OR trace | lesson, trace |
| EXECUTION | source_path contains "exec" | lesson, trace |
| RISK | source_path contains "risk" or "security" | lesson |
| TRADING | source_path contains "trade"/"market" OR domain | lesson |
| PERFORMANCE | reuse_value >= 4 OR skill | lesson, skill |
