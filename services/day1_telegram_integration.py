from datetime import datetime, timezone
from typing import Any

from services.telegram_notification_service import NotificationService


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def notify_runtime_started() -> dict[str, Any]:
    try:
        ns = NotificationService()
        result = ns.notify_runtime_start()
        return {
            "status": "OK",
            "handler": "day1_telegram_integration",
            "notification": "runtime_started",
            "recipients": len(result),
            "timestamp": _utc_now(),
        }
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


def notify_runtime_stopped(reason: str = "") -> dict[str, Any]:
    try:
        ns = NotificationService()
        result = ns.notify_runtime_stop(reason)
        return {
            "status": "OK",
            "handler": "day1_telegram_integration",
            "notification": "runtime_stopped",
            "reason": reason,
            "recipients": len(result),
            "timestamp": _utc_now(),
        }
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


def notify_scheduler_failure(details: dict) -> dict[str, Any]:
    try:
        ns = NotificationService()
        result = ns.alert_operators(f"SCHEDULER FAILURE: {details}", level="ERROR")
        return {
            "status": "OK",
            "notification": "scheduler_failure",
            "recipients": len(result),
            "timestamp": _utc_now(),
        }
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


def notify_mt5_failure(details: dict) -> dict[str, Any]:
    try:
        ns = NotificationService()
        result = ns.alert_operators(f"MT5 FAILURE: {details}", level="ERROR")
        return {
            "status": "OK",
            "notification": "mt5_failure",
            "recipients": len(result),
            "timestamp": _utc_now(),
        }
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


def notify_evidence_failure(details: dict) -> dict[str, Any]:
    try:
        ns = NotificationService()
        result = ns.alert_operators(f"EVIDENCE FAILURE: {details}", level="ERROR")
        return {
            "status": "OK",
            "notification": "evidence_failure",
            "recipients": len(result),
            "timestamp": _utc_now(),
        }
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


def notify_scorecard_available(scorecard_id: str) -> dict[str, Any]:
    try:
        ns = NotificationService()
        result = ns.broadcast(f"Daily KACE Scorecard available: {scorecard_id}", level="INFO")
        return {
            "status": "OK",
            "notification": "scorecard_available",
            "scorecard_id": scorecard_id,
            "recipients": len(result),
            "timestamp": _utc_now(),
        }
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


def verify_commands() -> dict[str, Any]:
    from services.telegram_gateway import MANDATORY_COMMANDS
    available = list(MANDATORY_COMMANDS.keys())
    return {
        "status": "OK",
        "handler": "day1_telegram_integration",
        "commands_available": available,
        "command_count": len(available),
        "timestamp": _utc_now(),
    }


__all__ = [
    "notify_runtime_started", "notify_runtime_stopped",
    "notify_scheduler_failure", "notify_mt5_failure",
    "notify_evidence_failure", "notify_scorecard_available",
    "verify_commands",
]
