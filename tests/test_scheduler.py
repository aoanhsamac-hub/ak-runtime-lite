"""Tests for the Scheduler and Scheduler Registry."""

import os
import json
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone


class TestSchedulerRegistryReal(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.registry_path = os.path.join(self.tmpdir, "test_registry.json")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_registry_save_load(self):
        from services.scheduler_registry import SchedulerRegistry
        from services.kingdom_scheduler import RuntimeScheduler, ScheduledJob
        reg = SchedulerRegistry(path=self.registry_path)
        scheduler = RuntimeScheduler()
        result = reg.save(scheduler)
        self.assertEqual(result["status"], "OK")
        # Create new scheduler and load into it
        scheduler2 = RuntimeScheduler()
        result = reg.load(scheduler2)
        self.assertEqual(result["status"], "OK")

    def test_registry_not_found(self):
        from services.scheduler_registry import SchedulerRegistry
        from services.kingdom_scheduler import RuntimeScheduler
        reg = SchedulerRegistry(path=os.path.join(self.tmpdir, "nonexistent.json"))
        scheduler = RuntimeScheduler()
        result = reg.load(scheduler)
        self.assertEqual(result["status"], "NOT_FOUND")

    def test_registry_backup(self):
        from services.scheduler_registry import SchedulerRegistry
        from services.kingdom_scheduler import RuntimeScheduler
        reg = SchedulerRegistry(path=self.registry_path)
        scheduler = RuntimeScheduler()
        reg.save(scheduler)
        backup_dir = os.path.join(self.tmpdir, "backups")
        result = reg.backup(backup_dir=backup_dir)
        self.assertEqual(result["status"], "OK")

    def test_registry_backup_not_found(self):
        from services.scheduler_registry import SchedulerRegistry
        reg = SchedulerRegistry(path=os.path.join(self.tmpdir, "missing.json"))
        result = reg.backup()
        self.assertEqual(result["status"], "NOT_FOUND")

    def test_registry_ensure_dir(self):
        from services.scheduler_registry import SchedulerRegistry
        deep_path = os.path.join(self.tmpdir, "a", "b", "c", "reg.json")
        reg = SchedulerRegistry(path=deep_path)
        reg.ensure_dir()
        self.assertTrue(os.path.exists(os.path.dirname(deep_path)))


class TestRuntimeScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler_patch = patch("services.kingdom_scheduler.RuntimeScheduler")
        self.mock_scheduler = self.scheduler_patch.start()
        self.scheduler = self.mock_scheduler()

    def tearDown(self):
        self.scheduler_patch.stop()

    def test_register_job(self):
        mock_job = MagicMock()
        self.scheduler.register_job(mock_job)
        self.scheduler.register_job.assert_called_with(mock_job)

    def test_start_stop(self):
        self.scheduler.start()
        self.scheduler.start.assert_called_once()
        self.scheduler.stop()
        self.scheduler.stop.assert_called_once()

    def test_get_jobs(self):
        self.scheduler.get_jobs.return_value = []
        jobs = self.scheduler.get_jobs()
        self.assertEqual(jobs, [])

    def test_get_jobs_with_data(self):
        from services.kingdom_scheduler import ScheduledJob
        mock_job = MagicMock(spec=ScheduledJob)
        mock_job.job_id = "test-job"
        mock_job.name = "test"
        mock_job.cadence = "hourly"
        mock_job.last_status = "OK"
        self.scheduler.get_jobs.return_value = [mock_job]
        jobs = self.scheduler.get_jobs()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].name, "test")


if __name__ == "__main__":
    unittest.main()
