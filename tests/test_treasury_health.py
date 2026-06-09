"""Tests for PSOP-01A treasury health monitor."""

from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "treasury"
REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"

from services import treasury_health_monitor as thm


def _reset_all_data():
    for fname in ["kingdom_revenue.json", "kingdom_treasury.json", "royal_treasury.json",
                   "kingdom_fund.json", "kingdom_budget.json",
                   "strategic_reserve.json", "emergency_reserve.json"]:
        path = DATA_DIR / fname
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            data["entries"] = []
            data["status"] = "INITIALIZED"
            data["updated_at"] = None
            path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def setup_function():
    _reset_all_data()


def test_check_revenue_health_empty():
    result = thm.check_revenue_health()
    assert result["status"] == "HEALTHY"
    assert result["score"] == 100


def test_check_treasury_health_empty():
    result = thm.check_treasury_health()
    assert result["status"] == "HEALTHY"


def test_check_budget_health_empty():
    result = thm.check_budget_health()
    assert result["status"] == "HEALTHY"


def test_check_reserve_health_empty():
    result = thm.check_reserve_health()
    assert result["status"] == "HEALTHY"


def test_check_audit_health_empty():
    result = thm.check_audit_health()
    assert result["status"] == "HEALTHY"


def test_all_health_checks_return_valid_status():
    for check in [thm.check_revenue_health, thm.check_treasury_health, thm.check_budget_health,
                   thm.check_reserve_health, thm.check_audit_health]:
        result = check()
        assert result["status"] in thm.HEALTH_STATUSES
        assert 0 <= result["score"] <= 100
        assert "reason" in result


def test_get_overall_health():
    result = thm.get_overall_health()
    assert "timestamp" in result
    assert "categories" in result
    assert "overall_status" in result
    assert "average_score" in result
    assert result["overall_status"] in thm.HEALTH_STATUSES


def test_overall_health_has_5_categories():
    result = thm.get_overall_health()
    assert len(result["categories"]) == 5


def test_overall_health_updates_registry():
    thm.get_overall_health()
    import yaml
    path = REGISTRIES_DIR / "TREASURY_HEALTH_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    inner = registry.get("treasury_health_registry", registry)
    assert inner.get("last_health_check") is not None
    assert inner.get("current_overall_status") in thm.HEALTH_STATUSES


def test_average_score_is_reasonable():
    result = thm.get_overall_health()
    assert 50 <= result["average_score"] <= 100
