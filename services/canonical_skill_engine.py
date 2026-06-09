from __future__ import annotations

from typing import Any
from memory.learning_registry.schemas import CanonicalSkillRecord, SKILL_FAMILY_TYPES


class CanonicalSkillEngine:
    """Classifies skills into canonical, superseded, overlapping, duplicate, isolated."""

    def __init__(self, candidate_skill_registry, family_registry, canonical_registry):
        self.candidate_skill_registry = candidate_skill_registry
        self.family_registry = family_registry
        self.canonical_registry = canonical_registry

    def classify_all(self, owner_agent: str = "Sage") -> list[CanonicalSkillRecord]:
        skills = self.candidate_skill_registry.list_all()
        if not skills:
            return []

        families = self.family_registry.list_all()
        family_skills: dict[str, list] = {}
        for f in families:
            family_skills[f.family_name] = []
        for s in skills:
            for f in families:
                if s.candidate_skill_id in f.member_skill_ids:
                    family_skills.setdefault(f.family_name, []).append(s)
                    break
            else:
                family_skills.setdefault("Engineering Family", []).append(s)

        results: list[CanonicalSkillRecord] = []
        seen_names: set[str] = set()
        name_groups: dict[str, list] = {}

        for s in skills:
            base = self._normalize_name(s.name)
            name_groups.setdefault(base, []).append(s)

        for base, group in name_groups.items():
            if len(group) == 1:
                s = group[0]
                family_id = self._find_family_id(s.candidate_skill_id, families)
                results.append(self.canonical_registry.create_canonical(
                    name=s.name,
                    description=s.description,
                    classification="CANONICAL",
                    source_skill_ids=[s.candidate_skill_id],
                    family_id=family_id,
                    confidence_score=s.confidence_score,
                    evidence=s.evidence,
                    owner_agent=owner_agent,
                    tags=s.tags + ["canonical"],
                    metadata={"original_id": s.candidate_skill_id},
                ))
                seen_names.add(s.candidate_skill_id)
                continue

            sorted_group = sorted(group, key=lambda x: x.confidence_score, reverse=True)
            primary = sorted_group[0]
            family_id = self._find_family_id(primary.candidate_skill_id, families)

            sup_ids = [s.candidate_skill_id for s in sorted_group[1:] if self._is_superseded(primary, s)]
            ovlp_ids = [s.candidate_skill_id for s in sorted_group[1:] if s.candidate_skill_id not in sup_ids]
            dup_ids = [s.candidate_skill_id for s in sorted_group[1:] if s.name.lower() == primary.name.lower()]

            results.append(self.canonical_registry.create_canonical(
                name=primary.name,
                description=primary.description,
                classification="CANONICAL",
                source_skill_ids=[s.candidate_skill_id for s in sorted_group],
                family_id=family_id,
                superseded_ids=sup_ids,
                overlapping_ids=ovlp_ids,
                duplicate_ids=dup_ids,
                merge_recommendations=[f"Merge {len(sorted_group)-1} related skills into canonical: {primary.name}"],
                confidence_score=primary.confidence_score,
                evidence={
                    "group_size": len(sorted_group),
                    "primary_id": primary.candidate_skill_id,
                    "superseded_count": len(sup_ids),
                    "overlapping_count": len(ovlp_ids),
                },
                owner_agent=owner_agent,
                tags=primary.tags + ["canonical"],
                metadata={"source_group": [s.candidate_skill_id for s in sorted_group]},
            ))
            seen_names.add(primary.candidate_skill_id)

        for s in skills:
            if s.candidate_skill_id not in seen_names:
                family_id = self._find_family_id(s.candidate_skill_id, families) if families else ""
                results.append(self.canonical_registry.create_canonical(
                    name=s.name, description=s.description,
                    classification="ISOLATED",
                    source_skill_ids=[s.candidate_skill_id],
                    family_id=family_id,
                    confidence_score=s.confidence_score,
                    evidence=s.evidence, owner_agent=owner_agent,
                    tags=s.tags + ["isolated"],
                ))

        return results

    @staticmethod
    def _normalize_name(name: str) -> str:
        import re
        return re.sub(r"\d+", "", name.lower().replace(":", "").replace("(", "").replace(")", "")).strip()

    @staticmethod
    def _is_superseded(primary, other) -> bool:
        if primary.confidence_score > other.confidence_score + 0.1:
            return True
        return False

    @staticmethod
    def _find_family_id(skill_id: str, families: list) -> str:
        for f in families:
            if skill_id in f.member_skill_ids:
                return f.family_id
        return ""
