from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


STOP_WORDS = {
    "skill", "skills", "cluster", "clusters", "signals", "signal",
    "insight", "insights", "candidate", "discovery", "discovered",
    "signals)", "(1", "(2", "(3", "(4", "(5", "(6", "(7", "(8", "(9", "(10",
    "(11", "(12", "(13", "(14", "(15",
    "pattern", "anomaly", "governance", "dataset", "repeatability",
    "decision", "execution", "risk", "trading", "performance",
    "engineering", "memory", "market", "process",
    "sources)", "source", "types)", "type",
    "consolidated", "emerging", "trend", "gap",
    "direct", "insight:",
}


@dataclass
class DuplicationResult:
    skill_id: str
    skill_name: str
    status: str  # unique / duplicate / superseded / overlapping / conflicting
    match_ids: list[str] = field(default_factory=list)
    match_names: list[str] = field(default_factory=list)
    reason: str = ""


@dataclass
class MergeSuggestion:
    primary_id: str
    primary_name: str
    secondary_ids: list[str]
    reason: str = ""


class SkillDeduplicationEngine:
    """Detects duplicate, superseded, overlapping, and conflicting skills.

    No automatic merge — all results are advisory.
    """

    def __init__(self, candidate_skill_registry):
        self.candidate_skill_registry = candidate_skill_registry

    def run_all(self) -> dict[str, Any]:
        skills = self.candidate_skill_registry.list_all()
        results: list[DuplicationResult] = []
        merge_suggestions: list[MergeSuggestion] = []

        for i, skill_a in enumerate(skills):
            for j, skill_b in enumerate(skills):
                if j <= i:
                    continue
                name_a = skill_a.name.lower()
                name_b = skill_b.name.lower()

                if name_a == name_b:
                    results.append(DuplicationResult(
                        skill_id=skill_b.candidate_skill_id,
                        skill_name=skill_b.name,
                        status="duplicate",
                        match_ids=[skill_a.candidate_skill_id],
                        match_names=[skill_a.name],
                        reason="Exact name match",
                    ))
                    merge_suggestions.append(MergeSuggestion(
                        primary_id=skill_a.candidate_skill_id,
                        primary_name=skill_a.name,
                        secondary_ids=[skill_b.candidate_skill_id],
                        reason="Duplicate skills -- consider merging",
                    ))
                    continue

                if self._is_subset(name_a, name_b):
                    results.append(DuplicationResult(
                        skill_id=skill_b.candidate_skill_id,
                        skill_name=skill_b.name,
                        status="superseded",
                        match_ids=[skill_a.candidate_skill_id],
                        match_names=[skill_a.name],
                        reason=f"'{skill_b.name}' appears to be superseded by '{skill_a.name}'",
                    ))
                    continue

                if self._overlaps(name_a, name_b):
                    results.append(DuplicationResult(
                        skill_id=skill_b.candidate_skill_id,
                        skill_name=skill_b.name,
                        status="overlapping",
                        match_ids=[skill_a.candidate_skill_id],
                        match_names=[skill_a.name],
                        reason=f"Overlap detected between '{skill_a.name}' and '{skill_b.name}'",
                    ))

                if self._conflicts(name_a, name_b):
                    results.append(DuplicationResult(
                        skill_id=skill_b.candidate_skill_id,
                        skill_name=skill_b.name,
                        status="conflicting",
                        match_ids=[skill_a.candidate_skill_id],
                        match_names=[skill_a.name],
                        reason=f"Potential conflict between '{skill_a.name}' and '{skill_b.name}'",
                    ))

        for skill in skills:
            if not any(r.skill_id == skill.candidate_skill_id for r in results):
                results.append(DuplicationResult(
                    skill_id=skill.candidate_skill_id,
                    skill_name=skill.name,
                    status="unique",
                    reason="No duplicate or conflict detected",
                ))

        return {
            "results": results,
            "merge_suggestions": merge_suggestions,
            "unique_count": sum(1 for r in results if r.status == "unique"),
            "duplicate_count": sum(1 for r in results if r.status == "duplicate"),
            "superseded_count": sum(1 for r in results if r.status == "superseded"),
            "overlapping_count": sum(1 for r in results if r.status == "overlapping"),
            "conflicting_count": sum(1 for r in results if r.status == "conflicting"),
        }

    @staticmethod
    def _sig_words(name: str) -> set[str]:
        words = set(name.replace(":", " ").replace("(", " ").replace(")", " ").split())
        return {w.lower() for w in words if w.lower() not in STOP_WORDS}

    def _is_subset(self, name_a: str, name_b: str) -> bool:
        words_a = self._sig_words(name_a)
        words_b = self._sig_words(name_b)
        if not words_a or not words_b:
            return False
        shorter = words_a if len(words_a) <= len(words_b) else words_b
        longer = words_b if len(words_a) <= len(words_b) else words_a
        return len(shorter) > 0 and shorter.issubset(longer) and len(shorter) >= len(longer) * 0.5

    def _overlaps(self, name_a: str, name_b: str) -> bool:
        words_a = self._sig_words(name_a)
        words_b = self._sig_words(name_b)
        common = words_a & words_b
        if not common:
            return False
        min_len = min(len(words_a), len(words_b))
        return len(common) >= min_len * 0.5 and min_len > 0

    @staticmethod
    def _conflicts(name_a: str, name_b: str) -> bool:
        conflict_markers = {"avoid", "never", "must_not", "prohibit", "reject", "forbid"}
        a_markers = set(name_a.split()) & conflict_markers
        b_markers = set(name_b.split()) & conflict_markers
        if not a_markers and not b_markers:
            return False
        common_ctx = set(name_a.split()) & set(name_b.split())
        return bool(common_ctx) and (bool(a_markers) != bool(b_markers))
