from __future__ import annotations

from typing import Any
from memory.capability_pipeline.schemas import CAPABILITY_FAMILY_TYPES


DOMAIN_TO_FAMILY = {
    "Trading": "Trading Operations",
    "Risk": "Risk Governance",
    "Execution": "Execution Intelligence",
    "Governance": "Knowledge Governance",
    "Memory": "Memory Governance",
    "Engineering": "Engineering Excellence",
    "Agent": "Agent Coordination",
}


class CapabilityFamilyEngine:
    """Creates capability families from discovered capabilities."""

    def __init__(self, capability_registry, family_registry):
        self.capability_registry = capability_registry
        self.family_registry = family_registry

    def discover_families(self, owner_agent: str = "Sage") -> list:
        caps = self.capability_registry.list_all()
        family_map = {ft: {"ids": [], "names": [], "confidences": []} for ft in CAPABILITY_FAMILY_TYPES}

        for cap in caps:
            family = DOMAIN_TO_FAMILY.get(cap.domain, "Engineering Excellence")
            if family in family_map:
                family_map[family]["ids"].append(cap.capability_id)
                family_map[family]["names"].append(cap.name)
                family_map[family]["confidences"].append(cap.confidence_score)

        families = []
        for fname, data in family_map.items():
            if not data["ids"]:
                continue
            avg_conf = sum(data["confidences"]) / len(data["confidences"]) if data["confidences"] else 0.0
            family = self.family_registry.create(
                family_name=fname,
                member_capability_ids=data["ids"],
                member_capability_names=data["names"],
                family_confidence=round(avg_conf, 2),
                evidence={
                    "member_count": len(data["ids"]),
                    "avg_confidence": round(avg_conf, 2),
                },
                owner_agent=owner_agent,
                tags=[fname.lower().replace(" ", "_"), "capability_family"],
            )
            families.append(family)
        return families
