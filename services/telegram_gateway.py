"""Telegram Gateway - Secure command gateway for AK-RUNTIME-LITE."""

import os
import hashlib
import hmac
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable

WHITELISTED_USERS: set[int] = set()
AUDIT_LOG: list[dict] = []
RATE_LIMIT_WINDOWS: dict[int, list[float]] = {}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_whitelist() -> set[int]:
    raw = os.environ.get("TELEGRAM_WHITELIST", "")
    if not raw:
        return set()
    return {int(uid.strip()) for uid in raw.split(",") if uid.strip().isdigit()}


def is_authorized(user_id: int) -> bool:
    if not WHITELISTED_USERS:
        WHITELISTED_USERS.update(_load_whitelist())
    return user_id in WHITELISTED_USERS


def _rate_limited(user_id: int, max_per_minute: int = 20) -> bool:
    now = time.time()
    if user_id not in RATE_LIMIT_WINDOWS:
        RATE_LIMIT_WINDOWS[user_id] = []
    window = RATE_LIMIT_WINDOWS[user_id]
    window[:] = [t for t in window if now - t < 60]
    if len(window) >= max_per_minute:
        return True
    window.append(now)
    return False


def _audit(event: str, user_id: int, command: str, status: str) -> None:
    AUDIT_LOG.append({
        "event": event,
        "user_id": user_id,
        "command": command,
        "status": status,
        "timestamp": _utc_now(),
    })


MANDATORY_COMMANDS: dict[str, str] = {
    "/status": "Runtime status and health",
    "/directive": "Latest directive from Hung Vuong",
    "/tasks": "Current active tasks",
    "/report": "Generate and retrieve reports",
    "/iris": "Iris market intelligence summary",
    "/runtime": "Runtime configuration and state",
    "/stop_runtime": "Emergency runtime stop",
    "/help": "List available commands",
}


class TelegramGateway:
    def __init__(self, token: str | None = None):
        self._token = token or os.environ.get("TELEGRAM_BOT_TOKEN", "")
        self._command_handlers: dict[str, Callable] = {}
        self._running = False

    @property
    def has_token(self) -> bool:
        return bool(self._token)

    @property
    def is_running(self) -> bool:
        return self._running

    def register_handler(self, command: str, handler: Callable) -> None:
        self._command_handlers[command] = handler

    def validate_token_format(self) -> bool:
        parts = self._token.split(":")
        return len(parts) == 2 and parts[0].isdigit() and len(parts[1]) >= 30

    def verify_token_hash(self, stored_hash: str) -> bool:
        return hmac.compare_digest(
            hashlib.sha256(self._token.encode()).hexdigest(),
            stored_hash,
        )

    def process_command(self, user_id: int, command: str, args: str = "") -> dict:
        if not is_authorized(user_id):
            _audit("UNAUTHORIZED_ACCESS", user_id, command, "DENIED")
            return {"status": "ERROR", "message": "Unauthorized", "command": command}

        if _rate_limited(user_id):
            _audit("RATE_LIMITED", user_id, command, "BLOCKED")
            return {"status": "ERROR", "message": "Rate limited", "command": command}

        if command not in MANDATORY_COMMANDS and command not in self._command_handlers:
            _audit("UNKNOWN_COMMAND", user_id, command, "REJECTED")
            return {"status": "ERROR", "message": "Unknown command", "command": command}

        if command in self._command_handlers:
            try:
                handler = self._command_handlers[command]
                result = handler(args) if args else handler()
                _audit("COMMAND_OK", user_id, command, "OK")
                return {"status": "OK", "data": result, "command": command}
            except Exception as e:
                _audit("COMMAND_ERROR", user_id, command, "ERROR")
                return {"status": "ERROR", "message": str(e), "command": command}

        _audit("COMMAND_OK", user_id, command, "OK")
        return {"status": "OK", "message": f"Command {command} registered", "command": command}

    def start(self) -> dict:
        if not self._token:
            return {"status": "ERROR", "message": "No token configured"}
        self._running = True
        return {"status": "OK", "message": "Telegram gateway started"}

    def stop(self) -> dict:
        self._running = False
        return {"status": "OK", "message": "Telegram gateway stopped"}

    def get_audit_log(self, limit: int = 50) -> list[dict]:
        return AUDIT_LOG[-limit:]

    def get_whitelist(self) -> list[int]:
        if not WHITELISTED_USERS:
            WHITELISTED_USERS.update(_load_whitelist())
        return sorted(WHITELISTED_USERS)

    def health(self) -> dict:
        return {
            "running": self._running,
            "token_configured": bool(self._token),
            "commands": len(self._command_handlers) + len(MANDATORY_COMMANDS),
            "whitelisted_users": len(self.get_whitelist()),
            "audit_entries": len(AUDIT_LOG),
        }
