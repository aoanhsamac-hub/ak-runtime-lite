from __future__ import annotations

from typing import Any

from memory.lancedb_adapter import LanceDBAdapter
from memory.schemas import LessonRecord


class LessonRegistry:
    table_name = "lessons"

    def __init__(self, adapter: LanceDBAdapter):
        self.adapter = adapter
        self._records: dict[str, LessonRecord] = {}
        self._hydrate()

    def _hydrate(self) -> None:
        rows = self.adapter.all(self.table_name)
        for row in rows:
            try:
                record = LessonRecord(**{k: v for k, v in row.items() if k in LessonRecord.__dataclass_fields__})
                self._records[record.lesson_id] = record
            except (TypeError, ValueError):
                continue

    def create_candidate(self, **payload) -> LessonRecord:
        record = LessonRecord(**payload)
        self._save(record)
        return record

    def get(self, lesson_id: str) -> LessonRecord:
        try:
            return self._records[lesson_id]
        except KeyError as exc:
            raise KeyError(f"lesson not found: {lesson_id}") from exc

    def mark_reviewed(self, lesson_id: str, reviewer_agent: str) -> LessonRecord:
        return self._transition(lesson_id, "REVIEWED", reviewer_agent)

    def approve(self, lesson_id: str, reviewer_agent: str) -> LessonRecord:
        return self._transition(lesson_id, "APPROVED", reviewer_agent)

    def deprecate(self, lesson_id: str, reviewer_agent: str) -> LessonRecord:
        return self._transition(lesson_id, "DEPRECATED", reviewer_agent)

    def quarantine(self, lesson_id: str, reviewer_agent: str) -> LessonRecord:
        return self._transition(lesson_id, "QUARANTINE", reviewer_agent)

    def list_records(self, offset: int = 0, limit: int = 0, status: str | None = None, owner_agent: str | None = None) -> list[LessonRecord]:
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

    def search(self, query: str, limit: int = 10) -> list[dict]:
        return self.adapter.search(self.table_name, query, limit)

    def _transition(self, lesson_id: str, status: str, reviewer_agent: str) -> LessonRecord:
        record = self.get(lesson_id).with_status(status, reviewer_agent)
        self._save(record)
        return record

    def _save(self, record: LessonRecord) -> None:
        self._records[record.lesson_id] = record
        self.adapter.insert(self.table_name, [record.to_dict()])

