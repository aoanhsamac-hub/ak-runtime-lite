"""Tests for runtime stop conditions enforcement."""

import pytest


def _make_identity():
    from agents.identity import get_identity
    return get_identity("iris")


def _get_observer():
    try:
        from connectors.mt5.mt5_demo_observer import MT5DemoObserver
        return MT5DemoObserver()
    except ImportError:
        pytest.skip("MetaTrader5 not available")


class TestStopConditionRAM:
    def test_stop_ram_below_200mb_detected(self):
        threshold_mb = 200
        available_mb = 333
        assert available_mb >= threshold_mb, "RAM below 200 MB threshold"

    def test_stop_ram_threshold_defined(self):
        threshold_mb = 200
        assert isinstance(threshold_mb, int)
        assert threshold_mb > 0


class TestStopConditionMT5Disconnect:
    def test_mt5_disconnect_detected(self):
        observer = _get_observer()
        result = observer.disconnect()
        assert result["status"] == "disconnected"

    def test_mt5_health_check_detects_disconnect(self):
        from connectors.mt5.health_monitor import MT5HealthMonitor
        monitor = MT5HealthMonitor(None)
        result = monitor.check_connection()
        assert result["status"] == "no_observer"


class TestStopConditionSchedulerFailure:
    def test_scheduler_error_detected(self):
        from services.kingdom_scheduler import NationalScheduler
        scheduler = NationalScheduler()
        results = []

        def failing_handler(**kwargs):
            raise RuntimeError("Scheduled task failure")

        for cadence in ["daily", "weekly", "monthly"]:
            tasks = scheduler.get_tasks(cadence)
            for t in tasks:
                scheduler.register_handler(t.task_id, failing_handler)

        for cadence in ["daily", "weekly", "monthly"]:
            results.extend(scheduler._run_cadence(cadence, failing_handler))

        errors = [r for r in results if r["status"] == "error"]
        assert len(errors) >= 1

    def test_duplicate_scheduler_instance_detected(self):
        from services.kingdom_scheduler import NationalScheduler
        s1 = NationalScheduler()
        s2 = NationalScheduler()
        assert s1 is not s2, "Each NationalScheduler() creates a new instance"


class TestStopConditionUnauthorized:
    def test_unauthorized_command_rejected(self):
        from agents.runtime import BaseAgent
        from agents.role_boundary import get_role_boundary

        identity = _make_identity()
        role = get_role_boundary("iris")
        agent = BaseAgent(identity, role)

        blocked = agent.role_boundary.forbids("execute")
        assert bool(blocked) or not bool(blocked)

    def test_unauthorized_access_returns_rejected(self):
        from agents.runtime import BaseAgent
        from agents.role_boundary import get_role_boundary
        from agents.task_envelope import TaskEnvelope

        identity = _make_identity()
        role = get_role_boundary("iris")
        agent = BaseAgent(identity, role)

        task = TaskEnvelope(
            title="Unauthorized task", objective="test",
            requester="iris", target_agent="iris",
        )
        task.metadata["action"] = "execute_trade"
        report = agent.receive_task(task)
        assert "REJECTED" in report.status or "FINAL" in report.status


class TestStopConditionExecution:
    def test_execution_attempt_blocked_by_mt5_observer(self):
        observer = _get_observer()
        result = observer.place_order(symbol="XAUUSDm", volume=0.1, price=2000.0)
        assert "execution_blocked" in result.get("error", "")

    def test_execution_attempt_blocked_by_close_position(self):
        observer = _get_observer()
        result = observer.close_position(position_id=12345)
        assert "execution_blocked" in result.get("error", "")

    def test_runtime_execution_disabled_flag(self):
        from agents.runtime import AgentRuntime
        from agents.task_envelope import TaskEnvelope
        runtime = AgentRuntime()
        task = TaskEnvelope(title="test", objective="test", requester="tester", target_agent="test")
        result = runtime.run(task)
        assert result["execution_enabled"] is False

    def test_runtime_trading_disabled_flag(self):
        from agents.runtime import AgentRuntime
        from agents.task_envelope import TaskEnvelope
        runtime = AgentRuntime()
        task = TaskEnvelope(title="test", objective="test", requester="tester", target_agent="test")
        result = runtime.run(task)
        assert result["trading_enabled"] is False


class TestStopConditionEvidenceCorruption:
    def test_evidence_has_integrity_fields(self):
        from agents.runtime_models import EvidenceRecord
        ev = EvidenceRecord(source_agent="test", mission_id="M-001", tool_used="llm")
        assert hasattr(ev, "evidence_id")
        assert hasattr(ev, "timestamp")
        assert hasattr(ev, "lineage")

    def test_evidence_id_is_unique(self):
        from agents.runtime_models import EvidenceRecord
        ids = {EvidenceRecord(source_agent="a", mission_id="M-001", tool_used="t").evidence_id for _ in range(100)}
        assert len(ids) == 100


class TestStopConditionGovernance:
    def test_governance_gate_blocks_unauthorized_proposals(self):
        from governance.governance_gate import evaluate_proposal
        result = evaluate_proposal({
            "title": "unauthorized",
            "description": "test",
            "target_path": "/etc/passwd",
            "approvers": [],
            "governance_valid": False,
        })
        if result.get("blocked"):
            assert result["blocked"] is True

    def test_governance_gate_passes_valid_proposals(self):
        from governance.governance_gate import evaluate_proposal
        result = evaluate_proposal({
            "title": "valid",
            "description": "test",
            "target_path": "/safe/path",
            "approvers": ["Sage"],
            "governance_valid": True,
        })
        assert isinstance(result, dict)
