from __future__ import annotations

from typing import Any

from memory.learning_registry.schemas import CandidateSkillRecord


class CandidateSkillRegistry:
    table_name = "candidate_skills"

    def __init__(self, adapter=None):
        self.adapter = adapter
        self._records: dict[str, CandidateSkillRecord] = {}
        self._hydrate()

    def _hydrate(self) -> None:
        if not self.adapter:
            return
        rows = self.adapter.all(self.table_name)
        for row in rows:
            try:
                filtered = {k: v for k, v in row.items() if k in CandidateSkillRecord.__dataclass_fields__}
                record = CandidateSkillRecord(**filtered)
                self._records[record.candidate_skill_id] = record
            except (TypeError, ValueError):
                continue

    def create_candidate(self, **payload) -> CandidateSkillRecord:
        payload.setdefault("status", "CANDIDATE")
        payload.setdefault("approval_status", "PENDING_REVIEW")
        payload.setdefault("activation_status", "DISABLED")
        record = CandidateSkillRecord(**payload)
        self._save(record)
        return record

    def get(self, candidate_skill_id: str) -> CandidateSkillRecord:
        try:
            return self._records[candidate_skill_id]
        except KeyError as exc:
            raise KeyError(f"candidate skill not found: {candidate_skill_id}") from exc

    def list_all(self, offset: int = 0, limit: int = 0,
                 status: str | None = None,
                 approval_status: str | None = None,
                 owner_agent: str | None = None) -> list[CandidateSkillRecord]:
        records = list(self._records.values())
        if status:
            records = [r for r in records if r.status == status]
        if approval_status:
            records = [r for r in records if r.approval_status == approval_status]
        if owner_agent:
            records = [r for r in records if r.owner_agent == owner_agent]
        if limit > 0:
            records = records[offset:offset + limit]
        elif offset > 0:
            records = records[offset:]
        return records

    def list_candidates(self) -> list[CandidateSkillRecord]:
        return [r for r in self._records.values() if r.status == "CANDIDATE"]

    def _save(self, record: CandidateSkillRecord) -> None:
        self._records[record.candidate_skill_id] = record
        if self.adapter:
            self.adapter.insert(self.table_name, [record.to_dict()])
