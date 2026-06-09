#!/usr/bin/env python3
"""MT5 Demo Sandbox Scan - OBSERVE ONLY, NO EXECUTION."""

import os
import sys

os.environ["MT5_VPS_HOST"] = "localhost"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from connectors.mt5.mt5_demo_observer import MT5DemoObserver
from services.iris.market_snapshot import MarketSnapshotCollector
from services.iris.zone_detector import ZoneDetector
from memory.market_forecast_registry import FORECASTS


def run_market_sandbox_scan(symbols: list[str], timeframes: list[str]) -> dict:
    results = {"scans": 0, "zones": 0, "forecasts": 0, "errors": []}

    observer = MT5DemoObserver()
    observer.connect()
    collector = MarketSnapshotCollector(observer)
    detector = ZoneDetector()

    for symbol in symbols:
        for tf in timeframes:
            try:
                snap = collector.collect(symbol, tf, count=100)
                zones = detector.detect(snap.ohlcv, symbol, tf) if snap.ohlcv else []
                results["scans"] += 1
                results["zones"] += len(zones)
                for zone in zones:
                    forecast = {
                        "forecast_id": f"FCST-{symbol}-{tf}-{len(FORECASTS._forecasts)}",
                        "symbol": symbol,
                        "timeframe": tf,
                        "zone_type": zone["zone_type"],
                        "zone_low": zone["zone_low"],
                        "zone_high": zone["zone_high"],
                        "confidence_score": zone["confidence_score"],
                        "evidence_count": zone["evidence_count"],
                    }
                    FORECASTS.record(forecast)
                    results["forecasts"] += 1
            except Exception as e:
                results["errors"].append(f"{symbol}/{tf}: {e}")
    observer.disconnect()
    return results


def main():
    symbols = ["XAUUSDm", "EURUSDm", "GBPUSDm", "USDJPYm"]
    timeframes = ["M5", "M15"]
    results = run_market_sandbox_scan(symbols, timeframes)
    print(f"Scans: {results['scans']}, Zones: {results['zones']}, Forecasts: {results['forecasts']}")
    if results["errors"]:
        print(f"Errors: {results['errors']}")
    return 0


if __name__ == "__main__":
    main()
