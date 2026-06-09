from __future__ import annotations

from typing import Any
from memory.learning_registry.schemas import ApprovedSkillRecord


class ApprovedSkillRegistry:
    table_name = "approved_skills"

    def __init__(self, adapter=None):
        self.adapter = adapter
        self._records: dict[str, ApprovedSkillRecord] = {}
        self._hydrate()

    def _hydrate(self) -> None:
        if not self.adapter:
            return
        rows = self.adapter.all(self.table_name)
        for row in rows:
            try:
                filtered = {k: v for k, v in row.items() if k in ApprovedSkillRecord.__dataclass_fields__}
                self._records[filtered["approved_skill_id"]] = ApprovedSkillRecord(**filtered)
            except (TypeError, ValueError):
                continue

    def approve(self, **payload) -> ApprovedSkillRecord:
        record = ApprovedSkillRecord(**payload)
        self._save(record)
        return record

    def get(self, approved_skill_id: str) -> ApprovedSkillRecord:
        try:
            return self._records[approved_skill_id]
        except KeyError as exc:
            raise KeyError(f"approved skill not found: {approved_skill_id}") from exc

    def list_all(self, status: str | None = None) -> list[ApprovedSkillRecord]:
        records = list(self._records.values())
        if status:
            records = [r for r in records if r.status == status]
        return records

    def _save(self, record: ApprovedSkillRecord) -> None:
        self._records[record.approved_skill_id] = record
        if self.adapter:
            self.adapter.insert(self.table_name, [record.to_dict()])

    def export_jsonl(self) -> list[dict[str, Any]]:
        return [r.to_dict() for r in self._records.values()]
