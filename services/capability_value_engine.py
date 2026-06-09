from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
MAX_CE_LEVEL = 4
CAP_VIOLATION = "PSOP-03 CAP: Capability Economy capped at Level 4."


class CapabilityValueError(Exception):
    pass


def _load_registry(name):
    import yaml
    path = REGISTRIES_DIR / name
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def assess_capability_value(capability_name, usage_count=0, task_completion_rate=0.0,
                            outcome_quality=0.0, adoption_count=0, evolution_cycle=0):
    if not capability_name:
        raise CapabilityValueError("capability_name is required")
    usage_value = min(usage_count * 5, 100)
    quality_value = min(task_completion_rate * outcome_quality * 100, 100)
    adoption_value = min(adoption_count * 10, 100)
    total_value = round((usage_value + quality_value + adoption_value) / 3, 2)
    return {
        "capability_name": capability_name,
        "usage_value": usage_value,
        "quality_value": round(quality_value, 2),
        "adoption_value": adoption_value,
        "total_value": total_value,
        "usage_count": usage_count,
        "task_completion_rate": task_completion_rate,
        "outcome_quality": outcome_quality,
        "adoption_count": adoption_count,
        "evolution_cycle": evolution_cycle,
        "assessed_at": _utc_now(),
        "cap_level": min(2 if usage_count > 0 else 0, MAX_CE_LEVEL),
    }


def get_domain_value_summary():
    import importlib
    domains = ["governance", "treasury", "agents", "capabilities", "knowledge", "datasets", "security", "trading"]
    summaries = {}
    for domain in domains:
        try:
            monitor = importlib.import_module(f"services.{domain}_health_monitor")
            if hasattr(monitor, "check") and callable(monitor.check):
                result = monitor.check()
                summaries[domain] = {
                    "status": result.get("status", "INITIALIZED"),
                    "score": result.get("score", 0),
                }
            else:
                summaries[domain] = {"status": "INITIALIZED", "score": 0}
        except (ImportError, AttributeError):
            try:
                monitor = importlib.import_module(f"services.{domain}_status_monitor")
                if hasattr(monitor, "check") and callable(monitor.check):
                    result = monitor.check()
                    summaries[domain] = {
                        "status": result.get("status", "INITIALIZED"),
                        "score": result.get("score", 0),
                    }
                else:
                    summaries[domain] = {"status": "INITIALIZED", "score": 0}
            except (ImportError, AttributeError):
                summaries[domain] = {"status": "INITIALIZED", "score": 0}
    total_score = sum(s["score"] for s in summaries.values())
    avg_score = round(total_score / len(summaries), 2) if summaries else 0
    return {
        "domains": summaries,
        "average_value_score": avg_score,
        "domain_count": len(summaries),
        "generated_at": _utc_now(),
    }
