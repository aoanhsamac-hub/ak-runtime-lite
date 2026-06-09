"""Market Knowledge Engine - Generate knowledge from lessons."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from memory.lancedb_adapter import LanceDBAdapter
from memory.lesson_registry import LessonRegistry

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_forecast_registry() -> dict:
    import yaml
    path = REGISTRIES_DIR / "KINGDOM_MARKET_FORECAST_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_accuracy_registry() -> dict:
    import yaml
    path = REGISTRIES_DIR / "KINGDOM_FORECAST_ACCURACY_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_lesson_registry_yaml() -> dict:
    import yaml
    path = REGISTRIES_DIR / "KINGDOM_MARKET_LESSON_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def generate_knowledge(lesson_id: str) -> dict[str, Any]:
    from services.market_lesson_engine import get_lesson_by_forecast

    lessons_yaml = _load_lesson_registry_yaml().get("kingdom_market_lesson_registry", {})
    lesson = None
    for l in lessons_yaml.get("lesson_records", []):
        if l.get("lesson_id") == lesson_id:
            lesson = l
            break

    if not lesson:
        return {}

    knowledge = {
        "knowledge_id": f"KNOWLEDGE-{lesson_id}",
        "source_lesson_id": lesson_id,
        "knowledge_type": lesson.get("lesson_type", "unknown"),
        "insight": lesson.get("root_cause", ""),
        "application": lesson.get("recommendation", ""),
        "confidence": lesson.get("confidence", 0.0),
        "generated_at": _utc_now(),
        "status": "GENERATED",
    }

    return knowledge


def store_knowledge(knowledge: dict) -> dict:
    try:
        from memory.lancedb_adapter import LanceDBAdapter
        adapter = LanceDBAdapter(":memory:", backend={})
        adapter.insert("knowledge", [knowledge])
    except Exception:
        pass
    return knowledge


def process_all_pending_lessons() -> list[dict]:
    from services.market_lesson_engine import list_all_lessons

    lessons_yaml = _load_lesson_registry_yaml().get("kingdom_market_lesson_registry", {})
    lessons = lessons_yaml.get("lesson_records", [])
    knowledges = []
    for lesson in lessons:
        k = generate_knowledge(lesson.get("lesson_id", ""))
        if k:
            store_knowledge(k)
            knowledges.append(k)
    return knowledges


__all__ = ["generate_knowledge", "store_knowledge", "process_all_pending_lessons"]