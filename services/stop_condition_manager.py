"""Stop Condition Manager - Manages stop condition lifecycle and escalation."""

from typing import Any, Callable
from services.runtime_guard import RuntimeGuard, STOP_CONDITIONS


class StopConditionManager:
    def __init__(self, guard: RuntimeGuard):
        self._guard = guard
        self._stop_history: list[dict] = []
        self._escalation_chain: list[Callable] = []

    def register_escalation(self, handler: Callable) -> None:
        self._escalation_chain.append(handler)

    def evaluate(self) -> dict:
        checks = self._guard.check_all()
        triggered = [k for k, v in checks.items() if not v.get("healthy", True)]
        result = {
            "all_healthy": len(triggered) == 0,
            "triggered_conditions": triggered,
            "details": {k: v for k, v in checks.items() if not v.get("healthy", True)},
            "stop_condition_descriptions": {k: STOP_CONDITIONS.get(k, k) for k in triggered},
        }
        self._stop_history.append(result)
        if triggered:
            self._escalate(result)
        return result

    def _escalate(self, result: dict) -> None:
        for handler in self._escalation_chain:
            try:
                handler(result)
            except Exception:
                pass

    def should_stop(self) -> bool:
        result = self.evaluate()
        return not result["all_healthy"]

    def stop_if_needed(self) -> dict | None:
        if self.should_stop():
            triggered = self.evaluate()["triggered_conditions"]
            reason = f"Stop conditions triggered: {', '.join(triggered)}"
            return self._guard.trigger_stop(reason)
        return None

    def get_history(self, limit: int = 20) -> list[dict]:
        return self._stop_history[-limit:]

    def get_stop_condition_definitions(self) -> dict:
        return dict(STOP_CONDITIONS)

    def health(self) -> dict:
        return {
            "conditions": len(STOP_CONDITIONS),
            "triggered_in_history": sum(1 for h in self._stop_history if not h["all_healthy"]),
            "escalation_handlers": len(self._escalation_chain),
        }
