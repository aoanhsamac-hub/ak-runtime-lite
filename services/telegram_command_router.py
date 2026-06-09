"""Telegram Command Router - Routes incoming commands to handlers."""

from typing import Callable
from services.telegram_gateway import TelegramGateway, MANDATORY_COMMANDS


class CommandRouter:
    def __init__(self, gateway: TelegramGateway):
        self._gateway = gateway
        self._fallback_handler: Callable | None = None

    def register_fallback(self, handler: Callable) -> None:
        self._fallback_handler = handler

    def route(self, user_id: int, text: str) -> dict:
        if not text.startswith("/"):
            return self._route_fallback(user_id, text)

        parts = text.strip().split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        status_handler = self._gateway._command_handlers.get("__status_all")
        if command == "/status" and status_handler:
            return self._gateway.process_command(user_id, command, args)

        return self._gateway.process_command(user_id, command, args)

    def _route_fallback(self, user_id: int, text: str) -> dict:
        if self._fallback_handler:
            try:
                result = self._fallback_handler(text)
                return {"status": "OK", "data": result, "command": "fallback"}
            except Exception as e:
                return {"status": "ERROR", "message": str(e), "command": "fallback"}
        return {"status": "ERROR", "message": "No handler for non-command input", "command": "fallback"}

    def get_help_text(self) -> str:
        lines = ["Available commands:"]
        for cmd, desc in sorted(MANDATORY_COMMANDS.items()):
            lines.append(f"  {cmd} - {desc}")
        return "\n".join(lines)

    def list_available_commands(self) -> list[dict]:
        result = []
        for cmd, desc in MANDATORY_COMMANDS.items():
            result.append({"command": cmd, "description": desc})
        return result
