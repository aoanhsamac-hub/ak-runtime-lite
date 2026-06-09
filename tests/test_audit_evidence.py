from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services import audit_evidence_compiler as aec


def test_import_audit_compiler():
    assert aec is not None
    assert hasattr(aec, "compile_treasury_audit")
    assert hasattr(aec, "compile_capability_audit")
    assert hasattr(aec, "compile_program_audit")
    assert hasattr(aec, "compile_governance_audit")
    assert hasattr(aec, "compile_all")


def test_compile_treasury_audit():
    result = aec.compile_treasury_audit()
    assert result["audit_type"] == "Treasury Evidence"
    assert "total_records" in result
    assert "evidence_ids" in result


def test_compile_capability_audit():
    result = aec.compile_capability_audit()
    assert result["audit_type"] == "Capability Evidence"
    assert "usage_records" in result
    assert "value_records" in result
    assert "roi_records" in result
    assert "total_evidence" in result


def test_compile_program_audit():
    result = aec.compile_program_audit()
    assert result["audit_type"] == "Program Evidence"
    assert "total_records" in result


def test_compile_governance_audit():
    result = aec.compile_governance_audit()
    assert result["audit_type"] == "Governance Evidence"
    assert result["all_present"] == True
    assert len(result["findings"]) == 6


def test_compile_all():
    result = aec.compile_all()
    assert "treasury" in result
    assert "capability" in result
    assert "program" in result
    assert "governance" in result
    assert "compiled_at" in result


def test_governance_findings_all_exist():
    result = aec.compile_governance_audit()
    for f in result["findings"]:
        assert f["exists"] == True, f"Registry missing: {f['registry']}"


def test_audit_evidence_index_exists():
    path = Path(__file__).resolve().parent.parent / "docs" / "audit" / "Q1_KINGDOM_AUDIT_EVIDENCE_INDEX.md"
    assert path.exists()


def test_audit_has_compiled_at():
    result = aec.compile_all()
    assert "T" in result["compiled_at"]
