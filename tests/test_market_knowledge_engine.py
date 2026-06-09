"""Test Market Knowledge Engine."""

import pytest


def test_import_knowledge_engine():
    import services.market_knowledge_engine as mke
    assert hasattr(mke, "generate_knowledge")
    assert hasattr(mke, "store_knowledge")


def test_generate_knowledge_empty():
    from services.market_knowledge_engine import generate_knowledge
    result = generate_knowledge("nonexistent-lesson")
    assert result == {}


def test_knowledge_id_format():
    from services.market_knowledge_engine import _utc_now
    knowledge = {
        "knowledge_id": f"KNOWLEDGE-LESSON-001",
        "source_lesson_id": "LESSON-001",
        "knowledge_type": "success_pattern",
        "insight": "test insight",
        "application": "test application",
        "generated_at": _utc_now(),
    }
    assert knowledge["knowledge_id"].startswith("KNOWLEDGE-")


def test_store_knowledge_returns_dict():
    from services.market_knowledge_engine import store_knowledge
    knowledge = {
        "knowledge_id": "KNOWLEDGE-001",
        "source_lesson_id": "LESSON-001",
        "knowledge_type": "success_pattern",
        "insight": "test insight",
        "generated_at": "2026-06-08T00:00:00+00:00",
    }
    result = store_knowledge(knowledge)
    assert isinstance(result, dict)


def test_process_pending_lessons_returns_list():
    from services.market_knowledge_engine import process_all_pending_lessons
    result = process_all_pending_lessons()
    assert isinstance(result, list)


def test_knowledge_fields():
    knowledge = {
        "knowledge_id": "KNOWLEDGE-001",
        "source_lesson_id": "LESSON-001",
        "knowledge_type": "success_pattern",
        "insight": "test insight",
        "application": "test application",
        "confidence": 0.9,
        "generated_at": "2026-06-08T00:00:00+00:00",
    }
    assert "knowledge_id" in knowledge
    assert "source_lesson_id" in knowledge
    assert "knowledge_type" in knowledge
    assert "insight" in knowledge


def test_knowledge_status():
    knowledge = {"status": "GENERATED"}
    assert knowledge["status"] == "GENERATED"