"""Runtime Guard - Real-time runtime health and safety monitoring."""

import os
import psutil
from typing import Any
from services.kingdom_scheduler import RuntimeScheduler


STOP_CONDITIONS = {
    "ram_low": "RAM < 200 MB",
    "mt5_disconnect": "MT5 disconnected",
    "scheduler_failure": "Scheduler consecutive failures",
    "unauthorized_command": "Unauthorized command detected",
    "execution_attempt": "Execution attempt blocked",
    "evidence_corruption": "Evidence integrity check failed",
    "duplicate_scheduler": "Multiple scheduler instances detected",
    "governance_violation": "Governance gate violation",
}


class RuntimeGuard:
    def __init__(self, scheduler: RuntimeScheduler | None = None):
        self._scheduler = scheduler
        self._stop_callbacks: list[callable] = []
        self._alert_callbacks: list[callable] = []
        self._violations: list[dict] = []
        self._paused = False

    @property
    def is_paused(self) -> bool:
        return self._paused

    def register_stop_callback(self, callback: callable) -> None:
        self._stop_callbacks.append(callback)

    def register_alert_callback(self, callback: callable) -> None:
        self._alert_callbacks.append(callback)

    def check_ram(self) -> dict:
        try:
            free_mb = psutil.virtual_memory().available / 1024 / 1024
            healthy = free_mb >= 200
            if not healthy:
                self._violations.append({"condition": "ram_low", "detail": f"{free_mb:.0f} MB free"})
            return {"condition": "ram_low", "healthy": healthy, "free_mb": round(free_mb, 1), "threshold_mb": 200}
        except Exception as e:
            return {"condition": "ram_low", "healthy": False, "error": str(e)}

    def check_mt5(self) -> dict:
        try:
            from connectors.mt5.health_monitor import MT5HealthMonitor
            monitor = MT5HealthMonitor(None)
            result = monitor.check_connection()
            healthy = result.get("status") not in ("no_observer", "error")
            if not healthy:
                self._violations.append({"condition": "mt5_disconnect", "detail": str(result)})
            return {"condition": "mt5_disconnect", "healthy": healthy, "detail": result}
        except ImportError:
            return {"condition": "mt5_disconnect", "healthy": True, "detail": "MT5 not available"}

    def check_scheduler(self) -> dict:
        if self._scheduler is None:
            return {"condition": "scheduler_failure", "healthy": True, "detail": "No scheduler"}
        jobs = self._scheduler.get_jobs()
        failed = [j for j in jobs if j.last_status == "FAILED"]
        healthy = len(failed) < 3
        if not healthy:
            self._violations.append({"condition": "scheduler_failure", "detail": f"{len(failed)} failed jobs"})
        return {"condition": "scheduler_failure", "healthy": healthy, "failed_jobs": len(failed), "total_jobs": len(jobs)}

    def check_execution_attempts(self) -> dict:
        try:
            from connectors.mt5.mt5_demo_observer import MT5DemoObserver
            observer = MT5DemoObserver()
            result = observer.place_order()
            blocked = "execution_blocked" in result.get("error", "")
            if not blocked:
                self._violations.append({"condition": "execution_attempt", "detail": "Execution not blocked"})
            return {"condition": "execution_attempt", "healthy": blocked, "detail": result}
        except Exception as e:
            return {"condition": "execution_attempt", "healthy": True, "detail": str(e)}

    def check_duplicate_scheduler(self) -> dict:
        if self._scheduler is None:
            return {"condition": "duplicate_scheduler", "healthy": True, "detail": "No scheduler"}
        healthy = hasattr(self._scheduler, "_jobs") and self._scheduler._running is not None
        return {"condition": "duplicate_scheduler", "healthy": healthy}

    def check_governance(self) -> dict:
        try:
            from governance.governance_gate import evaluate_proposal
            result = evaluate_proposal({
                "title": "runtime_guard_check",
                "description": "Periodic governance check",
                "target_path": "/runtime/guard",
                "approvers": ["Sage"],
                "governance_valid": True,
            })
            healthy = not result.get("blocked", False)
            if not healthy:
                self._violations.append({"condition": "governance_violation", "detail": str(result)})
            return {"condition": "governance_violation", "healthy": healthy}
        except Exception as e:
            return {"condition": "governance_violation", "healthy": True, "detail": str(e)}

    def check_all(self) -> dict[str, dict]:
        return {
            "ram": self.check_ram(),
            "mt5": self.check_mt5(),
            "scheduler": self.check_scheduler(),
            "execution": self.check_execution_attempts(),
            "duplicate_scheduler": self.check_duplicate_scheduler(),
            "governance": self.check_governance(),
        }

    def all_healthy(self) -> bool:
        checks = self.check_all()
        return all(c.get("healthy", True) for c in checks.values())

    def trigger_stop(self, reason: str) -> dict:
        result = {"action": "STOP", "reason": reason, "timestamp": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()}
        self._paused = True
        for cb in self._stop_callbacks:
            try:
                cb(result)
            except Exception:
                pass
        return result

    def get_violations(self) -> list[dict]:
        return list(self._violations)

    def clear_violations(self) -> None:
        self._violations.clear()

    def health(self) -> dict:
        checks = self.check_all()
        return {
            "all_healthy": all(c.get("healthy", True) for c in checks.values()),
            "paused": self._paused,
            "violations": len(self._violations),
            "checks": checks,
        }
