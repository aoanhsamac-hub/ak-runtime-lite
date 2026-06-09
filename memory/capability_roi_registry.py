from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class CapabilityROIRegistry:
    def __init__(self, memory_platform: Any):
        self._mp = memory_platform

    def record_roi(self, capability_name: str, value: float = 0.0, cost: float = 0.0,
                   evolution_cost: float = 0.0, evolution_value: float = 0.0,
                   evolution_cycle: int = 0, **extra: Any) -> dict:
        record = {
            "capability_name": capability_name,
            "total_value": value,
            "total_cost": cost,
            "roi": round((value / cost), 4) if cost > 0 else 0.0,
            "usage_count": 0,
            "adoption_status": "not_tracked",
            "retention_class": "CANONICAL",
            "evolution_cost": evolution_cost,
            "evolution_value": evolution_value,
            "evolution_cycle": evolution_cycle,
            "evolution_roi": round((evolution_value / evolution_cost), 4) if evolution_cost > 0 else 0.0,
            "created_at": _utc_now(),
        }
        record.update(extra)
        return self._mp.record_capability_roi(record)

    def record_usage(self, capability_name: str, agent_id: str = "",
                     success: bool = True, evolution_cycle: int = 0, **extra: Any) -> dict:
        record = {
            "capability_name": capability_name,
            "agent_id": agent_id,
            "success": success,
            "usage_count": 0,
            "total_value": 0.0,
            "total_cost": 0.0,
            "retention_class": "OPERATIONAL",
            "evolution_cycle": evolution_cycle,
            "created_at": _utc_now(),
        }
        record.update(extra)
        return self._mp.record_capability_usage(record)

    def get_roi(self, capability_name: str | None = None) -> list[dict]:
        return self._mp.get_capability_roi(capability_name)

    def calculate_roi(self, capability_name: str) -> dict:
        return self._mp.calculate_roi(capability_name)

    def get_usage(self, capability_name: str | None = None) -> list[dict]:
        return self._mp.get_capability_usage(capability_name)

    def summary(self) -> dict:
        all_roi = self.get_roi()
        all_usage = self.get_usage()
        return {
            "total_roi_records": len(all_roi),
            "total_usage_records": len(all_usage),
            "capabilities_tracked": len({r.get("capability_name") for r in all_roi if r.get("capability_name")}),
        }
