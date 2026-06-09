from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
MAX_CE_LEVEL = 4
CAP_VIOLATION = "PSOP-03 CAP: Capability Economy capped at Level 4."


class KnowledgeROIError(Exception):
    pass


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _get_registry_count(registry_name):
    try:
        import yaml
        path = REGISTRIES_DIR / registry_name
        if not path.exists():
            return 0
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not data:
            return 0
        inner = next(iter(data.values())) if isinstance(data, dict) else data
        if isinstance(inner, dict):
            for key in ["health_domains", "domains", "goals", "programs",
                        "health_categories", "accounts", "transactions"]:
                if key in inner and isinstance(inner[key], (list, dict)):
                    items = inner[key]
                    return len(items) if isinstance(items, list) else len(items.keys())
        return 1
    except Exception:
        return 0


def assess_knowledge_roi(knowledge_type, usage_count=0, curation_cost=0.0, impact_score=0.0):
    if not knowledge_type:
        raise KnowledgeROIError("knowledge_type is required")
    measured_impact = min(usage_count * impact_score, 100)
    roi = round((measured_impact / curation_cost), 4) if curation_cost > 0 else 0.0
    return {
        "knowledge_type": knowledge_type,
        "usage_count": usage_count,
        "curation_cost": curation_cost,
        "impact_score": impact_score,
        "measured_impact": measured_impact,
        "roi": roi,
        "assessed_at": _utc_now(),
        "cap_level": min(3 if roi > 0 else 0, MAX_CE_LEVEL),
    }


def get_knowledge_roi_summary():
    knowledge_registries = [
        ("lesson_registry", "knowledge_registry.yaml", "lessons"),
        ("skill_registry", "knowledge_registry.yaml", "skills"),
        ("capability_registry", "knowledge_registry.yaml", "capabilities"),
        ("evidence_registry", "knowledge_registry.yaml", "evidence"),
    ]
    total_usage = 0
    total_items = 0
    for name, registry_file, key in knowledge_registries:
        count = _get_registry_count(registry_file)
        total_items += count
    roi = round((total_items * 0.5), 4) if total_items > 0 else 0.0
    return {
        "total_knowledge_items": total_items,
        "total_usage": total_usage,
        "knowledge_roi": roi,
        "generated_at": _utc_now(),
    }
