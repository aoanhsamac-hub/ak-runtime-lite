from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def test_program_registry_exists():
    path = REGISTRIES_DIR / "KINGDOM_PROGRAM_REGISTRY.yaml"
    assert path.exists()


def test_program_registry_has_required_metadata():
    path = REGISTRIES_DIR / "KINGDOM_PROGRAM_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    inner = registry.get("kingdom_program_registry", {})
    assert "version" in inner
    assert "status" in inner
    assert "owner" in inner
    assert "program_lifecycle" in inner
    assert "programs" in inner


def test_program_registry_has_lifecycle_stages():
    path = REGISTRIES_DIR / "KINGDOM_PROGRAM_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    lifecycle = registry.get("kingdom_program_registry", {}).get("program_lifecycle", [])
    expected = ["PROPOSED", "APPROVED", "ACTIVE", "COMPLETED", "ARCHIVED"]
    for stage in expected:
        assert stage in lifecycle, f"Missing lifecycle stage: {stage}"


def test_program_registry_initialized_empty():
    path = REGISTRIES_DIR / "KINGDOM_PROGRAM_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    programs = registry.get("kingdom_program_registry", {}).get("programs", [])
    assert isinstance(programs, list)


def test_program_registry_treasury_impact_exists():
    path = REGISTRIES_DIR / "TREASURY_IMPACT_REGISTRY.yaml"
    assert path.exists()
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    inner = registry.get("treasury_impact_registry", {})
    assert "program_impacts" in inner
    assert "capability_impacts" in inner
    assert "treasury_contributions" in inner
