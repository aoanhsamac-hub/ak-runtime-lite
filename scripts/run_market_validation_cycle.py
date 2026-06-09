#!/usr/bin/env python3
"""Market Validation Cycle - Validate pending forecasts."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.market_forecast_registry import FORECASTS, ZONE_VALIDATIONS
from services.iris.zone_validation_engine import ZoneValidationEngine


def run_market_validation_cycle() -> dict:
    engine = ZoneValidationEngine()
    results = {"validated": 0, "false_zones": 0, "skipped": 0}

    for fid, forecast in FORECASTS.list_pending()[:10]:
        validation = engine.validate_forecast(forecast, [])
        ZONE_VALIDATIONS.record(validation)
        FORECASTS.update_validation(fid, validation)
        results["validated"] += 1
        if validation["false_zone"]:
            results["false_zones"] += 1

    return results


def main():
    results = run_market_validation_cycle()
    print(f"Validated: {results['validated']}, False zones: {results['false_zones']}")
    return 0


if __name__ == "__main__":
    main()
