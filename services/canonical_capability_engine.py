from __future__ import annotations

from typing import Any
from memory.capability_pipeline.schemas import CANONICAL_CLASSIFICATIONS


class CanonicalCapabilityEngine:
    """Classifies capabilities into canonical types."""

    def __init__(self, capability_registry, family_registry, canonical_registry):
        self.capability_registry = capability_registry
        self.family_registry = family_registry
        self.canonical_registry = canonical_registry

    def classify_all(self, owner_agent: str = "Sage") -> list:
        caps = self.capability_registry.list_all()
        if not caps:
            return []
        families = self.family_registry.list_all()
        name_groups = {}
        for cap in caps:
            base = self._normalize(cap.name)
            name_groups.setdefault(base, []).append(cap)
        seen_ids = set()
        results = []

        for base, group in name_groups.items():
            if len(group) == 1:
                cap = group[0]
                fam_id = self._find_family(cap.capability_id, families)
                results.append(self.canonical_registry.create(
                    name=cap.name, description=cap.description,
                    classification="CANONICAL", domain=cap.domain,
                    family_id=fam_id, source_capability_ids=[cap.capability_id],
                    confidence_score=cap.confidence_score, evidence=cap.evidence,
                    owner_agent=owner_agent, tags=cap.tags + ["canonical"],
                    metadata={"original_id": cap.capability_id},
                ))
                seen_ids.add(cap.capability_id)
                continue

            sorted_group = sorted(group, key=lambda x: x.confidence_score, reverse=True)
            primary = sorted_group[0]
            fam_id = self._find_family(primary.capability_id, families)
            sup_ids = [c.capability_id for c in sorted_group[1:] if c.confidence_score < primary.confidence_score - 0.1]
            ovlp_ids = [c.capability_id for c in sorted_group[1:] if c.capability_id not in sup_ids]
            results.append(self.canonical_registry.create(
                name=primary.name, description=primary.description,
                classification="CANONICAL", domain=primary.domain,
                family_id=fam_id, source_capability_ids=[c.capability_id for c in sorted_group],
                superseded_ids=sup_ids, overlapping_ids=ovlp_ids,
                confidence_score=primary.confidence_score,
                evidence={"group_size": len(sorted_group), "primary_id": primary.capability_id},
                owner_agent=owner_agent, tags=primary.tags + ["canonical"],
            ))
            seen_ids.add(primary.capability_id)

        for cap in caps:
            if cap.capability_id not in seen_ids:
                fam_id = self._find_family(cap.capability_id, families)
                results.append(self.canonical_registry.create(
                    name=cap.name, description=cap.description,
                    classification="ISOLATED", domain=cap.domain,
                    family_id=fam_id, source_capability_ids=[cap.capability_id],
                    confidence_score=cap.confidence_score, evidence=cap.evidence,
                    owner_agent=owner_agent, tags=cap.tags + ["isolated"],
                ))
        return results

    @staticmethod
    def _normalize(name: str) -> str:
        import re
        return re.sub(r"\d+", "", name.lower()).strip()

    @staticmethod
    def _find_family(cap_id: str, families: list) -> str:
        for f in families:
            if cap_id in f.member_capability_ids:
                return f.family_id
        return ""
