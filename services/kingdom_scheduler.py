"""Kingdom Scheduler Extended - Hourly, daily, weekly job scheduler for AK-RUNTIME-LITE."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable


CADENCE_HOURLY = "hourly"
CADENCE_DAILY = "daily"
CADENCE_WEEKLY = "weekly"

CADENCES = {CADENCE_HOURLY, CADENCE_DAILY, CADENCE_WEEKLY}


class JobStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    TIMEOUT = "TIMEOUT"


class JobPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class ScheduledJob:
    job_id: str
    name: str
    cadence: str
    target: str
    priority: JobPriority = JobPriority.MEDIUM
    timeout_seconds: int = 300
    enabled: bool = True
    last_run: str = ""
    last_status: str = JobStatus.PENDING.value
    owner: str = "Lang Lieu"
    params: dict[str, Any] = field(default_factory=dict)


class RuntimeScheduler:
    def __init__(self):
        self._jobs: dict[str, ScheduledJob] = {}
        self._handlers: dict[str, Callable] = {}
        self._running = False
        self._init_runtime_jobs()

    def _init_runtime_jobs(self):
        hourly = [
            ScheduledJob("hourly-forecast", "Iris Forecast", CADENCE_HOURLY,
                         "services.market_forecast_engine.run_forecast", priority=JobPriority.HIGH),
            ScheduledJob("hourly-reality", "Reality Check", CADENCE_HOURLY,
                         "services.forecast_accuracy_engine.check_reality", priority=JobPriority.HIGH),
            ScheduledJob("hourly-lesson", "Lesson Update", CADENCE_HOURLY,
                         "services.market_lesson_engine.extract_lessons", priority=JobPriority.MEDIUM),
            ScheduledJob("hourly-health", "Health Check", CADENCE_HOURLY,
                         "services.runtime_guard.check_health", priority=JobPriority.CRITICAL),
        ]
        daily = [
            ScheduledJob("daily-kace", "KACE Scorecard", CADENCE_DAILY,
                         "services.kingdom_scorecard_engine.generate_scorecard", priority=JobPriority.HIGH),
            ScheduledJob("daily-evidence", "Evidence Summary", CADENCE_DAILY,
                         "services.audit_evidence_compiler.compile_summary", priority=JobPriority.MEDIUM),
            ScheduledJob("daily-runtime", "Runtime Status", CADENCE_DAILY,
                         "services.runtime_supervisor.status_report", priority=JobPriority.HIGH),
        ]
        weekly = [
            ScheduledJob("weekly-kingdom", "Kingdom Review", CADENCE_WEEKLY,
                         "services.kingdom_health_aggregator.full_review", priority=JobPriority.HIGH),
            ScheduledJob("weekly-agent", "Agent Review", CADENCE_WEEKLY,
                         "services.agent_performance_engine.review_agents", priority=JobPriority.MEDIUM),
            ScheduledJob("weekly-audit", "Audit Readiness", CADENCE_WEEKLY,
                         "services.audit_readiness_engine.check_readiness", priority=JobPriority.HIGH),
        ]
        for job in hourly + daily + weekly:
            self._jobs[job.job_id] = job

    def register_job(self, job: ScheduledJob) -> None:
        self._jobs[job.job_id] = job

    def register_handler(self, job_id: str, handler: Callable) -> None:
        self._handlers[job_id] = handler

    def get_jobs(self, cadence: str | None = None) -> list[ScheduledJob]:
        if cadence:
            return [j for j in self._jobs.values() if j.cadence == cadence]
        return list(self._jobs.values())

    def run_cadence(self, cadence: str) -> list[dict[str, Any]]:
        results = []
        for job in self._jobs.values():
            if job.cadence != cadence or not job.enabled:
                continue
            handler = self._handlers.get(job.job_id)
            if handler is None:
                job.last_status = JobStatus.SKIPPED.value
                results.append({"job_id": job.job_id, "status": "skipped", "reason": "no_handler"})
                continue
            try:
                job.last_status = JobStatus.RUNNING.value
                result = handler(**job.params)
                job.last_run = _utc_now()
                job.last_status = JobStatus.SUCCESS.value
                results.append({"job_id": job.job_id, "status": "success"})
            except Exception as e:
                job.last_run = _utc_now()
                job.last_status = JobStatus.FAILED.value
                results.append({"job_id": job.job_id, "status": "error", "error": str(e)})
        return results

    def run_hourly(self) -> list[dict]:
        return self.run_cadence(CADENCE_HOURLY)

    def run_daily(self) -> list[dict]:
        return self.run_cadence(CADENCE_DAILY)

    def run_weekly(self) -> list[dict]:
        return self.run_cadence(CADENCE_WEEKLY)

    def start(self) -> dict:
        self._running = True
        return {"status": "OK", "running": True, "jobs": len(self._jobs)}

    def stop(self) -> dict:
        self._running = False
        return {"status": "OK", "running": False}

    def summary(self) -> dict[str, Any]:
        return {
            "running": self._running,
            "total_jobs": len(self._jobs),
            "hourly": len(self.get_jobs(CADENCE_HOURLY)),
            "daily": len(self.get_jobs(CADENCE_DAILY)),
            "weekly": len(self.get_jobs(CADENCE_WEEKLY)),
            "enabled": sum(1 for j in self._jobs.values() if j.enabled),
            "handlers": len(self._handlers),
        }


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
