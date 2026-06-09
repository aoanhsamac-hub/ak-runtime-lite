from agents.base import BaseAgent
from agents.identity import get_identity
from agents.role_boundary import get_role_boundary
from agents.runtime_models import AgentReportEnvelope
from connectors.llm_connector import LLMConnector


class IrisAgent(BaseAgent):
    def __init__(self, memory_interface=None, memory_client=None, llm_connector=None):
        super().__init__(get_identity("iris"), get_role_boundary("iris"), memory_interface, memory_client)
        self.llm = llm_connector or LLMConnector()

    def get_identity(self):
        return self.identity

    def get_role_boundary(self):
        return self.role_boundary

    def market_research(self, topic: str) -> dict:
        prompt = (
            f"Conduct market research on: {topic}\n"
            f"Provide: market overview, key trends, risk factors, sources."
        )
        llm_result = self.llm.execute(prompt)
        return {
            "topic": topic,
            "research": llm_result.get("content", ""),
            "mode": llm_result.get("mode", "mock"),
            "evidence_classification": "I4_SCENARIO",
            "disclaimer": "Paper-mode recommendation only. No live execution.",
            "recommendation": "research_complete",
        }

    def review_trading_hypothesis(self, hypothesis: dict) -> dict:
        prompt = (
            f"Review trading hypothesis:\n"
            f"Asset: {hypothesis.get('asset', 'unknown')}\n"
            f"Direction: {hypothesis.get('direction', 'unknown')}\n"
            f"Rationale: {hypothesis.get('rationale', 'none')}\n"
            f"Provide: hypothesis assessment, risk factors, confidence level."
        )
        llm_result = self.llm.execute(prompt)
        return {
            "hypothesis": hypothesis,
            "assessment": llm_result.get("content", ""),
            "mode": llm_result.get("mode", "mock"),
            "approved_for_paper": True,
            "requires_sage_review": True,
            "disclaimer": "Hypothesis reviewed for paper-mode only.",
        }

    def package_strategy_evidence(self, strategy: dict, evidence: list[dict]) -> dict:
        return {
            "strategy": strategy.get("name", "unknown"),
            "evidence_packaged": len(evidence),
            "status": "packaged",
            "ready_for_sage_review": True,
        }

    def generate_intelligence_report(self, mission_id: str) -> AgentReportEnvelope:
        return AgentReportEnvelope(
            agent_id=self.identity.agent_id,
            mission_id=mission_id,
            mission_type="intelligence_mission",
            summary="Market intelligence research completed",
            status="COMPLETED",
        )


def create_agent(memory_interface=None, memory_client=None, llm_connector=None):
    return IrisAgent(memory_interface, memory_client, llm_connector)
