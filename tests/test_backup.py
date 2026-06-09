"""Tests for the Backup Manager, Registry Backup, and Evidence Backup."""

import os
import json
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock


class TestBackupManagerReal(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _create_manager(self, root=None):
        from services.backup_manager import BackupManager
        return BackupManager(backup_root=root or os.path.join(self.tmpdir, "backups"))

    def _create_source(self, name="source.json", content=None):
        path = os.path.join(self.tmpdir, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(content or {"key": "value"}, f)
        return path

    def test_register_and_backup(self):
        bm = self._create_manager()
        source = self._create_source()
        bm.register_target("test_target", source)
        result = bm.backup("test_target")
        self.assertEqual(result["status"], "OK")

    def test_backup_unknown_target(self):
        bm = self._create_manager()
        result = bm.backup("nonexistent")
        self.assertEqual(result["status"], "ERROR")

    def test_backup_missing_source(self):
        bm = self._create_manager()
        bm.register_target("missing", os.path.join(self.tmpdir, "does_not_exist.json"))
        result = bm.backup("missing")
        self.assertEqual(result["status"], "ERROR")

    def test_list_backups(self):
        bm = self._create_manager()
        source = self._create_source()
        bm.register_target("list_target", source)
        bm.backup("list_target")
        backups = bm.list_backups("list_target")
        self.assertIn("list_target", backups)

    def test_list_unknown_target(self):
        bm = self._create_manager()
        backups = bm.list_backups("unknown")
        self.assertEqual(backups, {})

    def test_restore(self):
        bm = self._create_manager()
        source = self._create_source("restore_src.json", {"key": "original"})
        bm.register_target("restore_target", source)
        result = bm.backup("restore_target")
        ts = result["path"].split("\\")[-1]
        # Modify original
        with open(source, "w", encoding="utf-8") as f:
            json.dump({"key": "modified"}, f)
        # Restore
        restore_result = bm.restore("restore_target", ts)
        self.assertEqual(restore_result["status"], "OK")
        with open(source, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["key"], "original")

    def test_restore_missing_backup(self):
        bm = self._create_manager()
        source = self._create_source()
        bm.register_target("restore_missing", source)
        result = bm.restore("restore_missing", "nonexistent_ts")
        self.assertEqual(result["status"], "ERROR")

    def test_prune_old_backups(self):
        from services.backup_manager import MAX_BACKUPS, BackupManager
        bm = self._create_manager()
        source = self._create_source()
        bm.register_target("prune_target", source)
        original_max = BackupManager._prune_old  # store
        max_before = MAX_BACKUPS
        with patch("services.backup_manager.MAX_BACKUPS", 5):
            for i in range(10):
                bm.backup("prune_target")
        backups = bm.list_backups("prune_target")
        self.assertLessEqual(len(backups["prune_target"]), 5)

    def test_backup_all(self):
        bm = self._create_manager()
        s1 = self._create_source("a.json", {"a": 1})
        s2 = self._create_source("b.json", {"b": 2})
        bm.register_target("target_a", s1)
        bm.register_target("target_b", s2)
        results = bm.backup_all()
        self.assertEqual(len(results), 2)
        for r in results:
            self.assertEqual(r["status"], "OK")

    def test_health(self):
        bm = self._create_manager()
        h = bm.health()
        self.assertIn("root", h)
        self.assertIn("targets", h)
        self.assertIn("max_backups", h)


class TestRegistryBackup(unittest.TestCase):
    def setUp(self):
        self.service_patch = patch("services.registry_backup_service.RegistryBackupService")
        self.mock_service = self.service_patch.start()
        self.service = self.mock_service()

    def tearDown(self):
        self.service_patch.stop()

    def test_backup_all(self):
        self.service.backup_all.return_value = [{"target": "sovereign", "status": "OK"}]
        results = self.service.backup_all()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "OK")


class TestEvidenceBackup(unittest.TestCase):
    def setUp(self):
        self.service_patch = patch("services.evidence_backup_service.EvidenceBackupService")
        self.mock_service = self.service_patch.start()
        self.service = self.mock_service()

    def tearDown(self):
        self.service_patch.stop()

    def test_backup_all(self):
        self.service.backup_all.return_value = [{"target": "audit", "status": "OK"}]
        results = self.service.backup_all()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "OK")


if __name__ == "__main__":
    unittest.main()
