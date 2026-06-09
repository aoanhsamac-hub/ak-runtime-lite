"""Market Intelligence Cycle - Hourly forecast generation."""

from datetime import datetime, timezone


def run_cycle(symbols: list[str] | None = None, timeframes: list[str] | None = None) -> dict:
    from services.market_forecast_engine import generate_all_forecasts

    symbols = symbols or ["XAUUSDm", "EURUSDm", "GBPUSDm"]
    timeframes = timeframes or ["H1", "H4"]

    forecasts = generate_all_forecasts(symbols, timeframes)

    return {
        "cycle": "market_intelligence",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "forecasts_generated": len(forecasts),
        "forecast_ids": [f.get("forecast_id") for f in forecasts],
        "status": "completed",
    }


if __name__ == "__main__":
    result = run_cycle()
    print(f"Market Intelligence Cycle: {result['forecasts_generated']} forecasts generated")