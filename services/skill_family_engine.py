from __future__ import annotations

from typing import Any
from memory.learning_registry.schemas import SkillFamilyRecord, SKILL_FAMILY_TYPES, SKILL_CATEGORIES


CATEGORY_TO_FAMILY: dict[str, str] = {
    "Trading Skills": "Trading Family",
    "Risk Skills": "Risk Family",
    "Execution Skills": "Execution Family",
    "Memory Skills": "Memory Family",
    "Governance Skills": "Governance Family",
    "Engineering Skills": "Engineering Family",
    "Agent Skills": "Agent Family",
}


class SkillFamilyEngine:
    """Discovers skill families from candidate skills."""

    def __init__(self, candidate_skill_registry, family_registry):
        self.candidate_skill_registry = candidate_skill_registry
        self.family_registry = family_registry

    def discover_families(self, owner_agent: str = "Sage") -> list[SkillFamilyRecord]:
        skills = self.candidate_skill_registry.list_all()
        family_map: dict[str, dict[str, Any]] = {
            ftype: {"ids": [], "names": [], "confidences": [], "tags": []}
            for ftype in SKILL_FAMILY_TYPES
        }

        for skill in skills:
            family = self._classify_to_family(skill)
            if family and family in family_map:
                family_map[family]["ids"].append(skill.candidate_skill_id)
                family_map[family]["names"].append(skill.name)
                family_map[family]["confidences"].append(skill.confidence_score)
                family_map[family]["tags"].extend(skill.tags)

        families: list[SkillFamilyRecord] = []
        for fname, data in family_map.items():
            if not data["ids"]:
                continue
            avg_conf = sum(data["confidences"]) / len(data["confidences"]) if data["confidences"] else 0.0
            family = self.family_registry.create_family(
                family_name=fname,
                member_skill_ids=data["ids"],
                member_skill_names=data["names"],
                family_confidence=round(avg_conf, 2),
                evidence={
                    "member_count": len(data["ids"]),
                    "avg_confidence": round(avg_conf, 2),
                },
                owner_agent=owner_agent,
                tags=[fname.lower().replace(" ", "_"), "family"],
            )
            families.append(family)

        return families

    @staticmethod
    def _classify_to_family(skill) -> str:
        for cat, family in CATEGORY_TO_FAMILY.items():
            if cat.lower().replace(" ", "_") in str(skill.name).lower():
                return family
        for tag in skill.tags:
            normalized = tag.lower().replace(" ", "_").replace("-", "_")
            for family in SKILL_FAMILY_TYPES:
                key = family.lower().replace(" ", "_")
                if key.startswith(normalized) or normalized.startswith(key.rstrip("_family")):
                    return family
        return "Engineering Family"
