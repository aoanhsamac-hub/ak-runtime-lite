"""Tests for PSOP-01 treasury schemas."""

import json
from pathlib import Path


SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "docs" / "schemas"
SCHEMA_FILES = [
    "kingdom_revenue_schema.json",
    "kingdom_expense_schema.json",
    "kingdom_budget_schema.json",
    "treasury_transaction_schema.json",
    "reserve_transaction_schema.json",
]

REQUIRED_SCHEMA_FIELDS = ["schema", "version", "description", "required_fields", "fields"]


def test_all_schema_files_exist():
    for fname in SCHEMA_FILES:
        path = SCHEMAS_DIR / fname
        assert path.exists(), f"Missing schema: {path}"


def test_schema_has_required_structure():
    for fname in SCHEMA_FILES:
        path = SCHEMAS_DIR / fname
        schema = json.loads(path.read_text(encoding="utf-8"))
        for field in REQUIRED_SCHEMA_FIELDS:
            assert field in schema, f"{fname}: missing field '{field}'"


def test_schema_required_fields_are_in_fields():
    for fname in SCHEMA_FILES:
        path = SCHEMAS_DIR / fname
        schema = json.loads(path.read_text(encoding="utf-8"))
        for req in schema["required_fields"]:
            assert req in schema["fields"], f"{fname}: required field '{req}' not in fields definition"
            assert "type" in schema["fields"][req], f"{fname}: field '{req}' missing type"


def test_schema_version_format():
    for fname in SCHEMA_FILES:
        path = SCHEMAS_DIR / fname
        schema = json.loads(path.read_text(encoding="utf-8"))
        assert schema["version"].startswith("1."), f"{fname}: version must be 1.x"


def test_all_schemas_have_audit_fields():
    for fname in SCHEMA_FILES:
        path = SCHEMAS_DIR / fname
        schema = json.loads(path.read_text(encoding="utf-8"))
        assert "audit_id" in schema["fields"], f"{fname}: missing audit_id field"
        assert "created_at" in schema["fields"], f"{fname}: missing created_at field"
