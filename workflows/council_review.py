from __future__ import annotations

from typing import Any, Sequence

from agents.runtime_models import (
    ActivationState,
    AgentReportEnvelope,
    MissionEnvelope,
    MissionStatus,
    MissionType,
)


class CouncilReview:
    def __init__(self, agent_map: dict[str, Any]):
        self.agent_map = agent_map

    def run_review(self, mission: MissionEnvelope) -> dict:
        janus = self.agent_map.get("janus")
        sage = self.agent_map.get("sage")
        hermes = self.agent_map.get("hermes")

        if not janus:
            return {"status": "FAILED", "error": "Janus required for council review"}

        reports: list[AgentReportEnvelope] = []
        for agent_id in mission.target_agents:
            agent = self.agent_map.get(agent_id)
            if not agent:
                continue
            try:
                report = agent.receive_mission(mission)
                reports.append(report)
            except Exception as e:
                reports.append(AgentReportEnvelope(
                    agent_id=agent_id,
                    mission_id=mission.mission_id,
                    mission_type="council_mission",
                    summary=f"Error: {e}",
                    status="FAILED",
                ))

        consolidated = janus.aggregate_council_output(reports)
        llm_summary = janus.consolidate_council(reports)

        risk_result = None
        if sage:
            evidence_list = [
                {"evidence_id": eid, "classification": "I5_SPECULATIVE"}
                for r in reports for eid in r.evidence_ids
            ]
            risk_result = sage.review_risk(evidence_list)

        lesson_result = None
        if hermes:
            quality = hermes.review_evidence_quality(
                [{"classification": "I5_SPECULATIVE", "evidence_id": eid}
                 for r in reports for eid in r.evidence_ids]
            )
            lesson_result = quality

        return {
            "status": "COMPLETED",
            "mission_id": mission.mission_id,
            "consolidated_report": consolidated.to_dict(),
            "llm_consolidation": llm_summary,
            "risk_review": risk_result,
            "lesson_quality": lesson_result,
            "agent_reports": [r.to_dict() for r in reports],
        }

    def assess_readiness(self) -> dict:
        janus = self.agent_map.get("janus")
        sage = self.agent_map.get("sage")

        if not janus:
            return {"status": "FAILED", "error": "Janus required"}

        agent_readiness = janus.check_all_agents_ready(self.agent_map)
        compliance = None
        if sage:
            compliance = sage.compliance_report(
                ActivationState.SANDBOX_ACTIVE
            )

        return {
            "agent_readiness": agent_readiness,
            "compliance": compliance,
            "all_ready": agent_readiness.get("all_ready", False)
            and (compliance is None or compliance.get("all_pass", False)),
        }
