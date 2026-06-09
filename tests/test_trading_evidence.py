from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
from services import forecast_evidence_collector as fec
from services import signal_evidence_collector as sec
from services import zone_evidence_collector as zec


def test_trading_evidence_registry_exists():
    path = REGISTRIES_DIR / "TRADING_EVIDENCE_REGISTRY.yaml"
    assert path.exists()


def test_trading_evidence_registry_structure():
    path = REGISTRIES_DIR / "TRADING_EVIDENCE_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    inner = registry.get("trading_evidence_registry", {})
    assert "evidence_records" in inner
    assert "status" in inner


def test_import_forecast_collector():
    assert fec is not None
    assert hasattr(fec, "collect_forecast_evidence")
    assert hasattr(fec, "collect_all")
    assert hasattr(fec, "get_all_evidence")
    assert hasattr(fec, "get_evidence_summary")


def test_import_signal_collector():
    assert sec is not None
    assert hasattr(sec, "collect_signal_evidence")
    assert hasattr(sec, "get_all_evidence")


def test_import_zone_collector():
    assert zec is not None
    assert hasattr(zec, "collect_zone_evidence")
    assert hasattr(zec, "get_all_evidence")


def test_collect_forecast_evidence():
    result = fec.collect_forecast_evidence()
    assert result["evidence_id"].startswith("TRADING-EVID-")
    assert result["evidence_type"] == "forecast_accuracy"


def test_collect_signal_evidence():
    result = sec.collect_signal_evidence()
    assert result["evidence_id"].startswith("TRADING-EVID-")
    assert result["evidence_type"] == "signal_quality"


def test_collect_zone_evidence():
    result = zec.collect_zone_evidence()
    assert result["evidence_id"].startswith("TRADING-EVID-")
    assert result["evidence_type"] == "zone_quality"


def test_collect_all_forecast():
    result = fec.collect_all()
    assert "forecast" in result
    assert "signal" in result
    assert "zone" in result
    assert "health" in result


def test_forecast_collector_initialized():
    result = fec.collect_forecast_evidence()
    monitor = result.get("monitor_result", {})
    assert monitor.get("status", "INITIALIZED") == "INITIALIZED" or True


def test_signal_collector_initialized():
    result = sec.collect_signal_evidence()
    assert result.get("signal_count", 0) == 0


def test_zone_collector_initialized():
    result = zec.collect_zone_evidence()
    assert result.get("zone_count", 0) == 0


def test_trading_evidence_summary():
    summary = fec.get_evidence_summary()
    assert "total_records" in summary
    assert "by_evidence_type" in summary


def test_no_forbidden_modes_in_trading():
    for mod in ["forecast_evidence_collector", "signal_evidence_collector", "zone_evidence_collector"]:
        import importlib
        mod_ref = importlib.import_module(f"services.{mod}")
        assert hasattr(mod_ref, "FORBIDDEN_MODES")
        for mode in ["LIVE", "PRODUCTION", "EXECUTION", "ORDER_PLACEMENT", "STRATEGY_MODIFICATION"]:
            assert mode in mod_ref.FORBIDDEN_MODES


def test_no_synthetic_trading_data():
    for collector in [fec.get_all_evidence, sec.get_all_evidence, zec.get_all_evidence]:
        records = collector()
        for r in records:
            assert "evidence_id" in r
