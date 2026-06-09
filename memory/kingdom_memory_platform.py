from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LANCEDB_PATH = Path(__file__).resolve().parent / "lancedb"


RETENTION_CLASSES = {
    "TRANSIENT": {"retention_days": 30, "archive_policy": "auto_delete", "compaction_policy": "30d"},
    "OPERATIONAL": {"retention_days": 365, "archive_policy": "auto_archive", "compaction_policy": "1y"},
    "CANONICAL": {"retention_days": None, "archive_policy": "permanent", "compaction_policy": "never"},
    "ARCHIVAL": {"retention_days": None, "archive_policy": "compressed", "compaction_policy": "compressed_never"},
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _retention_until(retention_class: str) -> str | None:
    info = RETENTION_CLASSES.get(retention_class, RETENTION_CLASSES["OPERATIONAL"])
    days = info["retention_days"]
    if days is None:
        return None
    from datetime import timedelta
    return (datetime.now(timezone.utc) + timedelta(days=days)).replace(microsecond=0).isoformat()


def _retention_fields(retention_class: str = "OPERATIONAL") -> dict:
    info = RETENTION_CLASSES.get(retention_class, RETENTION_CLASSES["OPERATIONAL"])
    return {
        "retention_class": retention_class,
        "archive_policy": info["archive_policy"],
        "compaction_policy": info["compaction_policy"],
        "retention_until": _retention_until(retention_class),
    }


class KingdomMemoryPlatform:
    MANDATORY_TABLES = [
        "ak_evidence",
        "ak_lesson_candidates",
        "ak_lessons",
        "ak_knowledge",
        "ak_skills",
        "ak_capabilities",
        "ak_capability_usage",
        "ak_capability_roi",
        "ak_agent_performance",
        "ak_missions",
        "ak_council_reviews",
        "ak_audit_events",
        "ak_activation_events",
        "ak_capability_adoptions",
    ]

    def __init__(self, db_path: str | Path | None = None, adapter: Any = None):
        from memory.lancedb_adapter import LanceDBAdapter
        self.db_path = Path(db_path) if db_path else LANCEDB_PATH
        self.adapter = adapter or LanceDBAdapter(self.db_path)
        self._backend = None

    def connect(self):
        if self._backend is None:
            self._backend = self.adapter.connect()
        return self._backend

    # --- Evidence ---

    def record_evidence(self, record: dict) -> dict:
        data = dict(record)
        data.setdefault("evidence_id", record.get("evidence_id", ""))
        data.setdefault("retention_class", "OPERATIONAL")
        data.setdefault("created_at", _utc_now())
        data.update(_retention_fields(data.get("retention_class", "OPERATIONAL")))
        self.adapter.insert("ak_evidence", [data])
        return data

    def get_evidence(self, evidence_id: str | None = None) -> list[dict]:
        all_evidence = self.adapter.all("ak_evidence")
        if evidence_id:
            return [e for e in all_evidence if e.get("evidence_id") == evidence_id]
        return all_evidence

    def get_evidence_by_agent(self, agent_id: str) -> list[dict]:
        return [e for e in self.adapter.all("ak_evidence") if e.get("source_agent") == agent_id]

    def get_evidence_by_mission(self, mission_id: str) -> list[dict]:
        return [e for e in self.adapter.all("ak_evidence") if e.get("mission_id") == mission_id]

    # --- Lesson Candidates ---

    def record_lesson_candidate(self, record: dict) -> dict:
        data = dict(record)
        data.setdefault("lesson_id", record.get("lesson_id", ""))
        data.setdefault("status", "DRAFT")
        data.setdefault("retention_class", "OPERATIONAL")
        data.setdefault("created_at", _utc_now())
        data.update(_retention_fields(data.get("retention_class", "OPERATIONAL")))
        self.adapter.insert("ak_lesson_candidates", [data])
        return data

    def get_lesson_candidates(self, status: str | None = None) -> list[dict]:
        all_candidates = self.adapter.all("ak_lesson_candidates")
        if status:
            return [c for c in all_candidates if c.get("status") == status]
        return all_candidates

    def promote_lesson_candidate(self, lesson_id: str) -> dict | None:
        candidates = self.adapter.all("ak_lesson_candidates")
        target = None
        for c in candidates:
            if c.get("lesson_id") == lesson_id:
                target = c
                break
        if target is None:
            return None
        target["status"] = "APPROVED"
        self.adapter.insert("ak_lessons", [target])
        return target

    # --- Lessons (approved) ---

    def get_lessons(self, agent_id: str | None = None) -> list[dict]:
        all_lessons = self.adapter.all("ak_lessons")
        if agent_id:
            return [l for l in all_lessons if l.get("source_agent") == agent_id]
        return all_lessons

    # --- Knowledge ---

    def promote_to_knowledge(self, lesson_id: str, knowledge_data: dict) -> dict:
        data = dict(knowledge_data)
        data.setdefault("knowledge_id", f"KNOW-{lesson_id}")
        data.setdefault("source_lesson_id", lesson_id)
        data.setdefault("retention_class", "CANONICAL")
        data.setdefault("created_at", _utc_now())
        data.update(_retention_fields(data.get("retention_class", "CANONICAL")))
        self.adapter.insert("ak_knowledge", [data])
        return data

    def get_knowledge(self, knowledge_id: str | None = None) -> list[dict]:
        all_knowledge = self.adapter.all("ak_knowledge")
        if knowledge_id:
            return [k for k in all_knowledge if k.get("knowledge_id") == knowledge_id]
        return all_knowledge

    # --- Skills ---

    def promote_to_skill(self, knowledge_id: str, skill_data: dict) -> dict:
        data = dict(skill_data)
        data.setdefault("skill_id", f"SKILL-{knowledge_id}")
        data.setdefault("source_knowledge_id", knowledge_id)
        data.setdefault("retention_class", "CANONICAL")
        data.setdefault("created_at", _utc_now())
        data.update(_retention_fields(data.get("retention_class", "CANONICAL")))
        self.adapter.insert("ak_skills", [data])
        return data

    def get_skills(self, skill_id: str | None = None) -> list[dict]:
        all_skills = self.adapter.all("ak_skills")
        if skill_id:
            return [s for s in all_skills if s.get("skill_id") == skill_id]
        return all_skills

    # --- Capabilities ---

    def promote_to_capability(self, skill_id: str, capability_data: dict) -> dict:
        data = dict(capability_data)
        data.setdefault("capability_id", f"CAP-{skill_id}")
        data.setdefault("source_skill_id", skill_id)
        data.setdefault("retention_class", "CANONICAL")
        data.setdefault("created_at", _utc_now())
        data.update(_retention_fields(data.get("retention_class", "CANONICAL")))
        data.setdefault("adoption_status", "not_tracked")
        self.adapter.insert("ak_capabilities", [data])
        return data

    def get_capabilities(self, capability_id: str | None = None) -> list[dict]:
        all_cap = self.adapter.all("ak_capabilities")
        if capability_id:
            return [c for c in all_cap if c.get("capability_id") == capability_id]
        return all_cap

    # --- Capability Usage ---

    def record_capability_usage(self, record: dict) -> dict:
        data = dict(record)
        data.setdefault("usage_id", record.get("usage_id", ""))
        data.setdefault("retention_class", "OPERATIONAL")
        data.setdefault("created_at", _utc_now())
        data.update(_retention_fields(data.get("retention_class", "OPERATIONAL")))
        self.adapter.insert("ak_capability_usage", [data])
        return data

    def get_capability_usage(self, capability_name: str | None = None) -> list[dict]:
        all_usage = self.adapter.all("ak_capability_usage")
        if capability_name:
            return [u for u in all_usage if u.get("capability_name") == capability_name]
        return all_usage

    # --- Capability ROI ---

    def record_capability_roi(self, record: dict) -> dict:
        data = dict(record)
        data.setdefault("roi_id", record.get("roi_id", ""))
        data.setdefault("retention_class", "CANONICAL")
        data.setdefault("created_at", _utc_now())
        data.update(_retention_fields(data.get("retention_class", "CANONICAL")))
        data.setdefault("usage_count", 0)
        data.setdefault("total_value", 0.0)
        data.setdefault("total_cost", 0.0)
        data.setdefault("roi", 0.0)
        data.setdefault("adoption_status", "not_tracked")
        self.adapter.insert("ak_capability_roi", [data])
        return data

    def get_capability_roi(self, capability_name: str | None = None) -> list[dict]:
        all_roi = self.adapter.all("ak_capability_roi")
        if capability_name:
            return [r for r in all_roi if r.get("capability_name") == capability_name]
        return all_roi

    def calculate_roi(self, capability_name: str) -> dict:
        usage_records = self.get_capability_usage(capability_name)
        total_count = len(usage_records)
        roi_records = self.get_capability_roi(capability_name)
        if roi_records:
            latest = max(roi_records, key=lambda r: r.get("created_at", ""))
            total_value = latest.get("total_value", 0.0)
            total_cost = latest.get("total_cost", 0.0)
        else:
            total_value = 0.0
            total_cost = 0.0
        calculated_roi = (total_value / total_cost) if total_cost > 0 else 0.0
        return {
            "capability_name": capability_name,
            "usage_count": total_count,
            "total_value": total_value,
            "total_cost": total_cost,
            "roi": round(calculated_roi, 4),
        }

    # --- Agent Performance ---

    def record_agent_performance(self, record: dict) -> dict:
        data = dict(record)
        data.setdefault("retention_class", "OPERATIONAL")
        data.setdefault("created_at", _utc_now())
        data.update(_retention_fields(data.get("retention_class", "OPERATIONAL")))
        self.adapter.insert("ak_agent_performance", [data])
        return data

    def get_agent_performance(self, agent_id: str | None = None) -> list[dict]:
        all_perf = self.adapter.all("ak_agent_performance")
        if agent_id:
            return [p for p in all_perf if p.get("agent_id") == agent_id]
        return all_perf

    # --- Missions ---

    def record_mission(self, record: dict) -> dict:
        data = dict(record)
        data.setdefault("retention_class", "OPERATIONAL")
        data.setdefault("created_at", _utc_now())
        data.update(_retention_fields(data.get("retention_class", "OPERATIONAL")))
        self.adapter.insert("ak_missions", [data])
        return data

    def get_missions(self, status: str | None = None) -> list[dict]:
        all_missions = self.adapter.all("ak_missions")
        if status:
            return [m for m in all_missions if m.get("status") == status]
        return all_missions

    # --- Council Reviews ---

    def record_council_review(self, record: dict) -> dict:
        data = dict(record)
        data.setdefault("retention_class", "CANONICAL")
        data.setdefault("created_at", _utc_now())
        data.update(_retention_fields(data.get("retention_class", "CANONICAL")))
        self.adapter.insert("ak_council_reviews", [data])
        return data

    def get_council_reviews(self, review_id: str | None = None) -> list[dict]:
        all_reviews = self.adapter.all("ak_council_reviews")
        if review_id:
            return [r for r in all_reviews if r.get("review_id") == review_id]
        return all_reviews

    # --- Audit Events ---

    def record_audit_event(self, record: dict) -> dict:
        data = dict(record)
        data.setdefault("retention_class", "CANONICAL")
        data.setdefault("created_at", _utc_now())
        data.update(_retention_fields(data.get("retention_class", "CANONICAL")))
        self.adapter.insert("ak_audit_events", [data])
        return data

    def get_audit_events(self, actor: str | None = None) -> list[dict]:
        all_events = self.adapter.all("ak_audit_events")
        if actor:
            return [e for e in all_events if e.get("actor") == actor]
        return all_events

    # --- Activation Events ---

    def record_activation_event(self, record: dict) -> dict:
        data = dict(record)
        data.setdefault("retention_class", "CANONICAL")
        data.setdefault("created_at", _utc_now())
        data.update(_retention_fields(data.get("retention_class", "CANONICAL")))
        self.adapter.insert("ak_activation_events", [data])
        return data

    def get_activation_events(self, agent_id: str | None = None) -> list[dict]:
        all_events = self.adapter.all("ak_activation_events")
        if agent_id:
            return [e for e in all_events if e.get("agent_id") == agent_id]
        return all_events

    # --- Capability Adoptions ---

    def record_capability_adoption(self, record: dict) -> dict:
        data = dict(record)
        data.setdefault("adoption_id", record.get("adoption_id", ""))
        data.setdefault("retention_class", "CANONICAL")
        data.setdefault("created_at", _utc_now())
        data.update(_retention_fields(data.get("retention_class", "CANONICAL")))
        self.adapter.insert("ak_capability_adoptions", [data])
        return data

    def get_capability_adoptions(self, agent_id: str | None = None) -> list[dict]:
        all_adoptions = self.adapter.all("ak_capability_adoptions")
        if agent_id:
            return [a for a in all_adoptions if a.get("assigned_agent") == agent_id]
        return all_adoptions

    # --- Summary ---

    def summary(self) -> dict:
        return {
            "evidence_count": len(self.adapter.all("ak_evidence")),
            "lesson_candidates": len(self.adapter.all("ak_lesson_candidates")),
            "lessons_approved": len(self.adapter.all("ak_lessons")),
            "knowledge_records": len(self.adapter.all("ak_knowledge")),
            "skills": len(self.adapter.all("ak_skills")),
            "capabilities": len(self.adapter.all("ak_capabilities")),
            "capability_usage": len(self.adapter.all("ak_capability_usage")),
            "roi_records": len(self.adapter.all("ak_capability_roi")),
            "agent_performance": len(self.adapter.all("ak_agent_performance")),
            "missions": len(self.adapter.all("ak_missions")),
            "council_reviews": len(self.adapter.all("ak_council_reviews")),
            "audit_events": len(self.adapter.all("ak_audit_events")),
            "activation_events": len(self.adapter.all("ak_activation_events")),
            "capability_adoptions": len(self.adapter.all("ak_capability_adoptions")),
        }

    # --- Retention ---

    def apply_retention_policy(self, dry_run: bool = True) -> dict:
        actions = []
        now = _utc_now()
        for table_name in self.MANDATORY_TABLES:
            records = self.adapter.all(table_name)
            expired = []
            for record in records:
                retention_until = record.get("retention_until")
                if retention_until and retention_until < now:
                    expired.append(record)
            if expired and not dry_run:
                kept = [r for r in records if r not in expired]
                self.adapter.ensure_table(table_name, kept)
            actions.append({
                "table": table_name,
                "total": len(records),
                "expired": len(expired),
                "action": "dry_run" if dry_run else "deleted",
            })
        return {"actions": actions, "dry_run": dry_run}

    # --- Activation Readiness ---

    def check_activation_readiness(self) -> dict:
        evidence_count = len(self.adapter.all("ak_evidence"))
        lesson_count = len(self.adapter.all("ak_lesson_candidates"))
        usage_count = len(self.adapter.all("ak_capability_usage"))
        perf_count = len(self.adapter.all("ak_agent_performance"))
        all_pass = (
            evidence_count >= 7
            and lesson_count >= 1
            and usage_count >= 7
            and perf_count >= 7
        )
        return {
            "ready": all_pass,
            "evidence_count": evidence_count,
            "lesson_count": lesson_count,
            "usage_count": usage_count,
            "performance_records": perf_count,
            "reason": (
                "All readiness criteria met" if all_pass
                else f"Missing: evidence={evidence_count}/7, lessons={lesson_count}/1, usages={usage_count}/7, perf={perf_count}/7"
            ),
        }
