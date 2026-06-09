from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from memory.schemas.records import make_id, utc_now


OPENCODE_SKILL_KEYS = {"name", "description", "version", "author", "category", "dependencies", "tools"}
OPENHANDS_SKILL_KEYS = {"name", "description", "version", "author", "category", "dependencies", "tools"}

SOURCE_TYPES = {"opencode", "openhands"}


@dataclass(frozen=True)
class WorkflowSkillManifest:
    workflow_skill_id: str = field(default_factory=lambda: make_id("WFSK"))
    name: str = ""
    description: str = ""
    version: str = "1.0"
    source: str = "opencode"
    source_id: str = ""
    author: str = ""
    category: str = "imported"
    dependencies: list[str] = field(default_factory=list)
    required_tools: list[str] = field(default_factory=list)
    risk_level: str = "LEVEL_1_MODERATE"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.source not in SOURCE_TYPES:
            raise ValueError(f"invalid source: {self.source}")
        for name in ("name", "description"):
            if not getattr(self, name):
                raise ValueError(f"{name} is required")

    def to_dict(self) -> dict[str, Any]:
        return {
            "workflow_skill_id": self.workflow_skill_id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "source": self.source,
            "source_id": self.source_id,
            "author": self.author,
            "category": self.category,
            "dependencies": list(self.dependencies),
            "required_tools": list(self.required_tools),
            "risk_level": self.risk_level,
            "metadata": dict(self.metadata),
        }


class OpenCodeSkillImporter:
    def __init__(self, skill_registry: Any, human_sovereignty_gate: Any = None):
        self.skill_registry = skill_registry
        self.human_sovereignty_gate = human_sovereignty_gate
        self._import_log: list[dict] = []

    def detect_source(self, data: dict) -> str:
        if data.get("openhands_version") or data.get("oh_skill"):
            return "openhands"
        return "opencode"

    def parse_manifest(self, data: dict, source: str | None = None) -> WorkflowSkillManifest:
        actual_source = source or self.detect_source(data)
        manifest = WorkflowSkillManifest(
            name=data.get("name", ""),
            description=data.get("description", ""),
            version=data.get("version", "1.0"),
            source=actual_source,
            source_id=data.get("skill_id", data.get("id", "")),
            author=data.get("author", data.get("owner", "")),
            category="imported",
            dependencies=data.get("dependencies", []),
            required_tools=data.get("tools", data.get("required_tools", [])),
            risk_level=data.get("risk_level", "LEVEL_1_MODERATE"),
            metadata=data.get("metadata", {}),
        )
        return manifest

    def import_skill(self, manifest: WorkflowSkillManifest) -> str:
        ak_skill_id = self.skill_registry.create_candidate(
            _skip_lesson_validation=True,
            name=manifest.name,
            description=manifest.description,
            source_lessons=["WORKFLOW-IMPORT"],
            owner_agent="LangLieu",
            allowed_agents=["Hermes", "Sage", "LangLieu"],
            risk_level=manifest.risk_level,
            test_cases=[],
            category="imported",
            source=manifest.source,
            lifecycle_stage="PROPOSED",
            dependencies=manifest.dependencies,
            required_tools=manifest.required_tools,
            version=int(manifest.version.split(".")[0]) if manifest.version else 1,
            audit_requirements={
                "import_source": manifest.source,
                "source_id": manifest.source_id,
                "source_author": manifest.author,
            },
        )
        self._import_log.append({
            "source_skill_id": manifest.source_id,
            "ak_skill_id": ak_skill_id.skill_id,
            "name": manifest.name,
            "source": manifest.source,
            "status": "PROPOSED",
            "imported_at": utc_now(),
        })
        return ak_skill_id.skill_id

    def get_import_log(self) -> list[dict]:
        return list(self._import_log)

    def dry_run(self, data: dict) -> dict:
        source = self.detect_source(data)
        manifest = self.parse_manifest(data, source)
        return {
            "source_skill_id": manifest.source_id,
            "name": manifest.name,
            "detected_source": source,
            "ak_category": "imported",
            "ak_lifecycle_stage": "PROPOSED",
            "max_lifecycle_stage": "READY_FOR_SANDBOX",
            "warnings": ["Human Sovereignty Gate: max stage is READY_FOR_SANDBOX"],
            "dry_run": True,
        }