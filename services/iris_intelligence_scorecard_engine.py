"""Iris Intelligence Scorecard Engine - Unified market intelligence metrics."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_scorecard() -> dict:
    import yaml
    path = REGISTRIES_DIR / "IRIS_INTELLIGENCE_SCORECARD.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_scorecard(scorecard: dict) -> None:
    import yaml
    path = REGISTRIES_DIR / "IRIS_INTELLIGENCE_SCORECARD.yaml"
    path.write_text(yaml.dump(scorecard, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def calculate_intelligence_scorecard() -> dict[str, Any]:
    """Calculate unified intelligence scorecard."""
    from services.iris_forecast_benchmark_engine import get_benchmarks
    from services.market_lesson_engine import list_all_lessons
    from services.market_knowledge_engine import process_all_pending_lessons

    benchmarks = get_benchmarks()
    lessons = list_all_lessons()
    knowledge = process_all_pending_lessons()

    avg_accuracy = sum(b.get("overall_accuracy", 0) for b in benchmarks) / len(benchmarks) if benchmarks else 0

    return {
        "scorecard_id": f"SC-{datetime.now().strftime('%Y%m%d%H%M')}",
        "timestamp": _utc_now(),
        "forecast_count": len(benchmarks),
        "forecast_accuracy": round(avg_accuracy, 2),
        "lesson_count": len(lessons),
        "knowledge_count": len(knowledge),
        "skill_proposals": 0,
        "pattern_coverage": 0,
        "data_coverage": 0,
        "learning_velocity": 0,
    }


def generate_scorecard_report() -> dict:
    scorecard = calculate_intelligence_scorecard()
    return {
        "report_id": f"REPORT-SCORECARD-{datetime.now().strftime('%Y%m%d')}",
        "generated_at": _utc_now(),
        "scorecard": scorecard,
    }


__all__ = ["calculate_intelligence_scorecard", "generate_scorecard_report"]