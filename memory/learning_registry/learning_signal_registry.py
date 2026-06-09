from __future__ import annotations

from typing import Any

from memory.learning_registry.schemas import LearningSignalRecord


class LearningSignalRegistry:
    table_name = "learning_signals"

    def __init__(self, adapter=None):
        self.adapter = adapter
        self._records: dict[str, LearningSignalRecord] = {}
        self._hydrate()

    def _hydrate(self) -> None:
        if not self.adapter:
            return
        rows = self.adapter.all(self.table_name)
        for row in rows:
            try:
                filtered = {k: v for k, v in row.items() if k in LearningSignalRecord.__dataclass_fields__}
                record = LearningSignalRecord(**filtered)
                self._records[record.signal_id] = record
            except (TypeError, ValueError):
                continue

    def create_candidate(self, **payload) -> LearningSignalRecord:
        record = LearningSignalRecord(**payload)
        self._save(record)
        return record

    def get(self, signal_id: str) -> LearningSignalRecord:
        try:
            return self._records[signal_id]
        except KeyError as exc:
            raise KeyError(f"learning signal not found: {signal_id}") from exc

    def list_all(self, offset: int = 0, limit: int = 0,
                 signal_type: str | None = None,
                 source_kind: str | None = None,
                 owner_agent: str | None = None) -> list[LearningSignalRecord]:
        records = list(self._records.values())
        if signal_type:
            records = [r for r in records if r.signal_type == signal_type]
        if source_kind:
            records = [r for r in records if r.source_kind == source_kind]
        if owner_agent:
            records = [r for r in records if r.owner_agent == owner_agent]
        if limit > 0:
            records = records[offset:offset + limit]
        elif offset > 0:
            records = records[offset:]
        return records

    def _save(self, record: LearningSignalRecord) -> None:
        self._records[record.signal_id] = record
        if self.adapter:
            self.adapter.insert(self.table_name, [record.to_dict()])
