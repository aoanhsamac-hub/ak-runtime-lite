from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from memory.lesson_registry import LessonRegistry
from memory.schemas import LessonRecord, SkillRecord
from memory.skill_registry import SkillRegistry


@dataclass
class SkillDiscoveryResult:
    skill: SkillRecord | None
    status: str
    issues: list[str]


MIN_LESSONS_FOR_SKILL = 3
EVIDENCE_THRESHOLD = 0.7


class SkillDiscoveryPipeline:
    def __init__(self, skill_registry: SkillRegistry, lesson_registry: LessonRegistry):
        self.skill_registry = skill_registry
        self.lesson_registry = lesson_registry

    def discover(self, lesson_ids: list[str], owner_agent: str, skill_name: str, description: str) -> SkillDiscoveryResult:
        issues = self._validate_lessons(lesson_ids)
        if issues:
            return SkillDiscoveryResult(skill=None, status="BLOCKED", issues=issues)
        success_rate = self._measure_success_rate(lesson_ids)
        if success_rate < EVIDENCE_THRESHOLD:
            return SkillDiscoveryResult(
                skill=None,
                status="BLOCKED",
                issues=[f"evidence threshold not met: {success_rate:.2f} < {EVIDENCE_THRESHOLD}"],
            )
        payload = {
            "name": skill_name,
            "description": description,
            "source_lessons": lesson_ids,
            "owner_agent": owner_agent,
            "allowed_agents": [owner_agent],
            "risk_level": self._infer_risk_level(lesson_ids),
            "test_cases": self._build_test_cases(lesson_ids),
        }
        skill = self.skill_registry.create_candidate(**payload)
        return SkillDiscoveryResult(skill=skill, status="CANDIDATE", issues=[])

    def _validate_lessons(self, lesson_ids: list[str]) -> list[str]:
        issues = []
        if len(lesson_ids) < MIN_LESSONS_FOR_SKILL:
            issues.append(f"minimum {MIN_LESSONS_FOR_SKILL} approved lessons required, got {len(lesson_ids)}")
        for lid in lesson_ids:
            try:
                lesson = self.lesson_registry.get(lid)
                if lesson.status != "APPROVED":
                    issues.append(f"lesson {lid} is not APPROVED")
            except KeyError:
                issues.append(f"lesson not found: {lid}")
        return issues

    def _measure_success_rate(self, lesson_ids: list[str]) -> float:
        if not lesson_ids:
            return 0.0
        lessons = []
        for lid in lesson_ids:
            try:
                lessons.append(self.lesson_registry.get(lid))
            except KeyError:
                continue
        if not lessons:
            return 0.0
        successful = sum(1 for l in lessons if "success" in l.summary.lower() or "pass" in l.summary.lower())
        return successful / len(lessons)

    def _infer_risk_level(self, lesson_ids: list[str]) -> str:
        levels = {"LEVEL_4_CONSTITUTIONAL": 4, "LEVEL_3_CRITICAL": 3, "LEVEL_2_ELEVATED": 2, "LEVEL_1_MODERATE": 1}
        max_level = 1
        for lid in lesson_ids:
            try:
                lesson = self.lesson_registry.get(lid)
                level = levels.get(lesson.risk_level, 1)
                if level > max_level:
                    max_level = level
            except KeyError:
                continue
        reverse = {4: "LEVEL_4_CONSTITUTIONAL", 3: "LEVEL_3_CRITICAL", 2: "LEVEL_2_ELEVATED", 1: "LEVEL_1_MODERATE"}
        return reverse.get(max_level, "LEVEL_1_MODERATE")

    def _build_test_cases(self, lesson_ids: list[str]) -> list[str]:
        cases = []
        for lid in lesson_ids:
            try:
                lesson = self.lesson_registry.get(lid)
                case = f"verify: {lesson.title[:60]}"
                cases.append(case)
            except KeyError:
                continue
        return cases

    def submit_for_review(self, skill_id: str, reviewer: str) -> SkillDiscoveryResult:
        try:
            reviewed = self.skill_registry.mark_reviewed(skill_id, reviewer)
            return SkillDiscoveryResult(skill=reviewed, status="REVIEWED", issues=[])
        except (KeyError, ValueError) as exc:
            return SkillDiscoveryResult(skill=None, status="ERROR", issues=[str(exc)])

    def approve(self, skill_id: str, reviewer: str) -> SkillDiscoveryResult:
        try:
            approved = self.skill_registry.approve(skill_id, reviewer)
            return SkillDiscoveryResult(skill=approved, status="APPROVED", issues=[])
        except (KeyError, ValueError) as exc:
            return SkillDiscoveryResult(skill=None, status="ERROR", issues=[str(exc)])
