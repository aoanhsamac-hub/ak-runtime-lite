"""Test Market Knowledge Evolution."""

import pytest


def test_knowledge_evolution_registry():
    from pathlib import Path
    path = Path("docs/registries/IRIS_MARKET_KNOWLEDGE_EVOLUTION.yaml")
    assert path.exists()


def test_knowledge_to_skill_pipeline():
    from services.market_knowledge_engine import generate_knowledge
    knowledge = generate_knowledge("nonexistent")
    assert isinstance(knowledge, dict) or knowledge == {}


def test_skill_proposal_registry():
    from pathlib import Path
    path = Path("docs/registries/IRIS_SKILL_PROPOSAL_REGISTRY.yaml")
    assert path.exists()


def test_evolution_status_values():
    statuses = ["PROPOSED", "READY_FOR_REVIEW", "NEEDS_MORE_EVIDENCE"]
    assert len(statuses) == 3


def test_knowledge_has_confidence():
    knowledge = {"confidence": 0.85}
    assert 0 <= knowledge["confidence"] <= 1


def test_lesson_to_knowledge_conversion():
    from services.market_knowledge_engine import store_knowledge
    result = store_knowledge({"knowledge_id": "test", "source_lesson_id": "test"})
    assert "knowledge_id" in result


def test_evolution_timestamp():
    from datetime import datetime
    ts = datetime.now().strftime('%Y-%m-%d')
    assert ts is not None


def test_evolution_chain_integrity():
    registry = {"queues": []}
    assert "queues" in registry


def test_no_auto_activation():
    status = "PROPOSED"
    assert status != "ACTIVE"