from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from memory.decision_trace_registry import DecisionTraceRegistry
from memory.lesson_registry import LessonRegistry
from memory.schemas import LessonRecord


@dataclass
class LessonProductionResult:
    lesson: LessonRecord | None
    status: str
    issues: list[str]


class LessonProductionPipeline:
    def __init__(self, lesson_registry: LessonRegistry, trace_registry: DecisionTraceRegistry):
        self.lesson_registry = lesson_registry
        self.trace_registry = trace_registry

    def extract_from_trace(self, trace_id: str, owner_agent: str) -> LessonProductionResult:
        try:
            trace = self.trace_registry.get(trace_id)
        except KeyError as exc:
            return LessonProductionResult(lesson=None, status="ERROR", issues=[str(exc)])
        if trace.status != "APPROVED":
            return LessonProductionResult(
                lesson=None, status="BLOCKED", issues=["trace must be APPROVED before lesson extraction"]
            )
        payload = {
            "title": f"Lesson from {trace.decision}"[:120],
            "summary": trace.outcome[:200],
            "content": self._build_content(trace),
            "source": f"trace:{trace_id}",
            "owner_agent": owner_agent,
            "reviewer_agent": "Sage",
            "risk_level": trace.risk_level,
            "tags": [trace.agent.lower(), trace.outcome.lower()[:20]],
        }
        lesson = self.lesson_registry.create_candidate(**payload)
        return LessonProductionResult(lesson=lesson, status="CANDIDATE", issues=[])

    def _build_content(self, trace) -> str:
        parts = [
            f"Decision: {trace.decision}",
            f"Reasoning: {trace.reasoning}",
            f"Evidence: {'; '.join(trace.evidence)}",
            f"Outcome: {trace.outcome}",
        ]
        return "\n".join(parts)

    def submit_for_review(self, lesson_id: str, reviewer: str) -> LessonProductionResult:
        try:
            reviewed = self.lesson_registry.mark_reviewed(lesson_id, reviewer)
            return LessonProductionResult(lesson=reviewed, status="REVIEWED", issues=[])
        except (KeyError, ValueError) as exc:
            return LessonProductionResult(lesson=None, status="ERROR", issues=[str(exc)])

    def approve(self, lesson_id: str, reviewer: str) -> LessonProductionResult:
        try:
            approved = self.lesson_registry.approve(lesson_id, reviewer)
            return LessonProductionResult(lesson=approved, status="APPROVED", issues=[])
        except (KeyError, ValueError) as exc:
            return LessonProductionResult(lesson=None, status="ERROR", issues=[str(exc)])
