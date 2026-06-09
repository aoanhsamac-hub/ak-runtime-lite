"""Treasury allocation engine for PSOP-01A."""

import json
from datetime import datetime, timezone
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "treasury"
SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "docs" / "schemas"

KINGDOM_TREASURY_SHARE = 0.92
ROYAL_TREASURY_SHARE = 0.08


class AllocationError(Exception):
    pass


def _load_data(filename):
    path = DATA_DIR / filename
    return json.loads(path.read_text(encoding="utf-8"))


def _save_data(filename, data):
    path = DATA_DIR / filename
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _generate_transaction_id(existing_txns):
    year = datetime.now(timezone.utc).strftime("%Y")
    existing = [t for t in existing_txns if t.get("transaction_id", "").startswith(f"TXN-{year}-")]
    seq = len(existing) + 1
    return f"TXN-{year}-{seq:04d}"


def _generate_audit_id():
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"AUDIT-ALLOC-{ts}"


def validate_revenue_amount(amount):
    if not isinstance(amount, (int, float)) or amount <= 0:
        raise AllocationError(f"Revenue amount must be positive, got {amount}")


def allocate(revenue_amount, revenue_id, authority):
    validate_revenue_amount(revenue_amount)

    kingdom_amount = round(revenue_amount * KINGDOM_TREASURY_SHARE, 2)
    royal_amount = round(revenue_amount * ROYAL_TREASURY_SHARE, 2)
    remainder = round(revenue_amount - kingdom_amount - royal_amount, 2)
    if remainder != 0:
        kingdom_amount += remainder

    timestamp = datetime.now(timezone.utc).isoformat()
    audit_id = _generate_audit_id()

    kingdom_treasury = _load_data("kingdom_treasury.json")
    royal_treasury = _load_data("royal_treasury.json")

    kingdom_txn_id = _generate_transaction_id(kingdom_treasury.get("entries", []))
    royal_txn_id = _generate_transaction_id(royal_treasury.get("entries", []))

    kingdom_txn = {
        "transaction_id": kingdom_txn_id,
        "timestamp": timestamp,
        "from_account": "RevenueIngestion",
        "to_account": "KingdomTreasury",
        "amount": kingdom_amount,
        "transaction_type": "Allocation",
        "reference": revenue_id,
        "authority": authority,
        "approval_chain": [authority],
        "description": f"92% allocation from revenue {revenue_id}",
        "status": "COMPLETED",
        "audit_id": audit_id,
        "created_at": timestamp,
        "updated_at": None,
    }

    royal_txn = {
        "transaction_id": royal_txn_id,
        "timestamp": timestamp,
        "from_account": "RevenueIngestion",
        "to_account": "RoyalTreasury",
        "amount": royal_amount,
        "transaction_type": "Allocation",
        "reference": revenue_id,
        "authority": authority,
        "approval_chain": [authority],
        "description": f"8% allocation from revenue {revenue_id}",
        "status": "COMPLETED",
        "audit_id": audit_id,
        "created_at": timestamp,
        "updated_at": None,
    }

    n_entries = kingdom_treasury.get("entries", [])
    n_entries.append(kingdom_txn)
    kingdom_treasury["entries"] = n_entries
    kingdom_treasury["status"] = "ACTIVE"
    kingdom_treasury["updated_at"] = timestamp
    _save_data("kingdom_treasury.json", kingdom_treasury)

    r_entries = royal_treasury.get("entries", [])
    r_entries.append(royal_txn)
    royal_treasury["entries"] = r_entries
    royal_treasury["status"] = "ACTIVE"
    royal_treasury["updated_at"] = timestamp
    _save_data("royal_treasury.json", royal_treasury)

    return {
        "audit_id": audit_id,
        "kingdom_treasury": kingdom_txn,
        "royal_treasury": royal_txn,
        "allocation_breakdown": {
            "total_revenue": revenue_amount,
            "kingdom_treasury_92": kingdom_amount,
            "royal_treasury_8": royal_amount,
        },
    }


def get_allocation_count():
    nt = _load_data("kingdom_treasury.json")
    return len(nt.get("entries", []))


def get_allocation_history():
    nt = _load_data("kingdom_treasury.json")
    rt = _load_data("royal_treasury.json")
    return {
        "kingdom_treasury_entries": nt.get("entries", []),
        "royal_treasury_entries": rt.get("entries", []),
    }
