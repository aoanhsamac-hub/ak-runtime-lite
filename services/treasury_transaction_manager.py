"""Treasury transaction manager for PSOP-01A."""

import json
from datetime import datetime, timezone
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "treasury"

TXN_LIFECYCLE = ["PROPOSED", "VALIDATED", "APPROVED", "RECORDED", "AUDITED"]

VALID_TRANSACTION_TYPES = [
    "Allocation", "Transfer", "Withdrawal", "Deposit",
    "SurplusDistribution", "EmergencyDrawdown",
]

VALID_ACCOUNTS = [
    "KingdomTreasury", "RoyalTreasury", "KingdomFund",
    "StrategicReserve", "EmergencyReserve", "BudgetAccount",
]


class TransactionError(Exception):
    pass


def _generate_txn_id(existing_ids):
    year = datetime.now(timezone.utc).strftime("%Y")
    existing = [i for i in existing_ids if i.startswith(f"TXN-{year}-")]
    seq = len(existing) + 1
    return f"TXN-{year}-{seq:04d}"


def _generate_audit_id():
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"AUDIT-TXN-{ts}"


def _load_registry():
    path = Path(__file__).resolve().parent.parent / "docs" / "registries" / "TREASURY_TRANSACTION_STATUS_REGISTRY.yaml"
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry):
    path = Path(__file__).resolve().parent.parent / "docs" / "registries" / "TREASURY_TRANSACTION_STATUS_REGISTRY.yaml"
    import yaml
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def create_transaction(from_account, to_account, amount, transaction_type, authority, reference=None, description=None):
    if from_account not in VALID_ACCOUNTS:
        raise TransactionError(f"Invalid from_account: {from_account}")
    if to_account not in VALID_ACCOUNTS:
        raise TransactionError(f"Invalid to_account: {to_account}")
    if transaction_type not in VALID_TRANSACTION_TYPES:
        raise TransactionError(f"Invalid transaction_type: {transaction_type}")
    if not isinstance(amount, (int, float)) or amount <= 0:
        raise TransactionError(f"Amount must be positive, got {amount}")
    if not authority or not isinstance(authority, str):
        raise TransactionError("Authority must be a non-empty string")

    timestamp = datetime.now(timezone.utc).isoformat()
    audit_id = _generate_audit_id()

    registry = _load_registry()
    transactions = registry.get("treasury_transaction_status_registry", {}).get("transactions", [])
    existing_ids = [t["transaction_id"] for t in transactions]
    txn_id = _generate_txn_id(existing_ids)

    record = {
        "transaction_id": txn_id,
        "timestamp": timestamp,
        "from_account": from_account,
        "to_account": to_account,
        "amount": amount,
        "transaction_type": transaction_type,
        "reference": reference or "",
        "authority": authority,
        "approval_chain": [authority],
        "description": description or "",
        "status": "PROPOSED",
        "audit_id": audit_id,
        "created_at": timestamp,
        "updated_at": None,
    }

    transactions.append(record)
    registry["treasury_transaction_status_registry"]["transactions"] = transactions
    registry["treasury_transaction_status_registry"]["current_transactions"] = len(transactions)
    registry["treasury_transaction_status_registry"]["last_transaction_id"] = txn_id
    registry["treasury_transaction_status_registry"]["last_transaction_date"] = timestamp
    _save_registry(registry)

    return record


def validate_transaction(txn_id):
    registry = _load_registry()
    transactions = registry.get("treasury_transaction_status_registry", {}).get("transactions", [])
    for txn in transactions:
        if txn["transaction_id"] == txn_id:
            if txn["status"] != "PROPOSED":
                raise TransactionError(f"Cannot validate transaction {txn_id}: status is {txn['status']}")
            txn["status"] = "VALIDATED"
            txn["updated_at"] = datetime.now(timezone.utc).isoformat()
            _save_registry(registry)
            return txn
    raise TransactionError(f"Transaction {txn_id} not found")


def approve_transaction(txn_id, approver):
    registry = _load_registry()
    transactions = registry.get("treasury_transaction_status_registry", {}).get("transactions", [])
    for txn in transactions:
        if txn["transaction_id"] == txn_id:
            if txn["status"] != "VALIDATED":
                raise TransactionError(f"Cannot approve transaction {txn_id}: status is {txn['status']}")
            txn["status"] = "APPROVED"
            txn["approval_chain"] = txn.get("approval_chain", []) + [approver]
            txn["updated_at"] = datetime.now(timezone.utc).isoformat()
            _save_registry(registry)
            return txn
    raise TransactionError(f"Transaction {txn_id} not found")


def complete_transaction(txn_id, recorder):
    registry = _load_registry()
    transactions = registry.get("treasury_transaction_status_registry", {}).get("transactions", [])
    for txn in transactions:
        if txn["transaction_id"] == txn_id:
            if txn["status"] != "APPROVED":
                raise TransactionError(f"Cannot complete transaction {txn_id}: status is {txn['status']}")
            txn["status"] = "RECORDED"
            txn["approval_chain"] = txn.get("approval_chain", []) + [recorder]
            txn["updated_at"] = datetime.now(timezone.utc).isoformat()
            _save_registry(registry)
            return txn
    raise TransactionError(f"Transaction {txn_id} not found")


def audit_transaction(txn_id, auditor):
    registry = _load_registry()
    transactions = registry.get("treasury_transaction_status_registry", {}).get("transactions", [])
    for txn in transactions:
        if txn["transaction_id"] == txn_id:
            if txn["status"] != "RECORDED":
                raise TransactionError(f"Cannot audit transaction {txn_id}: status is {txn['status']}")
            txn["status"] = "AUDITED"
            txn["approval_chain"] = txn.get("approval_chain", []) + [auditor]
            txn["updated_at"] = datetime.now(timezone.utc).isoformat()
            _save_registry(registry)
            return txn
    raise TransactionError(f"Transaction {txn_id} not found")


def get_transaction(txn_id):
    registry = _load_registry()
    transactions = registry.get("treasury_transaction_status_registry", {}).get("transactions", [])
    for txn in transactions:
        if txn["transaction_id"] == txn_id:
            return txn
    raise TransactionError(f"Transaction {txn_id} not found")


def list_transactions_by_status(status):
    registry = _load_registry()
    transactions = registry.get("treasury_transaction_status_registry", {}).get("transactions", [])
    return [t for t in transactions if t.get("status") == status]
