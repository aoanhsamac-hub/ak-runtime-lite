from __future__ import annotations

import pytest

from services.kingdom_scheduler import (
    CADENCE_HOURLY,
    CADENCE_DAILY,
    CADENCE_WEEKLY,
    CADENCES,
    RuntimeScheduler,
    ScheduledJob,
    JobPriority,
    JobStatus,
)


@pytest.fixture
def scheduler():
    return RuntimeScheduler()


class TestCadences:
    def test_cadences_defined(self):
        assert CADENCE_HOURLY == "hourly"
        assert CADENCE_DAILY == "daily"
        assert CADENCE_WEEKLY == "weekly"
        assert len(CADENCES) == 3


class TestScheduledJob:
    def test_create_job(self):
        job = ScheduledJob(
            job_id="test-1",
            name="Test Job",
            cadence=CADENCE_HOURLY,
            target="module.Class.method",
        )
        assert job.job_id == "test-1"
        assert job.enabled
        assert job.last_run == ""

    def test_job_priority_default(self):
        job = ScheduledJob(job_id="t", name="T", cadence=CADENCE_DAILY, target="t")
        assert job.priority == JobPriority.MEDIUM


class TestRuntimeScheduler:
    def test_default_jobs_created(self, scheduler):
        jobs = scheduler.get_jobs()
        assert len(jobs) > 0

    def test_hourly_jobs(self, scheduler):
        hourly = scheduler.get_jobs(CADENCE_HOURLY)
        assert len(hourly) == 4
        names = {j.name for j in hourly}
        assert "Iris Forecast" in names
        assert "Reality Check" in names
        assert "Lesson Update" in names
        assert "Health Check" in names

    def test_daily_jobs(self, scheduler):
        daily = scheduler.get_jobs(CADENCE_DAILY)
        assert len(daily) == 3
        names = {j.name for j in daily}
        assert "KACE Scorecard" in names
        assert "Evidence Summary" in names
        assert "Runtime Status" in names

    def test_weekly_jobs(self, scheduler):
        weekly = scheduler.get_jobs(CADENCE_WEEKLY)
        assert len(weekly) == 3
        names = {j.name for j in weekly}
        assert "Kingdom Review" in names
        assert "Agent Review" in names
        assert "Audit Readiness" in names

    def test_register_custom_job(self, scheduler):
        job = ScheduledJob(
            job_id="custom-1",
            name="Custom Job",
            cadence=CADENCE_HOURLY,
            target="custom",
        )
        scheduler.register_job(job)
        assert scheduler.get_jobs(CADENCE_HOURLY)[-1].job_id == "custom-1"

    def test_run_hourly_with_no_handler(self, scheduler):
        results = scheduler.run_hourly()
        assert len(results) == 4
        for r in results:
            assert r["status"] == "skipped"
            assert r["reason"] == "no_handler"

    def test_run_hourly_with_handler(self, scheduler):
        def fake_handler(**kwargs):
            return {"ok": True}

        for job in scheduler.get_jobs(CADENCE_HOURLY):
            scheduler.register_handler(job.job_id, fake_handler)

        results = scheduler.run_hourly()
        assert all(r["status"] == "success" for r in results)

    def test_run_hourly_handler_error(self, scheduler):
        def broken_handler(**kwargs):
            raise RuntimeError("oops")

        for job in scheduler.get_jobs(CADENCE_HOURLY):
            scheduler.register_handler(job.job_id, broken_handler)

        results = scheduler.run_hourly()
        assert all(r["status"] == "error" for r in results)

    def test_run_daily(self, scheduler):
        results = scheduler.run_daily()
        assert len(results) == 3

    def test_run_weekly(self, scheduler):
        results = scheduler.run_weekly()
        assert len(results) == 3

    def test_summary(self, scheduler):
        s = scheduler.summary()
        assert s["hourly"] == 4
        assert s["daily"] == 3
        assert s["weekly"] == 3
        assert s["total_jobs"] == 10
        assert s["enabled"] == 10

    def test_get_jobs_by_invalid_cadence(self, scheduler):
        jobs = scheduler.get_jobs("invalid")
        assert jobs == []

    def test_start_stop(self, scheduler):
        result = scheduler.start()
        assert result["running"] is True
        result = scheduler.stop()
        assert result["running"] is False

    def test_register_handler(self, scheduler):
        handler = lambda **kw: {"ok": True}
        scheduler.register_handler("hourly-forecast", handler)
        assert "hourly-forecast" in scheduler._handlers
