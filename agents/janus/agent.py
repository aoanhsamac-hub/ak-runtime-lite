from typing import Any, Sequence

from agents.base import BaseAgent
from agents.identity import get_identity
from agents.role_boundary import get_role_boundary
from agents.runtime_models import (
    ActivationState,
    AgentReportEnvelope,
    MissionEnvelope,
    MissionStatus,
    MissionType,
)
from connectors.llm_connector import LLMConnector


class JanusAgent(BaseAgent):
    def __init__(self, memory_interface=None, memory_client=None, llm_connector=None):
        super().__init__(get_identity("janus"), get_role_boundary("janus"), memory_interface, memory_client)
        self.llm = llm_connector or LLMConnector()

    def get_identity(self):
        return self.identity

    def get_role_boundary(self):
        return self.role_boundary

    def plan_mission(self, objective: str, target_agents: list[str] | None = None) -> MissionEnvelope:
        return MissionEnvelope(
            mission_type=MissionType.COUNCIL,
            title=f"Mission: {objective[:60]}",
            objective=objective,
            requester=self.identity.agent_id,
            target_agents=target_agents or [],
            status=MissionStatus.PLANNED,
        )

    def route_mission(self, mission: MissionEnvelope, agent_map: dict[str, Any]) -> dict:
        results = {}
        for agent_id in mission.target_agents:
            agent = agent_map.get(agent_id)
            if agent is None:
                results[agent_id] = {"status": "ERROR", "error": "agent not found"}
                continue
            try:
                report = agent.receive_mission(mission)
                results[agent_id] = report.to_dict()
            except Exception as e:
                results[agent_id] = {"status": "ERROR", "error": str(e)}
        return {
            "mission_id": mission.mission_id,
            "objective": mission.objective,
            "agent_results": results,
            "all_completed": all(
                r.get("status") == "COMPLETED" for r in results.values()
            ),
        }

    def consolidate_council(self, reports: Sequence[AgentReportEnvelope]) -> dict:
        prompt = (
            f"Consolidate {len(reports)} agent reports into a single council summary.\n"
            f"Reports: {[r.summary for r in reports]}\n"
            f"Provide: overall status, key findings, recommendations."
        )
        llm_result = self.llm.execute(prompt)
        return {
            "total_reports": len(reports),
            "completed": sum(1 for r in reports if r.status == "COMPLETED"),
            "llm_consolidation": llm_result.get("content", ""),
            "mode": llm_result.get("mode", "mock"),
        }

    def resolve_dependencies(self, mission: MissionEnvelope) -> list[str]:
        return mission.target_agents

    def aggregate_council_output(self, reports: Sequence[AgentReportEnvelope]) -> AgentReportEnvelope:
        return AgentReportEnvelope(
            agent_id=self.identity.agent_id,
            mission_id=reports[0].mission_id if reports else "",
            mission_type="council_mission",
            summary=f"Council consolidated: {len(reports)} agents reporting",
            evidence_ids=[eid for r in reports for eid in r.evidence_ids],
            lesson_ids=[lid for r in reports for lid in r.lesson_ids],
            status="COMPLETED",
        )

    def check_all_agents_ready(self, agent_map: dict[str, Any]) -> dict:
        results = {}
        for aid, agent in agent_map.items():
            ctx = agent.get_context() if hasattr(agent, "get_context") else None
            results[aid] = {
                "activation_state": ctx.activation_state.value if ctx else "UNKNOWN",
                "boot_status": agent.status() if hasattr(agent, "status") else "UNKNOWN",
            }
        all_ready = all(
            r["activation_state"] not in ("LOCKED", "UNKNOWN")
            for r in results.values()
        )
        return {"all_ready": all_ready, "agents": results}


def create_agent(memory_interface=None, memory_client=None, llm_connector=None):
    return JanusAgent(memory_interface, memory_client, llm_connector)
