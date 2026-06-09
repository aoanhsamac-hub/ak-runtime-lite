from __future__ import annotations


class DistillationPipeline:
    def distill(self, reports: list[dict]) -> dict:
        lesson_target = max(1, min(20, len(reports) // 5 or len(reports)))
        skill_target = max(1, min(5, lesson_target // 4 or 1))
        capability_target = 1 if skill_target else 0
        return {
            "reports": len(reports),
            "lesson_target": lesson_target,
            "skill_target": skill_target,
            "capability_target": capability_target,
            "auto_promote": False,
        }

