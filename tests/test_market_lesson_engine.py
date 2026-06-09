"""Test Market Lesson Engine Integration."""

import pytest


def test_lesson_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/IRIS_MARKET_LESSON_REGISTRY.yaml")
    assert path.exists()


def test_knowledge_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/IRIS_MARKET_KNOWLEDGE_REGISTRY.yaml")
    assert path.exists()


def test_skill_proposal_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/IRIS_SKILL_PROPOSAL_REGISTRY.yaml")
    assert path.exists()


def test_lesson_proposal_flow():
    from services.market_lesson_engine import extract_lesson, list_all_lessons
    lessons = list_all_lessons()
    assert isinstance(lessons, list)


def test_knowledge_proposal_flow():
    from services.market_knowledge_engine import generate_knowledge, process_all_pending_lessons
    knowledges = process_all_pending_lessons()
    assert isinstance(knowledges, list)


def test_evolution_queue_exists():
    from pathlib import Path
    path = Path("docs/registries/IRIS_MARKET_KNOWLEDGE_EVOLUTION.yaml")
    assert path.exists()


def test_combined_workflow():
    from services.iris_data_import_engine import validate_dataset
    from services.iris_feature_extraction_engine import extract_features
    result = validate_dataset([], "XAUUSDm", "H1")
    features = extract_features([], "XAUUSDm")
    assert "trend" in features


def test_no_synthetic_lessons():
    from services.market_lesson_engine import extract_lesson
    result = extract_lesson("nonexistent", "nonexistent")
    assert result == {}


def test_lesson_knowledge_chain():
    from services.market_knowledge_engine import generate_knowledge
    knowledge = generate_knowledge("nonexistent")
    assert knowledge == {}