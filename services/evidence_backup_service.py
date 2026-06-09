"""Evidence Backup Service - Backs up evidence registries and audit logs."""

from pathlib import Path
from typing import Any
from services.backup_manager import BackupManager


EVIDENCE_PATHS = {
    "audit_log": "D:\\AK\\governance\\audit",
    "evidence_registry": "D:\\AK\\memory\\evidence_registry",
    "adoption_registry": "D:\\AK\\memory\\adoption_registry.py",
    "capability_roi": "D:\\AK\\memory\\capability_roi_registry.py",
}


class EvidenceBackupService:
    def __init__(self, backup_manager: BackupManager | None = None):
        self._manager = backup_manager or BackupManager()
        for name, path in EVIDENCE_PATHS.items():
            p = Path(path)
            if p.exists():
                self._manager.register_target(f"evidence_{name}", str(p))

    def backup_all_evidence(self) -> list[dict]:
        results = []
        for name in list(self._manager._targets.keys()):
            if name.startswith("evidence_"):
                results.append(self._manager.backup(name))
        return results

    def backup_evidence(self, evidence_name: str) -> dict:
        return self._manager.backup(f"evidence_{evidence_name}")

    def list_evidence_backups(self) -> dict:
        return self._manager.list_backups()

    def health(self) -> dict:
        return {"evidence_targets": [k for k in self._manager._targets.keys() if k.startswith("evidence_")]}
