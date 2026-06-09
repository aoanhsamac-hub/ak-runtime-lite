"""Test all 7 agents' LLM API calling capability with timeouts."""
import time

from agents.janus.agent import JanusAgent
from agents.sage.agent import SageAgent
from agents.hermes.agent import HermesAgent
from agents.iris.agent import IrisAgent
from agents.helen.agent import HelenAgent
from agents.lang_lieu.agent import LangLieuAgent
from agents.yet_kieu.agent import YetKieuAgent
from agents.runtime_models import ActivationState, EvidenceRecord, EvidenceClassification, MissionEnvelope, MissionType, AgentReportEnvelope
from connectors.llm_connector import LLMConnector


LLM_KWARGS = {"timeout": 15, "max_tokens": 128, "temperature": 0.1}


import os

LLM_KWARGS = {"timeout": 20, "max_tokens": 128}


def _make_evidence(text="Sample evidence"):
    return EvidenceRecord(
        evidence_id="ev-test-001",
        source_agent="test",
        mission_id="m-test",
        tool_used="test",
        input_summary=text,
        output_summary=text,
        classification=EvidenceClassification.I5_SPECULATIVE,
    )


def _make_reports():
    return [
        AgentReportEnvelope(agent_id="iris", mission_id="m1", summary="Research complete", status="COMPLETED"),
        AgentReportEnvelope(agent_id="helen", mission_id="m2", summary="Intelligence gathered", status="COMPLETED"),
    ]


def test_janus_llm():
    agent = JanusAgent()
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    result = agent.consolidate_council(_make_reports())
    assert result is not None
    mode = result.get("mode", "unknown")
    content = result.get("llm_consolidation") or ""
    print(f"  janus: mode={mode}, content_len={len(content)}")
    assert mode == "api", f"Expected api mode, got {mode}"


def test_sage_llm():
    agent = SageAgent()
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    result = agent.veto_proposal({"title": "Test", "description": "Test description", "risk_level": "LOW"})
    assert result is not None
    mode = result.get("mode", "unknown")
    reason = result.get("reason") or ""
    print(f"  sage: mode={mode}, content_len={len(reason)}")
    assert mode == "api", f"Expected api mode, got {mode}"


def test_hermes_llm():
    agent = HermesAgent()
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    result = agent.distill_lesson([_make_evidence()])
    assert result is not None
    print(f"  hermes: lesson_title={result.title[:60]}")


def test_iris_llm():
    agent = IrisAgent()
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    result = agent.market_research("AI market trends 2026")
    assert result is not None
    mode = result.get("mode", "unknown")
    content = result.get("research") or ""
    print(f"  iris: mode={mode}, content_len={len(content)}")


def test_helen_llm():
    agent = HelenAgent()
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    result = agent.research_topic("quantum computing", domain="technology")
    assert result is not None
    mode = result.get("mode", "unknown")
    content = result.get("research") or ""
    print(f"  helen: mode={mode}, content_len={len(content)}")


def test_lang_lieu_llm():
    agent = LangLieuAgent()
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    result = agent.plan_implementation("Build a test script")
    assert result is not None
    mode = result.get("mode", "unknown")
    plan = result.get("plan") or ""
    print(f"  lang_lieu: mode={mode}, content_len={len(plan)}")


def test_yet_kieu_llm():
    agent = YetKieuAgent()
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    result = agent.incident_report({"type": "disk_full", "description": "Disk space low", "severity": "MEDIUM"})
    assert result is not None
    mode = result.get("mode", "unknown")
    analysis = result.get("analysis") or ""
    print(f"  yet_kieu: mode={mode}, content_len={len(analysis)}")


def test_all_agents_boot_and_have_llm():
    agents = [
        ("janus", JanusAgent()),
        ("sage", SageAgent()),
        ("hermes", HermesAgent()),
        ("iris", IrisAgent()),
        ("helen", HelenAgent()),
        ("lang_lieu", LangLieuAgent()),
        ("yet_kieu", YetKieuAgent()),
    ]
    for name, agent in agents:
        status = agent.boot()
        assert status["status"] == "operational", f"{name} boot failed: {status}"
        assert hasattr(agent, "llm"), f"{name} missing llm"
        assert agent.llm is not None, f"{name} llm is None"
    print("  all 7 agents booted with LLM: OK")


if __name__ == "__main__":
    print("=== All 7 Agents LLM API Test ===")
    print(f"Provider: openrouter | Key set: {bool(os.environ.get('OPENROUTER_API_KEY'))}")
    print()

    tests = [
        ("boot", test_all_agents_boot_and_have_llm),
        ("janus", test_janus_llm),
        ("sage", test_sage_llm),
        ("hermes", test_hermes_llm),
        ("iris", test_iris_llm),
        ("helen", test_helen_llm),
        ("lang_lieu", test_lang_lieu_llm),
        ("yet_kieu", test_yet_kieu_llm),
    ]

    start = time.time()
    results = {}
    for name, fn in tests:
        t0 = time.time()
        try:
            fn()
            results[name] = "PASS"
        except Exception as e:
            results[name] = f"FAIL: {e}"
        print(f"  [{name}] {results[name]} ({time.time()-t0:.1f}s)")

    elapsed = time.time() - start
    passed = sum(1 for v in results.values() if v == "PASS")
    print(f"\nResults: {passed}/{len(results)} passed ({elapsed:.1f}s)")
