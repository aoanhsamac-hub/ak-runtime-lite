from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping, Sequence
from uuid import uuid4


class ActivationState(str, Enum):
    LOCKED = "LOCKED"
    READY_FOR_SANDBOX = "READY_FOR_SANDBOX"
    SANDBOX_ACTIVE = "SANDBOX_ACTIVE"
    PILOT_ACTIVE = "PILOT_ACTIVE"
    OPERATIONAL_LIMITED = "OPERATIONAL_LIMITED"
    OPERATIONAL_APPROVED = "OPERATIONAL_APPROVED"


class MissionType(str, Enum):
    COUNCIL = "council_mission"
    ENGINEERING = "engineering_mission"
    MEMORY = "memory_mission"
    INTELLIGENCE = "intelligence_mission"
    INFRASTRUCTURE = "infrastructure_mission"
    GOVERNANCE = "governance_mission"
    ACTIVATION = "activation_mission"


class MissionStatus(str, Enum):
    DRAFT = "DRAFT"
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class EvidenceClassification(str, Enum):
    I0_OFFICIAL_VERIFIED = "I0_OFFICIAL_VERIFIED"
    I1_PROBABLE = "I1_PROBABLE"
    I2_HYPOTHESIS = "I2_HYPOTHESIS"
    I3_THEORY = "I3_THEORY"
    I4_SCENARIO = "I4_SCENARIO"
    I5_SPECULATIVE = "I5_SPECULATIVE"
    I6_FICTION = "I6_FICTION"
    I7_LEGEND = "I7_LEGEND"
    I8_RUMOR = "I8_RUMOR"
    I9_REJECTED = "I9_REJECTED"


class ToolStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _new_id(prefix: str = "ID") -> str:
    return f"{prefix}-{uuid4().hex[:12].upper()}"


@dataclass
class AgentContext:
    agent_id: str
    agent_name: str
    role: str
    department: str
    authority_level: str
    activation_state: ActivationState = ActivationState.LOCKED
    capabilities: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "role": self.role,
            "department": self.department,
            "authority_level": self.authority_level,
            "activation_state": self.activation_state.value,
            "capabilities": list(self.capabilities),
            "metadata": dict(self.metadata),
        }


@dataclass
class MissionEnvelope:
    mission_id: str = field(default_factory=lambda: _new_id("MISSION"))
    mission_type: MissionType = MissionType.COUNCIL
    title: str = ""
    objective: str = ""
    requester: str = ""
    target_agents: list[str] = field(default_factory=list)
    status: MissionStatus = MissionStatus.DRAFT
    required_tools: list[str] = field(default_factory=list)
    evidence_requirements: list[str] = field(default_factory=list)
    input_data: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_utc_now)
    completed_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass
class ToolRequest:
    tool_id: str = field(default_factory=lambda: _new_id("TOOL"))
    tool_name: str = ""
    params: dict[str, Any] = field(default_factory=dict)
    requester_agent: str = ""
    status: ToolStatus = ToolStatus.PENDING
    result: ToolResult | None = None
    started_at: str = ""
    completed_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass
class ToolResult:
    success: bool = False
    output: Any = None
    error: str = ""
    duration_ms: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "duration_ms": self.duration_ms,
            "metadata": dict(self.metadata),
        }


@dataclass
class EvidenceRecord:
    evidence_id: str = field(default_factory=lambda: _new_id("EVIDENCE"))
    source_agent: str = ""
    mission_id: str = ""
    tool_used: str = ""
    input_summary: str = ""
    output_summary: str = ""
    classification: EvidenceClassification = EvidenceClassification.I5_SPECULATIVE
    owner: str = ""
    reviewer: str = ""
    status: str = "DRAFT"
    timestamp: str = field(default_factory=_utc_now)
    lineage: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = dict(self.__dict__)
        d["classification"] = self.classification.value
        return d


@dataclass
class LessonRecord:
    lesson_id: str = field(default_factory=lambda: _new_id("LESSON"))
    source_evidence_ids: list[str] = field(default_factory=list)
    source_agent: str = ""
    mission_id: str = ""
    title: str = ""
    description: str = ""
    context: str = ""
    outcome: str = ""
    quality_score: float = 0.0
    status: str = "DRAFT"
    reviewer: str = ""
    owner: str = ""
    timestamp: str = field(default_factory=_utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass
class CapabilityUsageRecord:
    usage_id: str = field(default_factory=lambda: _new_id("USAGE"))
    agent_id: str = ""
    capability_name: str = ""
    mission_type: str = ""
    success: bool = False
    duration_ms: float = 0.0
    evidence_count: int = 0
    lesson_count: int = 0
    error: str = ""
    roi_estimate: float = 0.0
    adoption_status: str = "not_tracked"
    timestamp: str = field(default_factory=_utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass
class AgentReportEnvelope:
    report_id: str = field(default_factory=lambda: _new_id("REPORT"))
    agent_id: str = ""
    mission_id: str = ""
    mission_type: str = ""
    summary: str = ""
    evidence_ids: list[str] = field(default_factory=list)
    lesson_ids: list[str] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)
    status: str = "DRAFT"
    recommendation: str = ""
    created_at: str = field(default_factory=_utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)
