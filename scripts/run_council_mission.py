#!/usr/bin/env python3
"""Run a council mission with all 7 AK agents."""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_council_mission(objective: str) -> dict:
    from agents.janus.agent import create_agent as create_janus
    from agents.sage.agent import create_agent as create_sage
    from agents.hermes.agent import create_agent as create_hermes
    from agents.iris.agent import create_agent as create_iris
    from agents.helen.agent import create_agent as create_helen
    from agents.lang_lieu.agent import create_agent as create_lang_lieu
    from agents.yet_kieu.agent import create_agent as create_yet_kieu
    from agents.runtime_models import ActivationState
    from workflows.mission_runtime import MissionRuntime
    from workflows.council_review import CouncilReview
    from memory.learning_runtime import LearningRuntime
    from memory.evidence_registry import EvidenceRegistry
    from memory.usage_registry import CapabilityUsageRegistry as UsageRegistry
    from memory.learning_runtime import LessonCandidateRegistry, AgentPerformanceRegistry

    class FakeMemoryInterface:
        def normalize_agent(self, agent):
            aliases = {"lang_lieu": "LangLieu", "yet_kieu": "YetKieu"}
            return aliases.get(agent, agent.title())

        def _validate_agent(self, agent):
            return None

        def record_decision_trace(self, payload):
            return {"trace_id": "TRACE-COUNCIL", **payload}

    fake_memory = FakeMemoryInterface()

    creators = [create_janus, create_sage, create_hermes, create_iris, create_helen, create_lang_lieu, create_yet_kieu]
    agents = {}
    for creator in creators:
        agent = creator(memory_interface=fake_memory)
        agent.boot()
        agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
        agents[agent.identity.agent_id] = agent

    learning = LearningRuntime()
    runtime = MissionRuntime(agents, learning)
    council = CouncilReview(agents)

    # Run mission
    mission_result = runtime.run_council_mission(objective)

    # Run council review
    janus = agents.get("janus")
    if janus and mission_result.get("status") == "COMPLETED":
        agent_reports = mission_result.get("reports", [])
        review_result = council.assess_readiness()
    else:
        review_result = {"status": "SKIPPED", "reason": "Mission not completed"}

    # Persist registries
    for agent in agents.values():
        for ev in agent.get_evidence_registry():
            learning.evidence.record_evidence(ev)
        for ls in agent.get_lesson_registry():
            learning.lessons.record_lesson(ls)
        for us in agent.get_usage_registry():
            learning.usage.record_usage(us)

    return {
        "mission": mission_result,
        "council_review": review_result,
        "registries": {
            "evidence": learning.evidence.summary(),
            "lessons": learning.lessons.summary(),
            "usage": learning.usage.summary(),
            "performance": learning.performance.summary(),
        },
    }


def main():
    import sys
    objective = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Build first AK operational learning mission"
    print(f"Running council mission: {objective}")
    result = run_council_mission(objective)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result.get("mission", {}).get("status") == "COMPLETED":
        print("\nRESULT: COUNCIL MISSION COMPLETED")
        return 0
    else:
        print("\nRESULT: COUNCIL MISSION FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
