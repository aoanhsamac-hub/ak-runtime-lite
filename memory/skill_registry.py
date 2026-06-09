from __future__ import annotations

from typing import Any

from memory.lancedb_adapter import LanceDBAdapter
from memory.lesson_registry import LessonRegistry
from memory.schemas import SkillRecord
from memory.schemas.records import (
    SKILL_STATUSES,
    SKILL_LIFECYCLE_STAGES,
    SKILL_CATEGORIES,
    SKILL_SOURCES,
)


class SkillRegistry:
    table_name = "ak_skills"

    def __init__(self, adapter: LanceDBAdapter, lesson_registry: LessonRegistry):
        self.adapter = adapter
        self.lesson_registry = lesson_registry
        self._records: dict[str, SkillRecord] = {}
        self._hydrate()

    def _hydrate(self) -> None:
        rows = self.adapter.all(self.table_name)
        for row in rows:
            try:
                filtered = {k: v for k, v in row.items() if k in SkillRecord.__dataclass_fields__}
                record = SkillRecord(**filtered)
                self._records[record.skill_id] = record
            except (TypeError, ValueError):
                continue

    def create_candidate(self, _skip_lesson_validation: bool = False, **payload) -> SkillRecord:
        if not _skip_lesson_validation:
            self._validate_lessons(payload.get("source_lessons", []))
        payload.setdefault("lifecycle_stage", "PROPOSED")
        payload.setdefault("category", "core")
        payload.setdefault("source", "internal")
        record = SkillRecord(**payload)
        self._save(record)
        return record

    def get(self, skill_id: str) -> SkillRecord:
        try:
            return self._records[skill_id]
        except KeyError as exc:
            raise KeyError(f"skill not found: {skill_id}") from exc

    def mark_reviewed(self, skill_id: str, reviewer_agent: str) -> SkillRecord:
        return self._transition_status(skill_id, "REVIEWED", reviewer_agent)

    def approve(self, skill_id: str, reviewer_agent: str) -> SkillRecord:
        return self._transition_status(skill_id, "APPROVED", reviewer_agent)

    def activate(self, skill_id: str, owner_agent: str) -> SkillRecord:
        return self._transition_status(skill_id, "ACTIVE", owner_agent)

    def deprecate(self, skill_id: str, reviewer_agent: str) -> SkillRecord:
        return self._transition_status(skill_id, "DEPRECATED", reviewer_agent)

    def suspend(self, skill_id: str, reviewer_agent: str, reason: str) -> SkillRecord:
        record = self.get(skill_id)
        updated = record.with_version(
            status="SUSPENDED",
            reviewer_agent=reviewer_agent,
            audit_requirements={**record.audit_requirements, "suspension_reason": reason, "suspended_at": record.updated_at}
        )
        self._save(updated)
        return updated

    def retire(self, skill_id: str, reviewer_agent: str, reason: str) -> SkillRecord:
        record = self.get(skill_id)
        updated = record.with_version(
            status="RETIRED",
            reviewer_agent=reviewer_agent,
            lifecycle_stage="RETIRED",
            audit_requirements={**record.audit_requirements, "retirement_reason": reason, "retired_at": record.updated_at}
        )
        self._save(updated)
        return updated

    def archive(self, skill_id: str) -> SkillRecord:
        record = self.get(skill_id)
        updated = record.with_version(
            lifecycle_stage="ARCHIVED",
            audit_requirements={**record.audit_requirements, "archived_at": record.updated_at}
        )
        self._save(updated)
        return updated

    def transition_lifecycle(self, skill_id: str, lifecycle_stage: str, reviewer_agent: str | None = None) -> SkillRecord:
        if lifecycle_stage not in SKILL_LIFECYCLE_STAGES:
            raise ValueError(f"invalid lifecycle_stage: {lifecycle_stage}")
        record = self.get(skill_id)
        updated = record.with_lifecycle_stage(lifecycle_stage, reviewer_agent)
        self._save(updated)
        return updated

    def list_records(
        self,
        offset: int = 0,
        limit: int = 0,
        status: str | None = None,
        lifecycle_stage: str | None = None,
        owner_agent: str | None = None,
        category: str | None = None,
        source: str | None = None,
    ) -> list[SkillRecord]:
        records = list(self._records.values())
        if status is not None:
            records = [r for r in records if r.status == status]
        if lifecycle_stage is not None:
            records = [r for r in records if r.lifecycle_stage == lifecycle_stage]
        if owner_agent is not None:
            records = [r for r in records if r.owner_agent == owner_agent]
        if category is not None:
            records = [r for r in records if r.category == category]
        if source is not None:
            records = [r for r in records if r.source == source]
        if limit > 0:
            records = records[offset:offset + limit]
        elif offset > 0:
            records = records[offset:]
        return records

    def approved_for_agent(self, agent_id: str | None = None) -> list[SkillRecord]:
        records = [r for r in self._records.values() if r.status in {"APPROVED", "ACTIVE"}]
        if agent_id is None:
            return records
        return [r for r in records if agent_id in r.allowed_agents and agent_id not in r.forbidden_users]

    def get_by_category(self, category: str) -> list[SkillRecord]:
        return [r for r in self._records.values() if r.category == category]

    def get_by_source(self, source: str) -> list[SkillRecord]:
        return [r for r in self._records.values() if r.source == source]

    def get_by_lifecycle_stage(self, lifecycle_stage: str) -> list[SkillRecord]:
        return [r for r in self._records.values() if r.lifecycle_stage == lifecycle_stage]

    def update_ownership(
        self,
        skill_id: str,
        primary_users: list[str] | None = None,
        secondary_users: list[str] | None = None,
        forbidden_users: list[str] | None = None,
    ) -> SkillRecord:
        record = self.get(skill_id)
        updated = record.with_version(
            primary_users=primary_users if primary_users is not None else record.primary_users,
            secondary_users=secondary_users if secondary_users is not None else record.secondary_users,
            forbidden_users=forbidden_users if forbidden_users is not None else record.forbidden_users,
            allowed_agents=list(dict.fromkeys(
                (primary_users or record.primary_users) + (secondary_users or record.secondary_users)
            )),
        )
        self._save(updated)
        return updated

    def add_dependency(self, skill_id: str, dependency_id: str) -> SkillRecord:
        record = self.get(skill_id)
        deps = list(record.dependencies)
        if dependency_id not in deps:
            deps.append(dependency_id)
        updated = record.with_version(dependencies=deps)
        self._save(updated)
        return updated

    def remove_dependency(self, skill_id: str, dependency_id: str) -> SkillRecord:
        record = self.get(skill_id)
        deps = [d for d in record.dependencies if d != dependency_id]
        updated = record.with_version(dependencies=deps)
        self._save(updated)
        return updated

    def _validate_lessons(self, lesson_ids: list[str]) -> None:
        if not lesson_ids:
            raise ValueError("source_lessons is required")
        for lesson_id in lesson_ids:
            lesson = self.lesson_registry.get(lesson_id)
            if lesson.status != "APPROVED":
                raise ValueError("skills require approved source lessons")

    def _transition_status(self, skill_id: str, status: str, reviewer_agent: str | None = None) -> SkillRecord:
        if status not in SKILL_STATUSES:
            raise ValueError(f"invalid skill status: {status}")
        record = self.get(skill_id)
        updated = record.with_status(status, reviewer_agent)
        self._save(updated)
        return updated

    def _save(self, record: SkillRecord) -> None:
        self._records[record.skill_id] = record
        self.adapter.insert(self.table_name, [record.to_dict()])