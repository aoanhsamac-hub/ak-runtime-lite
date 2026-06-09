"""Kingdom status aggregator for PSOP-02."""

import json
from datetime import datetime, timezone
from pathlib import Path


REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
SERVICES_DIR = Path(__file__).resolve().parent.parent / "services"

DOMAIN_MONITORS = {
    "governance": "governance_health_monitor",
    "treasury": "treasury_status_monitor",
    "agents": "agent_status_monitor",
    "capabilities": "capability_health_monitor",
    "knowledge": "knowledge_health_monitor",
    "datasets": "knowledge_health_monitor",
    "security": "security_status_monitor",
    "trading": "security_status_monitor",
}


class AggregationError(Exception):
    pass


def _load_registry():
    path = REGISTRIES_DIR / "KINGDOM_STATUS_REGISTRY.yaml"
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry):
    path = REGISTRIES_DIR / "KINGDOM_STATUS_REGISTRY.yaml"
    import yaml
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _import_monitor(name):
    import importlib
    return importlib.import_module(f"services.{name}")


def aggregate_all():
    registry = _load_registry()
    domains = registry.get("kingdom_status_registry", {}).get("domains", {})
    timestamp = datetime.now(timezone.utc).isoformat()

    status_order = {"HEALTHY": 0, "WATCH": 1, "WARNING": 2, "CRITICAL": 3, "INITIALIZED": 0}

    results = {}
    for domain_key, monitor_name in DOMAIN_MONITORS.items():
        try:
            monitor = _import_monitor(monitor_name)
            if hasattr(monitor, "check") and callable(monitor.check):
                result = monitor.check()
            elif hasattr(monitor, "get_status") and callable(monitor.get_status):
                result = monitor.get_status()
            else:
                status_methods = [m for m in dir(monitor) if "status" in m.lower() or "health" in m.lower()]
                if status_methods:
                    method = getattr(monitor, status_methods[0])
                    result = method() if callable(method) else {"status": "HEALTHY", "detail": f"Via {status_methods[0]}"}
                else:
                    result = {"status": "HEALTHY", "detail": f"No status method found on {monitor_name}"}
        except Exception as e:
            result = {"status": "WARNING", "detail": f"Monitor error: {str(e)}", "error": str(e)}

        status = result.get("status", "HEALTHY") if isinstance(result, dict) else "HEALTHY"
        if domain_key in domains:
            domains[domain_key]["status"] = status
            domains[domain_key]["last_updated"] = timestamp
            domains[domain_key]["detail"] = result.get("detail", "") if isinstance(result, dict) else str(result)[:100]
        results[domain_key] = {"status": status, "detail": result.get("detail", "") if isinstance(result, dict) else str(result)[:100]}

    all_statuses = [d.get("status", "HEALTHY") for d in domains.values()]
    worst = max(all_statuses, key=lambda s: status_order.get(s, 0)) if all_statuses else "HEALTHY"

    registry["kingdom_status_registry"]["domains"] = domains
    registry["kingdom_status_registry"]["overall_status"] = worst
    registry["kingdom_status_registry"]["last_aggregated"] = timestamp
    _save_registry(registry)

    return {
        "timestamp": timestamp,
        "domains": results,
        "overall_status": worst,
    }
