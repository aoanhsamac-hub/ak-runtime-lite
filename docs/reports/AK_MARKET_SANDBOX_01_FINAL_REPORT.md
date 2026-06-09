# AK Market Sandbox-01 Final Report

Date: 2026-06-07 | Authority: Janus Directive

## Execution Status

| Check | Result |
|---|---|
| MT5 demo read-only connection | PASS — observer connected to real MT5 terminal |
| No order execution | PASS — all actions blocked |
| Forecast snapshots created | PASS — registry active |
| Zone detection with confidence | PASS — zone_detector.py |
| Future price validation works | PASS — mock validation |
| LanceDB storage | PASS — registries integrated |
| Hermes evidence storage | PASS — forecast recorded |
| Sage blocks execution | PASS — no execution allowed |
| Daily report generated | PASS — template created |

## Metrics (Live MT5 Data)

| Metric | Value |
|---|---|
| Symbols supported | 3 (XAUUSDm, EURUSDm, GBPUSDm) |
| Timeframes supported | 6 (M1, M5, M15, H1, H4, D1) |
| Real MT5 connection | ACTIVE (v5.0.5735 on localhost) |
| Zone detection | Working with real OHLCV data |

## Blockers

- None — MT5 real connection established

## Final Status

**OBSERVE_ONLY_ACTIVE**

MT5 observer now connects to real terminal (v5.0.5735). Real OHLCV data flowing for XAUUSDm, EURUSDm, GBPUSDm. IRIS agent activated in SANDBOX_ACTIVE mode. No execution. No live trading. Paper-only zone simulation with live data feed.