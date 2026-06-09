"""Registry Backup Service - Backs up YAML/JSON registries."""

import json
from pathlib import Path
from typing import Any
from services.backup_manager import BackupManager


REGISTRY_PATHS = {
    "sovereign": "D:\\AK\\sovereign\\registries",
    "docs": "D:\\AK\\docs\\registries",
    "governance": "D:\\AK\\governance\\registries",
}


class RegistryBackupService:
    def __init__(self, backup_manager: BackupManager | None = None):
        self._manager = backup_manager or BackupManager()
        for name, path in REGISTRY_PATHS.items():
            p = Path(path)
            if p.exists():
                self._manager.register_target(f"registry_{name}", str(p))

    def backup_all_registries(self) -> list[dict]:
        results = []
        for name in list(self._manager._targets.keys()):
            if name.startswith("registry_"):
                results.append(self._manager.backup(name))
        return results

    def backup_registry(self, registry_name: str) -> dict:
        return self._manager.backup(f"registry_{registry_name}")

    def list_registry_backups(self) -> dict:
        return self._manager.list_backups()

    def health(self) -> dict:
        return {"registry_targets": [k for k in self._manager._targets.keys() if k.startswith("registry_")]}
