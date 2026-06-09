"""Treasury audit service for PSOP-01A."""

import json
from datetime import datetime, timezone
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "treasury"
REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"

AUDIT_SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
VALID_RECORD_TYPES = ["revenue", "treasury", "allocation", "reporting", "audit"]


class AuditError(Exception):
    pass


def _load_data(filename):
    path = DATA_DIR / filename
    return json.loads(path.read_text(encoding="utf-8"))


def _load_registry(registry_name):
    path = REGISTRIES_DIR / registry_name
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _generate_audit_id():
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"AUDIT-SVC-{ts}"


def validate_revenue_records():
    revenue = _load_data("kingdom_revenue.json")
    entries = revenue.get("entries", [])
    findings = []
    for entry in entries:
        missing = []
        for field in ["revenue_id", "timestamp", "source", "amount", "authority", "status", "audit_id"]:
            if not entry.get(field):
                missing.append(field)
        if missing:
            findings.append({
                "record_id": entry.get("revenue_id", "unknown"),
                "type": "revenue",
                "severity": "HIGH" if "audit_id" in missing else "MEDIUM",
                "issue": f"Missing fields: {missing}",
            })
        if entry.get("amount", 0) <= 0:
            findings.append({
                "record_id": entry.get("revenue_id", "unknown"),
                "type": "revenue",
                "severity": "CRITICAL",
                "issue": "Non-positive amount",
            })
    return findings


def validate_treasury_records():
    treasury = _load_data("kingdom_treasury.json")
    entries = treasury.get("entries", [])
    findings = []
    for entry in entries:
        missing = []
        for field in ["transaction_id", "timestamp", "amount", "transaction_type", "status", "audit_id"]:
            if not entry.get(field):
                missing.append(field)
        if missing:
            findings.append({
                "record_id": entry.get("transaction_id", "unknown"),
                "type": "treasury",
                "severity": "HIGH" if "audit_id" in missing else "MEDIUM",
                "issue": f"Missing fields: {missing}",
            })
    return findings


def validate_allocation_records():
    nt = _load_data("kingdom_treasury.json")
    rt = _load_data("royal_treasury.json")
    findings = []

    alloc_txns = [e for e in nt.get("entries", []) if e.get("transaction_type") == "Allocation"]
    for txn in alloc_txns:
        if txn.get("amount", 0) <= 0:
            findings.append({
                "record_id": txn.get("transaction_id", "unknown"),
                "type": "allocation",
                "severity": "CRITICAL",
                "issue": "Non-positive allocation amount",
            })

    rt_alloc = [e for e in rt.get("entries", []) if e.get("transaction_type") == "Allocation"]
    for txn in rt_alloc:
        if txn.get("amount", 0) <= 0:
            findings.append({
                "record_id": txn.get("transaction_id", "unknown"),
                "type": "allocation",
                "severity": "CRITICAL",
                "issue": "Non-positive allocation amount",
            })

    kingdom_alloc_total = sum(e.get("amount", 0) for e in alloc_txns)
    royal_alloc_total = sum(e.get("amount", 0) for e in rt_alloc)
    if len(alloc_txns) > 0 and len(rt_alloc) > 0:
        total = kingdom_alloc_total + royal_alloc_total
        if total > 0:
            kingdom_pct = round(kingdom_alloc_total / total * 100, 2)
            if abs(kingdom_pct - 92) > 1:
                findings.append({
                    "record_id": "allocation-summary",
                    "type": "allocation",
                    "severity": "HIGH",
                    "issue": f"Kingdom Treasury allocation is {kingdom_pct}%, expected ~92%",
                })

    return findings


def validate_reporting_records():
    registry = _load_registry("TREASURY_REPORT_REGISTRY.yaml")
    report_types = registry.get("report_types", [])
    findings = []
    for rpt in report_types:
        if rpt.get("status") != "TEMPLATE_READY":
            findings.append({
                "record_id": rpt.get("type", "unknown"),
                "type": "reporting",
                "severity": "MEDIUM",
                "issue": f"Report type status is {rpt.get('status')}, expected TEMPLATE_READY",
            })
    return findings


def validate_audit_records():
    revenue = _load_data("kingdom_revenue.json")
    entries = revenue.get("entries", [])
    findings = []
    audit_ids = set()
    for entry in entries:
        aid = entry.get("audit_id")
        if aid:
            if aid in audit_ids:
                findings.append({
                    "record_id": entry.get("revenue_id", "unknown"),
                    "type": "audit",
                    "severity": "HIGH",
                    "issue": f"Duplicate audit_id: {aid}",
                })
            audit_ids.add(aid)
    return findings


def run_full_audit():
    timestamp = datetime.now(timezone.utc).isoformat()
    audit_id = _generate_audit_id()

    all_findings = []
    all_findings.extend(validate_revenue_records())
    all_findings.extend(validate_treasury_records())
    all_findings.extend(validate_allocation_records())
    all_findings.extend(validate_reporting_records())
    all_findings.extend(validate_audit_records())

    critical = [f for f in all_findings if f["severity"] == "CRITICAL"]
    high = [f for f in all_findings if f["severity"] == "HIGH"]

    result = {
        "audit_id": audit_id,
        "timestamp": timestamp,
        "total_findings": len(all_findings),
        "critical_count": len(critical),
        "high_count": len(high),
        "medium_count": len([f for f in all_findings if f["severity"] == "MEDIUM"]),
        "low_count": len([f for f in all_findings if f["severity"] == "LOW"]),
        "findings": all_findings,
        "status": "PASS" if len(critical) == 0 and len(high) == 0 else "FAIL",
    }

    return result
