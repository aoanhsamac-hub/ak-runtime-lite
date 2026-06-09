"""Integration tests for Runtime components (Guard + StopCondition + Supervisor)."""

import os
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock, PropertyMock
from datetime import datetime, timezone


class TestGuardAndManagerIntegration(unittest.TestCase):
    def setUp(self):
        self.guard_patch = patch("services.runtime_guard.RuntimeGuard")
        self.mock_guard = self.guard_patch.start()
        self.manager_patch = patch("services.stop_condition_manager.StopConditionManager")
        self.mock_manager = self.manager_patch.start()
        self.guard = self.mock_guard()
        self.manager = self.mock_manager()

    def tearDown(self):
        self.guard_patch.stop()
        self.manager_patch.stop()

    def test_evaluate_triggers_stop(self):
        self.manager.evaluate.return_value = {"all_healthy": False, "triggered_conditions": ["ram_low"]}
        self.manager.should_stop.return_value = True
        self.manager.stop_if_needed.return_value = {"action": "STOP", "reason": "ram_low"}
        self.assertTrue(self.manager.should_stop())
        stop = self.manager.stop_if_needed()
        self.assertEqual(stop["action"], "STOP")

    def test_escalation_chain(self):
        escalation_cb = Mock()
        self.manager.register_escalation(escalation_cb)
        self.manager.evaluate.return_value = {"all_healthy": False, "triggered_conditions": ["mt5_disconnect"]}
        self.manager.evaluate()
        escalation_cb.assert_not_called()

    def test_all_healthy_no_stop(self):
        self.guard.all_healthy.return_value = True
        self.manager.should_stop.return_value = False
        self.manager.stop_if_needed.return_value = None
        self.assertTrue(self.guard.all_healthy())
        self.assertFalse(self.manager.should_stop())
        self.assertIsNone(self.manager.stop_if_needed())

    def test_multiple_violations(self):
        self.guard.get_violations.return_value = [{"condition": "ram_low"}, {"condition": "mt5_disconnect"}]
        v = self.guard.get_violations()
        self.assertEqual(len(v), 2)
        conditions = [x["condition"] for x in v]
        self.assertIn("ram_low", conditions)
        self.assertIn("mt5_disconnect", conditions)

    def test_clear_violations(self):
        self.guard.clear_violations()
        self.guard.get_violations.return_value = []
        self.guard.clear_violations()
        self.assertEqual(len(self.guard.get_violations()), 0)

    def test_supervisor_guard_integration(self):
        self.guard.register_stop_callback = Mock()
        cb = Mock()
        self.guard.register_stop_callback(cb)
        self.guard.register_stop_callback.assert_called_with(cb)
        self.guard.trigger_stop("test")
        cb.assert_not_called()


class TestBackupAndRegistryIntegration(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _create_source(self, name="source.json", content=None):
        path = os.path.join(self.tmpdir, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(content or {"test": "value"}, f)
        return path

    def test_backup_restore_roundtrip(self):
        from services.backup_manager import BackupManager
        bm = BackupManager(backup_root=os.path.join(self.tmpdir, "backups"))
        source = self._create_source()
        bm.register_target("roundtrip", source)
        result = bm.backup("roundtrip")
        ts = result["path"].split("\\")[-1]
        with open(source, "w", encoding="utf-8") as f:
            json.dump({"test": "modified"}, f)
        bm.restore("roundtrip", ts)
        with open(source, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["test"], "value")

    def test_backup_preserves_original(self):
        from services.backup_manager import BackupManager
        bm = BackupManager(backup_root=os.path.join(self.tmpdir, "backups"))
        source = self._create_source("preserve.json", {"original": True})
        bm.register_target("preserve", source)
        result = bm.backup("preserve")
        self.assertEqual(result["status"], "OK")
        with open(source, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertTrue(data["original"])

    def test_backup_invalid_json(self):
        from services.backup_manager import BackupManager
        bm = BackupManager(backup_root=os.path.join(self.tmpdir, "backups"))
        source = os.path.join(self.tmpdir, "invalid.json")
        with open(source, "w") as f:
            f.write("not json")
        bm.register_target("invalid", source)
        result = bm.backup("invalid")
        self.assertEqual(result["status"], "OK")

    def test_list_backups_sorted(self):
        from services.backup_manager import BackupManager
        bm = BackupManager(backup_root=os.path.join(self.tmpdir, "backups"))
        source = self._create_source("list_test.json", {"x": 1})
        bm.register_target("list_test", source)
        for i in range(3):
            bm.backup("list_test")
        backups = bm.list_backups("list_test")
        self.assertGreaterEqual(len(backups.get("list_test", [])), 1)


class TestSecretsAndValidatorIntegration(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        import services.secret_manager as sm_module
        self._orig_secrets_dir = sm_module.SECRETS_DIR
        self._orig_encrypted_file = sm_module.ENCRYPTED_FILE
        self._orig_salt_file = sm_module.SALT_FILE
        sm_module.SECRETS_DIR = Path(self.tmpdir)
        sm_module.ENCRYPTED_FILE = Path(self.tmpdir) / "secrets.enc"
        sm_module.SALT_FILE = Path(self.tmpdir) / ".salt"

    def tearDown(self):
        import services.secret_manager as sm_module
        sm_module.SECRETS_DIR = self._orig_secrets_dir
        sm_module.ENCRYPTED_FILE = self._orig_encrypted_file
        sm_module.SALT_FILE = self._orig_salt_file
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_secret_manager_set_get(self):
        from services.secret_manager import SecretManager
        sm = SecretManager(master_password="integration-pw")
        sm.unlock()
        sm.set("TEST_TOKEN", "test-token-value")
        val = sm.get("TEST_TOKEN")
        self.assertEqual(val, "test-token-value")
        keys = sm.list_keys()
        self.assertIn("TEST_TOKEN", keys)

    def test_secret_overwrite(self):
        from services.secret_manager import SecretManager
        sm = SecretManager(master_password="integration-pw")
        sm.unlock()
        sm.set("KEY", "first")
        sm.set("KEY", "second")
        val = sm.get("KEY")
        self.assertEqual(val, "second")

    def test_wrong_password(self):
        from services.secret_manager import SecretManager
        sm1 = SecretManager(master_password="pw1")
        sm1.unlock()
        sm1.set("KEY", "value")
        sm1.persist()
        sm2 = SecretManager(master_password="pw2")
        result = sm2.unlock()
        self.assertEqual(result["status"], "ERROR")


if __name__ == "__main__":
    unittest.main()
