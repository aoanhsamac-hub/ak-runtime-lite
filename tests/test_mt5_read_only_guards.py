"""Tests for MT5 read-only guard enforcement."""

import pytest


class TestMT5ReadOnlyGuards:
    def _get_observer(self):
        try:
            from connectors.mt5.mt5_demo_observer import MT5DemoObserver
            return MT5DemoObserver()
        except ImportError:
            pytest.skip("MetaTrader5 not available")

    def _get_observer_module(self):
        try:
            import connectors.mt5.mt5_demo_observer as mod
            return mod
        except ImportError:
            pytest.skip("MetaTrader5 not available")

    def test_place_order_blocked(self):
        observer = self._get_observer()
        result = observer.place_order()
        assert "execution_blocked" in result.get("error", "")

    def test_close_position_blocked(self):
        observer = self._get_observer()
        result = observer.close_position()
        assert "execution_blocked" in result.get("error", "")

    def test_observer_docstring_readonly(self):
        mod = self._get_observer_module()
        assert "READ-ONLY" in mod.__doc__.upper()

    def test_observer_allows_get_ohlcv(self):
        observer = self._get_observer()
        result = observer.get_ohlcv("XAUUSDm", 5)
        assert "ohlcv" in result

    def test_observer_allows_get_tick(self):
        observer = self._get_observer()
        result = observer.get_tick("XAUUSDm")
        assert "bid" in result and "ask" in result

    def test_observer_allows_get_spread(self):
        observer = self._get_observer()
        spread = observer.get_spread("XAUUSDm")
        assert isinstance(spread, float)

    def test_observer_allows_health_check(self):
        observer = self._get_observer()
        result = observer.health_check()
        assert "status" in result

    def test_order_send_not_imported_in_observer(self):
        mod = self._get_observer_module()
        with open(mod.__file__) as f:
            source = f.read()
        assert "order_send" not in source, "order_send must not appear in observer source"

    def test_no_mt5_trade_imports(self):
        mod = self._get_observer_module()
        with open(mod.__file__) as f:
            source = f.read()
        forbidden = ["order_send", "order_modify", "order_close", "PositionOpen", "TradeSend"]
        for item in forbidden:
            assert item not in source, f"Forbidden MT5 trade function found: {item}"

    def test_build_validation_blocks_order_send(self):
        from services.build_validation_runtime import BuildValidationRuntime
        validator = BuildValidationRuntime()
        result = validator.validate_code("order_send(symbol, volume, price, ...)", "test-cap")
        assert not result["is_valid"]
        assert any("order_send" in v for v in result["violations"])

    def test_build_validation_blocks_forbidden_patterns(self):
        from services.build_validation_runtime import BuildValidationRuntime
        validator = BuildValidationRuntime()
        patterns = ["import os.system", "subprocess.call", "eval(", "exec("]
        for pat in patterns:
            result = validator.validate_code(pat, f"test-pattern-{patterns.index(pat)}")
            assert not result["is_valid"]

    def test_build_validation_passes_clean_code(self):
        from services.build_validation_runtime import BuildValidationRuntime
        validator = BuildValidationRuntime()
        result = validator.validate_code("x = 1\ny = x + 2\nprint(y)", "test-clean")
        assert result["is_valid"]

    def test_mt5_health_monitor_checks_connection(self):
        observer = self._get_observer()
        from connectors.mt5.health_monitor import MT5HealthMonitor
        monitor = MT5HealthMonitor(observer)
        result = monitor.check_connection()
        assert "status" in result

    def test_mt5_health_monitor_no_observer(self):
        from connectors.mt5.health_monitor import MT5HealthMonitor
        monitor = MT5HealthMonitor(None)
        result = monitor.check_connection()
        assert result["status"] == "no_observer"

    def test_runtime_execution_disabled_by_default(self):
        from agents.runtime import AgentRuntime
        from agents.task_envelope import TaskEnvelope
        runtime = AgentRuntime()
        task = TaskEnvelope(title="test", objective="test", requester="tester", target_agent="test")
        result = runtime.run(task)
        assert result["execution_enabled"] is False
        assert result["trading_enabled"] is False
        assert result["mt5_enabled"] is False

    def test_forbidden_actions_in_reviewer_runtime(self):
        from services.reviewer_runtime import ReviewerRuntime
        forbidden = ReviewerRuntime.FORBIDDEN_ACTIONS
        assert "self_approve" in forbidden
        assert "auto_promote" in forbidden
        assert "bypass_review" in forbidden
        assert "skip_validation" in forbidden
