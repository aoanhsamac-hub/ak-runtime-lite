#!/usr/bin/env python3
"""Market Daily Report Generator."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.market_forecast_registry import FORECASTS, ZONE_VALIDATIONS
from datetime import datetime, timezone


def run_market_daily_report() -> dict:
    summary = ZONE_VALIDATIONS.summary()
    return {"date": datetime.now(timezone.utc).date().isoformat(), "zone_accuracy": summary}


def main():
    report = run_market_daily_report()
    print(f"Market Daily Report: {report['date']}")
    print(f"Zone accuracy: {report['zone_accuracy']}")
    return 0


if __name__ == "__main__":
    main()