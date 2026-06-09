from __future__ import annotations

from typing import Any

from memory.learning_registry.schemas import InsightRecord


class InsightRegistry:
    table_name = "insights"

    def __init__(self, adapter=None):
        self.adapter = adapter
        self._records: dict[str, InsightRecord] = {}
        self._hydrate()

    def _hydrate(self) -> None:
        if not self.adapter:
            return
        rows = self.adapter.all(self.table_name)
        for row in rows:
            try:
                filtered = {k: v for k, v in row.items() if k in InsightRecord.__dataclass_fields__}
                record = InsightRecord(**filtered)
                self._records[record.insight_id] = record
            except (TypeError, ValueError):
                continue

    def create_candidate(self, **payload) -> InsightRecord:
        record = InsightRecord(**payload)
        self._save(record)
        return record

    def get(self, insight_id: str) -> InsightRecord:
        try:
            return self._records[insight_id]
        except KeyError as exc:
            raise KeyError(f"insight not found: {insight_id}") from exc

    def list_all(self, offset: int = 0, limit: int = 0,
                 insight_type: str | None = None,
                 owner_agent: str | None = None) -> list[InsightRecord]:
        records = list(self._records.values())
        if insight_type:
            records = [r for r in records if r.insight_type == insight_type]
        if owner_agent:
            records = [r for r in records if r.owner_agent == owner_agent]
        if limit > 0:
            records = records[offset:offset + limit]
        elif offset > 0:
            records = records[offset:]
        return records

    def _save(self, record: InsightRecord) -> None:
        self._records[record.insight_id] = record
        if self.adapter:
            self.adapter.insert(self.table_name, [record.to_dict()])
