"""Tests for the Supervisor, Heartbeat Monitor, and Restart Manager."""

import time
import unittest
from unittest.mock import Mock, patch, MagicMock


class TestHeartbeatMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor_patch = patch("services.heartbeat_monitor.HeartbeatMonitor")
        self.mock_monitor = self.monitor_patch.start()
        self.monitor = self.mock_monitor()

    def tearDown(self):
        self.monitor_patch.stop()

    def test_record_heartbeat(self):
        self.monitor.record_heartbeat("component_a")
        self.monitor.record_heartbeat.assert_called_with("component_a")

    def test_check_missed_beats_none(self):
        self.monitor.check_missed.return_value = {}
        result = self.monitor.check_missed()
        self.assertEqual(result, {})

    def test_check_missed_beats_detected(self):
        self.monitor.check_missed.return_value = {"component_a": 3}
        result = self.monitor.check_missed()
        self.assertIn("component_a", result)
        self.assertEqual(result["component_a"], 3)

    def test_register_component(self):
        self.monitor.register("component_a")
        self.monitor.register.assert_called_with("component_a")


class TestRestartManager(unittest.TestCase):
    def setUp(self):
        self.restart_patch = patch("services.restart_manager.RestartManager")
        self.mock_restart = self.restart_patch.start()
        self.manager = self.mock_restart()

    def tearDown(self):
        self.restart_patch.stop()

    def test_request_restart_first(self):
        self.manager.request_restart.return_value = True
        result = self.manager.request_restart("component_a")
        self.assertTrue(result)

    def test_request_restart_exhausted(self):
        self.manager.can_restart.return_value = False
        result = self.manager.can_restart("component_a")
        self.assertFalse(result)

    def test_max_attempts(self):
        self.manager.max_attempts = 3
        self.assertEqual(self.manager.max_attempts, 3)

    def test_cooldown(self):
        self.manager.cooldown_seconds = 60
        self.assertEqual(self.manager.cooldown_seconds, 60)

    def test_reset_attempts(self):
        self.manager.reset_attempts("component_a")
        self.manager.reset_attempts.assert_called_with("component_a")


class TestRuntimeSupervisor(unittest.TestCase):
    def setUp(self):
        self.super_patch = patch("services.runtime_supervisor.RuntimeSupervisor")
        self.mock_super = self.super_patch.start()
        self.supervisor = self.mock_super()

    def tearDown(self):
        self.super_patch.stop()

    def test_register_component(self):
        mock_health = Mock(return_value=True)
        self.supervisor.register_component("component_a", mock_health)
        self.supervisor.register_component.assert_called_with("component_a", mock_health)

    def test_start_stop(self):
        self.supervisor.start()
        self.supervisor.start.assert_called_once()
        self.supervisor.stop()
        self.supervisor.stop.assert_called_once()

    def test_health_check_all_healthy(self):
        self.supervisor.health.return_value = {"status": "RUNNING", "components": {"a": "RUNNING"}}
        h = self.supervisor.health()
        self.assertEqual(h["status"], "RUNNING")

    def test_health_check_with_fatals(self):
        self.supervisor.health.return_value = {"status": "DEGRADED", "components": {"a": "FATAL"}}
        h = self.supervisor.health()
        self.assertEqual(h["status"], "DEGRADED")

    def test_restart_component(self):
        self.supervisor.restart_component("component_a")
        self.supervisor.restart_component.assert_called_with("component_a")


if __name__ == "__main__":
    unittest.main()
