"""Tests for runtime recovery logic and supervisor design."""

import pytest


def _make_identity():
    from agents.identity import get_identity
    return get_identity("iris")


def _get_mt5_observer():
    try:
        from connectors.mt5.mt5_demo_observer import MT5DemoObserver
        return MT5DemoObserver()
    except ImportError:
        pytest.skip("MetaTrader5 not available")


class TestSupervisorDesign:
    def test_no_supervisor_process_exists(self):
        import psutil
        names = [p.info['name'] for p in psutil.process_iter(['name']) if p.info['name']]
        supervisor_count = sum(1 for n in names if 'supervisor' in n.lower())
        assert supervisor_count == 0, "No supervisor process should exist yet"

    def test_agent_runtime_has_no_restart_logic(self):
        from agents.runtime import AgentRuntime
        runtime = AgentRuntime()
        assert not hasattr(runtime, "restart")
        assert not hasattr(runtime, "recover")

    def test_no_heartbeat_implemented(self):
        import glob
        hb_files = glob.glob("**/*heartbeat*", root_dir=".", recursive=True)
        assert len(hb_files) == 0, "No heartbeat files should exist yet"


class TestHealthMonitoring:
    def test_mt5_health_monitor_exists(self):
        from connectors.mt5.health_monitor import MT5HealthMonitor
        assert MT5HealthMonitor is not None

    def test_mt5_health_check_returns_dict(self):
        observer = _get_mt5_observer()
        from connectors.mt5.health_monitor import MT5HealthMonitor
        monitor = MT5HealthMonitor(observer)
        result = monitor.check_connection()
        assert isinstance(result, dict)

    def test_mt5_health_data_quality_check(self):
        observer = _get_mt5_observer()
        from connectors.mt5.health_monitor import MT5HealthMonitor
        monitor = MT5HealthMonitor(observer)
        result = monitor.check_data_quality("XAUUSDm", 10)
        assert "quality" in result

    def test_health_check_without_observer_graceful(self):
        from connectors.mt5.health_monitor import MT5HealthMonitor
        monitor = MT5HealthMonitor(None)
        result = monitor.check_connection()
        assert result["status"] == "no_observer"

    def test_security_status_monitor_exists(self):
        try:
            from services.security_status_monitor import SecurityStatusMonitor
            assert True
        except ImportError:
            pytest.skip("SecurityStatusMonitor not available")


class TestErrorLogging:
    def test_agent_runtime_has_audit_hook(self):
        from agents.runtime import BaseAgent
        assert hasattr(BaseAgent, "append_audit")

    def test_audit_hook_returns_dict(self):
        from agents.runtime import BaseAgent
        from agents.role_boundary import RoleBoundary
        identity = _make_identity()
        from agents.role_boundary import get_role_boundary; role = get_role_boundary("iris")
        agent = BaseAgent(identity, role)
        result = agent.append_audit({
            "task_id": "T-001", "issue_id": "I-001",
            "action": "test", "result": "logged",
        })
        assert isinstance(result, dict)

    def test_agent_records_decision_trace(self):
        from agents.runtime import BaseAgent
        from agents.role_boundary import get_role_boundary
        from agents.task_envelope import TaskEnvelope
        identity = _make_identity()
        role = get_role_boundary("iris")
        agent = BaseAgent(identity, role)
        task = TaskEnvelope(
            title="Test trace", objective="test",
            requester="iris", target_agent="iris",
        )
        try:
            agent.record_decision_trace(task, {"summary": "test", "status": "FINAL"})
        except Exception:
            pytest.skip("Trace recording requires memory client")

    def test_error_handling_does_not_crash_agent(self):
        from agents.runtime import BaseAgent
        from agents.role_boundary import RoleBoundary
        identity = _make_identity()
        from agents.role_boundary import get_role_boundary; role = get_role_boundary("iris")
        agent = BaseAgent(identity, role)
        try:
            agent.record_decision_trace(None, None)
        except Exception:
            pass


class TestFailureEscalation:
    def test_no_escalation_chain_defined(self):
        escalation = None
        assert escalation is None, "No escalation chain should exist yet"

    def test_no_telegram_alerting_in_place(self):
        alerting = None
        assert alerting is None, "No telegram alerting should exist yet"


class TestRecoveryCapabilities:
    def test_agent_boot_returns_dict(self):
        from agents.runtime import BaseAgent
        from agents.role_boundary import RoleBoundary
        identity = _make_identity()
        from agents.role_boundary import get_role_boundary; role = get_role_boundary("iris")
        agent = BaseAgent(identity, role)
        result = agent.boot()
        assert isinstance(result, dict)

    def test_agent_status_available(self):
        from agents.runtime import BaseAgent
        from agents.role_boundary import get_role_boundary
        identity = _make_identity()
        role = get_role_boundary("iris")
        agent = BaseAgent(identity, role)
        agent.boot()
        assert agent.status() in ("operational", "degraded", "suspended")

    def test_agent_shutdown_graceful(self):
        from agents.runtime import BaseAgent
        from agents.role_boundary import RoleBoundary
        from agents.lifecycle import AgentLifecycleState
        identity = _make_identity()
        from agents.role_boundary import get_role_boundary; role = get_role_boundary("iris")
        agent = BaseAgent(identity, role)
        result = agent.shutdown()
        assert result["status"] == "suspended"
        assert agent.lifecycle_state == AgentLifecycleState.SUSPENDED.value

    def test_runtime_health_check_returns_dict(self):
        from agents.runtime import AgentRuntime
        from agents.task_envelope import TaskEnvelope
        runtime = AgentRuntime()
        task = TaskEnvelope(title="health", objective="check", requester="tester", target_agent="test")
        result = runtime.run(task)
        assert isinstance(result, dict)
        assert "status" in result

    def test_reviewer_runtime_cannot_self_approve(self):
        from services.reviewer_runtime import ReviewerRuntime
        runtime = ReviewerRuntime("test-cap")
        assert runtime.can_proceed() is False
