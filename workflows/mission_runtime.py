from __future__ import annotations

from typing import Any, Sequence

from agents.runtime_models import (
    ActivationState,
    AgentReportEnvelope,
    MissionEnvelope,
    MissionStatus,
    MissionType,
)
from memory.learning_runtime import LearningRuntime


class MissionRuntime:
    def __init__(self, agent_map: dict[str, Any], learning_runtime: LearningRuntime | None = None):
        self.agent_map = agent_map
        self.learning = learning_runtime or LearningRuntime()

    def run_mission(self, mission: MissionEnvelope) -> dict:
        janus = self.agent_map.get("janus")
        sage = self.agent_map.get("sage")

        if janus is None:
            return {"status": "FAILED", "error": "Janus agent not available"}

        mission.status = MissionStatus.IN_PROGRESS

        reports: list[AgentReportEnvelope] = []
        for agent_id in mission.target_agents:
            agent = self.agent_map.get(agent_id)
            if agent is None:
                continue
            try:
                report = agent.receive_mission(mission)
                reports.append(report)
                self.learning.process_mission_output(report)
            except Exception as e:
                reports.append(AgentReportEnvelope(
                    agent_id=agent_id,
                    mission_id=mission.mission_id,
                    mission_type=mission.mission_type.value,
                    summary=f"Agent failed: {e}",
                    status="FAILED",
                ))

        consolidated = janus.consolidate_council(reports)

        if sage and mission.mission_type in (
            MissionType.ACTIVATION, MissionType.GOVERNANCE
        ):
            gate = sage.validate_activation(
                ActivationState.SANDBOX_ACTIVE,
                {"evidence_count": consolidated.get("total_evidence", 0)},
            )
            if not gate.get("allowed", False):
                mission.status = MissionStatus.BLOCKED
                return {
                    "status": "BLOCKED",
                    "mission_id": mission.mission_id,
                    "reason": gate.get("reason", "Blocked by Sage"),
                    "consolidated": consolidated,
                    "reports": [r.to_dict() for r in reports],
                }

        mission.status = MissionStatus.COMPLETED
        return {
            "status": "COMPLETED",
            "mission_id": mission.mission_id,
            "consolidated": consolidated,
            "reports": [r.to_dict() for r in reports],
        }

    def run_council_mission(self, objective: str) -> dict:
        janus = self.agent_map.get("janus")
        if janus is None:
            return {"status": "FAILED", "error": "Janus not available"}

        all_agents = [aid for aid in self.agent_map if aid != "janus"]
        mission = janus.plan_mission(objective, all_agents)
        mission.mission_type = MissionType.COUNCIL
        return self.run_mission(mission)

    def run_activation_mission(self) -> dict:
        janus = self.agent_map.get("janus")
        sage = self.agent_map.get("sage")
        if not janus or not sage:
            return {"status": "FAILED", "error": "Required agents not available"}

        readiness = self.learning.check_activation_readiness()
        if not readiness.get("ready", False):
            return {
                "status": "BLOCKED",
                "reason": readiness.get("reason", "Not ready"),
                "readiness": readiness,
            }

        gate = sage.validate_activation(ActivationState.SANDBOX_ACTIVE, readiness)
        if not gate.get("allowed", False):
            return {
                "status": "BLOCKED",
                "reason": gate.get("reason", "Blocked by Sage"),
                "gate": gate,
            }

        for agent in self.agent_map.values():
            if hasattr(agent, "set_activation_state"):
                agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)

        compliance = sage.compliance_report(ActivationState.SANDBOX_ACTIVE)
        return {
            "status": "SANDBOX_ACTIVE",
            "readiness": readiness,
            "gate": gate,
            "compliance": compliance,
        }

    def get_agent_status(self) -> dict:
        results = {}
        for aid, agent in self.agent_map.items():
            ctx = agent.get_context() if hasattr(agent, "get_context") else None
            results[aid] = {
                "activation_state": ctx.activation_state.value if ctx else "UNKNOWN",
                "status": agent.status() if hasattr(agent, "status") else "UNKNOWN",
            }
        return results
