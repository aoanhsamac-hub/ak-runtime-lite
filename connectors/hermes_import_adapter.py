from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from memory.schemas.records import make_id, utc_now


HERMES_SKILL_STATES = {"DRAFT", "REVIEWED", "APPROVED", "ACTIVE", "DEPRECATED"}

AK_SKILL_STATES = {
    "DRAFT": "PROPOSED", "REVIEWED": "SANDBOXED", "APPROVED": "APPROVED",
    "ACTIVE": "ACTIVE", "DEPRECATED": "DEPRECATED",
}

HERMES_SKILL_CATEGORIES = {"trading", "risk", "execution", "governance", "memory", "engineering", "agent"}

AK_CATEGORY_MAP = {
    "trading": "imported", "risk": "imported", "execution": "imported",
    "governance": "imported", "memory": "imported", "engineering": "imported",
    "agent": "imported",
}


@dataclass(frozen=True)
class HermesSkillManifest:
    hermes_skill_id: str = ""
    name: str = ""
    description: str = ""
    version: str = "1.0"
    owner: str = ""
    status: str = "DRAFT"
    category: str = "engineering"
    dependencies: list[str] = field(default_factory=list)
    required_tools: list[str] = field(default_factory=list)
    risk_level: str = "LEVEL_1_MODERATE"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.status not in HERMES_SKILL_STATES:
            raise ValueError(f"invalid Hermes skill status: {self.status}")
        if self.category not in HERMES_SKILL_CATEGORIES:
            raise ValueError(f"invalid Hermes category: {self.category}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "hermes_skill_id": self.hermes_skill_id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "owner": self.owner,
            "status": self.status,
            "category": self.category,
            "dependencies": list(self.dependencies),
            "required_tools": list(self.required_tools),
            "risk_level": self.risk_level,
            "metadata": dict(self.metadata),
        }


class HermesSkillImporter:
    def __init__(self, skill_registry: Any, lifecycle_engine: Any = None):
        self.skill_registry = skill_registry
        self.lifecycle_engine = lifecycle_engine
        self._import_log: list[dict] = []

    def parse_manifest(self, data: dict) -> HermesSkillManifest:
        manifest = HermesSkillManifest(
            hermes_skill_id=data.get("skill_id", data.get("hermes_skill_id", "")),
            name=data.get("name", ""),
            description=data.get("description", ""),
            version=data.get("version", "1.0"),
            owner=data.get("owner", data.get("owner_agent", "")),
            status=data.get("status", "DRAFT"),
            category=data.get("category", "engineering"),
            dependencies=data.get("dependencies", []),
            required_tools=data.get("required_tools", []),
            risk_level=data.get("risk_level", "LEVEL_1_MODERATE"),
            metadata=data.get("metadata", {}),
        )
        return manifest

    def import_skill(self, manifest: HermesSkillManifest) -> str:
        ak_skill_id = self.skill_registry.create_candidate(
            _skip_lesson_validation=True,
            name=manifest.name,
            description=manifest.description,
            source_lessons=["HERMES-IMPORT"],
            owner_agent="Hermes",
            allowed_agents=["Hermes", "Sage"],
            risk_level=manifest.risk_level,
            test_cases=[],
            category="imported",
            source="hermes",
            lifecycle_stage="PROPOSED",
            dependencies=manifest.dependencies,
            required_tools=manifest.required_tools,
            version=int(manifest.version.split(".")[0]) if manifest.version else 1,
            audit_requirements={"import_source": "hermes", "hermes_id": manifest.hermes_skill_id},
        )
        self._import_log.append({
            "hermes_skill_id": manifest.hermes_skill_id,
            "ak_skill_id": ak_skill_id.skill_id,
            "name": manifest.name,
            "status": "PROPOSED",
            "imported_at": utc_now(),
        })
        return ak_skill_id.skill_id

    def get_import_log(self) -> list[dict]:
        return list(self._import_log)

    def dry_run(self, data: dict) -> dict:
        manifest = self.parse_manifest(data)
        return {
            "hermes_skill_id": manifest.hermes_skill_id,
            "name": manifest.name,
            "ak_category": "imported",
            "ak_lifecycle_stage": "PROPOSED",
            "warnings": [],
            "dry_run": True,
        }