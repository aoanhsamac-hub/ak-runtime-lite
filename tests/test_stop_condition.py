"""Tests for the Runtime Guard and Stop Condition Manager."""

import os
import unittest
from unittest.mock import Mock, patch, MagicMock, PropertyMock
from datetime import datetime, timezone


class TestRuntimeGuard(unittest.TestCase):
    def setUp(self):
        self.guard_patch = patch("services.runtime_guard.RuntimeGuard")
        self.mock_guard = self.guard_patch.start()
        self.guard = self.mock_guard()

    def tearDown(self):
        self.guard_patch.stop()

    def test_check_ram_healthy(self):
        self.guard.check_ram.return_value = {"condition": "ram_low", "healthy": True, "free_mb": 500.0}
        result = self.guard.check_ram()
        self.assertTrue(result["healthy"])
        self.assertGreater(result["free_mb"], 200)

    def test_check_ram_low(self):
        self.guard.check_ram.return_value = {"condition": "ram_low", "healthy": False, "free_mb": 50.0}
        result = self.guard.check_ram()
        self.assertFalse(result["healthy"])
        self.assertLess(result["free_mb"], 200)

    def test_check_mt5_disconnected(self):
        self.guard.check_mt5.return_value = {"condition": "mt5_disconnect", "healthy": False, "detail": "no_observer"}
        result = self.guard.check_mt5()
        self.assertFalse(result["healthy"])

    def test_check_mt5_healthy(self):
        self.guard.check_mt5.return_value = {"condition": "mt5_disconnect", "healthy": True, "detail": "connected"}
        result = self.guard.check_mt5()
        self.assertTrue(result["healthy"])

    def test_check_scheduler_healthy(self):
        self.guard.check_scheduler.return_value = {"condition": "scheduler_failure", "healthy": True, "failed_jobs": 0}
        result = self.guard.check_scheduler()
        self.assertTrue(result["healthy"])

    def test_check_scheduler_failed(self):
        self.guard.check_scheduler.return_value = {"condition": "scheduler_failure", "healthy": False, "failed_jobs": 3}
        result = self.guard.check_scheduler()
        self.assertFalse(result["healthy"])

    def test_execution_blocked(self):
        self.guard.check_execution_attempts.return_value = {"condition": "execution_attempt", "healthy": True, "blocked": True}
        result = self.guard.check_execution_attempts()
        self.assertTrue(result["healthy"])

    def test_execution_not_blocked(self):
        self.guard.check_execution_attempts.return_value = {"condition": "execution_attempt", "healthy": False, "blocked": False}
        result = self.guard.check_execution_attempts()
        self.assertFalse(result["healthy"])

    def test_duplicate_scheduler(self):
        self.guard.check_duplicate_scheduler.return_value = {"condition": "duplicate_scheduler", "healthy": True}
        result = self.guard.check_duplicate_scheduler()
        self.assertTrue(result["healthy"])

    def test_governance_violation(self):
        self.guard.check_governance.return_value = {"condition": "governance_violation", "healthy": False}
        result = self.guard.check_governance()
        self.assertFalse(result["healthy"])

    def test_all_healthy_true(self):
        self.guard.all_healthy.return_value = True
        self.assertTrue(self.guard.all_healthy())

    def test_all_healthy_false(self):
        self.guard.all_healthy.return_value = False
        self.assertFalse(self.guard.all_healthy())

    def test_trigger_stop(self):
        self.guard.trigger_stop.return_value = {"action": "STOP", "reason": "ram_low"}
        result = self.guard.trigger_stop("ram_low")
        self.assertEqual(result["action"], "STOP")
        self.assertEqual(result["reason"], "ram_low")

    def test_is_paused(self):
        type(self.guard).is_paused = PropertyMock(return_value=False)
        self.assertFalse(self.guard.is_paused)

    def test_health_report(self):
        self.guard.health.return_value = {"all_healthy": True, "paused": False, "violations": 0}
        h = self.guard.health()
        self.assertTrue(h["all_healthy"])

    def test_register_callbacks(self):
        cb = Mock()
        self.guard.register_stop_callback(cb)
        self.guard.register_stop_callback.assert_called_with(cb)

    def test_violations_tracking(self):
        self.guard.get_violations.return_value = [{"condition": "ram_low"}]
        violations = self.guard.get_violations()
        self.assertEqual(len(violations), 1)


class TestStopConditionManager(unittest.TestCase):
    def setUp(self):
        self.manager_patch = patch("services.stop_condition_manager.StopConditionManager")
        self.mock_manager = self.manager_patch.start()
        self.manager = self.mock_manager()

    def tearDown(self):
        self.manager_patch.stop()

    def test_evaluate_all_healthy(self):
        self.manager.evaluate.return_value = {"all_healthy": True, "triggered_conditions": []}
        result = self.manager.evaluate()
        self.assertTrue(result["all_healthy"])

    def test_evaluate_with_triggers(self):
        self.manager.evaluate.return_value = {"all_healthy": False, "triggered_conditions": ["ram_low"]}
        result = self.manager.evaluate()
        self.assertFalse(result["all_healthy"])
        self.assertIn("ram_low", result["triggered_conditions"])

    def test_should_stop_true(self):
        self.manager.should_stop.return_value = True
        self.assertTrue(self.manager.should_stop())

    def test_should_stop_false(self):
        self.manager.should_stop.return_value = False
        self.assertFalse(self.manager.should_stop())

    def test_stop_if_needed(self):
        self.manager.stop_if_needed.return_value = {"action": "STOP"}
        result = self.manager.stop_if_needed()
        self.assertIsNotNone(result)

    def test_stop_if_not_needed(self):
        self.manager.should_stop.return_value = False
        self.manager.evaluate.return_value = {"all_healthy": True, "triggered_conditions": []}
        self.manager.stop_if_needed.return_value = None
        result = self.manager.stop_if_needed()
        self.assertIsNone(result)

    def test_get_history(self):
        self.manager.get_history.return_value = [{"all_healthy": True}]
        history = self.manager.get_history()
        self.assertEqual(len(history), 1)

    def test_get_definitions(self):
        self.manager.get_stop_condition_definitions.return_value = {"ram_low": "RAM < 200 MB"}
        defs = self.manager.get_stop_condition_definitions()
        self.assertIn("ram_low", defs)

    def test_register_escalation(self):
        handler = Mock()
        self.manager.register_escalation(handler)
        self.manager.register_escalation.assert_called_with(handler)


if __name__ == "__main__":
    unittest.main()
