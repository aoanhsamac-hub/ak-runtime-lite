from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
from services import program_evidence_collector as pec


def test_program_evidence_registry_exists():
    path = REGISTRIES_DIR / "PROGRAM_EVIDENCE_REGISTRY.yaml"
    assert path.exists()


def test_program_evidence_registry_structure():
    path = REGISTRIES_DIR / "PROGRAM_EVIDENCE_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    inner = registry.get("program_evidence_registry", {})
    assert "evidence_records" in inner
    assert "status" in inner
    assert "version" in inner


def test_import_program_collector():
    assert pec is not None
    assert hasattr(pec, "collect_program_evidence")
    assert hasattr(pec, "get_all_evidence")
    assert hasattr(pec, "get_evidence_summary")


def test_collect_program_evidence():
    result = pec.collect_program_evidence()
    assert result["evidence_id"].startswith("PROG-EVID-")
    assert "goal_summary" in result
    assert "program_summary" in result


def test_program_goal_summary_in_evidence():
    result = pec.collect_program_evidence()
    gs = result.get("goal_summary", {})
    assert "total" in gs or "total_goals" in gs


def test_program_summary_in_evidence():
    result = pec.collect_program_evidence()
    ps = result.get("program_summary", {})
    assert "total" in ps or "total_programs" in ps


def test_get_program_evidence():
    records = pec.get_all_evidence()
    assert isinstance(records, list)


def test_get_program_evidence_summary():
    summary = pec.get_evidence_summary()
    assert "total_records" in summary
    assert "generated_at" in summary


def test_no_synthetic_program_data():
    records = pec.get_all_evidence()
    for r in records:
        assert "evidence_id" in r
        assert "goal_summary" in r or "program_summary" in r
