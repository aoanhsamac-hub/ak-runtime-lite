from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from memory.schemas.records import _require, make_id, utc_now


CAPABILITY_DOMAINS = {
    "Trading", "Risk", "Execution", "Governance", "Memory", "Engineering", "Agent",
}
CAPABILITY_FAMILY_TYPES = {
    "Trading Operations", "Risk Governance", "Memory Governance",
    "Knowledge Governance", "Agent Coordination", "Execution Intelligence",
    "Engineering Excellence",
}
CANONICAL_CLASSIFICATIONS = {"CANONICAL", "SUPERSEDED", "OVERLAPPING", "DUPLICATE", "ISOLATED"}
MATURITY_LEVELS = {"EMERGING", "DEVELOPING", "ESTABLISHED", "ADVANCED", "SOVEREIGN"}
READINESS_LEVELS = {"PROMOTION_READY", "NEEDS_EVIDENCE", "NEEDS_REVIEW", "NOT_READY"}
CAPABILITY_STATUSES = {"CANDIDATE", "ACTIVE", "DEPRECATED", "ARCHIVED"}
LEARNING_RISK_LEVELS = {"LEVEL_0_SOVEREIGN", "LEVEL_1_MODERATE", "LEVEL_2_HIGH", "LEVEL_3_CRITICAL"}


@dataclass(frozen=True)
class CapabilityCandidateRecord:
    capability_id: str = field(default_factory=lambda: make_id("CAPC"))
    name: str = ""
    description: str = ""
    domain: str = ""
    source_skill_ids: list[str] = field(default_factory=list)
    source_trace_ids: list[str] = field(default_factory=list)
    confidence_score: float = 0.0
    evidence: dict[str, Any] = field(default_factory=dict)
    owner_agent: str = ""
    reviewer_agent: str = "Sage"
    risk_level: str = "LEVEL_1_MODERATE"
    status: str = "CANDIDATE"
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)
    version: int = 1

    def __post_init__(self):
        for name in ("name", "description", "domain", "owner_agent"):
            _require(getattr(self, name), name)
        if self.domain not in CAPABILITY_DOMAINS:
            raise ValueError(f"invalid domain: {self.domain}")
        if self.status not in CAPABILITY_STATUSES:
            raise ValueError(f"invalid capability status: {self.status}")
        if self.risk_level not in LEARNING_RISK_LEVELS:
            raise ValueError(f"invalid risk_level: {self.risk_level}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


EVOLUTION_STATES = {"LOCKED", "UNLOCKED", "EVOLVING_MATURITY", "EVOLVING_CYCLE", "EVOLVED", "ROLLED_BACK"}
EVOLUTION_EVENT_TYPES = {"MATURITY_PROGRESSION", "CAPABILITY_EVOLUTION", "ROLLBACK", "PROMOTION"}
MATURITY_LEVEL_EVOLUTION_ORDER: dict[str, int] = {
    "EMERGING": 1, "DEVELOPING": 2, "ESTABLISHED": 3, "ADVANCED": 4, "SOVEREIGN": 5,
}


@dataclass(frozen=True)
class EvolutionEventRecord:
    event_id: str = field(default_factory=lambda: make_id("EVT"))
    capability_id: str = ""
    event_type: str = ""
    from_state: str = ""
    to_state: str = ""
    trigger: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)
    agent_id: str = ""
    governance_issue_id: str = ""
    description: str = ""
    timestamp: str = field(default_factory=utc_now)

    def __post_init__(self):
        if self.event_type not in EVOLUTION_EVENT_TYPES:
            raise ValueError(f"invalid event_type: {self.event_type}")
        if not self.capability_id:
            raise ValueError("capability_id is required")
        if self.from_state and self.from_state not in EVOLUTION_STATES:
            raise ValueError(f"invalid from_state: {self.from_state}")
        if self.to_state and self.to_state not in EVOLUTION_STATES:
            raise ValueError(f"invalid to_state: {self.to_state}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CapabilityFamilyRecord:
    family_id: str = field(default_factory=lambda: make_id("CPF"))
    family_name: str = ""
    member_capability_ids: list[str] = field(default_factory=list)
    member_capability_names: list[str] = field(default_factory=list)
    family_confidence: float = 0.0
    evidence: dict[str, Any] = field(default_factory=dict)
    owner_agent: str = ""
    reviewer_agent: str = "Sage"
    risk_level: str = "LEVEL_1_MODERATE"
    status: str = "CANDIDATE"
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)
    version: int = 1

    def __post_init__(self):
        for name in ("family_name", "owner_agent"):
            _require(getattr(self, name), name)
        if self.family_name not in CAPABILITY_FAMILY_TYPES:
            raise ValueError(f"invalid family_name: {self.family_name}")
        if self.status not in CAPABILITY_STATUSES:
            raise ValueError(f"invalid family status: {self.status}")
        if self.risk_level not in LEARNING_RISK_LEVELS:
            raise ValueError(f"invalid risk_level: {self.risk_level}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CanonicalCapabilityRecord:
    canonical_id: str = field(default_factory=lambda: make_id("CCAP"))
    name: str = ""
    description: str = ""
    classification: str = "CANONICAL"
    domain: str = ""
    family_id: str = ""
    source_capability_ids: list[str] = field(default_factory=list)
    canonical_ref: str = ""
    superseded_ids: list[str] = field(default_factory=list)
    overlapping_ids: list[str] = field(default_factory=list)
    duplicate_ids: list[str] = field(default_factory=list)
    merge_recommendations: list[str] = field(default_factory=list)
    confidence_score: float = 0.0
    evidence: dict[str, Any] = field(default_factory=dict)
    owner_agent: str = ""
    reviewer_agent: str = "Sage"
    risk_level: str = "LEVEL_1_MODERATE"
    status: str = "CANDIDATE"
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)
    version: int = 1

    def __post_init__(self):
        for name in ("name", "description", "classification", "domain", "owner_agent"):
            _require(getattr(self, name), name)
        if self.classification not in CANONICAL_CLASSIFICATIONS:
            raise ValueError(f"invalid classification: {self.classification}")
        if self.domain not in CAPABILITY_DOMAINS:
            raise ValueError(f"invalid domain: {self.domain}")
        if self.status not in CAPABILITY_STATUSES:
            raise ValueError(f"invalid status: {self.status}")
        if self.risk_level not in LEARNING_RISK_LEVELS:
            raise ValueError(f"invalid risk_level: {self.risk_level}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PromotionRecommendationRecord:
    recommendation_id: str = field(default_factory=lambda: make_id("CREC"))
    capability_id: str = ""
    capability_name: str = ""
    canonical_id: str = ""
    recommender: str = ""
    reviewer: str = ""
    decision: str = ""
    reason: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)
    risk_score: float = 0.0
    governance_score: float = 0.0
    owner_agent: str = ""
    timestamp: str = field(default_factory=utc_now)

    def __post_init__(self):
        if self.decision not in READINESS_LEVELS:
            raise ValueError(f"invalid readiness decision: {self.decision}")
        if not self.capability_id:
            raise ValueError("capability_id is required")
        if not self.reviewer:
            raise ValueError("reviewer is required")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
