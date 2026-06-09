"""Zone Validation Registry - Store zone validation results."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


ZONE_VALIDATIONS: dict[str, dict] = {}


class ZoneValidationRegistry:
    def __init__(self):
        self._validations = ZONE_VALIDATIONS

    def record(self, validation: dict) -> dict:
        fid = validation.get("forecast_id", f"ZONE-VAL-{len(self._validations)}")
        record = {**validation, "recorded_at": datetime.now(timezone.utc).isoformat()}
        self._validations[fid] = record
        return record

    def get(self, forecast_id: str) -> dict | None:
        return self._validations.get(forecast_id)

    def list_all(self) -> list[dict]:
        return list(self._validations.values())

    def summary(self) -> dict:
        total = len(self._validations)
        if total == 0:
            return {"total": 0, "zone_touched": 0, "false_zone_rate": 0.0}
        touched = sum(1 for v in self._validations.values() if v.get("zone_touched"))
        return {"total": total, "zone_touched": touched, "false_zone_rate": (total - touched) / total}


__all__ = ["ZoneValidationRegistry", "ZONE_VALIDATIONS"]