"""Test NEURON capability backlog registries."""

from memory.capability_backlog import BACKLOG, STATES
from memory.prompt_registry import PROMPTS, PROMPT_VERSIONS, PROMPT_BENCHMARKS
from memory.fine_tuning_registry import DATASET_LINEAGE, TRAINING, MODELS
from memory.dual_brain_registry import FAST_BRAIN, SLOW_BRAIN, ROUTING, ESCALATION


def test_backlog_states_exist():
    assert "ACTIVE" in STATES
    assert "SANDBOX_ONLY" in STATES
    assert "TRAINING_LOCKED" in STATES
    assert "OBSERVE_ONLY" in STATES
    assert "BACKLOG" in STATES
    assert "ARCHIVED" in STATES


def test_backlog_contains_neuron_layers():
    summary = BACKLOG.summary()
    assert summary["total"] >= 0


def test_prompt_registry_exists():
    assert PROMPTS is not None


def test_prompt_version_registry_exists():
    assert PROMPT_VERSIONS is not None


def test_prompt_benchmark_registry_exists():
    assert PROMPT_BENCHMARKS is not None


def test_fine_tuning_registries_exist():
    assert DATASET_LINEAGE is not None
    assert TRAINING is not None
    assert MODELS is not None


def test_dual_brain_registries_exist():
    assert FAST_BRAIN is not None
    assert SLOW_BRAIN is not None
    assert ROUTING is not None
    assert ESCALATION is not None


def test_routing_returns_valid_mode():
    result = ROUTING.route("test prompt", fast_available=True, confidence=0.9)
    assert result["selected_mode"] in ("FAST", "SLOW")