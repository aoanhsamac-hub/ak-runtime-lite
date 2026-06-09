from __future__ import annotations

from typing import Any

from memory.lancedb_adapter import LanceDBAdapter
from memory.schemas import DatasetRecord


class DatasetRegistry:
    table_name = "datasets"

    def __init__(self, adapter: LanceDBAdapter):
        self.adapter = adapter
        self._records: dict[str, DatasetRecord] = {}
        self._hydrate()

    def _hydrate(self) -> None:
        rows = self.adapter.all(self.table_name)
        for row in rows:
            try:
                record = DatasetRecord(**{k: v for k, v in row.items() if k in DatasetRecord.__dataclass_fields__})
                self._records[record.dataset_id] = record
            except (TypeError, ValueError):
                continue

    def create(self, **payload) -> DatasetRecord:
        record = DatasetRecord(**payload)
        self._records[record.dataset_id] = record
        self.adapter.insert(self.table_name, [record.to_dict()])
        return record

    def list_records(self, offset: int = 0, limit: int = 0, status: str | None = None, owner_agent: str | None = None) -> list[DatasetRecord]:
        records = list(self._records.values())
        if status is not None:
            records = [r for r in records if r.status == status]
        if owner_agent is not None:
            records = [r for r in records if r.owner_agent == owner_agent]
        if limit > 0:
            records = records[offset:offset + limit]
        elif offset > 0:
            records = records[offset:]
        return records

