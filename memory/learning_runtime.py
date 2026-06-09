from __future__ import annotations

from typing import Any, Sequence

from agents.runtime_models import (
    ActivationState,
    AgentReportEnvelope,
    CapabilityUsageRecord,
    EvidenceRecord,
    LessonRecord,
)


class LessonCandidateRegistry:
    """Backward-compatible wrapper around KingdomMemoryPlatform."""
    def __init__(self, path: Any = None):
        from memory.kingdom_memory_platform import KingdomMemoryPlatform
        self.memory = KingdomMemoryPlatform()

    def record_lesson(self, lesson: LessonRecord | dict) -> dict:
        if hasattr(lesson, "to_dict"):
            data = lesson.to_dict()
        else:
            data = dict(lesson)
        return self.memory.record_lesson_candidate(data)

    def get_all(self) -> list[dict]:
        return self.memory.get_lesson_candidates()

    def get_by_agent(self, agent_id: str) -> list[dict]:
        return [r for r in self.get_all() if r.get("source_agent") == agent_id]

    def summary(self) -> dict:
        records = self.get_all()
        return {
            "total_lessons": len(records),
            "unique_agents": len(set(r.get("source_agent", "") for r in records)),
        }


class AgentPerformanceRegistry:
    """Backward-compatible wrapper around KingdomMemoryPlatform."""
    def __init__(self, path: Any = None):
        from memory.kingdom_memory_platform import KingdomMemoryPlatform
        self.memory = KingdomMemoryPlatform()

    def record_performance(self, data: dict) -> dict:
        return self.memory.record_agent_performance(data)

    def get_all(self) -> list[dict]:
        return self.memory.get_agent_performance()

    def get_by_agent(self, agent_id: str) -> list[dict]:
        return [r for r in self.get_all() if r.get("agent_id") == agent_id]

    def summary(self) -> dict:
        records = self.get_all()
        return {
            "total_records": len(records),
            "unique_agents": len(set(r.get("agent_id", "") for r in records)),
        }


class LearningRuntime:
    def __init__(
        self,
        memory_platform: Any = None,
        evidence_registry: Any = None,
        lesson_registry: Any = None,
        usage_registry: Any = None,
        performance_registry: Any = None,
    ):
        has_legacy = any(x is not None for x in (evidence_registry, lesson_registry, usage_registry, performance_registry))
        if memory_platform is not None:
            self.memory = memory_platform
        elif not has_legacy:
            from memory.kingdom_memory_platform import KingdomMemoryPlatform as NMP
            self.memory = NMP()
        else:
            self.memory = None
        self.evidence = evidence_registry
        self.lessons = lesson_registry
        self.usage = usage_registry
        self.performance = performance_registry

    def _ev(self):
        return self.evidence if self.evidence is not None else self.memory

    def _ls(self):
        return self.lessons if self.lessons is not None else self.memory

    def _us(self):
        return self.usage if self.usage is not None else self.memory

    def _pf(self):
        return self.performance if self.performance is not None else self.memory

    def process_mission_output(self, report: AgentReportEnvelope) -> dict:
        evidence_count = 0
        lesson_count = 0
        ev = self._ev()
        ls = self._ls()
        us = self._us()
        pf = self._pf()

        for ev_id in report.evidence_ids:
            if hasattr(ev, "record_evidence"):
                ev.record_evidence({"evidence_id": ev_id, "source_agent": report.agent_id, "mission_id": report.mission_id})
            else:
                ev.record_evidence({"evidence_id": ev_id, "source_agent": report.agent_id, "mission_id": report.mission_id})
            evidence_count += 1

        for ls_id in report.lesson_ids:
            lesson_data = {
                "lesson_id": ls_id,
                "source_agent": report.agent_id,
                "mission_id": report.mission_id,
                "title": f"Lesson from {report.mission_id}",
                "status": "DRAFT",
            }
            if hasattr(ls, "record_lesson"):
                ls.record_lesson(lesson_data)
            else:
                ls.record_lesson_candidate(lesson_data)
            lesson_count += 1

        usage_data = {
            "agent_id": report.agent_id,
            "capability_name": report.mission_type,
            "success": report.status == "COMPLETED",
            "evidence_count": evidence_count,
            "lesson_count": lesson_count,
        }
        if hasattr(us, "record_usage"):
            us.record_usage(usage_data)
        else:
            us.record_capability_usage(usage_data)

        perf_data = {
            "agent_id": report.agent_id,
            "mission_id": report.mission_id,
            "mission_type": report.mission_type,
            "status": report.status,
            "evidence_count": evidence_count,
            "lesson_count": lesson_count,
        }
        if hasattr(pf, "record_performance"):
            pf.record_performance(perf_data)
        else:
            pf.record_agent_performance(perf_data)

        return {
            "evidence_recorded": evidence_count,
            "lessons_recorded": lesson_count,
            "usage_recorded": 1,
            "performance_recorded": 1,
        }

    def hermes_distill_lessons(self) -> list[dict]:
        ls = self._ls()
        if hasattr(ls, "get_all"):
            candidates = ls.get_all()
        else:
            candidates = ls.get_lesson_candidates()
        lessons = [c for c in candidates if c.get("status") == "DRAFT"]
        for lesson in lessons:
            lesson["status"] = "REVIEWED"
        return lessons

    def sage_block_unsafe(self, activation_state: ActivationState) -> dict:
        if activation_state in (
            ActivationState.OPERATIONAL_APPROVED,
            ActivationState.OPERATIONAL_LIMITED,
            ActivationState.PILOT_ACTIVE,
        ):
            return {
                "blocked": True,
                "reason": f"Activation state {activation_state.value} requires higher authority",
                "recommended_state": ActivationState.SANDBOX_ACTIVE.value,
            }
        return {
            "blocked": False,
            "reason": "Activation state change allowed",
        }

    def janus_consolidate_council(self, reports: Sequence[AgentReportEnvelope]) -> dict:
        return {
            "total_agents": len(reports),
            "completed": sum(1 for r in reports if r.status == "COMPLETED"),
            "failed": sum(1 for r in reports if r.status in ("FAILED", "LOCKED")),
            "total_evidence": sum(len(r.evidence_ids) for r in reports),
            "total_lessons": sum(len(r.lesson_ids) for r in reports),
            "agents_reporting": [r.agent_id for r in reports],
            "consolidated_at": __import__("datetime").datetime.now(
                __import__("datetime").timezone.utc
            ).replace(microsecond=0).isoformat(),
        }

    def check_activation_readiness(self) -> dict:
        ev = self._ev()
        ls = self._ls()
        us = self._us()
        pf = self._pf()

        if hasattr(ev, "get_all"):
            evidence_count = len(ev.get_all())
        else:
            evidence_count = len(ev.get_evidence())

        if hasattr(ls, "get_all"):
            lesson_count = len(ls.get_all())
        else:
            lesson_count = len(ls.get_lesson_candidates())

        if hasattr(us, "summary"):
            raw = us.summary()
            usage_count = raw.get("total_usages") or raw.get("capability_usage") or 0
        else:
            usage_count = len(us.get_capability_usage())

        if hasattr(pf, "summary"):
            raw = pf.summary()
            perf_count = raw.get("total_records") or raw.get("agent_performance") or 0
        else:
            perf_count = len(pf.get_agent_performance())

        all_pass = (
            evidence_count >= 7
            and lesson_count >= 1
            and usage_count >= 7
        )
        return {
            "ready": all_pass,
            "evidence_count": evidence_count,
            "lesson_count": lesson_count,
            "usage_count": usage_count,
            "performance_records": perf_count,
            "reason": (
                "All readiness criteria met" if all_pass
                else f"Missing: evidence={evidence_count}/7, lessons={lesson_count}/1, usages={usage_count}/7"
            ),
        }

    def summary(self) -> dict:
        if self.memory is not None and hasattr(self.memory, "summary"):
            return self.memory.summary()
        return {}
