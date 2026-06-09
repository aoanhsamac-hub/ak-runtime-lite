"""Scheduler Registry - Persistent registry for scheduled jobs."""

import json
import os
from pathlib import Path
from typing import Any
from services.kingdom_scheduler import RuntimeScheduler, ScheduledJob, JobPriority


REGISTRY_DIR = Path(__file__).resolve().parent.parent / "data" / "registries"
REGISTRY_PATH = REGISTRY_DIR / "scheduler_registry.json"


class SchedulerRegistry:
    def __init__(self, path: str | None = None):
        self._path = Path(path) if path else REGISTRY_PATH

    def ensure_dir(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, scheduler: RuntimeScheduler) -> dict:
        self.ensure_dir()
        data = {
            "jobs": [self._job_to_dict(j) for j in scheduler.get_jobs()],
            "summary": scheduler.summary(),
        }
        with open(self._path, "w") as f:
            json.dump(data, f, indent=2)
        return {"status": "OK", "path": str(self._path), "jobs": len(data["jobs"])}

    def load(self, scheduler: RuntimeScheduler) -> dict:
        if not self._path.exists():
            return {"status": "NOT_FOUND", "path": str(self._path)}
        with open(self._path) as f:
            data = json.load(f)
        for jd in data.get("jobs", []):
            job = self._dict_to_job(jd)
            scheduler.register_job(job)
        return {"status": "OK", "loaded": len(data.get("jobs", []))}

    def _job_to_dict(self, job: ScheduledJob) -> dict:
        return {
            "job_id": job.job_id,
            "name": job.name,
            "cadence": job.cadence,
            "target": job.target,
            "priority": job.priority.value,
            "timeout_seconds": job.timeout_seconds,
            "enabled": job.enabled,
            "last_run": job.last_run,
            "last_status": job.last_status,
            "owner": job.owner,
        }

    def _dict_to_job(self, d: dict) -> ScheduledJob:
        return ScheduledJob(
            job_id=d["job_id"],
            name=d["name"],
            cadence=d["cadence"],
            target=d["target"],
            priority=JobPriority(d.get("priority", "MEDIUM")),
            timeout_seconds=d.get("timeout_seconds", 300),
            enabled=d.get("enabled", True),
            last_run=d.get("last_run", ""),
            last_status=d.get("last_status", "PENDING"),
            owner=d.get("owner", "Lang Lieu"),
        )

    def backup(self, backup_dir: str | None = None) -> dict:
        if not self._path.exists():
            return {"status": "NOT_FOUND"}
        bdir = Path(backup_dir) if backup_dir else self._path.parent / "backups"
        bdir.mkdir(parents=True, exist_ok=True)
        import shutil
        from datetime import datetime
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        dst = bdir / f"scheduler_registry_{ts}.json"
        shutil.copy2(self._path, dst)
        return {"status": "OK", "backup_path": str(dst)}
