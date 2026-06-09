"""Revenue ingestion service for PSOP-01A."""

import json
from datetime import datetime, timezone
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "treasury"
SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "docs" / "schemas"

VALID_SOURCES = [
    "Trading", "Investment", "Service", "Technology", "Licensing",
    "Consulting", "Education", "Content", "E-Commerce", "Infrastructure", "Other",
]

VALID_CATEGORIES = ["Operating", "Capital", "Extraordinary"]

REVENUE_LIFECYCLE = ["RECORDED", "VERIFIED", "SETTLED", "DISPUTED"]


def _load_schema():
    path = SCHEMAS_DIR / "kingdom_revenue_schema.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _load_revenue_ledger():
    path = DATA_DIR / "kingdom_revenue.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _save_revenue_ledger(ledger):
    path = DATA_DIR / "kingdom_revenue.json"
    path.write_text(json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8")


def _generate_revenue_id(ledger):
    year = datetime.now(timezone.utc).strftime("%Y")
    existing = [e for e in ledger.get("entries", []) if e.get("revenue_id", "").startswith(f"REV-{year}-")]
    seq = len(existing) + 1
    return f"REV-{year}-{seq:04d}"


def _generate_audit_id():
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"AUDIT-REV-{ts}"


class RevenueIngestionError(Exception):
    pass


def validate_source(source):
    if source not in VALID_SOURCES:
        raise RevenueIngestionError(f"Invalid revenue source: {source}. Must be one of {VALID_SOURCES}")


def validate_authority(authority):
    if not authority or not isinstance(authority, str):
        raise RevenueIngestionError("Authority must be a non-empty string")


def validate_amount(amount):
    if not isinstance(amount, (int, float)) or amount <= 0:
        raise RevenueIngestionError(f"Amount must be positive, got {amount}")


def validate_category(category):
    if category not in VALID_CATEGORIES:
        raise RevenueIngestionError(f"Invalid category: {category}. Must be one of {VALID_CATEGORIES}")


def validate_audit_trail(audit_id):
    if not audit_id or not isinstance(audit_id, str):
        raise RevenueIngestionError("Audit ID must be a non-empty string")


def ingest_revenue(source, category, amount, authority, reference=None, description=None):
    schema = _load_schema()
    schema_fields = schema.get("required_fields", [])

    validate_source(source)
    validate_category(category)
    validate_amount(amount)
    validate_authority(authority)

    ledger = _load_revenue_ledger()
    revenue_id = _generate_revenue_id(ledger)
    audit_id = _generate_audit_id()
    timestamp = datetime.now(timezone.utc).isoformat()

    record = {
        "revenue_id": revenue_id,
        "timestamp": timestamp,
        "source": source,
        "category": category,
        "amount": amount,
        "authority": authority,
        "reference": reference or "",
        "description": description or "",
        "status": "RECORDED",
        "audit_id": audit_id,
        "created_at": timestamp,
        "updated_at": None,
    }

    missing = [f for f in schema_fields if f not in record]
    if missing:
        raise RevenueIngestionError(f"Missing required fields: {missing}")

    entries = ledger.get("entries", [])
    entries.append(record)
    ledger["entries"] = entries
    ledger["status"] = "ACTIVE"
    ledger["updated_at"] = timestamp
    _save_revenue_ledger(ledger)

    return record


def get_revenue_count():
    ledger = _load_revenue_ledger()
    return len(ledger.get("entries", []))


def get_revenue_by_status(status):
    ledger = _load_revenue_ledger()
    return [e for e in ledger.get("entries", []) if e.get("status") == status]


def update_revenue_status(revenue_id, new_status, authority):
    if new_status not in REVENUE_LIFECYCLE:
        raise RevenueIngestionError(f"Invalid status: {new_status}. Must be one of {REVENUE_LIFECYCLE}")
    ledger = _load_revenue_ledger()
    for entry in ledger.get("entries", []):
        if entry["revenue_id"] == revenue_id:
            entry["status"] = new_status
            entry["updated_at"] = datetime.now(timezone.utc).isoformat()
            _save_revenue_ledger(ledger)
            return entry
    raise RevenueIngestionError(f"Revenue record {revenue_id} not found")
