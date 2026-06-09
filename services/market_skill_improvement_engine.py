"""Market Skill Improvement Engine - Create skill proposals from market knowledge."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_registry() -> dict:
    import yaml
    path = REGISTRIES_DIR / "KINGDOM_MARKET_LESSON_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry: dict) -> None:
    import yaml
    path = REGISTRIES_DIR / "KINGDOM_MARKET_LESSON_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_proposal_id() -> str:
    counter = 1
    for lesson in _load_registry().get("kingdom_market_lesson_registry", {}).get("lesson_records", []):
        if lesson.get("skill_proposal"):
            counter += 1
    return f"PROPOSAL-{counter:04d}"


def create_skill_proposal(lesson_id: str) -> dict[str, Any]:
    from services.market_lesson_engine import list_all_lessons

    lessons_yaml = _load_registry().get("kingdom_market_lesson_registry", {})
    lesson = None
    for l in lessons_yaml.get("lesson_records", []):
        if l.get("lesson_id") == lesson_id:
            lesson = l
            break

    if not lesson:
        return {}

    proposal = {
        "proposal_id": _generate_proposal_id(),
        "source_lesson_id": lesson_id,
        "skill_name": f"market_analysis_{lesson.get('lesson_type', 'unknown')}",
        "description": f"Skill derived from {lesson_id}",
        "status": "PROPOSED",
        "created_at": _utc_now(),
        "evidence_rating": lesson.get("confidence", 0.0),
    }

    registry = _load_registry()
    lesson_inner = registry.get("kingdom_market_lesson_registry", {})
    for i, l in enumerate(lesson_inner.get("lesson_records", [])):
        if l.get("lesson_id") == lesson_id:
            lesson_inner["lesson_records"][i]["skill_proposal"] = proposal
            break
    lesson_inner["last_updated"] = _utc_now()
    registry["kingdom_market_lesson_registry"] = lesson_inner
    _save_registry(registry)

    return proposal


def get_skill_proposals_by_status(status: str) -> list[dict]:
    proposals = []
    lesson_inner = _load_registry().get("kingdom_market_lesson_registry", {})
    for lesson in lesson_inner.get("lesson_records", []):
        proposal = lesson.get("skill_proposal")
        if proposal and proposal.get("status") == status:
            proposals.append(proposal)
    return proposals


def count_proposals() -> dict[str, int]:
    counts = {"PROPOSED": 0, "READY_FOR_REVIEW": 0, "NEEDS_MORE_EVIDENCE": 0}
    lesson_inner = _load_registry().get("kingdom_market_lesson_registry", {})
    for lesson in lesson_inner.get("lesson_records", []):
        proposal = lesson.get("skill_proposal")
        if proposal:
            status = proposal.get("status", "PROPOSED")
            counts[status] = counts.get(status, 0) + 1
    return counts


__all__ = ["create_skill_proposal", "get_skill_proposals_by_status", "count_proposals"]