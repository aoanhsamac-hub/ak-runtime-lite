from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any
from uuid import uuid4


LESSON_STATUSES = {"DRAFT", "REVIEWED", "APPROVED", "DEPRECATED", "QUARANTINE"}
SKILL_STATUSES = {"DRAFT", "REVIEWED", "APPROVED", "ACTIVE", "SUSPENDED", "RETIRED", "DEPRECATED", "QUARANTINE"}
CAPABILITY_STATUSES = {"DRAFT", "REVIEWED", "APPROVED", "ACTIVE", "DEPRECATED", "QUARANTINE"}

SKILL_LIFECYCLE_STAGES = {
    "PROPOSED", "DISCOVERED", "SANDBOXED", "VALIDATED", "APPROVED",
    "ACTIVE", "SUSPENDED", "DEPRECATED", "RETIRED", "ARCHIVED"
}

SKILL_CATEGORIES = {"core", "imported", "internal", "deprecated", "retired"}
SKILL_SOURCES = {"hermes", "opencode", "openhands", "internal", "legacy", "discovered"}
DEPENDENCY_RELATIONSHIP_TYPES = {
    "depends_on", "conflicts_with", "supersedes", "enhances",
    "requires_dataset", "produces_dataset",
    "requires_tool", "provides_tool",
    "assigned_to", "executable_by", "monitored_by",
    "part_of_capability", "enables_capability"
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:12].upper()}"


def stable_hash(*parts: Any) -> str:
    text = "|".join(str(part) for part in parts)
    return sha256(text.encode("utf-8")).hexdigest()


def _require(value: Any, name: str) -> None:
    if value is None or value == "" or value == []:
        raise ValueError(f"{name} is required")


@dataclass(frozen=True)
class LessonRecord:
    title: str
    summary: str
    content: str
    source: str
    owner_agent: str
    reviewer_agent: str
    risk_level: str
    tags: list[str]
    lesson_id: str = field(default_factory=lambda: make_id("LESSON"))
    source_hash: str = ""
    status: str = "DRAFT"
    created_at: str = field(default_factory=utc_now)
    version: int = 1

    def __post_init__(self):
        for name in ("title", "summary", "content", "source", "owner_agent", "reviewer_agent", "risk_level"):
            _require(getattr(self, name), name)
        if self.status not in LESSON_STATUSES:
            raise ValueError(f"invalid lesson status: {self.status}")
        if not self.source_hash:
            object.__setattr__(self, "source_hash", stable_hash(self.source, self.content))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def with_status(self, status: str, reviewer_agent: str | None = None) -> "LessonRecord":
        return LessonRecord(
            lesson_id=self.lesson_id,
            title=self.title,
            summary=self.summary,
            content=self.content,
            source=self.source,
            source_hash=self.source_hash,
            owner_agent=self.owner_agent,
            reviewer_agent=reviewer_agent or self.reviewer_agent,
            status=status,
            created_at=self.created_at,
            version=self.version + 1,
            risk_level=self.risk_level,
            tags=list(self.tags),
        )


@dataclass(frozen=True)
class SkillRecord:
    name: str
    description: str
    source_lessons: list[str]
    owner_agent: str
    allowed_agents: list[str]
    risk_level: str
    test_cases: list[str]
    skill_id: str = field(default_factory=lambda: make_id("SKILL"))
    reviewer_agent: str = ""
    source_hash: str = ""
    status: str = "DRAFT"
    created_at: str = field(default_factory=utc_now)
    version: int = 1
    lifecycle_stage: str = "PROPOSED"
    updated_at: str = ""
    primary_users: list[str] = field(default_factory=list)
    secondary_users: list[str] = field(default_factory=list)
    forbidden_users: list[str] = field(default_factory=list)
    category: str = "core"
    source: str = "internal"
    dependencies: list[str] = field(default_factory=list)
    required_tools: list[str] = field(default_factory=list)
    governance_requirements: dict[str, Any] = field(default_factory=dict)
    validation_requirements: dict[str, Any] = field(default_factory=dict)
    performance_metrics: dict[str, Any] = field(default_factory=dict)
    retirement_conditions: dict[str, Any] = field(default_factory=dict)
    stop_conditions: dict[str, Any] = field(default_factory=dict)
    audit_requirements: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.reviewer_agent:
            object.__setattr__(self, "reviewer_agent", self.owner_agent)
        if not self.source_hash:
            object.__setattr__(self, "source_hash", stable_hash(self.name, self.description, self.source_lessons))
        if not self.updated_at:
            object.__setattr__(self, "updated_at", self.created_at)
        if not self.primary_users and self.allowed_agents:
            primary = self.allowed_agents[0]
            if primary not in self.forbidden_users:
                object.__setattr__(self, "primary_users", [primary])
        if not self.secondary_users and len(self.allowed_agents) > 1:
            secondary = [a for a in self.allowed_agents[1:] if a not in self.forbidden_users]
            if secondary:
                object.__setattr__(self, "secondary_users", secondary)
        for name in (
            "name",
            "description",
            "source_lessons",
            "owner_agent",
            "reviewer_agent",
            "allowed_agents",
            "risk_level",
            "source_hash",
        ):
            _require(getattr(self, name), name)
        if self.status not in SKILL_STATUSES:
            raise ValueError(f"invalid skill status: {self.status}")
        if self.lifecycle_stage not in SKILL_LIFECYCLE_STAGES:
            raise ValueError(f"invalid skill lifecycle_stage: {self.lifecycle_stage}")
        if self.category not in SKILL_CATEGORIES:
            raise ValueError(f"invalid skill category: {self.category}")
        if self.source not in SKILL_SOURCES:
            raise ValueError(f"invalid skill source: {self.source}")
        for user in self.forbidden_users:
            if user == self.owner_agent:
                raise ValueError(f"forbidden user {user} cannot be the owner_agent")
            if user in self.primary_users or user in self.secondary_users:
                raise ValueError(f"forbidden user {user} cannot be in primary/secondary users")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def with_status(self, status: str, reviewer_agent: str | None = None) -> "SkillRecord":
        return SkillRecord(
            skill_id=self.skill_id,
            name=self.name,
            description=self.description,
            source_lessons=list(self.source_lessons),
            owner_agent=self.owner_agent,
            reviewer_agent=reviewer_agent or self.reviewer_agent,
            source_hash=self.source_hash,
            allowed_agents=list(self.allowed_agents),
            risk_level=self.risk_level,
            status=status,
            version=self.version + 1,
            test_cases=list(self.test_cases),
            created_at=self.created_at,
            lifecycle_stage=self.lifecycle_stage,
            updated_at=utc_now(),
            primary_users=list(self.primary_users),
            secondary_users=list(self.secondary_users),
            forbidden_users=list(self.forbidden_users),
            category=self.category,
            source=self.source,
            dependencies=list(self.dependencies),
            required_tools=list(self.required_tools),
            governance_requirements=dict(self.governance_requirements),
            validation_requirements=dict(self.validation_requirements),
            performance_metrics=dict(self.performance_metrics),
            retirement_conditions=dict(self.retirement_conditions),
            stop_conditions=dict(self.stop_conditions),
            audit_requirements=dict(self.audit_requirements),
        )

    def with_lifecycle_stage(self, lifecycle_stage: str, reviewer_agent: str | None = None) -> "SkillRecord":
        return SkillRecord(
            skill_id=self.skill_id,
            name=self.name,
            description=self.description,
            source_lessons=list(self.source_lessons),
            owner_agent=self.owner_agent,
            reviewer_agent=reviewer_agent or self.reviewer_agent,
            source_hash=self.source_hash,
            allowed_agents=list(self.allowed_agents),
            risk_level=self.risk_level,
            status=self.status,
            version=self.version + 1,
            test_cases=list(self.test_cases),
            created_at=self.created_at,
            lifecycle_stage=lifecycle_stage,
            updated_at=utc_now(),
            primary_users=list(self.primary_users),
            secondary_users=list(self.secondary_users),
            forbidden_users=list(self.forbidden_users),
            category=self.category,
            source=self.source,
            dependencies=list(self.dependencies),
            required_tools=list(self.required_tools),
            governance_requirements=dict(self.governance_requirements),
            validation_requirements=dict(self.validation_requirements),
            performance_metrics=dict(self.performance_metrics),
            retirement_conditions=dict(self.retirement_conditions),
            stop_conditions=dict(self.stop_conditions),
            audit_requirements=dict(self.audit_requirements),
        )

    def with_version(self, **updates) -> "SkillRecord":
        return SkillRecord(
            skill_id=self.skill_id,
            name=updates.get("name", self.name),
            description=updates.get("description", self.description),
            source_lessons=list(updates.get("source_lessons", self.source_lessons)),
            owner_agent=updates.get("owner_agent", self.owner_agent),
            reviewer_agent=updates.get("reviewer_agent", self.reviewer_agent),
            source_hash=self.source_hash,
            allowed_agents=list(updates.get("allowed_agents", self.allowed_agents)),
            risk_level=updates.get("risk_level", self.risk_level),
            status=updates.get("status", self.status),
            version=self.version + 1,
            test_cases=list(updates.get("test_cases", self.test_cases)),
            created_at=self.created_at,
            lifecycle_stage=updates.get("lifecycle_stage", self.lifecycle_stage),
            updated_at=utc_now(),
            primary_users=list(updates.get("primary_users", self.primary_users)),
            secondary_users=list(updates.get("secondary_users", self.secondary_users)),
            forbidden_users=list(updates.get("forbidden_users", self.forbidden_users)),
            category=updates.get("category", self.category),
            source=updates.get("source", self.source),
            dependencies=list(updates.get("dependencies", self.dependencies)),
            required_tools=list(updates.get("required_tools", self.required_tools)),
            governance_requirements=dict(updates.get("governance_requirements", self.governance_requirements)),
            validation_requirements=dict(updates.get("validation_requirements", self.validation_requirements)),
            performance_metrics=dict(updates.get("performance_metrics", self.performance_metrics)),
            retirement_conditions=dict(updates.get("retirement_conditions", self.retirement_conditions)),
            stop_conditions=dict(updates.get("stop_conditions", self.stop_conditions)),
            audit_requirements=dict(updates.get("audit_requirements", self.audit_requirements)),
        )


@dataclass(frozen=True)
class CapabilityRecord:
    name: str
    skills: list[str]
    owner_agent: str
    reviewer_agent: str
    status: str
    maturity_level: str
    metrics: dict[str, Any]
    capability_id: str = field(default_factory=lambda: make_id("CAP"))
    risk_level: str = "LEVEL_1_MODERATE"
    source_hash: str = ""
    created_at: str = field(default_factory=utc_now)
    version: int = 1

    def __post_init__(self):
        if not self.source_hash:
            object.__setattr__(self, "source_hash", stable_hash(self.name, self.skills, self.metrics))
        for name in (
            "name",
            "skills",
            "owner_agent",
            "reviewer_agent",
            "status",
            "maturity_level",
            "risk_level",
            "source_hash",
        ):
            _require(getattr(self, name), name)
        if self.status not in CAPABILITY_STATUSES:
            raise ValueError(f"invalid capability status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DatasetRecord:
    name: str
    source: str
    owner_agent: str
    reviewer_agent: str
    risk_level: str
    status: str = "DRAFT"
    dataset_id: str = field(default_factory=lambda: make_id("DATASET"))
    source_hash: str = ""
    created_at: str = field(default_factory=utc_now)
    version: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        for name in ("name", "source", "owner_agent", "reviewer_agent", "risk_level"):
            _require(getattr(self, name), name)
        if not self.source_hash:
            object.__setattr__(self, "source_hash", stable_hash(self.source, self.name))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DecisionTraceRecord:
    agent: str
    decision: str
    reasoning: str
    evidence: list[str]
    outcome: str
    lesson_generated: str | None = None
    trace_id: str = field(default_factory=lambda: make_id("TRACE"))
    owner_agent: str = ""
    reviewer_agent: str = "Sage"
    source_hash: str = ""
    status: str = "DRAFT"
    risk_level: str = "LEVEL_1_MODERATE"
    version: int = 1
    created_at: str = field(default_factory=utc_now)
    timestamp: str = field(default_factory=utc_now)

    def __post_init__(self):
        if not self.owner_agent:
            object.__setattr__(self, "owner_agent", self.agent)
        if not self.source_hash:
            object.__setattr__(self, "source_hash", stable_hash(self.agent, self.decision, self.evidence, self.outcome))
        for name in (
            "agent",
            "owner_agent",
            "reviewer_agent",
            "source_hash",
            "status",
            "risk_level",
            "version",
            "created_at",
            "decision",
            "reasoning",
            "evidence",
            "outcome",
        ):
            _require(getattr(self, name), name)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
