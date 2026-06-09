"""NEURON T3 Fine-tuning Infrastructure Registries - TRAINING_LOCKED."""

from __future__ import annotations

from datetime import datetime, timezone


class DatasetLineageRegistry:
    def __init__(self):
        self._datasets = {}

    def register(self, dataset_id: str, source: str, description: str, owner_agent: str, risk_level: str = "LEVEL_3_SOVEREIGN") -> dict:
        record = {
            "dataset_id": dataset_id,
            "source": source,
            "description": description,
            "owner_agent": owner_agent,
            "risk_level": risk_level,
            "activation_state": "TRAINING_LOCKED",
            "lineage": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._datasets[dataset_id] = record
        return record

    def add_lineage(self, dataset_id: str, parent_id: str) -> None:
        if dataset_id in self._datasets:
            self._datasets[dataset_id]["lineage"].append(parent_id)


class TrainingRegistry:
    def __init__(self):
        self._trainings = {}

    def register(self, training_id: str, dataset_id: str, config: dict, owner_agent: str) -> dict:
        return {"training_id": training_id, "dataset_id": dataset_id, "config": config, "owner_agent": owner_agent, "status": "LOCKED"}


class ModelRegistry:
    def __init__(self):
        self._models = {}

    def register(self, model_id: str, name: str, owner_agent: str, status: str = "OBSERVE_ONLY") -> dict:
        self._models[model_id] = {"model_id": model_id, "name": name, "owner_agent": owner_agent, "status": status}
        return self._models[model_id]


DATASET_LINEAGE = DatasetLineageRegistry()
TRAINING = TrainingRegistry()
MODELS = ModelRegistry()

__all__ = ["DatasetLineageRegistry", "TrainingRegistry", "ModelRegistry", "DATASET_LINEAGE", "TRAINING", "MODELS"]