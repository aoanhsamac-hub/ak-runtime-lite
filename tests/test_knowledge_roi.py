from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services import knowledge_roi_engine as kre


def test_import_knowledge_roi():
    assert kre is not None
    assert hasattr(kre, "assess_knowledge_roi")
    assert hasattr(kre, "get_knowledge_roi_summary")


def test_assess_knowledge_roi():
    result = kre.assess_knowledge_roi("lesson", usage_count=10, curation_cost=5.0, impact_score=0.8)
    assert result["knowledge_type"] == "lesson"
    assert "roi" in result
    assert "measured_impact" in result
    assert result["cap_level"] <= kre.MAX_CE_LEVEL


def test_knowledge_roi_zero_cost():
    result = kre.assess_knowledge_roi("skill", usage_count=5, curation_cost=0, impact_score=0.5)
    assert result["roi"] == 0.0


def test_assess_no_type_raises():
    import pytest
    with pytest.raises(kre.KnowledgeROIError):
        kre.assess_knowledge_roi("")


def test_get_knowledge_roi_summary():
    result = kre.get_knowledge_roi_summary()
    assert "total_knowledge_items" in result
    assert "knowledge_roi" in result


def test_no_fabricated_knowledge_data():
    result = kre.get_knowledge_roi_summary()
    assert result.get("knowledge_roi", 0) >= 0
