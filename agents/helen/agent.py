from agents.base import BaseAgent
from agents.identity import get_identity
from agents.role_boundary import get_role_boundary
from agents.runtime_models import AgentReportEnvelope
from connectors.llm_connector import LLMConnector


class HelenAgent(BaseAgent):
    def __init__(self, memory_interface=None, memory_client=None, llm_connector=None):
        super().__init__(get_identity("helen"), get_role_boundary("helen"), memory_interface, memory_client)
        self.llm = llm_connector or LLMConnector()

    def get_identity(self):
        return self.identity

    def get_role_boundary(self):
        return self.role_boundary

    def research_topic(self, topic: str, domain: str = "technology") -> dict:
        prompt = (
            f"Research {domain} topic: {topic}\n"
            f"Provide: key findings, sources, confidence level, limitations."
        )
        llm_result = self.llm.execute(prompt)
        return {
            "topic": topic,
            "domain": domain,
            "research": llm_result.get("content", ""),
            "mode": llm_result.get("mode", "mock"),
            "evidence_classification": "I2_HYPOTHESIS",
        }

    def classify_source(self, source: str, content: str) -> dict:
        prompt = (
            f"Classify this information source:\n"
            f"Source: {source}\n"
            f"Content: {content[:300]}\n"
            f"Provide: information classification (I0-I9), confidence, reasoning."
        )
        llm_result = self.llm.execute(prompt)
        return {
            "source": source,
            "classification": llm_result.get("content", "I5_SPECULATIVE"),
            "mode": llm_result.get("mode", "mock"),
        }

    def validate_research(self, research_output: dict) -> dict:
        return {
            "validated": True,
            "source_verified": research_output.get("mode", "mock") == "api",
            "classification": research_output.get("evidence_classification", "I5_SPECULATIVE"),
            "reviewer": self.identity.agent_id,
        }

    def generate_intelligence_report(self, mission_id: str) -> AgentReportEnvelope:
        return AgentReportEnvelope(
            agent_id=self.identity.agent_id,
            mission_id=mission_id,
            mission_type="intelligence_mission",
            summary="External intelligence research completed",
            evidence_ids=[e.evidence_id for e in self._evidence_registry],
            status="COMPLETED",
        )


def create_agent(memory_interface=None, memory_client=None, llm_connector=None):
    return HelenAgent(memory_interface, memory_client, llm_connector)
