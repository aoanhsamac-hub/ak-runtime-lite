from __future__ import annotations

from typing import Any
from memory.learning_registry.schemas import CanonicalSkillRecord


class CanonicalSkillRegistry:
    table_name = "canonical_skills"

    def __init__(self, adapter=None):
        self.adapter = adapter
        self._records: dict[str, CanonicalSkillRecord] = {}
        self._hydrate()

    def _hydrate(self) -> None:
        if not self.adapter:
            return
        rows = self.adapter.all(self.table_name)
        for row in rows:
            try:
                filtered = {k: v for k, v in row.items() if k in CanonicalSkillRecord.__dataclass_fields__}
                self._records[filtered["canonical_id"]] = CanonicalSkillRecord(**filtered)
            except (TypeError, ValueError):
                continue

    def create_canonical(self, **payload) -> CanonicalSkillRecord:
        record = CanonicalSkillRecord(**payload)
        self._save(record)
        return record

    def get(self, canonical_id: str) -> CanonicalSkillRecord:
        try:
            return self._records[canonical_id]
        except KeyError as exc:
            raise KeyError(f"canonical skill not found: {canonical_id}") from exc

    def list_all(self, classification: str | None = None) -> list[CanonicalSkillRecord]:
        records = list(self._records.values())
        if classification:
            records = [r for r in records if r.classification == classification]
        return records

    def _save(self, record: CanonicalSkillRecord) -> None:
        self._records[record.canonical_id] = record
        if self.adapter:
            self.adapter.insert(self.table_name, [record.to_dict()])
