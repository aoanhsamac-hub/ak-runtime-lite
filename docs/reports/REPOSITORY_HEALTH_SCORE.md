# AK Repository Health Score

Authority: Janus Directive WP35.4A | Date: 2026-06-08

## Health Metrics

| Metric | Score | Weight | Weighted |
|---|---|---|---|
| Duplicate documents (% of total) | 15% duplicate → **85/100** | 25% | 21.25 |
| Obsolete documents (% of total) | 5% obsolete → **95/100** | 15% | 14.25 |
| Orphan documents (% of total) | 2% orphan → **98/100** | 10% | 9.80 |
| Registry coverage | 90% → **90/100** | 20% | 18.00 |
| Single source of truth compliance | 70% → **70/100** | 15% | 10.50 |
| Repository structure clarity | 75% → **75/100** | 10% | 7.50 |
| Cross-referencing completeness | 80% → **80/100** | 5% | 4.00 |

## Overall Health Score

**85.3 / 100** — GOOD (needs maintenance)

## Score Breakdown

### Strengths (High Scores)
- **Orphan documents**: Very few truly orphan docs (98/100)
- **Obsolete documents**: Most superseded docs already identified (95/100)
- **Registry coverage**: Most domains have registry (90/100)

### Weaknesses (Low Scores)
- **Single source of truth**: Legal canon mirrors in codex/ and governance/ need consolidation (70/100)
- **Repository structure clarity**: Multiple docs/governance vs docs/legal/canon vs docs/reviews needs cleanup (75/100)

### Improvement Opportunities
- **Duplication (85/100)**: 15% of docs are duplicates, mostly legal mirrors
- **Cross-referencing (80/100)**: Some reports not linked from AK_MEMORY.md

## Detailed Scoring

### 1. Duplicate Document Score: 85/100
| Type | Count | Impact |
|---|---|---|
| Legal canon mirrors | 4 file groups | -5 |
| Report sub-reports | 8 files | -5 |
| Registry duplicates | 2 file groups | -3 |
| Specification superseded | 5 files | -2 |
| **Total deduction** | -15 | - |

### 2. Obsolete Document Score: 95/100
| Type | Count | Impact |
|---|---|---|
| Superseded governance docs | 4 | -2 |
| Superseded specs | 5 | -2 |
| Superseded codex docs | 3 | -1 |
| **Total deduction** | -5 | - |

### 3. Orphan Document Score: 98/100
| Type | Count | Impact |
|---|---|---|
| Unreferenced sovereign docs | 2 | -1 |
| _pytest_tmp dirs | 28 (temp) | -1 |
| **Total deduction** | -2 | - |

### 4. Registry Coverage: 90/100
| Domain | Coverage | Status |
|---|---|---|
| Legal documents | 90% | Covered by sovereign/ |
| Governance | 100% | Covered by governance/ |
| Memory | 100% | Covered by memory/ |
| Skills | 100% | Covered by learning_registry/ |
| Capabilities | 100% | Covered by capability_registry/ |
| Market data | 80% | Covered by market_forecast_registry/ |
| Infrastructure | 60% | Partially covered |
| **Average** | **90%** | - |

### 5. Single Source of Truth: 70/100
| Domain | Compliance | Issue |
|---|---|---|
| Legal framework | 60% | Duplicate codex/governance mirrors |
| Governance | 100% | Python code is authoritative |
| Agent definitions | 100% | agents/identity.py |
| Reports | 70% | Sub-reports exist alongside finals |
| Specifications | 60% | Phase specs alongside unified |

### 6. Structure Clarity: 75/100
| Factor | Score | Note |
|---|---|---|
| Directory naming consistency | 70 | docs/governance vs docs/legal |
| File naming conventions | 80 | Mostly consistent |
| Hierarchy depth | 80 | 3-4 levels acceptable |
| Redundancy | 70 | Multiple index files |

### 7. Cross-Referencing: 80/100
| Factor | Score | Note |
|---|---|---|
| AK_MEMORY.md coverage | 85 | Most files referenced |
| LEGAL_CANON_INDEX coverage | 90 | All laws indexed |
| Report-to-source links | 75 | Some reports not linked |
| Registry-to-document links | 70 | Partial |

## Post-Consolidation Target Score

After applying consolidation plan:
- **Duplicate**: 85 → 95
- **Obsolete**: 95 → 98
- **Orphan**: 98 → 99
- **Registry**: 90 → 95
- **SOT**: 70 → 90
- **Structure**: 75 → 85
- **Cross-ref**: 80 → 90

**Target Overall Score: 93.2 / 100** (EXCELLENT)
