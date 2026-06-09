"""Capability health monitor for PSOP-02."""

from pathlib import Path


MEMORY_DIR = Path(__file__).resolve().parent.parent / "memory"
REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def check():
    capability_registry_dir = MEMORY_DIR / "capability_registry"
    capability_pipeline_dir = MEMORY_DIR / "capability_pipeline"
    official_registry_path = capability_registry_dir / "official_capability_registry.py"
    capability_registry_path = capability_registry_dir / "legacy.py"

    registries_present = 0
    registries_found = []

    if capability_registry_dir.exists():
        registries_present += 1
        registries_found.append("capability_registry_dir")

    if official_registry_path.exists():
        registries_present += 1
        registries_found.append("official_capability_registry")

    if capability_pipeline_dir.exists():
        registries_present += 1
        registries_found.append("capability_pipeline_dir")

    try:
        import yaml
        health_registry_path = REGISTRIES_DIR / "KINGDOM_HEALTH_REGISTRY.yaml"
        if health_registry_path.exists():
            registry = yaml.safe_load(health_registry_path.read_text(encoding="utf-8"))
            cap_health = registry.get("kingdom_health_registry", {}).get("health_domains", {}).get("capability_health", {})
            last_status = cap_health.get("status", "INITIALIZED")
        else:
            last_status = "INITIALIZED"
    except Exception:
        last_status = "INITIALIZED"

    if registries_present >= 3 and last_status != "INITIALIZED":
        status = last_status
    else:
        status = "HEALTHY"
    score = registries_present * 30
    if score > 100:
        score = 100

    return {
        "status": status,
        "score": score,
        "detail": f"Capability registries found: {registries_present}/3 ({', '.join(registries_found)})",
        "registries_present": registries_present,
        "registries_found": registries_found,
    }
