from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from memory.capability_registry import CapabilityRegistry
from memory.schemas import CapabilityRecord, SkillRecord
from memory.skill_registry import SkillRegistry


@dataclass
class CapabilityEvolutionResult:
    capability: CapabilityRecord | None
    status: str
    issues: list[str]


MIN_SKILLS_FOR_CAPABILITY = 2
MATURITY_LEVELS = ["EMERGING", "DEVELOPING", "ESTABLISHED", "MATURE"]


class CapabilityEvolutionPipeline:
    def __init__(self, capability_registry: CapabilityRegistry, skill_registry: SkillRegistry):
        self.capability_registry = capability_registry
        self.skill_registry = skill_registry

    def evolve(self, name: str, skill_ids: list[str], owner_agent: str, reviewer_agent: str) -> CapabilityEvolutionResult:
        issues = self._validate_skills(skill_ids)
        if issues:
            return CapabilityEvolutionResult(capability=None, status="BLOCKED", issues=issues)
        maturity = self._assess_maturity(skill_ids)
        capability = self.capability_registry.create(
            name=name,
            skills=[{"skill_id": sid, "status": "ACTIVE"} for sid in skill_ids],
            owner_agent=owner_agent,
            reviewer_agent=reviewer_agent,
            status="DRAFT",
            maturity_level=maturity,
            metrics=self._build_metrics(skill_ids),
        )
        return CapabilityEvolutionResult(capability=capability, status="CANDIDATE", issues=[])

    def _validate_skills(self, skill_ids: list[str]) -> list[str]:
        issues = []
        if len(skill_ids) < MIN_SKILLS_FOR_CAPABILITY:
            issues.append(f"minimum {MIN_SKILLS_FOR_CAPABILITY} skills required, got {len(skill_ids)}")
        for sid in skill_ids:
            try:
                skill = self.skill_registry.get(sid)
                if skill.status not in {"APPROVED", "ACTIVE"}:
                    issues.append(f"skill {sid} must be APPROVED or ACTIVE")
            except KeyError:
                issues.append(f"skill not found: {sid}")
        return issues

    def _assess_maturity(self, skill_ids: list[str]) -> str:
        approved_count = 0
        active_count = 0
        for sid in skill_ids:
            try:
                skill = self.skill_registry.get(sid)
                if skill.status == "ACTIVE":
                    active_count += 1
                elif skill.status == "APPROVED":
                    approved_count += 1
            except KeyError:
                continue
        if active_count >= 3 and len(skill_ids) >= 5:
            return "MATURE"
        if active_count >= 2 and len(skill_ids) >= 3:
            return "ESTABLISHED"
        if approved_count >= 2:
            return "DEVELOPING"
        return "EMERGING"

    def _build_metrics(self, skill_ids: list[str]) -> dict[str, Any]:
        return {
            "skill_count": len(skill_ids),
            "active_count": sum(1 for sid in skill_ids if self._is_active(sid)),
            "approved_count": sum(1 for sid in skill_ids if self._is_approved(sid)),
        }

    def _is_active(self, skill_id: str) -> bool:
        try:
            return self.skill_registry.get(skill_id).status == "ACTIVE"
        except KeyError:
            return False

    def _is_approved(self, skill_id: str) -> bool:
        try:
            return self.skill_registry.get(skill_id).status == "APPROVED"
        except KeyError:
            return False
