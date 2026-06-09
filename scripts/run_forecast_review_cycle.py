"""Forecast Review Cycle - Compare pending forecasts against reality."""

from datetime import datetime, timezone


def run_cycle(hours_waited: int = 1) -> dict:
    from services.market_forecast_engine import list_pending_forecasts
    from services.forecast_accuracy_engine import calculate_accuracy

    pending = list_pending_forecasts()
    accuracies = []

    for forecast in pending[:10]:
        acc = calculate_accuracy(forecast.get("forecast_id", ""), hours_waited)
        if acc:
            accuracies.append(acc)

    return {
        "cycle": "forecast_review",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "forecasts_compared": len(accuracies),
        "accuracy_ids": [a.get("accuracy_id") for a in accuracies],
        "status": "completed",
    }


if __name__ == "__main__":
    result = run_cycle()
    print(f"Forecast Review Cycle: {result['forecasts_compared']} forecasts compared")