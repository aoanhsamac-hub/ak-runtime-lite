from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agents.runtime_models import CapabilityUsageRecord


USAGE_REGISTRY_PATH = Path(__file__).resolve().parent / "capability_usage_registry.jsonl"


class CapabilityUsageRegistry:
    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path else USAGE_REGISTRY_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record_usage(self, record: CapabilityUsageRecord | dict) -> dict:
        if isinstance(record, CapabilityUsageRecord):
            data = record.to_dict()
        else:
            data = dict(record)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
        return data

    def get_all(self) -> list[dict]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]

    def get_by_agent(self, agent_id: str) -> list[dict]:
        return [r for r in self.get_all() if r.get("agent_id") == agent_id]

    def get_by_capability(self, capability_name: str) -> list[dict]:
        return [r for r in self.get_all() if r.get("capability_name") == capability_name]

    def summary(self) -> dict:
        all_records = self.get_all()
        total = len(all_records)
        successes = sum(1 for r in all_records if r.get("success"))
        agents = set(r.get("agent_id", "") for r in all_records)
        return {
            "total_usages": total,
            "success_count": successes,
            "success_rate": round(successes / total, 4) if total else 0.0,
            "unique_agents": len(agents),
            "agents": sorted(agents),
        }
