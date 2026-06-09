# AK Signal Clustering Report

## Overview
Clustering engine groups 559 signals into 12 clusters across 7 cluster types.

## Cluster Types and Counts

| Cluster Type | Count | Signals Covered |
|-------------|-------|----------------|
| DECISION | 2 | 107 decision signals |
| ENGINEERING | 1 | 218 pattern+dataset signals |
| EXECUTION | 2 | 3 execution signals |
| GOVERNANCE | 2 | 101 governance signals |
| MEMORY | 1 | 94 repeatability+performance signals |
| RISK | 2 | 4 risk+anomaly signals |
| TRADING | 2 | 32 trading signals |

## Clustering Methods

### Type-based Clustering
Groups signals by their mapped cluster type (DECISION, TRADING, RISK, EXECUTION, GOVERNANCE, ENGINEERING, MEMORY).

### Domain-based Clustering
Groups signals sharing tags that represent knowledge domains (agent_knowledge, trading_knowledge, risk_knowledge, execution_knowledge, market_knowledge, engineering_knowledge, memory_knowledge, governance_knowledge).

## Cluster Properties
- Each cluster: source_signal_ids, signal_count, confidence_score (aggregated), evidence, traceability
- All clusters: status=CANDIDATE
- All clusters: governed by 8-gate check
