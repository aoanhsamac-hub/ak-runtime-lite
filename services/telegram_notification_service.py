"""Telegram Notification Service - Sends alerts and notifications to authorized users."""

import os
from typing import Any
from services.telegram_gateway import WHITELISTED_USERS, _load_whitelist


class NotificationService:
    def __init__(self, gateway=None):
        self._gateway = gateway
        self._alert_levels = {"INFO": 0, "WARNING": 1, "ERROR": 2, "CRITICAL": 3}

    def send_notification(self, user_id: int, message: str, level: str = "INFO") -> dict:
        if user_id <= 0:
            return {"status": "ERROR", "message": "Invalid user_id"}
        return {
            "status": "QUEUED",
            "user_id": user_id,
            "message": message[:4096],
            "level": level,
            "timestamp": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        }

    def broadcast(self, message: str, level: str = "INFO", min_level: str = "INFO") -> list[dict]:
        if not WHITELISTED_USERS:
            WHITELISTED_USERS.update(_load_whitelist())
        results = []
        current_level = self._alert_levels.get(level, 0)
        min_lvl = self._alert_levels.get(min_level, 0)
        if current_level < min_lvl:
            return results
        for uid in WHITELISTED_USERS:
            results.append(self.send_notification(uid, message, level))
        return results

    def alert_operators(self, message: str, level: str = "ERROR") -> list[dict]:
        return self.broadcast(message, level=level, min_level="WARNING")

    def notify_stop_condition(self, condition: str, details: dict) -> list[dict]:
        msg = f"STOP CONDITION TRIGGERED: {condition}\nDetails: {details}"
        return self.broadcast(msg, level="CRITICAL", min_level="WARNING")

    def notify_recovery(self, component: str, action: str, result: dict) -> list[dict]:
        msg = f"RECOVERY: {component} - {action}\nResult: {result.get('status', 'UNKNOWN')}"
        return self.broadcast(msg, level="WARNING", min_level="WARNING")

    def notify_runtime_start(self) -> list[dict]:
        return self.broadcast("AK-RUNTIME-LITE started", level="INFO", min_level="INFO")

    def notify_runtime_stop(self, reason: str = "") -> list[dict]:
        msg = f"AK-RUNTIME-LITE stopped"
        if reason:
            msg += f" - Reason: {reason}"
        return self.broadcast(msg, level="WARNING", min_level="INFO")

    def health(self) -> dict:
        return {
            "whitelisted_users": len(WHITELISTED_USERS) if WHITELISTED_USERS else len(_load_whitelist()),
            "alert_levels": list(self._alert_levels.keys()),
        }
