from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AgentRole(str, Enum):
    ORCHESTRATOR = "orchestrator"
    GOVERNANCE = "governance"
    MEMORY = "memory"
    ECONOMIC = "economic"
    INFORMATION = "information"
    ENGINEERING = "engineering"
    SECURITY = "security"


class AgentDepartment(str, Enum):
    COORDINATION = "coordination"
    SOVEREIGN_COURT = "sovereign_court"
    MEMORY_CORPUS = "memory_corpus"
    TREASURY = "treasury"
    INTELLIGENCE = "intelligence"
    ENGINEERING = "engineering"
    SECURITY = "security"


class AgentAuthorityLevel(str, Enum):
    OBSERVE = "observe"
    PROPOSE = "propose"
    REVIEW = "review"
    COORDINATE = "coordinate"
    VETO = "veto"


@dataclass(frozen=True)
class AgentIdentity:
    agent_id: str
    name: str
    technical_name: str
    department: str
    constitutional_role: str
    authority_level: str
    owner: str
    reviewer: str
    status: str = "operational"
    capabilities: tuple[str, ...] = ()
    skills: tuple[str, ...] = ()
    maturity_level: str = ""
    evolution_cycle: int = 0

    def to_dict(self) -> dict:
        base = dict(self.__dict__)
        base["capabilities"] = list(self.capabilities)
        base["skills"] = list(self.skills)
        return base


AGENT_IDENTITIES: dict[str, AgentIdentity] = {
    "janus": AgentIdentity("janus", "Janus", "janus", AgentDepartment.COORDINATION.value, "Mission orchestration and coordination", AgentAuthorityLevel.COORDINATE.value, "Hung Vuong", "Sage",
                           capabilities=("orchestration", "council_consolidation", "mission_routing", "agent_coordination"),
                           skills=("strategic_planning", "multi_agent_coordination", "report_aggregation")),
    "sage": AgentIdentity("sage", "Sage", "sage", AgentDepartment.SOVEREIGN_COURT.value, "Governance, risk, review, veto", AgentAuthorityLevel.VETO.value, "Hung Vuong", "Hung Vuong",
                           capabilities=("governance_review", "risk_classification", "compliance_audit", "veto_authority"),
                           skills=("governance_gate", "risk_assessment", "policy_enforcement")),
    "hermes": AgentIdentity("hermes", "Hermes", "hermes", AgentDepartment.MEMORY_CORPUS.value, "Memory, lessons, datasets, archive", AgentAuthorityLevel.REVIEW.value, "Hung Vuong", "Sage",
                           capabilities=("lesson_distillation", "evidence_review", "dataset_management", "memory_reporting"),
                           skills=("knowledge_extraction", "evidence_quality_scoring", "archive_management")),
    "iris": AgentIdentity("iris", "Iris", "iris", AgentDepartment.TREASURY.value, "Economic and market intelligence", AgentAuthorityLevel.PROPOSE.value, "Hung Vuong", "Sage",
                           capabilities=("market_analysis", "economic_intelligence", "portfolio_analysis", "budget_proposal"),
                           skills=("market_research", "economic_forecasting", "resource_allocation")),
    "helen": AgentIdentity("helen", "Helen", "helen", AgentDepartment.INTELLIGENCE.value, "Information validation and external context", AgentAuthorityLevel.PROPOSE.value, "Hung Vuong", "Sage",
                           capabilities=("information_validation", "macro_analysis", "civilization_intelligence", "communication_draft"),
                           skills=("source_classification", "external_context_research", "cross_reference")),
    "lang_lieu": AgentIdentity("lang_lieu", "Lang Lieu", "lang_lieu", AgentDepartment.ENGINEERING.value, "Engineering and architecture", AgentAuthorityLevel.PROPOSE.value, "Hung Vuong", "Sage",
                           capabilities=("code_generation", "architecture_design", "test_automation", "technical_reporting"),
                           skills=("python_engineering", "system_architecture", "code_review")),
    "yet_kieu": AgentIdentity("yet_kieu", "Yet Kieu", "yet_kieu", AgentDepartment.SECURITY.value, "Security and infrastructure observation", AgentAuthorityLevel.REVIEW.value, "Hung Vuong", "Sage",
                           capabilities=("infrastructure_monitoring", "security_review", "incident_response", "runtime_observation"),
                           skills=("security_audit", "infrastructure_analysis", "incident_management")),
}


def get_identity(agent_id: str) -> AgentIdentity:
    return AGENT_IDENTITIES[agent_id]
