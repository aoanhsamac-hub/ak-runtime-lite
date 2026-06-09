from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from memory.schemas.records import _require, make_id, stable_hash, utc_now, DEPENDENCY_RELATIONSHIP_TYPES


@dataclass(frozen=True)
class SkillDependencyRecord:
    dependency_id: str = field(default_factory=lambda: make_id("DEP"))
    source_skill_id: str = ""
    target_id: str = ""
    target_type: str = ""
    relationship_type: str = ""
    strength: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)
    created_by: str = ""

    def __post_init__(self):
        for name in ("source_skill_id", "target_id", "target_type", "relationship_type"):
            _require(getattr(self, name), name)
        if self.relationship_type not in DEPENDENCY_RELATIONSHIP_TYPES:
            raise ValueError(f"invalid relationship_type: {self.relationship_type}")
        valid_target_types = {"skill", "dataset", "tool", "agent", "capability"}
        if self.target_type not in valid_target_types:
            raise ValueError(f"invalid target_type: {self.target_type}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SkillOwnershipRecord:
    ownership_id: str = field(default_factory=lambda: make_id("OWN"))
    skill_id: str = ""
    owner_agent: str = ""
    primary_users: list[str] = field(default_factory=list)
    secondary_users: list[str] = field(default_factory=list)
    forbidden_users: list[str] = field(default_factory=list)
    assigned_at: str = field(default_factory=utc_now)
    assigned_by: str = ""
    access_level: str = "OWNER"

    def __post_init__(self):
        for name in ("skill_id", "owner_agent", "assigned_by"):
            _require(getattr(self, name), name)
        valid_access = {"OWNER", "PRIMARY_USER", "SECONDARY_USER", "FORBIDDEN_USER"}
        if self.access_level not in valid_access:
            raise ValueError(f"invalid access_level: {self.access_level}")
        for user in self.forbidden_users:
            if user in self.primary_users or user in self.secondary_users:
                raise ValueError(f"forbidden user {user} cannot be in primary/secondary users")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)