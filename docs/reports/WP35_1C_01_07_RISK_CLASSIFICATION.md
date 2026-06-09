# WP35-1C-01-07: Risk Classification

## Risk Levels
| Level | Code | Description |
|-------|------|-------------|
| Sovereign | LEVEL_0_SOVEREIGN | Human-only decisions |
| Moderate | LEVEL_1_MODERATE | Standard learning operations |
| High | LEVEL_2_HIGH | Agent-affecting skills |
| Critical | LEVEL_3_CRITICAL | System-level changes |

## Risk Distribution in Dry Run
| Risk Level | Signals | Insights | Candidate Skills |
|------------|---------|----------|-----------------|
| LEVEL_1_MODERATE | 323 | 6 | 6 |
| LEVEL_2_HIGH | 0 | 0 | 0 |
| LEVEL_3_CRITICAL | 0 | 0 | 0 |
| LEVEL_0_SOVEREIGN | 0 | 0 | 0 |

All records default to LEVEL_1_MODERATE (standard learning operations).

## Governance Risk Gates
- **risk_appropriate**: Validates risk_level is one of the 4 defined levels
- **no_auto_promotion**: Prevents HIGH/CRITICAL records from being promoted without review
- **SOVEREIGN risk**: Reserved for human-only decisions (no agent autonomy)
- **CRITICAL risk**: Requires full governance review

## Promotion Risk Rules (Deferred to WP35-1C-02)
| Current Status | Promotion Target | Risk Gate |
|---------------|-----------------|-----------|
| CANDIDATE | APPROVED | Requires Sage/Hermes review |
| PENDING_REVIEW | APPROVED | Requires evidence validation |
| DISABLED | ENABLED | Level_2_HIGH+ requires governance |
