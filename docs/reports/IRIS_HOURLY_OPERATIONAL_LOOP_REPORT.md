# IRIS Hourly Operational Loop Report

**Date:** 2026-06-08

## Workflow

```
Market Snapshot (H1)
    ↓
Feature Extraction
    ↓
Pattern Discovery
    ↓
Forecast Generation
    ↓
Benchmark Storage
    ↓
Accuracy Check (Wait)
    ↓
Lesson Extraction
    ↓
Knowledge Generation
    ↓
Evidence Storage
    ↓
KACE Integration
```

## Services

- iris_data_import_engine.get_market_snapshot()
- iris_feature_extraction_engine.extract_features()
- iris_pattern_discovery_engine.discover_patterns()
- market_forecast_engine.generate_forecast()
- iris_forecast_benchmark_engine.benchmark_forecast()
- market_lesson_engine.extract_lesson()
- market_knowledge_engine.generate_knowledge()

## Cadence

Every 1 hour, 24/7 - read-only observation only.

## Status

OPERATIONAL - awaiting full MT5 connection.