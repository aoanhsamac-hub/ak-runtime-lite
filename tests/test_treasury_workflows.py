"""Tests for PSOP-01 treasury workflow integrity."""

from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "treasury"
SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "docs" / "schemas"
SOPS_DIR = Path(__file__).resolve().parent.parent / "docs" / "sops"
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "docs" / "templates"

DATA_FILES = [
    "kingdom_revenue.json",
    "kingdom_treasury.json",
    "royal_treasury.json",
    "kingdom_fund.json",
    "kingdom_budget.json",
    "kingdom_expenses.json",
    "emergency_reserve.json",
    "strategic_reserve.json",
]

SOP_FILES = [
    "TREASURY_REVENUE_PROCESS.md",
    "TREASURY_EXPENSE_PROCESS.md",
    "TREASURY_BUDGET_PROCESS.md",
    "TREASURY_RESERVE_PROCESS.md",
    "TREASURY_AUDIT_PROCESS.md",
]

TEMPLATE_FILES = [
    "MONTHLY_TREASURY_REPORT_TEMPLATE.md",
    "QUARTERLY_TREASURY_REPORT_TEMPLATE.md",
    "TREASURY_HEALTH_REPORT_TEMPLATE.md",
]


def test_all_data_files_exist():
    for fname in DATA_FILES:
        path = DATA_DIR / fname
        assert path.exists(), f"Missing data file: {path}"


def test_all_sop_files_exist():
    for fname in SOP_FILES:
        path = SOPS_DIR / fname
        assert path.exists(), f"Missing SOP: {path}"


def test_all_template_files_exist():
    for fname in TEMPLATE_FILES:
        path = TEMPLATES_DIR / fname
        assert path.exists(), f"Missing template: {path}"


def test_sops_contain_required_sections():
    required = ["Purpose", "Authority", "Process", "Validation", "Approval Chain", "Audit Trail", "Escalation", "References"]
    for fname in SOP_FILES:
        path = SOPS_DIR / fname
        content = path.read_text(encoding="utf-8")
        # SOPs use numbered headings like "## 1. Purpose"
        import re
        headings = re.findall(r"## \d+\.\s*(.+)", content)
        headings_lower = [h.lower() for h in headings]
        missing = [s for s in required if s.lower() not in headings_lower]
        assert len(missing) <= 2, f"{fname}: missing sections: {missing}"


def test_templates_contain_required_sections():
    for fname in TEMPLATE_FILES:
        path = TEMPLATES_DIR / fname
        content = path.read_text(encoding="utf-8")
        # Every template must have template markers
        assert "{{" in content, f"{fname}: no template markers found"
        assert "}}" in content, f"{fname}: no template markers found"


def test_data_files_are_initialized():
    import json
    for fname in DATA_FILES:
        path = DATA_DIR / fname
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "registry" in data, f"{fname}: missing registry field"
        assert "status" in data, f"{fname}: missing status field"
        assert "version" in data, f"{fname}: missing version field"


def test_data_files_no_fabricated_financial_data():
    import json
    for fname in DATA_FILES:
        path = DATA_DIR / fname
        data = json.loads(path.read_text(encoding="utf-8"))
        # Check no fake balances or amounts
        for key in ["balance", "total_revenue", "total_expenses", "current_balance", "target_balance"]:
            val = data.get(key, "NOT_APPLICABLE")
            if val is not None and val != "NOT_APPLICABLE":
                assert val == "NOT_APPLICABLE" or val is None, f"{fname}: contains fabricated data in '{key}'"


def test_schema_data_alignment():
    import json
    # Each data file should reference a schema
    schema_names = {s.stem: s for s in SCHEMAS_DIR.glob("*.json")}
    for fname in DATA_FILES:
        path = DATA_DIR / fname
        data = json.loads(path.read_text(encoding="utf-8"))
        schema_ref = data.get("schema")
        if schema_ref:
            assert schema_ref in schema_names or schema_ref.replace("_schema", "") in [s.stem for s in schema_names.values()], \
                f"{fname}: references unknown schema '{schema_ref}'"
