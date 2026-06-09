# AK Market Sandbox-01 Execution Plan

Date: 2026-06-07 | Authority: Janus Directive — MT5 DEMO MARKET OBSERVATION & ZONE VALIDATION LOOP

## Components Built

| Component | Path | Status |
|---|---|---|
| MT5 Demo Observer | connectors/mt5/mt5_demo_observer.py | OBSERVE_ONLY |
| Market Snapshot Collector | intelligence/iris/market_snapshot.py | ACTIVE |
| Zone Detector | intelligence/iris/zone_detector.py | ACTIVE |
| Forecast Engine | intelligence/iris/zone_validation_engine.py | ACTIVE |
| Forecast Registry | memory/market_forecast_registry.py | ACTIVE |
| Zone Validation Registry | memory/zone_validation_registry.py | ACTIVE |
| MT5 Health Monitor | infrastructure/yet_kieu/mt5_health_monitor.py | ACTIVE |
| Sandbox Loop Workflow | workflows/market_sandbox_loop.yaml | OBSERVE_ONLY |

## Agent Responsibilities

- Yết Kiêu: MT5 health + data quality
- Iris: Zone detection + forecast generation
- Helen: Challenge macro sessions
- Sage: Review risk, block unsafe
- Janus: Consolidate decisions
- Hermes: Store evidence + lessons

## Activation Status

- Mode: OBSERVE_ONLY
- No execution functions called
- All order actions return `error: blocked`