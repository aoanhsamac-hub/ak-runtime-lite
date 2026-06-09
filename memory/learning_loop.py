from __future__ import annotations

from memory.lesson_registry import LessonRegistry
from memory.skill_registry import SkillRegistry


class LearningLoop:
    def __init__(self, lesson_registry: LessonRegistry, skill_registry: SkillRegistry):
        self.lesson_registry = lesson_registry
        self.skill_registry = skill_registry

    def observe(self, **payload):
        return self.lesson_registry.create_candidate(**payload)

    def submit_lesson_for_review(self, lesson_id: str, reviewer_agent: str):
        return self.lesson_registry.mark_reviewed(lesson_id, reviewer_agent)

    def approve_lesson(self, lesson_id: str, reviewer_agent: str):
        return self.lesson_registry.approve(lesson_id, reviewer_agent)

    def create_skill_candidate(self, **payload):
        return self.skill_registry.create_candidate(**payload)

    def approve_skill(self, skill_id: str, reviewer_agent: str):
        return self.skill_registry.approve(skill_id, reviewer_agent)

