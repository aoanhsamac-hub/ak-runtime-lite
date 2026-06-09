"""Test Iris Data Import."""

import pytest


def test_import_data_engine():
    import services.iris_data_import_engine as die
    assert hasattr(die, "validate_dataset")


def test_validate_empty_dataset():
    from services.iris_data_import_engine import validate_dataset
    result = validate_dataset([], "XAUUSDm", "H1")
    assert result["is_valid"] == False


def test_validate_timestamps():
    from datetime import datetime
    from services.iris_data_import_engine import _utc_now
    ts = _utc_now()
    assert "T" in ts


def test_dataset_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/IRIS_DATASET_REGISTRY.yaml")
    assert path.exists()


def test_quality_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/IRIS_DATA_QUALITY_REGISTRY.yaml")
    assert path.exists()


def test_dataset_id_format():
    from services.iris_data_import_engine import _generate_dataset_id
    ds_id = _generate_dataset_id("XAUUSDm", "H1")
    assert "IRIS-DATASET" in ds_id


def test_features_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/IRIS_FEATURE_REGISTRY.yaml")
    assert path.exists()


def test_patterns_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/IRIS_PATTERN_REGISTRY.yaml")
    assert path.exists()


def test_benchmark_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/IRIS_FORECAST_BENCHMARK_REGISTRY.yaml")
    assert path.exists()


def test_market_lesson_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/IRIS_MARKET_LESSON_REGISTRY.yaml")
    assert path.exists()


def test_market_knowledge_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/IRIS_MARKET_KNOWLEDGE_REGISTRY.yaml")
    assert path.exists()


def test_skill_proposal_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/IRIS_SKILL_PROPOSAL_REGISTRY.yaml")
    assert path.exists()


def test_scorecard_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/IRIS_INTELLIGENCE_SCORECARD.yaml")
    assert path.exists()


def test_evolution_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/IRIS_MARKET_KNOWLEDGE_EVOLUTION.yaml")
    assert path.exists()