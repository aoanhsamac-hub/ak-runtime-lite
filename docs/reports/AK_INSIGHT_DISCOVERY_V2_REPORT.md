# AK Insight Discovery V2 Report

## Overview
V2 insight discovery engine produced 21 insights across 7 types from 12 signal clusters and signal groups.

## Insight Types

| Type | Count | Description |
|------|-------|-------------|
| PROCESS | 4 | Decision/process-oriented insights |
| SKILL | 2 | Engineering/skill insights |
| RISK | 3 | Risk/anomaly insights |
| GOVERNANCE | 3 | Governance insights |
| MARKET | 3 | Trading/market insights |
| EXECUTION | 3 | Execution insights |
| PERFORMANCE | 3 | Performance/repeatability insights |

## Discovery Methods

### Cluster-based Discovery (12 insights)
Insights derived from signal clusters with evidence weighting and confidence aggregation.

### Direct Signal Discovery (9 insights)
Insights derived directly from signal groups (min 2 signals per group) with duplicate suppression.

## Features
- Evidence weighting per insight
- Confidence scoring (aggregated from source signals)
- Duplicate suppression (signature-based): same title from same cluster type is suppressed
- Traceability to source signal IDs
- Metadata tracking discovery source (cluster vs direct)
