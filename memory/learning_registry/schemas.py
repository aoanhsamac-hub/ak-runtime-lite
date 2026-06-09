from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from memory.schemas.records import _require, make_id, stable_hash, utc_now


SIGNAL_TYPES = {
    "PATTERN", "ANOMALY", "REPEATABILITY", "GOVERNANCE", "DATASET",
    "DECISION", "EXECUTION", "RISK", "TRADING", "PERFORMANCE",
}
INSIGHT_TYPES = {
    "PATTERN", "CONSOLIDATION", "GAP", "TREND", "RISK",
    "PROCESS", "SKILL", "GOVERNANCE", "MARKET", "EXECUTION", "PERFORMANCE",
}
LEARNING_STATUSES = {"CANDIDATE", "ACTIVE", "DEPRECATED", "ARCHIVED"}
APPROVAL_STATUSES = {"PENDING_REVIEW", "APPROVED", "REJECTED"}
ACTIVATION_STATUSES = {"DISABLED", "ENABLED"}

LEARNING_RISK_LEVELS = {"LEVEL_0_SOVEREIGN", "LEVEL_1_MODERATE", "LEVEL_2_HIGH", "LEVEL_3_CRITICAL"}

CLUSTER_TYPES = {
    "DECISION", "TRADING", "RISK", "EXECUTION",
    "GOVERNANCE", "ENGINEERING", "MEMORY",
}
SKILL_CATEGORIES = {
    "Trading Skills", "Risk Skills", "Execution Skills",
    "Governance Skills", "Memory Skills", "Engineering Skills", "Agent Skills",
}
SKILL_FAMILY_TYPES = {
    "Trading Family", "Risk Family", "Execution Family",
    "Memory Family", "Governance Family", "Engineering Family", "Agent Family",
}
MATURITY_LEVELS = {"EMERGING", "DEVELOPING", "ESTABLISHED", "ADVANCED", "SOVEREIGN"}
CANONICAL_CLASSIFICATIONS = {"CANONICAL", "SUPERSEDED", "OVERLAPPING", "DUPLICATE", "ISOLATED"}
PROMOTION_DECISIONS = {"APPROVED", "REJECTED", "NEEDS_REVIEW", "NEEDS_EVIDENCE", "ARCHIVED"}


@dataclass(frozen=True)
class LearningSignalRecord:
    signal_id: str = field(default_factory=lambda: make_id("LSIG"))
    signal_type: str = ""
    source_kind: str = ""
    source_id: str = ""
    source_hash: str = ""
    title: str = ""
    description: str = ""
    content: str = ""
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
        for name in ("signal_type", "source_kind", "source_id", "title", "owner_agent", "reviewer_agent"):
            _require(getattr(self, name), name)
        if self.signal_type not in SIGNAL_TYPES:
            raise ValueError(f"invalid signal_type: {self.signal_type}")
        if self.status not in LEARNING_STATUSES:
            raise ValueError(f"invalid signal status: {self.status}")
        if self.risk_level not in LEARNING_RISK_LEVELS:
            raise ValueError(f"invalid risk_level: {self.risk_level}")
        if not self.source_hash:
            object.__setattr__(self, "source_hash", stable_hash(self.source_kind, self.source_id, self.content))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InsightRecord:
    insight_id: str = field(default_factory=lambda: make_id("INS"))
    insight_type: str = ""
    title: str = ""
    description: str = ""
    source_signal_ids: list[str] = field(default_factory=list)
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
        for name in ("insight_type", "title", "description", "owner_agent", "reviewer_agent"):
            _require(getattr(self, name), name)
        if self.insight_type not in INSIGHT_TYPES:
            raise ValueError(f"invalid insight_type: {self.insight_type}")
        if self.status not in LEARNING_STATUSES:
            raise ValueError(f"invalid insight status: {self.status}")
        if self.risk_level not in LEARNING_RISK_LEVELS:
            raise ValueError(f"invalid risk_level: {self.risk_level}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SignalClusterRecord:
    cluster_id: str = field(default_factory=lambda: make_id("CLS"))
    cluster_type: str = ""
    title: str = ""
    description: str = ""
    source_signal_ids: list[str] = field(default_factory=list)
    signal_count: int = 0
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
        for name in ("cluster_type", "title", "description", "owner_agent", "reviewer_agent"):
            _require(getattr(self, name), name)
        if self.cluster_type not in CLUSTER_TYPES:
            raise ValueError(f"invalid cluster_type: {self.cluster_type}")
        if self.status not in LEARNING_STATUSES:
            raise ValueError(f"invalid cluster status: {self.status}")
        if self.risk_level not in LEARNING_RISK_LEVELS:
            raise ValueError(f"invalid risk_level: {self.risk_level}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)



@dataclass(frozen=True)
class CandidateSkillRecord:
    candidate_skill_id: str = field(default_factory=lambda: make_id("CSK"))
    name: str = ""
    description: str = ""
    source_insight_ids: list[str] = field(default_factory=list)
    source_signal_ids: list[str] = field(default_factory=list)
    source_lesson_ids: list[str] = field(default_factory=list)
    owner_agent: str = ""
    reviewer_agent: str = "Sage"
    risk_level: str = "LEVEL_1_MODERATE"
    status: str = "CANDIDATE"
    approval_status: str = "PENDING_REVIEW"
    activation_status: str = "DISABLED"
    test_cases: list[str] = field(default_factory=list)
    allowed_agents: list[str] = field(default_factory=list)
    confidence_score: float = 0.0
    evidence: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)
    version: int = 1

    def __post_init__(self):
        for name in ("name", "description", "owner_agent", "reviewer_agent"):
            _require(getattr(self, name), name)
        if self.status not in LEARNING_STATUSES:
            raise ValueError(f"invalid candidate status: {self.status}")
        if self.approval_status not in APPROVAL_STATUSES:
            raise ValueError(f"invalid approval_status: {self.approval_status}")
        if self.activation_status not in ACTIVATION_STATUSES:
            raise ValueError(f"invalid activation_status: {self.activation_status}")
        if self.risk_level not in LEARNING_RISK_LEVELS:
            raise ValueError(f"invalid risk_level: {self.risk_level}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


PROMOTION_DECISIONS_SET = frozenset(PROMOTION_DECISIONS)


@dataclass(frozen=True)
class PromotionDecisionRecord:
    decision_id: str = field(default_factory=lambda: make_id("PDEC"))
    skill_id: str = ""
    skill_name: str = ""
    canonical_id: str = ""
    reviewer: str = ""
    decision: str = ""
    reason: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)
    risk_score: float = 0.0
    governance_score: float = 0.0
    policy_version: str = "1.0"
    owner_agent: str = ""
    timestamp: str = field(default_factory=utc_now)

    def __post_init__(self):
        if self.decision not in PROMOTION_DECISIONS:
            raise ValueError(f"invalid promotion decision: {self.decision}")
        if not self.skill_id:
            raise ValueError("skill_id is required")
        if not self.reviewer:
            raise ValueError("reviewer is required")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ApprovedSkillRecord:
    approved_skill_id: str = field(default_factory=lambda: make_id("APSK"))
    name: str = ""
    description: str = ""
    canonical_id: str = ""
    candidate_skill_id: str = ""
    family_id: str = ""
    owner_agent: str = ""
    reviewer_agent: str = ""
    approval_authority: str = ""
    risk_level: str = "LEVEL_1_MODERATE"
    status: str = "ACTIVE"
    confidence_score: float = 0.0
    evidence: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    promotion_decision_id: str = ""
    created_at: str = field(default_factory=utc_now)
    version: int = 1

    def __post_init__(self):
        for name in ("name", "description", "owner_agent", "approval_authority"):
            _require(getattr(self, name), name)
        if self.status not in LEARNING_STATUSES:
            raise ValueError(f"invalid approved skill status: {self.status}")
        if self.risk_level not in LEARNING_RISK_LEVELS:
            raise ValueError(f"invalid risk_level: {self.risk_level}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SkillFamilyRecord:
    family_id: str = field(default_factory=lambda: make_id("SFAM"))
    family_name: str = ""
    member_skill_ids: list[str] = field(default_factory=list)
    member_skill_names: list[str] = field(default_factory=list)
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
        for name in ("family_name", "owner_agent", "reviewer_agent"):
            _require(getattr(self, name), name)
        if self.family_name not in SKILL_FAMILY_TYPES:
            raise ValueError(f"invalid family_name: {self.family_name}")
        if self.status not in LEARNING_STATUSES:
            raise ValueError(f"invalid family status: {self.status}")
        if self.risk_level not in LEARNING_RISK_LEVELS:
            raise ValueError(f"invalid risk_level: {self.risk_level}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CanonicalSkillRecord:
    canonical_id: str = field(default_factory=lambda: make_id("CANON"))
    name: str = ""
    description: str = ""
    classification: str = "CANONICAL"
    source_skill_ids: list[str] = field(default_factory=list)
    family_id: str = ""
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
        for name in ("name", "description", "classification", "owner_agent", "reviewer_agent"):
            _require(getattr(self, name), name)
        if self.classification not in CANONICAL_CLASSIFICATIONS:
            raise ValueError(f"invalid classification: {self.classification}")
        if self.status not in LEARNING_STATUSES:
            raise ValueError(f"invalid status: {self.status}")
        if self.risk_level not in LEARNING_RISK_LEVELS:
            raise ValueError(f"invalid risk_level: {self.risk_level}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
