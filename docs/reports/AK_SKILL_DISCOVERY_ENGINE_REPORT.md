# AK Skill Discovery Engine Report

## Overview
Skill Discovery Engine produced 33 candidate skills from 21 insights and 12 clusters.

## Skill Categories

| Category | Skills | Source |
|----------|--------|--------|
| Trading Skills | 5 | MARKET insights + TRADING clusters |
| Risk Skills | 5 | RISK insights + RISK clusters |
| Execution Skills | 4 | EXECUTION insights + EXECUTION clusters |
| Governance Skills | 4 | GOVERNANCE insights + GOVERNANCE clusters |
| Memory Skills | 3 | PERFORMANCE insights + MEMORY clusters |
| Engineering Skills | 8 | SKILL insights + ENGINEERING clusters |
| Agent Skills | 4 | PROCESS insights + DECISION clusters |

## Discovery Methods

### From Insights (21 skills)
Each insight generates one candidate skill with full traceability:
- source_insight_ids -> source_signal_ids -> source_lesson_ids
- Evidence includes discovery_method="insight" and insight_type

### From Clusters (12 skills)
Each cluster generates one candidate skill directly:
- source_signal_ids -> source_lesson_ids
- Evidence includes discovery_method="cluster" and cluster_type

## Status
- 33/33: status=CANDIDATE
- 33/33: approval_status=PENDING_REVIEW
- 33/33: activation_status=DISABLED
- 0 autonomous promotions
