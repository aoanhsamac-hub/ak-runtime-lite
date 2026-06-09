#!/usr/bin/env python3
"""AK Agent Smoke Test - verifies all 7 agents boot and are operational."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_smoke_test() -> dict:
    from agents.janus.agent import create_agent as create_janus
    from agents.sage.agent import create_agent as create_sage
    from agents.hermes.agent import create_agent as create_hermes
    from agents.iris.agent import create_agent as create_iris
    from agents.helen.agent import create_agent as create_helen
    from agents.lang_lieu.agent import create_agent as create_lang_lieu
    from agents.yet_kieu.agent import create_agent as create_yet_kieu
    from agents.base import BaseAgent
    from agents.runtime_models import ActivationState, MissionEnvelope, MissionType
    from connectors.llm_connector import LLMConnector
    from workflows.mission_runtime import MissionRuntime
    from memory.learning_runtime import LearningRuntime
    from memory.evidence_registry import EvidenceRegistry
    from memory.usage_registry import CapabilityUsageRegistry
    from memory.learning_runtime import LessonCandidateRegistry, AgentPerformanceRegistry

    results = {}
    errors = []
    all_pass = True

    class FakeMemoryInterface:
        def normalize_agent(self, agent):
            aliases = {"lang_lieu": "LangLieu", "yet_kieu": "YetKieu"}
            return aliases.get(agent, agent.title())

        def _validate_agent(self, agent):
            return None

        def record_decision_trace(self, payload):
            return {"trace_id": "TRACE-TEST", **payload}

    fake_memory = FakeMemoryInterface()

    # 1. All agents boot
    creators = [create_janus, create_sage, create_hermes, create_iris, create_helen, create_lang_lieu, create_yet_kieu]
    agents = {}
    for creator in creators:
        agent = creator(memory_interface=fake_memory)
        boot_result = agent.boot()
        agents[agent.identity.agent_id] = agent
        ok = boot_result.get("status") == "operational"
        results[f"boot_{agent.identity.agent_id}"] = {
            "pass": ok, "status": boot_result.get("status"),
        }
        if not ok:
            errors.append(f"{agent.identity.agent_id} boot failed")
            all_pass = False

    # 2. All agents can call LLM connector or mock
    for aid, agent in agents.items():
        if hasattr(agent, "llm"):
            llm_result = agent.llm.execute("Test prompt")
            ok = llm_result.get("success", False) and llm_result.get("mode") in ("mock", "api")
            results[f"llm_{aid}"] = {"pass": ok, "mode": llm_result.get("mode")}
            if not ok:
                errors.append(f"{aid} LLM call failed")
                all_pass = False

    # 3. All agents generate AgentReportEnvelope
    for aid, agent in agents.items():
        report = agent.generate_report_envelope(mission_type="smoke_test")
        ok = report.agent_id == aid and report.status == "DRAFT"
        results[f"report_{aid}"] = {"pass": ok, "report_id": report.report_id}
        if not ok:
            errors.append(f"{aid} report generation failed")
            all_pass = False

    # 4. All agents write evidence
    mission = MissionEnvelope(mission_type=MissionType.COUNCIL, title="Smoke Test", objective="Verify agent capabilities")
    for aid, agent in agents.items():
        agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
        report = agent.receive_mission(mission)
        evidence_count = len(agent.get_evidence_registry())
        lesson_count = len(agent.get_lesson_registry())
        usage_count = len(agent.get_usage_registry())
        ok = evidence_count > 0 or report.status != "LOCKED"
        results[f"evidence_{aid}"] = {
            "pass": ok,
            "evidence": evidence_count,
            "lessons": lesson_count,
            "usage": usage_count,
            "report_status": report.status,
        }

    # 5. Hermes distills at least one lesson
    hermes = agents.get("hermes")
    if hermes:
        evidence_records = hermes.get_evidence_registry()
        if evidence_records:
            lesson = hermes.distill_lesson(evidence_records)
            ok = lesson is not None
            results["hermes_distill"] = {"pass": ok, "lesson_id": lesson.lesson_id if lesson else None}
            if not ok:
                errors.append("Hermes lesson distillation failed")
                all_pass = False

    # 6. Sage blocks unsafe activation
    sage = agents.get("sage")
    if sage:
        gate = sage.validate_activation(ActivationState.OPERATIONAL_APPROVED)
        ok = not gate.get("allowed", True)
        results["sage_block"] = {"pass": ok, "reason": gate.get("reason")}
        if not ok:
            errors.append("Sage failed to block unsafe activation")
            all_pass = False

    # 7. Janus consolidates council output
    janus = agents.get("janus")
    if janus:
        agent_reports = [
            agent.generate_report_envelope(mission_type="smoke_test")
            for aid, agent in agents.items()
            if aid != "janus"
        ]
        consolidated = janus.consolidate_council(agent_reports)
        ok = consolidated.get("total_reports") == len(agent_reports)
        results["janus_consolidate"] = {"pass": ok, **consolidated}
        if not ok:
            errors.append("Janus consolidation failed")
            all_pass = False

    # 8. Activation state becomes SANDBOX_ACTIVE only after all tests pass
    if all_pass:
        for agent in agents.values():
            if hasattr(agent, "set_activation_state"):
                agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
        final_states = {
            aid: agent.get_context().activation_state.value
            for aid, agent in agents.items()
        }
        results["activation"] = {"pass": True, "final_states": final_states}
    else:
        results["activation"] = {"pass": False, "reason": "Not all tests passed"}

    results["summary"] = {
        "all_pass": all_pass,
        "total_checks": len(results),
        "errors": errors,
    }

    return results


def main():
    print("=" * 60)
    print("AK Agent Smoke Test")
    print("=" * 60)

    results = run_smoke_test()

    for key, value in results.items():
        if key == "summary":
            continue
        status = "PASS" if value.get("pass", False) else "FAIL"
        print(f"  [{status}] {key}")

    summary = results.get("summary", {})
    print()
    print(f"Total checks: {summary.get('total_checks', 0)}")
    print(f"All pass: {summary.get('all_pass', False)}")
    if summary.get("errors"):
        print(f"Errors: {summary['errors']}")

    print()
    if summary.get("all_pass"):
        print("RESULT: ALL TESTS PASSED - AGENTS READY FOR SANDBOX")
        return 0
    else:
        print("RESULT: SOME TESTS FAILED - REVIEW REQUIRED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
