from __future__ import annotations

from typing import Any

from memory.lancedb_adapter import LanceDBAdapter
from memory.schemas.dependencies import SkillDependencyRecord, SkillOwnershipRecord
from memory.schemas.records import DEPENDENCY_RELATIONSHIP_TYPES


class SkillDependencyRegistry:
    table_name = "ak_skill_dependencies"

    def __init__(self, adapter: LanceDBAdapter):
        self.adapter = adapter
        self._records: dict[str, SkillDependencyRecord] = {}
        self._hydrate()

    def _hydrate(self) -> None:
        rows = self.adapter.all(self.table_name)
        for row in rows:
            try:
                filtered = {k: v for k, v in row.items() if k in SkillDependencyRecord.__dataclass_fields__}
                record = SkillDependencyRecord(**filtered)
                self._records[record.dependency_id] = record
            except (TypeError, ValueError):
                continue

    def create(self, **payload) -> SkillDependencyRecord:
        record = SkillDependencyRecord(**payload)
        self._save(record)
        return record

    def get(self, dependency_id: str) -> SkillDependencyRecord:
        try:
            return self._records[dependency_id]
        except KeyError as exc:
            raise KeyError(f"dependency not found: {dependency_id}") from exc

    def get_by_source(self, source_skill_id: str) -> list[SkillDependencyRecord]:
        return [r for r in self._records.values() if r.source_skill_id == source_skill_id]

    def get_by_target(self, target_id: str, target_type: str | None = None) -> list[SkillDependencyRecord]:
        records = [r for r in self._records.values() if r.target_id == target_id]
        if target_type:
            records = [r for r in records if r.target_type == target_type]
        return records

    def get_by_relationship(self, relationship_type: str) -> list[SkillDependencyRecord]:
        if relationship_type not in DEPENDENCY_RELATIONSHIP_TYPES:
            raise ValueError(f"invalid relationship_type: {relationship_type}")
        return [r for r in self._records.values() if r.relationship_type == relationship_type]

    def delete(self, dependency_id: str) -> None:
        if dependency_id in self._records:
            del self._records[dependency_id]
            self.adapter.insert(self.table_name, [{"dependency_id": dependency_id, "_deleted": True}])

    def list_all(self, offset: int = 0, limit: int = 0) -> list[SkillDependencyRecord]:
        records = list(self._records.values())
        if limit > 0:
            records = records[offset:offset + limit]
        elif offset > 0:
            records = records[offset:]
        return records

    def _save(self, record: SkillDependencyRecord) -> None:
        self._records[record.dependency_id] = record
        self.adapter.insert(self.table_name, [record.to_dict()])

    def check_circular(self, source_skill_id: str, target_id: str, target_type: str) -> bool:
        if target_type != "skill":
            return False
        visited = set()
        stack = [target_id]
        while stack:
            current = stack.pop()
            if current == source_skill_id:
                return True
            if current in visited:
                continue
            visited.add(current)
            deps = self.get_by_source(current)
            for dep in deps:
                if dep.target_type == "skill":
                    stack.append(dep.target_id)
        return False


class SkillOwnershipRegistry:
    table_name = "ak_skill_ownership"

    def __init__(self, adapter: LanceDBAdapter):
        self.adapter = adapter
        self._records: dict[str, SkillOwnershipRecord] = {}
        self._hydrate()

    def _hydrate(self) -> None:
        rows = self.adapter.all(self.table_name)
        for row in rows:
            try:
                filtered = {k: v for k, v in row.items() if k in SkillOwnershipRecord.__dataclass_fields__}
                record = SkillOwnershipRecord(**filtered)
                self._records[record.ownership_id] = record
            except (TypeError, ValueError):
                continue

    def create(self, **payload) -> SkillOwnershipRecord:
        record = SkillOwnershipRecord(**payload)
        self._save(record)
        return record

    def get(self, ownership_id: str) -> SkillOwnershipRecord:
        try:
            return self._records[ownership_id]
        except KeyError as exc:
            raise KeyError(f"ownership not found: {ownership_id}") from exc

    def get_by_skill(self, skill_id: str) -> SkillOwnershipRecord | None:
        for record in self._records.values():
            if record.skill_id == skill_id:
                return record
        return None

    def get_by_owner(self, owner_agent: str) -> list[SkillOwnershipRecord]:
        return [r for r in self._records.values() if r.owner_agent == owner_agent]

    def get_by_user(self, agent_id: str, access_level: str | None = None) -> list[SkillOwnershipRecord]:
        records = []
        for record in self._records.values():
            if access_level == "OWNER" and record.owner_agent == agent_id:
                records.append(record)
            elif access_level == "PRIMARY_USER" and agent_id in record.primary_users:
                records.append(record)
            elif access_level == "SECONDARY_USER" and agent_id in record.secondary_users:
                records.append(record)
            elif access_level == "FORBIDDEN_USER" and agent_id in record.forbidden_users:
                records.append(record)
            elif access_level is None:
                if (record.owner_agent == agent_id or
                    agent_id in record.primary_users or
                    agent_id in record.secondary_users or
                    agent_id in record.forbidden_users):
                    records.append(record)
        return records

    def update(self, skill_id: str, **updates) -> SkillOwnershipRecord:
        existing = self.get_by_skill(skill_id)
        if not existing:
            raise KeyError(f"ownership not found for skill: {skill_id}")
        payload = {
            "ownership_id": existing.ownership_id,
            "skill_id": existing.skill_id,
            "owner_agent": updates.get("owner_agent", existing.owner_agent),
            "primary_users": updates.get("primary_users", existing.primary_users),
            "secondary_users": updates.get("secondary_users", existing.secondary_users),
            "forbidden_users": updates.get("forbidden_users", existing.forbidden_users),
            "assigned_at": existing.assigned_at,
            "assigned_by": updates.get("assigned_by", existing.assigned_by),
            "access_level": updates.get("access_level", existing.access_level),
        }
        record = SkillOwnershipRecord(**payload)
        self._save(record)
        return record

    def _save(self, record: SkillOwnershipRecord) -> None:
        self._records[record.ownership_id] = record
        self.adapter.insert(self.table_name, [record.to_dict()])