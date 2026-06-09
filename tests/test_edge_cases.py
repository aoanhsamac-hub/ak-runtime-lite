"""Edge case and error handling tests across all runtime components."""

import os
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock


class TestEdgeCases(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_scheduler_registry_corrupt_json(self):
        reg_path = os.path.join(self.tmpdir, "corrupt.json")
        with open(reg_path, "w") as f:
            f.write("{corrupt json}")
        from services.scheduler_registry import SchedulerRegistry
        from services.kingdom_scheduler import RuntimeScheduler
        reg = SchedulerRegistry(path=reg_path)
        scheduler = RuntimeScheduler()
        with self.assertRaises(json.JSONDecodeError):
            reg.load(scheduler)

    def test_backup_nonexistent_target(self):
        from services.backup_manager import BackupManager
        bm = BackupManager(backup_root=os.path.join(self.tmpdir, "backups"))
        result = bm.backup("nonexistent")
        self.assertEqual(result["status"], "ERROR")

    def test_backup_restore_nonexistent(self):
        from services.backup_manager import BackupManager
        bm = BackupManager(backup_root=os.path.join(self.tmpdir, "backups"))
        bm.register_target("test", os.path.join(self.tmpdir, "dummy.json"))
        result = bm.restore("test", "no_such_backup")
        self.assertEqual(result["status"], "ERROR")

    def test_secret_manager_no_password(self):
        with patch.dict(os.environ, {}, clear=True):
            from services.secret_manager import SecretManager
            sm = SecretManager()
            self.assertFalse(sm.is_configured())

    def test_stop_condition_empty_history(self):
        from services.stop_condition_manager import StopConditionManager
        from services.runtime_guard import RuntimeGuard
        guard = RuntimeGuard()
        manager = StopConditionManager(guard)
        history = manager.get_history()
        self.assertEqual(len(history), 0)

    def test_runtime_guard_no_scheduler(self):
        from services.runtime_guard import RuntimeGuard
        guard = RuntimeGuard(scheduler=None)
        result = guard.check_scheduler()
        self.assertTrue(result["healthy"])
        self.assertEqual(result["detail"], "No scheduler")

    def test_runtime_guard_no_mt5(self):
        from services.runtime_guard import RuntimeGuard
        guard = RuntimeGuard()
        result = guard.check_mt5()
        self.assertIn("healthy", result)

    def test_guard_trigger_stop_pauses(self):
        from services.runtime_guard import RuntimeGuard
        guard = RuntimeGuard()
        result = guard.trigger_stop("test_stop")
        self.assertEqual(result["action"], "STOP")
        self.assertIn("timestamp", result)
        self.assertTrue(guard.is_paused)

    def test_guard_trigger_stop_calls_callbacks(self):
        from services.runtime_guard import RuntimeGuard
        guard = RuntimeGuard()
        cb = Mock()
        guard.register_stop_callback(cb)
        guard.trigger_stop("test")
        cb.assert_called_once()

    def test_stop_manager_get_definitions(self):
        from services.stop_condition_manager import StopConditionManager
        from services.runtime_guard import RuntimeGuard
        guard = RuntimeGuard()
        manager = StopConditionManager(guard)
        defs = manager.get_stop_condition_definitions()
        self.assertIn("ram_low", defs)
        self.assertIn("mt5_disconnect", defs)
        self.assertIn("scheduler_failure", defs)
        self.assertIn("unauthorized_command", defs)
        self.assertIn("execution_attempt", defs)
        self.assertIn("evidence_corruption", defs)
        self.assertIn("duplicate_scheduler", defs)
        self.assertIn("governance_violation", defs)
        self.assertEqual(len(defs), 8)

    def test_manager_escalation_handlers(self):
        from services.stop_condition_manager import StopConditionManager
        from services.runtime_guard import RuntimeGuard
        guard = RuntimeGuard()
        manager = StopConditionManager(guard)
        handler = Mock()
        manager.register_escalation(handler)
        h = manager.health()
        self.assertEqual(h["escalation_handlers"], 1)

    def test_backup_rotation_caps_at_max(self):
        from services.backup_manager import BackupManager
        bm = BackupManager(backup_root=os.path.join(self.tmpdir, "backups"))
        source = os.path.join(self.tmpdir, "rotate_source.json")
        with open(source, "w") as f:
            json.dump({"test": True}, f)
        bm.register_target("rotate_cap", source)
        with patch("services.backup_manager.MAX_BACKUPS", 5):
            for i in range(10):
                bm.backup("rotate_cap")
        backups = bm.list_backups("rotate_cap")
        self.assertLessEqual(len(backups["rotate_cap"]), 5)

    def test_secret_delete_nonexistent(self):
        import services.secret_manager as sm_module
        self._orig_secrets_dir = sm_module.SECRETS_DIR
        self._orig_encrypted_file = sm_module.ENCRYPTED_FILE
        self._orig_salt_file = sm_module.SALT_FILE
        sm_module.SECRETS_DIR = Path(self.tmpdir)
        sm_module.ENCRYPTED_FILE = Path(self.tmpdir) / "secrets.enc"
        sm_module.SALT_FILE = Path(self.tmpdir) / ".salt"
        from services.secret_manager import SecretManager
        sm = SecretManager(master_password="pw")
        sm.unlock()
        result = sm.delete("NONEXISTENT")
        sm_module.SECRETS_DIR = self._orig_secrets_dir
        sm_module.ENCRYPTED_FILE = self._orig_encrypted_file
        sm_module.SALT_FILE = self._orig_salt_file
        self.assertEqual(result["status"], "OK")

    def test_vault_creates_on_first_set(self):
        import services.secret_manager as sm_module
        self._orig_secrets_dir = sm_module.SECRETS_DIR
        self._orig_encrypted_file = sm_module.ENCRYPTED_FILE
        self._orig_salt_file = sm_module.SALT_FILE
        sm_module.SECRETS_DIR = Path(self.tmpdir)
        sm_module.ENCRYPTED_FILE = Path(self.tmpdir) / "secrets.enc"
        sm_module.SALT_FILE = Path(self.tmpdir) / ".salt"
        from services.secret_manager import SecretManager
        sm = SecretManager(master_password="pw")
        sm.unlock()
        self.assertFalse(sm_module.ENCRYPTED_FILE.exists())
        sm.set("A", "1")
        sm.persist()
        self.assertTrue(sm_module.ENCRYPTED_FILE.exists())
        sm_module.SECRETS_DIR = self._orig_secrets_dir
        sm_module.ENCRYPTED_FILE = self._orig_encrypted_file
        sm_module.SALT_FILE = self._orig_salt_file

    def test_secret_unlock_locked(self):
        import services.secret_manager as sm_module
        self._orig_secrets_dir = sm_module.SECRETS_DIR
        self._orig_encrypted_file = sm_module.ENCRYPTED_FILE
        self._orig_salt_file = sm_module.SALT_FILE
        sm_module.SECRETS_DIR = Path(self.tmpdir)
        sm_module.ENCRYPTED_FILE = Path(self.tmpdir) / "secrets.enc"
        sm_module.SALT_FILE = Path(self.tmpdir) / ".salt"
        from services.secret_manager import SecretManager
        sm = SecretManager(master_password="pw")
        result = sm.unlock()
        sm_module.SECRETS_DIR = self._orig_secrets_dir
        sm_module.ENCRYPTED_FILE = self._orig_encrypted_file
        sm_module.SALT_FILE = self._orig_salt_file
        self.assertEqual(result["status"], "OK")

    def test_runtime_guard_check_execution(self):
        from services.runtime_guard import RuntimeGuard
        guard = RuntimeGuard()
        result = guard.check_execution_attempts()
        self.assertIn("healthy", result)

    def test_runtime_guard_health(self):
        from services.runtime_guard import RuntimeGuard
        guard = RuntimeGuard()
        h = guard.health()
        self.assertIn("all_healthy", h)
        self.assertIn("paused", h)
        self.assertIn("violations", h)


if __name__ == "__main__":
    unittest.main()
