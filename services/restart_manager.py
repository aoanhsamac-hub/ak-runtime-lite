"""Restart Manager - Manages component restart with cooldown and max attempts."""

import time
from typing import Any, Callable


class RestartManager:
    MAX_ATTEMPTS = 3
    COOLDOWN_SECONDS = 60

    def __init__(self):
        self._attempts: dict[str, int] = {}
        self._last_restart: dict[str, float] = {}
        self._restart_handlers: dict[str, Callable] = {}

    def register_handler(self, component: str, handler: Callable) -> None:
        self._restart_handlers[component] = handler

    def can_restart(self, component: str) -> bool:
        now = time.time()
        last = self._last_restart.get(component, 0)
        if now - last < self.COOLDOWN_SECONDS:
            return False
        return self._attempts.get(component, 0) < self.MAX_ATTEMPTS

    def restart(self, component: str) -> dict:
        if not self.can_restart(component):
            return {
                "status": "BLOCKED",
                "component": component,
                "reason": "Max attempts or cooldown",
                "attempts": self._attempts.get(component, 0),
                "cooldown_remaining": max(0, self.COOLDOWN_SECONDS - (time.time() - self._last_restart.get(component, 0))),
            }
        handler = self._restart_handlers.get(component)
        if handler is None:
            return {"status": "ERROR", "component": component, "reason": "No restart handler"}
        try:
            self._attempts[component] = self._attempts.get(component, 0) + 1
            self._last_restart[component] = time.time()
            result = handler()
            return {
                "status": "RESTARTED",
                "component": component,
                "attempt": self._attempts[component],
                "result": result,
            }
        except Exception as e:
            return {"status": "FAILED", "component": component, "error": str(e)}

    def reset_attempts(self, component: str) -> None:
        self._attempts[component] = 0
        self._last_restart[component] = 0.0

    def reset_all(self) -> None:
        self._attempts.clear()
        self._last_restart.clear()

    def summary(self) -> dict[str, Any]:
        return {
            "max_attempts": self.MAX_ATTEMPTS,
            "cooldown": self.COOLDOWN_SECONDS,
            "components": list(self._restart_handlers.keys()),
            "attempts": dict(self._attempts),
        }
