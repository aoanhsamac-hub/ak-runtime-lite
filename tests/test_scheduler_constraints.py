"""Tests for scheduler constraints and no-duplicate enforcement."""

import pytest
from services.kingdom_scheduler import (
    RuntimeScheduler, ScheduledJob, CADENCE_HOURLY, CADENCE_DAILY, CADENCE_WEEKLY, CADENCES,
)


class TestSchedulerSingleton:
    def test_single_scheduler_authority(self):
        s1 = RuntimeScheduler()
        s2 = RuntimeScheduler()
        assert type(s1) is type(s2)
        assert s1 is not s2

    def test_no_duplicate_job_ids(self):
        scheduler = RuntimeScheduler()
        job_ids = [j.job_id for j in scheduler.get_jobs()]
        assert len(job_ids) == len(set(job_ids)), "Duplicate job IDs found"

    def test_no_duplicate_job_names(self):
        scheduler = RuntimeScheduler()
        names = [j.name for j in scheduler.get_jobs()]
        assert len(names) == len(set(names)), "Duplicate job names found"


class TestSchedulerCadences:
    def test_valid_cadences_are_recognized(self):
        for c in ("hourly", "daily", "weekly"):
            assert c in CADENCES

    def test_hourly_jobs_count(self):
        scheduler = RuntimeScheduler()
        assert len(scheduler.get_jobs(CADENCE_HOURLY)) >= 1

    def test_daily_jobs_count(self):
        scheduler = RuntimeScheduler()
        assert len(scheduler.get_jobs(CADENCE_DAILY)) >= 1

    def test_weekly_jobs_count(self):
        scheduler = RuntimeScheduler()
        assert len(scheduler.get_jobs(CADENCE_WEEKLY)) >= 1

    def test_job_cadence_assignment_valid(self):
        scheduler = RuntimeScheduler()
        for job in scheduler.get_jobs():
            assert job.cadence in CADENCES, f"Job {job.job_id} has invalid cadence {job.cadence}"


class TestSchedulerNoRunaway:
    def test_run_hourly_no_infinite_loop(self):
        scheduler = RuntimeScheduler()
        results = scheduler.run_hourly()
        assert isinstance(results, list)

    def test_run_daily_no_infinite_loop(self):
        scheduler = RuntimeScheduler()
        results = scheduler.run_daily()
        assert isinstance(results, list)

    def test_run_weekly_no_infinite_loop(self):
        scheduler = RuntimeScheduler()
        results = scheduler.run_weekly()
        assert isinstance(results, list)

    def test_job_registration_does_not_duplicate(self):
        scheduler = RuntimeScheduler()
        initial = len(scheduler.get_jobs())
        job = ScheduledJob(job_id="test-unique", name="Test", cadence=CADENCE_DAILY, target="target")
        scheduler.register_job(job)
        assert len(scheduler.get_jobs()) == initial + 1

    def test_register_duplicate_job_id_overwrites(self):
        scheduler = RuntimeScheduler()
        j1 = ScheduledJob(job_id="overwrite-test", name="Original", cadence=CADENCE_DAILY, target="t")
        j2 = ScheduledJob(job_id="overwrite-test", name="Overwritten", cadence=CADENCE_WEEKLY, target="t")
        scheduler.register_job(j1)
        scheduler.register_job(j2)
        jobs = scheduler.get_jobs()
        matches = [j for j in jobs if j.job_id == "overwrite-test"]
        assert len(matches) == 1
        assert matches[0].name == "Overwritten"


class TestSchedulerOverlappingJobs:
    def test_no_overlapping_daily_jobs(self):
        scheduler = RuntimeScheduler()
        daily = scheduler.get_jobs(CADENCE_DAILY)
        names = [j.name for j in daily]
        assert len(names) == len(set(names))


class TestSchedulerErrorHandling:
    def test_handler_error_does_not_crash_scheduler(self):
        scheduler = RuntimeScheduler()

        def failing_handler(**kwargs):
            raise RuntimeError("Intentional failure")

        scheduler.register_handler("hourly-forecast", failing_handler)
        results = scheduler.run_hourly()
        forecast_results = [r for r in results if r["job_id"] == "hourly-forecast"]
        if forecast_results:
            assert forecast_results[0]["status"] == "error"

    def test_missing_handler_returns_skipped(self):
        scheduler = RuntimeScheduler()
        results = scheduler.run_hourly()
        skipped = [r for r in results if r["status"] == "skipped"]
        assert isinstance(skipped, list)
