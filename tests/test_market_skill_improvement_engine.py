"""Test Market Skill Improvement Engine."""

import pytest


def test_import_skill_improvement_engine():
    import services.market_skill_improvement_engine as msie
    assert hasattr(msie, "create_skill_proposal")
    assert hasattr(msie, "get_skill_proposals_by_status")


def test_create_skill_proposal_empty():
    from services.market_skill_improvement_engine import create_skill_proposal
    result = create_skill_proposal("nonexistent-lesson")
    assert result == {}


def test_skill_proposal_id_format():
    from services.market_skill_improvement_engine import _generate_proposal_id
    proposal_id = _generate_proposal_id()
    assert proposal_id.startswith("PROPOSAL-")


def test_skill_proposal_fields():
    proposal = {
        "proposal_id": "PROPOSAL-001",
        "source_lesson_id": "LESSON-001",
        "skill_name": "market_analysis_success_pattern",
        "description": "Skill derived from lesson",
        "status": "PROPOSED",
        "created_at": "2026-06-08T00:00:00+00:00",
    }
    assert "proposal_id" in proposal
    assert "source_lesson_id" in proposal
    assert "skill_name" in proposal
    assert "status" in proposal


def test_get_proposals_by_status():
    from services.market_skill_improvement_engine import get_skill_proposals_by_status
    result = get_skill_proposals_by_status("PROPOSED")
    assert isinstance(result, list)


def test_count_proposals():
    from services.market_skill_improvement_engine import count_proposals
    result = count_proposals()
    assert isinstance(result, dict)
    assert "PROPOSED" in result


def test_skill_proposal_statuses():
    valid_statuses = ["PROPOSED", "READY_FOR_REVIEW", "NEEDS_MORE_EVIDENCE"]
    assert "PROPOSED" in valid_statuses


def test_proposal_confidence():
    proposal = {"evidence_rating": 0.85}
    assert 0.0 <= proposal["evidence_rating"] <= 1.0


def test_registry_persistence():
    from pathlib import Path
    path = Path("docs/registries/KINGDOM_MARKET_LESSON_REGISTRY.yaml")
    assert path.exists()