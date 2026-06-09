from __future__ import annotations

from typing import Any
from memory.learning_registry.schemas import SkillFamilyRecord


class SkillFamilyRegistry:
    table_name = "skill_families"

    def __init__(self, adapter=None):
        self.adapter = adapter
        self._records: dict[str, SkillFamilyRecord] = {}
        self._hydrate()

    def _hydrate(self) -> None:
        if not self.adapter:
            return
        rows = self.adapter.all(self.table_name)
        for row in rows:
            try:
                filtered = {k: v for k, v in row.items() if k in SkillFamilyRecord.__dataclass_fields__}
                self._records[filtered["family_id"]] = SkillFamilyRecord(**filtered)
            except (TypeError, ValueError):
                continue

    def create_family(self, **payload) -> SkillFamilyRecord:
        record = SkillFamilyRecord(**payload)
        self._save(record)
        return record

    def get(self, family_id: str) -> SkillFamilyRecord:
        try:
            return self._records[family_id]
        except KeyError as exc:
            raise KeyError(f"family not found: {family_id}") from exc

    def list_all(self) -> list[SkillFamilyRecord]:
        return list(self._records.values())

    def _save(self, record: SkillFamilyRecord) -> None:
        self._records[record.family_id] = record
        if self.adapter:
            self.adapter.insert(self.table_name, [record.to_dict()])
