"""Kingdom health aggregator for PSOP-02."""

from datetime import datetime, timezone
from pathlib import Path


REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
SERVICES_DIR = Path(__file__).resolve().parent.parent / "services"


class HealthAggregationError(Exception):
    pass


def _load_registry():
    path = REGISTRIES_DIR / "KINGDOM_HEALTH_REGISTRY.yaml"
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry):
    path = REGISTRIES_DIR / "KINGDOM_HEALTH_REGISTRY.yaml"
    import yaml
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


HEALTH_MONITORS = {
    "governance_health": "governance_health_monitor",
    "treasury_health": "treasury_status_monitor",
    "agents_health": "agent_status_monitor",
    "capability_health": "capability_health_monitor",
    "knowledge_health": "knowledge_health_monitor",
    "dataset_health": "knowledge_health_monitor",
    "security_health": "security_status_monitor",
    "trading_health": "security_status_monitor",
}


def _import_monitor(name):
    import importlib
    return importlib.import_module(f"services.{name}")


def aggregate_health():
    registry = _load_registry()
    health_domains = registry.get("kingdom_health_registry", {}).get("health_domains", {})
    timestamp = datetime.now(timezone.utc).isoformat()

    status_score_map = {"HEALTHY": 95, "WATCH": 70, "WARNING": 45, "CRITICAL": 15, "INITIALIZED": 100}

    results = {}
    for domain_key, monitor_name in HEALTH_MONITORS.items():
        try:
            monitor = _import_monitor(monitor_name)
            check_methods = [m for m in dir(monitor) if m.startswith("check_") or m.startswith("get_health")]
            if check_methods:
                method = getattr(monitor, check_methods[0])
                result = method() if callable(method) else {"status": "HEALTHY"}
            else:
                result = {"status": "HEALTHY", "score": 100}
        except Exception as e:
            result = {"status": "WARNING", "score": 50, "error": str(e)}

        status = result.get("status", "HEALTHY") if isinstance(result, dict) else "HEALTHY"
        score = result.get("score", status_score_map.get(status, 50)) if isinstance(result, dict) else 100

        if domain_key in health_domains:
            health_domains[domain_key]["status"] = status
            health_domains[domain_key]["score"] = score
            health_domains[domain_key]["last_checked"] = timestamp

        results[domain_key] = {"status": status, "score": score}

    scores = [r["score"] for r in results.values()]
    avg_score = sum(scores) // len(scores) if scores else 0

    status_order = {"HEALTHY": 0, "WATCH": 1, "WARNING": 2, "CRITICAL": 3}
    statuses = [r["status"] for r in results.values()]
    worst = max(statuses, key=lambda s: status_order.get(s, 0))

    registry["kingdom_health_registry"]["health_domains"] = health_domains
    registry["kingdom_health_registry"]["current_overall_status"] = worst
    registry["kingdom_health_registry"]["overall_score"] = avg_score
    registry["kingdom_health_registry"]["last_health_check"] = timestamp
    _save_registry(registry)

    return {
        "timestamp": timestamp,
        "domains": results,
        "overall_status": worst,
        "overall_score": avg_score,
    }
