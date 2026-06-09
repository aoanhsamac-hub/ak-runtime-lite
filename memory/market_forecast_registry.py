"""Market Forecast Registry - Store forecasts in LanceDB."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class MarketForecastRegistry:
    def __init__(self):
        self._forecasts: dict[str, dict] = {}

    def record(self, forecast: dict) -> dict:
        fid = forecast.get("forecast_id", f"FCST-{len(self._forecasts)}")
        record = {
            **forecast,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "validation_status": "PENDING",
        }
        self._forecasts[fid] = record
        return record

    def get(self, forecast_id: str) -> dict | None:
        return self._forecasts.get(forecast_id)

    def list_pending(self) -> list[dict]:
        return [f for f in self._forecasts.values() if f.get("status") == "PENDING_VALIDATION"]

    def update_validation(self, forecast_id: str, validation: dict) -> dict | None:
        if forecast_id in self._forecasts:
            self._forecasts[forecast_id]["validation_result"] = validation
            self._forecasts[forecast_id]["status"] = "VALIDATED"
            return self._forecasts[forecast_id]
        return None


class ZoneValidationRegistry:
    def __init__(self):
        self._validations: dict[str, dict] = {}

    def record(self, validation: dict) -> dict:
        vid = validation.get("forecast_id", f"VAL-{len(self._validations)}")
        record = {**validation, "recorded_at": datetime.now(timezone.utc).isoformat()}
        self._validations[vid] = record
        return record

    def get(self, forecast_id: str) -> dict | None:
        return self._validations.get(forecast_id)

    def summary(self) -> dict:
        total = len(self._validations)
        validated = sum(1 for v in self._validations.values() if v.get("zone_touched"))
        false_zones = total - validated
        return {"total": total, "validated": validated, "false_zones": false_zones, "accuracy_rate": validated / total if total else 0}


FORECASTS = MarketForecastRegistry()
ZONE_VALIDATIONS = ZoneValidationRegistry()

__all__ = ["MarketForecastRegistry", "ZoneValidationRegistry", "FORECASTS", "ZONE_VALIDATIONS"]