from memory.decision_trace_registry import DecisionTraceRegistry
from memory.lancedb_adapter import LanceDBAdapter

from tests.test_lancedb_adapter import FakeBackend


def test_decision_trace_records_required_reasoning_and_evidence(tmp_path):
    registry = DecisionTraceRegistry(LanceDBAdapter(tmp_path, backend=FakeBackend()))

    trace = registry.record(
        agent="LangLieu",
        decision="Use lazy LanceDB adapter",
        reasoning="Dependency is not installed yet.",
        evidence=["importlib check"],
        outcome="Adapter fails closed until dependency exists.",
        lesson_generated="L-1",
    )

    assert trace.trace_id.startswith("TRACE-")
    assert trace.evidence == ["importlib check"]


def test_decision_trace_rejects_missing_evidence(tmp_path):
    registry = DecisionTraceRegistry(LanceDBAdapter(tmp_path, backend=FakeBackend()))

    try:
        registry.record(
            agent="LangLieu",
            decision="No evidence",
            reasoning="Incomplete",
            evidence=[],
            outcome="Rejected",
        )
    except ValueError as exc:
        assert "evidence" in str(exc).lower()
    else:
        raise AssertionError("missing evidence must be rejected")
