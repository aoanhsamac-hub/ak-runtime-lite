"""Treasury reporting service for PSOP-01A."""

import json
from datetime import datetime, timezone
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "treasury"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "docs" / "reports"
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "docs" / "templates"
REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
SOPS_DIR = Path(__file__).resolve().parent.parent / "docs" / "sops"


class ReportingError(Exception):
    pass


def _load_data(filename):
    path = DATA_DIR / filename
    return json.loads(path.read_text(encoding="utf-8"))


def _load_template(template_name):
    path = TEMPLATES_DIR / template_name
    return path.read_text(encoding="utf-8")


def _load_registry(registry_name):
    path = REGISTRIES_DIR / registry_name
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _generate_report_id(report_type):
    ts = datetime.now(timezone.utc).strftime("%Y%m%d")
    prefix = report_type[:4].upper()
    return f"RPT-{prefix}-{ts}"


def get_revenue_summary():
    revenue = _load_data("kingdom_revenue.json")
    entries = revenue.get("entries", [])
    total = sum(e.get("amount", 0) for e in entries)
    by_source = {}
    for e in entries:
        source = e.get("source", "Unknown")
        by_source[source] = by_source.get(source, 0) + e.get("amount", 0)
    return {
        "total_revenue": total,
        "entry_count": len(entries),
        "by_source": by_source,
    }


def get_treasury_summary():
    nt = _load_data("kingdom_treasury.json")
    rt = _load_data("royal_treasury.json")
    nf = _load_data("kingdom_fund.json")
    return {
        "kingdom_treasury_entries": len(nt.get("entries", [])),
        "royal_treasury_entries": len(rt.get("entries", [])),
        "kingdom_fund_entries": len(nf.get("entries", [])),
    }


def get_reserve_summary():
    sr = _load_data("strategic_reserve.json")
    er = _load_data("emergency_reserve.json")
    return {
        "strategic_reserve_entries": len(sr.get("entries", [])),
        "emergency_reserve_entries": len(er.get("entries", [])),
    }


def generate_monthly_report(month, year):
    summary = get_revenue_summary()
    treasury = get_treasury_summary()
    reserves = get_reserve_summary()

    report_id = _generate_report_id("MONTHLY")
    timestamp = datetime.now(timezone.utc).isoformat()

    report = {
        "report_id": report_id,
        "report_type": "Monthly Treasury Report",
        "period": f"{year}-{month:02d}",
        "generated_at": timestamp,
        "revenue_summary": summary,
        "treasury_summary": treasury,
        "reserve_summary": reserves,
        "status": "GENERATED",
    }

    return report


def generate_quarterly_report(quarter, year):
    summary = get_revenue_summary()
    treasury = get_treasury_summary()
    reserves = get_reserve_summary()

    report_id = _generate_report_id("QUART")
    timestamp = datetime.now(timezone.utc).isoformat()

    report = {
        "report_id": report_id,
        "report_type": "Quarterly Treasury Report",
        "period": f"{year}-Q{quarter}",
        "generated_at": timestamp,
        "revenue_summary": summary,
        "treasury_summary": treasury,
        "reserve_summary": reserves,
        "status": "GENERATED",
    }

    return report


def generate_health_report():
    health_registry = _load_registry("TREASURY_HEALTH_REGISTRY.yaml")
    inner = health_registry.get("treasury_health_registry", health_registry)
    categories = inner.get("health_categories", {})

    report_id = _generate_report_id("HEALT")
    timestamp = datetime.now(timezone.utc).isoformat()

    health_data = {}
    for cat_name, cat_data in categories.items():
        health_data[cat_name] = {
            "status": cat_data.get("status", "INITIALIZED"),
            "score": cat_data.get("score"),
            "last_checked": cat_data.get("last_checked"),
        }

    report = {
        "report_id": report_id,
        "report_type": "Treasury Health Report",
        "generated_at": timestamp,
        "health_data": health_data,
        "overall_status": inner.get("current_overall_status", "INITIALIZED"),
        "status": "GENERATED",
    }

    return report
