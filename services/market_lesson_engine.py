"""Market Lesson Engine - Extract lessons from forecast accuracy results."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_accuracy_registry() -> dict:
    import yaml
    path = REGISTRIES_DIR / "KINGDOM_FORECAST_ACCURACY_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_lesson_registry() -> dict:
    import yaml
    path = REGISTRIES_DIR / "KINGDOM_MARKET_LESSON_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_lesson_registry(registry: dict) -> None:
    import yaml
    path = REGISTRIES_DIR / "KINGDOM_MARKET_LESSON_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_lesson_id() -> str:
    registry = _load_lesson_registry()
    inner = registry.get("kingdom_market_lesson_registry", registry)
    counter = len(inner.get("lesson_records", [])) + 1
    return f"LESSON-{counter:04d}"


def extract_lesson(accuracy_id: str, forecast_id: str) -> dict[str, Any]:
    accuracy = None
    acc_inner = _load_accuracy_registry().get("kingdom_forecast_accuracy_registry", {})
    for a in acc_inner.get("accuracy_records", []):
        if a.get("accuracy_id") == accuracy_id:
            accuracy = a
            break

    forecast = None
    fcst_inner = __import__("services.market_forecast_engine", fromlist=["get_forecast"]).get_forecast(forecast_id)
    if fcst_inner:
        forecast = fcst_inner

    if not accuracy or not forecast:
        return {}

    lesson_type = "success_pattern" if accuracy.get("outcome") == "success" else "failure_analysis"
    root_cause = "zone_correctly_identified" if accuracy.get("zone_accuracy") else "zone_misidentified"
    recommendation = "continue_current_approach" if accuracy.get("zone_accuracy") else "review_zone_detection_logic"

    lesson = {
        "lesson_id": _generate_lesson_id(),
        "forecast_id": forecast_id,
        "accuracy_id": accuracy_id,
        "lesson_type": lesson_type,
        "root_cause": root_cause,
        "recommendation": recommendation,
        "confidence": accuracy.get("accuracy_score", 0.0),
        "created_at": _utc_now(),
    }

    registry = _load_lesson_registry()
    lesson_inner = registry.get("kingdom_market_lesson_registry", {})
    lesson_inner.setdefault("lesson_records", []).append(lesson)
    lesson_inner["last_lesson_id"] = lesson["lesson_id"]
    lesson_inner["last_updated"] = _utc_now()
    registry["kingdom_market_lesson_registry"] = lesson_inner
    _save_lesson_registry(registry)

    return lesson


def list_all_lessons() -> list[dict]:
    registry = _load_lesson_registry()
    inner = registry.get("kingdom_market_lesson_registry", {})
    return inner.get("lesson_records", [])


def get_lesson_by_forecast(forecast_id: str) -> dict | None:
    for lesson in list_all_lessons():
        if lesson.get("forecast_id") == forecast_id:
            return lesson
    return None


__all__ = ["extract_lesson", "list_all_lessons", "get_lesson_by_forecast"]