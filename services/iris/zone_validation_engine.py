"""Market Forecast Engine - Generate forecasts from zones and market state."""

from datetime import datetime, timezone
from typing import Any


class MarketForecast:
    def __init__(self, forecast_id: str, symbol: str, timeframe: str):
        self.forecast_id = forecast_id
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.symbol = symbol
        self.timeframe = timeframe
        self.price = 0.0
        self.spread = 0.0
        self.session = "unknown"
        self.regime = "unknown"
        self.direction_bias = "neutral"
        self.zone_type = "unknown"
        self.zone_low = 0.0
        self.zone_high = 0.0
        self.entry_logic = ""
        self.invalidation_level = 0.0
        self.tp1 = 0.0
        self.tp2 = 0.0
        self.expected_time_window = "unknown"
        self.confidence_score = 0.0
        self.evidence_count = 0
        self.source_count = 0
        self.iris_rationale = ""
        self.helen_challenge = ""
        self.sage_risk_status = "PENDING_REVIEW"
        self.janus_decision = "PENDING"
        self.status = "PENDING_VALIDATION"

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in vars(self).items() if not k.startswith("_")}


class ZoneValidationEngine:
    def __init__(self):
        self.windows = ["15m", "30m", "60m", "240m", "eod"]

    def validate_forecast(self, forecast: MarketForecast, price_path: list[float]) -> dict[str, Any]:
        zone_touched = any(forecast.zone_low <= p <= forecast.zone_high for p in price_path) if price_path else False
        return {
            "forecast_id": forecast.forecast_id,
            "zone_touched": zone_touched,
            "touch_time": forecast.timestamp if zone_touched else None,
            "direction_correct": False,
            "tp1_hit": False,
            "tp2_hit": False,
            "invalidation_hit": False,
            "max_favorable_excursion": 0.0,
            "max_adverse_excursion": 0.0,
            "false_zone": not zone_touched,
            "spread_penalty": forecast.spread,
            "final_score": 0.0 if not zone_touched else 0.7,
            "validated_at": datetime.now(timezone.utc).isoformat(),
            "status": "validated",
        }


__all__ = ["MarketForecast", "ZoneValidationEngine"]