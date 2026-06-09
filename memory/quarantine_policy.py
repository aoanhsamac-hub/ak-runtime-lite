from __future__ import annotations

from typing import Any


REQUIRED_METADATA = {"owner_agent", "reviewer_agent", "source_hash", "status", "version"}


class QuarantinePolicy:
    def evaluate(self, record: dict[str, Any], governance_valid: bool = True) -> dict[str, Any]:
        missing = sorted(key for key in REQUIRED_METADATA if not record.get(key))
        if not governance_valid:
            missing.append("governance_valid")
        if not missing:
            return {"quarantine": False, "missing": [], "record": record}
        quarantined = dict(record)
        quarantined["status"] = "QUARANTINE"
        quarantined["quarantine_reason"] = "missing or invalid: " + ", ".join(missing)
        return {"quarantine": True, "missing": missing, "record": quarantined}

