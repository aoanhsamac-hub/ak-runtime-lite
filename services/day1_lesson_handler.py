from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
FORECAST_REGISTRY_FILE = "FORECAST_REGISTRY.json"
BENCHMARK_REGISTRY_FILE = "FORECAST_BENCHMARK_REGISTRY.json"
LESSON_REGISTRY_FILE = "MARKET_LESSON_REGISTRY.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_json(name: str) -> dict:
    import json
    path = REGISTRIES_DIR / name
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_json(name: str, registry: dict) -> None:
    import json
    path = REGISTRIES_DIR / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")


def _generate_lesson_id() -> str:
    registry = _load_json(LESSON_REGISTRY_FILE)
    inner = registry.get("market_lesson_registry", {})
    counter = len(inner.get("lesson_records", [])) + 1
    return f"LESSON-{counter:04d}"


CATEGORIES = {
    "success": "forecast direction matched market movement",
    "failure": "forecast direction did not match market movement",
    "neutral": "market movement was within expected range",
    "unknown": "insufficient data to evaluate",
}


def run_lesson_handler() -> dict[str, Any]:
    bench_reg = _load_json(BENCHMARK_REGISTRY_FILE)
    if "forecast_benchmark_registry" not in bench_reg:
        bench_reg["forecast_benchmark_registry"] = {}
    bench_inner = bench_reg["forecast_benchmark_registry"]
    benchmarks = bench_inner.get("benchmark_records", [])
    lesson_reg = _load_json(LESSON_REGISTRY_FILE)
    if "market_lesson_registry" not in lesson_reg:
        lesson_reg["market_lesson_registry"] = {}
    lesson_inner = lesson_reg["market_lesson_registry"]
    lessons_created = 0
    for benchmark in benchmarks:
        if benchmark.get("lesson_extracted", False):
            continue
        acc = benchmark.get("overall_accuracy", 0.5)
        if acc >= 0.7:
            category = "success"
        elif acc >= 0.4:
            category = "neutral"
        elif acc > 0:
            category = "failure"
        else:
            category = "unknown"
        lesson = {
            "lesson_id": _generate_lesson_id(),
            "forecast_id": benchmark.get("forecast_id", ""),
            "benchmark_id": benchmark.get("benchmark_id", ""),
            "symbol": benchmark.get("symbol", ""),
            "timeframe": benchmark.get("timeframe", ""),
            "category": category,
            "description": CATEGORIES.get(category, "unknown outcome"),
            "accuracy_score": acc,
            "created_at": _utc_now(),
            "handler_type": "day1_lesson_handler",
        }
        lesson_inner.setdefault("lesson_records", []).append(lesson)
        benchmark["lesson_extracted"] = True
        lessons_created += 1
    lesson_inner["last_run"] = _utc_now()
    lesson_inner["lesson_count"] = lessons_created
    lesson_inner["status"] = "ACTIVE"
    _save_json(LESSON_REGISTRY_FILE, lesson_reg)
    _save_json(BENCHMARK_REGISTRY_FILE, bench_reg)
    return {
        "status": "OK",
        "handler": "day1_lesson_handler",
        "lessons_created": lessons_created,
        "timestamp": _utc_now(),
        "registry": str(REGISTRIES_DIR / LESSON_REGISTRY_FILE),
    }


def get_lessons() -> list[dict]:
    reg = _load_json(LESSON_REGISTRY_FILE)
    inner = reg.get("market_lesson_registry", {})
    return inner.get("lesson_records", [])


def get_lesson_summary() -> dict[str, Any]:
    records = get_lessons()
    by_category: dict[str, int] = {}
    for r in records:
        cat = str(r.get("category", "unknown"))
        by_category[cat] = by_category.get(cat, 0) + 1
    return {
        "total_lessons": len(records),
        "by_category": by_category,
        "last_run": _load_json(LESSON_REGISTRY_FILE).get("market_lesson_registry", {}).get("last_run", ""),
    }


__all__ = ["run_lesson_handler", "get_lessons", "get_lesson_summary"]
