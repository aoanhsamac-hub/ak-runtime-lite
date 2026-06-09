from __future__ import annotations

from typing import Any

from memory.lancedb_adapter import LanceDBAdapter
from memory.schemas import DecisionTraceRecord


class DecisionTraceRegistry:
    table_name = "decision_traces"

    def __init__(self, adapter: LanceDBAdapter):
        self.adapter = adapter
        self._records: dict[str, DecisionTraceRecord] = {}
        self._hydrate()

    def _hydrate(self) -> None:
        rows = self.adapter.all(self.table_name)
        for row in rows:
            try:
                record = DecisionTraceRecord(**{k: v for k, v in row.items() if k in DecisionTraceRecord.__dataclass_fields__})
                self._records[record.trace_id] = record
            except (TypeError, ValueError):
                continue

    def record(self, **payload) -> DecisionTraceRecord:
        trace = DecisionTraceRecord(**payload)
        self._records[trace.trace_id] = trace
        self.adapter.insert(self.table_name, [trace.to_dict()])
        return trace

    def list_records(self, offset: int = 0, limit: int = 0, status: str | None = None, owner_agent: str | None = None) -> list[DecisionTraceRecord]:
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

