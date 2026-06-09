"""Test Audit Evidence Engine."""

import pytest


def test_import_audit_evidence_engine():
    import services.audit_evidence_engine as aee
    assert hasattr(aee, "consolidate_all_evidence")
    assert hasattr(aee, "update_audit_index")


def test_consolidate_all_evidence():
    from services.audit_evidence_engine import consolidate_all_evidence
    result = consolidate_all_evidence()
    assert isinstance(result, dict)
    assert "evidence_sources" in result


def test_evidence_sources_structure():
    from services.audit_evidence_engine import consolidate_all_evidence
    result = consolidate_all_evidence()
    sources = result.get("evidence_sources", {})
    assert "treasury_evidence" in sources
    assert "trading_evidence" in sources


def test_update_audit_index():
    from services.audit_evidence_engine import update_audit_index
    result = update_audit_index()
    assert "total_evidence" in result


def test_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/KINGDOM_AUDIT_EVIDENCE_INDEX.yaml")
    assert path.exists()


def test_no_duplicate_evidence():
    from services.audit_evidence_engine import consolidate_all_evidence
    result1 = consolidate_all_evidence()
    result2 = consolidate_all_evidence()
    assert result1["total_evidence"] == result2["total_evidence"]


def test_evidence_count_non_negative():
    from services.audit_evidence_engine import consolidate_all_evidence
    result = consolidate_all_evidence()
    for source, count in result["evidence_sources"].items():
        assert count >= 0


def test_timestamp_in_result():
    from services.audit_evidence_engine import consolidate_all_evidence
    result = consolidate_all_evidence()
    assert "timestamp" in result


def test_consolidation_id_format():
    from services.audit_evidence_engine import consolidate_all_evidence
    result = consolidate_all_evidence()
    assert "consolidation_id" in result
    assert "EVID-CONSOL" in result["consolidation_id"]