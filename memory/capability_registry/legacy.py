from __future__ import annotations

from typing import Any

from memory.lancedb_adapter import LanceDBAdapter
from memory.schemas import CapabilityRecord


class CapabilityRegistry:
    table_name = "capabilities"

    def __init__(self, adapter: LanceDBAdapter):
        self.adapter = adapter
        self._records: dict[str, CapabilityRecord] = {}
        self._hydrate()

    def _hydrate(self) -> None:
        rows = self.adapter.all(self.table_name)
        for row in rows:
            try:
                record = CapabilityRecord(**{k: v for k, v in row.items() if k in CapabilityRecord.__dataclass_fields__})
                self._records[record.capability_id] = record
            except (TypeError, ValueError):
                continue

    def create(
        self,
        name: str,
        skills: list[dict[str, Any] | str],
        owner_agent: str,
        reviewer_agent: str,
        status: str,
        maturity_level: str,
        metrics: dict[str, Any],
    ) -> CapabilityRecord:
        skill_ids = self._validate_skills(skills)
        record = CapabilityRecord(
            name=name,
            skills=skill_ids,
            owner_agent=owner_agent,
            reviewer_agent=reviewer_agent,
            status=status,
            maturity_level=maturity_level,
            metrics=metrics,
        )
        self._records[record.capability_id] = record
        self.adapter.insert(self.table_name, [record.to_dict()])
        return record

    def list_records(self, offset: int = 0, limit: int = 0, status: str | None = None, owner_agent: str | None = None) -> list[CapabilityRecord]:
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

    def _validate_skills(self, skills: list[dict[str, Any] | str]) -> list[str]:
        if not skills:
            raise ValueError("skills is required")
        skill_ids: list[str] = []
        for skill in skills:
            if isinstance(skill, str):
                skill_ids.append(skill)
                continue
            status = skill.get("status")
            if status not in {"ACTIVE", "APPROVED"}:
                raise ValueError("capability skills must be active or approved")
            skill_id = skill.get("skill_id")
            if not skill_id:
                raise ValueError("skill_id is required")
            skill_ids.append(skill_id)
        return skill_ids
