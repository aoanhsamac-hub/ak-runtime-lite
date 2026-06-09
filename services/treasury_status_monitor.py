"""Treasury status monitor for PSOP-02."""

import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "treasury"
SERVICES_DIR = Path(__file__).resolve().parent.parent / "services"
REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"

TREASURY_DOMAINS = [
    "revenue_health",
    "treasury_health",
    "budget_health",
    "reserve_health",
    "audit_health",
]


def _load_data(filename):
    path = DATA_DIR / filename
    return json.loads(path.read_text(encoding="utf-8"))


def check():
    health_path = REGISTRIES_DIR / "TREASURY_HEALTH_REGISTRY.yaml"
    import yaml
    if health_path.exists():
        registry = yaml.safe_load(health_path.read_text(encoding="utf-8"))
        categories = registry.get("treasury_health_registry", {}).get("health_categories", {})
    else:
        categories = {}

    active_scores = []
    for domain in TREASURY_DOMAINS:
        if domain in categories:
            score = categories[domain].get("score")
            if score is not None:
                active_scores.append(score)

    if active_scores:
        avg_score = sum(active_scores) // len(active_scores)
    else:
        avg_score = 100

    last_check = registry.get("treasury_health_registry", {}).get("last_health_check") if health_path.exists() else None
    overall = registry.get("treasury_health_registry", {}).get("current_overall_status", "INITIALIZED") if health_path.exists() else "INITIALIZED"

    if overall == "INITIALIZED" or overall is None:
        overall = "HEALTHY"

    return {
        "status": overall,
        "score": avg_score,
        "detail": f"{len(active_scores)}/{len(TREASURY_DOMAINS)} treasury domains scored, average {avg_score}/100",
        "domains_active": len(active_scores),
        "domains_total": len(TREASURY_DOMAINS),
        "last_health_check": last_check,
    }
