"""Runtime Supervisor - Monitoring, heartbeat, and restart management for AK-RUNTIME-LITE."""

import time
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable


HEARTBEAT_INTERVAL = 30
MAX_RESTART_ATTEMPTS = 3
RESTART_COOLDOWN = 60


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ComponentStatus:
    name: str
    healthy: bool = True
    last_heartbeat: str = ""
    failures: int = 0
    last_error: str = ""


class RuntimeSupervisor:
    def __init__(self):
        self._components: dict[str, ComponentStatus] = {}
        self._health_checks: dict[str, Callable] = {}
        self._running = False
        self._heartbeat_thread: threading.Thread | None = None
        self._restart_count = 0
        self._last_restart = 0.0
        self._alert_callback: Callable | None = None

    def register_component(self, name: str, health_check: Callable | None = None) -> None:
        self._components[name] = ComponentStatus(name=name)
        if health_check:
            self._health_checks[name] = health_check

    def record_heartbeat(self, component: str) -> dict:
        if component not in self._components:
            return {"status": "ERROR", "message": f"Unknown component: {component}"}
        self._components[component].last_heartbeat = _utc_now()
        self._components[component].healthy = True
        self._components[component].failures = 0
        return {"status": "OK", "component": component}

    def record_failure(self, component: str, error: str) -> dict:
        if component not in self._components:
            return {"status": "ERROR", "message": f"Unknown component: {component}"}
        comp = self._components[component]
        comp.failures += 1
        comp.last_error = error
        comp.healthy = False
        return {"status": "WARNING", "component": component, "failures": comp.failures}

    def check_component(self, component: str) -> dict:
        if component not in self._components:
            return {"status": "UNKNOWN", "component": component}
        comp = self._components[component]
        if comp.name in self._health_checks:
            try:
                result = self._health_checks[comp.name]()
                comp.healthy = result.get("healthy", True)
            except Exception as e:
                comp.healthy = False
                comp.last_error = str(e)
        return {
            "component": component,
            "healthy": comp.healthy,
            "failures": comp.failures,
            "last_heartbeat": comp.last_heartbeat,
            "last_error": comp.last_error,
        }

    def can_restart(self) -> bool:
        now = time.time()
        if now - self._last_restart < RESTART_COOLDOWN:
            return False
        return self._restart_count < MAX_RESTART_ATTEMPTS

    def restart_component(self, component: str, restart_fn: Callable) -> dict:
        if not self.can_restart():
            return {"status": "BLOCKED", "reason": "Max restart attempts reached or cooldown active"}
        try:
            self._restart_count += 1
            self._last_restart = time.time()
            result = restart_fn()
            self.record_heartbeat(component)
            return {"status": "RESTARTED", "component": component, "attempt": self._restart_count}
        except Exception as e:
            self.record_failure(component, f"Restart failed: {e}")
            return {"status": "FAILED", "component": component, "error": str(e)}

    def set_alert_callback(self, callback: Callable) -> None:
        self._alert_callback = callback

    def _heartbeat_loop(self) -> None:
        while self._running:
            time.sleep(HEARTBEAT_INTERVAL)
            for name in self._components:
                comp = self._components[name]
                if not comp.last_heartbeat:
                    continue
                try:
                    last_hb = datetime.fromisoformat(comp.last_heartbeat)
                    elapsed = (datetime.now(timezone.utc) - last_hb).total_seconds()
                    if elapsed > HEARTBEAT_INTERVAL * 3:
                        comp.healthy = False
                        comp.failures += 1
                        comp.last_error = f"No heartbeat for {elapsed:.0f}s"
                        if self._alert_callback:
                            self._alert_callback({
                                "type": "heartbeat_missed",
                                "component": name,
                                "elapsed": elapsed,
                            })
                except Exception:
                    pass

    def start(self) -> dict:
        if self._running:
            return {"status": "OK", "message": "Already running"}
        self._running = True
        self._heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self._heartbeat_thread.start()
        return {"status": "OK", "message": "Supervisor started"}

    def stop(self) -> dict:
        self._running = False
        return {"status": "OK", "message": "Supervisor stopped"}

    def reset_restart_count(self) -> None:
        self._restart_count = 0

    def status_report(self) -> dict[str, Any]:
        all_healthy = all(c.healthy for c in self._components.values()) if self._components else True
        return {
            "running": self._running,
            "components": {n: self.check_component(n) for n in self._components},
            "all_healthy": all_healthy,
            "restart_count": self._restart_count,
            "can_restart": self.can_restart(),
            "uptime": _utc_now(),
        }
