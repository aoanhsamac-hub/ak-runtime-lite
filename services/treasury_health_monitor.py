"""Treasury health monitor for PSOP-01A."""

import json
from datetime import datetime, timezone
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "treasury"
REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "docs" / "schemas"

HEALTH_STATUSES = ["HEALTHY", "WATCH", "WARNING", "CRITICAL"]


class HealthMonitorError(Exception):
    pass


def _load_data(filename):
    path = DATA_DIR / filename
    return json.loads(path.read_text(encoding="utf-8"))


def _load_registry(registry_name):
    path = REGISTRIES_DIR / registry_name
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry_name, data):
    path = REGISTRIES_DIR / registry_name
    import yaml
    path.write_text(yaml.dump(data, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def check_revenue_health():
    revenue = _load_data("kingdom_revenue.json")
    entries = revenue.get("entries", [])
    total = sum(e.get("amount", 0) for e in entries)
    source_count = len(set(e.get("source") for e in entries))
    entry_count = len(entries)

    if entry_count == 0:
        return {"status": "HEALTHY", "score": 100, "reason": "No revenue data yet (pre-revenue phase)"}
    if total < 0:
        return {"status": "CRITICAL", "score": 0, "reason": "Negative total revenue"}
    if source_count >= 5:
        return {"status": "HEALTHY", "score": 90, "reason": f"Diverse revenue from {source_count} sources"}
    if source_count >= 3:
        return {"status": "WATCH", "score": 70, "reason": f"Moderate revenue diversity, {source_count} sources"}
    return {"status": "WARNING", "score": 50, "reason": f"Low revenue diversity, only {source_count} sources"}


def check_treasury_health():
    nt = _load_data("kingdom_treasury.json")
    rt = _load_data("royal_treasury.json")
    nf = _load_data("kingdom_fund.json")
    nt_entries = len(nt.get("entries", []))
    rt_entries = len(rt.get("entries", []))
    nf_entries = len(nf.get("entries", []))

    total_txns = nt_entries + rt_entries + nf_entries
    if total_txns == 0:
        return {"status": "HEALTHY", "score": 100, "reason": "No treasury transactions yet (pre-operational)"}
    return {"status": "HEALTHY", "score": 85, "reason": f"{total_txns} transactions across treasury accounts"}


def check_budget_health():
    budget = _load_data("kingdom_budget.json")
    entries = budget.get("entries", [])
    if len(entries) == 0:
        return {"status": "HEALTHY", "score": 100, "reason": "No budget data yet (pre-operational)"}

    over_budget = [e for e in entries if e.get("variance", 0) > 10]
    if len(over_budget) == 0:
        return {"status": "HEALTHY", "score": 90, "reason": "All categories within budget"}
    if len(over_budget) <= 2:
        return {"status": "WATCH", "score": 70, "reason": f"{len(over_budget)} categories over budget"}
    return {"status": "WARNING", "score": 50, "reason": f"{len(over_budget)} categories over budget"}


def check_reserve_health():
    sr = _load_data("strategic_reserve.json")
    er = _load_data("emergency_reserve.json")
    sr_entries = len(sr.get("entries", []))
    er_entries = len(er.get("entries", []))

    if sr_entries == 0 and er_entries == 0:
        return {"status": "HEALTHY", "score": 100, "reason": "No reserve activity (pre-operational)"}
    return {"status": "HEALTHY", "score": 85, "reason": f"{sr_entries + er_entries} reserve transactions recorded"}


def check_audit_health():
    revenue = _load_data("kingdom_revenue.json")
    entries = revenue.get("entries", [])

    no_audit = [e for e in entries if not e.get("audit_id")]
    if len(entries) == 0:
        return {"status": "HEALTHY", "score": 100, "reason": "No records to audit (pre-operational)"}
    if len(no_audit) == 0:
        return {"status": "HEALTHY", "score": 95, "reason": "All records have audit trail"}
    ratio = len(no_audit) / len(entries)
    if ratio < 0.1:
        return {"status": "WATCH", "score": 75, "reason": f"{len(no_audit)} records missing audit trail"}
    return {"status": "WARNING", "score": 50, "reason": f"{len(no_audit)}/{len(entries)} records missing audit trail"}


def get_overall_health():
    checks = [
        ("revenue_health", check_revenue_health()),
        ("treasury_health", check_treasury_health()),
        ("budget_health", check_budget_health()),
        ("reserve_health", check_reserve_health()),
        ("audit_health", check_audit_health()),
    ]

    status_order = {"HEALTHY": 0, "WATCH": 1, "WARNING": 2, "CRITICAL": 3}
    worst_status = max((c[1]["status"] for c in checks), key=lambda s: status_order.get(s, 0))
    avg_score = sum(c[1]["score"] for c in checks) // len(checks)

    timestamp = datetime.now(timezone.utc).isoformat()

    registry = _load_registry("TREASURY_HEALTH_REGISTRY.yaml")
    inner = registry.get("treasury_health_registry", registry)
    categories = inner.get("health_categories", {})
    for name, result in checks:
        if name in categories:
            categories[name]["status"] = result["status"]
            categories[name]["score"] = result["score"]
            categories[name]["last_checked"] = timestamp
    inner["current_overall_status"] = worst_status
    inner["last_health_check"] = timestamp
    _save_registry("TREASURY_HEALTH_REGISTRY.yaml", registry)

    return {
        "timestamp": timestamp,
        "categories": dict(checks),
        "overall_status": worst_status,
        "average_score": avg_score,
    }
