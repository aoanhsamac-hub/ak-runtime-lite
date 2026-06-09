#!/usr/bin/env python3
"""AK Control CLI - Unified interface for agent operations."""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def cmd_ask(target: str, question: str) -> dict:
    from connectors.llm_connector import LLMConnector
    llm = LLMConnector()
    prompt = f"[{target}] {question}\nProvide a structured response with analysis and recommendations."
    result = llm.execute(prompt)
    return {
        "target": target,
        "question": question,
        "response": result.get("content", ""),
        "mode": result.get("mode", "mock"),
    }


def cmd_council(objective: str) -> dict:
    from scripts.run_council_mission import run_council_mission
    return run_council_mission(objective)


def cmd_status() -> dict:
    from agents.janus.agent import create_agent as create_janus
    from agents.sage.agent import create_agent as create_sage
    from agents.hermes.agent import create_agent as create_hermes
    from agents.iris.agent import create_agent as create_iris
    from agents.helen.agent import create_agent as create_helen
    from agents.lang_lieu.agent import create_agent as create_lang_lieu
    from agents.yet_kieu.agent import create_agent as create_yet_kieu
    from agents.runtime_models import ActivationState
    from workflows.mission_runtime import MissionRuntime
    from memory.learning_runtime import LearningRuntime

    class FakeMemoryInterface:
        def normalize_agent(self, agent):
            aliases = {"lang_lieu": "LangLieu", "yet_kieu": "YetKieu"}
            return aliases.get(agent, agent.title())

        def _validate_agent(self, agent):
            return None

        def record_decision_trace(self, payload):
            return {"trace_id": "TRACE-STATUS", **payload}

    fake_memory = FakeMemoryInterface()
    creators = [create_janus, create_sage, create_hermes, create_iris, create_helen, create_lang_lieu, create_yet_kieu]
    agents = {}
    for creator in creators:
        agent = creator(memory_interface=fake_memory)
        agent.boot()
        agents[agent.identity.agent_id] = agent

    learning = LearningRuntime()
    runtime = MissionRuntime(agents, learning)
    return {
        "agents": runtime.get_agent_status(),
        "readiness": learning.check_activation_readiness(),
        "registries": {
            "evidence": learning.evidence.summary(),
            "lessons": learning.lessons.summary(),
            "usage": learning.usage.summary(),
        },
    }


def cmd_smoke() -> dict:
    from scripts.run_agent_smoke_test import run_smoke_test
    return run_smoke_test()


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python akctl.py ask <agent> <question>")
        print("  python akctl.py council <objective>")
        print("  python akctl.py status")
        print("  python akctl.py smoke")
        return 1

    command = sys.argv[1]

    if command == "ask" and len(sys.argv) >= 4:
        target = sys.argv[2]
        question = " ".join(sys.argv[3:])
        result = cmd_ask(target, question)
    elif command == "council":
        objective = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Assess AK readiness for sandbox activation"
        result = cmd_council(objective)
    elif command == "status":
        result = cmd_status()
    elif command == "smoke":
        result = cmd_smoke()
    else:
        print(f"Unknown command: {command}")
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
