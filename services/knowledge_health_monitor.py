"""Knowledge health monitor for PSOP-02."""

from pathlib import Path


MEMORY_DIR = Path(__file__).resolve().parent.parent / "memory"
LEARNING_REGISTRY_DIR = MEMORY_DIR / "learning_registry"


def check():
    knowledge_count = 0
    total_registries = 0
    registries_ok = 0

    registry_map = {
        "lesson_registry": MEMORY_DIR / "lesson_registry.py",
        "skill_registry": MEMORY_DIR / "skill_registry.py",
        "capability_registry": MEMORY_DIR / "capability_registry",
        "evidence_registry": MEMORY_DIR / "evidence_registry.py",
        "usage_registry": MEMORY_DIR / "usage_registry.py",
        "adoption_registry": MEMORY_DIR / "adoption_registry.py",
    }

    for name, path in registry_map.items():
        total_registries += 1
        if path.exists():
            registries_ok += 1

    if LEARNING_REGISTRY_DIR.exists():
        total_registries += 1
        schema_dir = LEARNING_REGISTRY_DIR / "schemas"
        if schema_dir.exists():
            registries_ok += 1

    integrity_rate = round(registries_ok / total_registries * 100) if total_registries > 0 else 100

    if integrity_rate == 100:
        status = "HEALTHY"
        detail = f"All {total_registries} knowledge registries present and intact"
    elif integrity_rate >= 75:
        status = "WATCH"
        detail = f"{registries_ok}/{total_registries} knowledge registries present"
    elif integrity_rate >= 50:
        status = "WARNING"
        detail = f"{registries_ok}/{total_registries} knowledge registries present"
    else:
        status = "CRITICAL"
        detail = f"Only {registries_ok}/{total_registries} knowledge registries present"

    return {
        "status": status,
        "score": integrity_rate,
        "detail": detail,
        "registries_ok": registries_ok,
        "total_registries": total_registries,
    }
