from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agents.runtime_models import EvidenceRecord


EVIDENCE_REGISTRY_PATH = Path(__file__).resolve().parent / "evidence_registry.jsonl"


class EvidenceRegistry:
    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path else EVIDENCE_REGISTRY_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record_evidence(self, record: EvidenceRecord | dict) -> dict:
        if isinstance(record, EvidenceRecord):
            data = record.to_dict()
        else:
            data = dict(record)
        if "classification" in data and hasattr(data.get("classification"), "value"):
            data["classification"] = data["classification"].value
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
        return data

    def get_all(self) -> list[dict]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]

    def get_by_agent(self, agent_id: str) -> list[dict]:
        return [r for r in self.get_all() if r.get("source_agent") == agent_id]

    def get_by_mission(self, mission_id: str) -> list[dict]:
        return [r for r in self.get_all() if r.get("mission_id") == mission_id]

    def summary(self) -> dict:
        all_records = self.get_all()
        return {
            "total_evidence": len(all_records),
            "unique_agents": len(set(r.get("source_agent", "") for r in all_records)),
            "classifications": list(set(r.get("classification", "") for r in all_records)),
        }
