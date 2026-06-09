"""Backup Manager - Automated backup system for AK-RUNTIME-LITE."""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone
from typing import Any


BACKUP_ROOT = Path(__file__).resolve().parent.parent / "data" / "backups"
MAX_BACKUPS = 14


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


class BackupManager:
    def __init__(self, backup_root: str | None = None):
        self._root = Path(backup_root) if backup_root else BACKUP_ROOT
        self._targets: dict[str, Path] = {}

    def register_target(self, name: str, path: str) -> None:
        self._targets[name] = Path(path)

    def backup(self, name: str) -> dict:
        if name not in self._targets:
            return {"status": "ERROR", "reason": f"Unknown target: {name}"}
        src = self._targets[name]
        if not src.exists():
            return {"status": "ERROR", "reason": f"Source not found: {src}"}
        backup_dir = self._root / name / _ts()
        backup_dir.mkdir(parents=True, exist_ok=True)
        try:
            if src.is_file():
                shutil.copy2(src, backup_dir / src.name)
            elif src.is_dir():
                shutil.copytree(src, backup_dir / src.name, dirs_exist_ok=True)
            self._prune_old(name)
            return {"status": "OK", "name": name, "path": str(backup_dir), "timestamp": _ts()}
        except Exception as e:
            return {"status": "ERROR", "reason": str(e)}

    def backup_all(self) -> list[dict]:
        results = []
        for name in self._targets:
            results.append(self.backup(name))
        return results

    def list_backups(self, name: str | None = None) -> dict[str, list[dict]]:
        result = {}
        targets = [name] if name else list(self._targets.keys())
        for t in targets:
            backup_dir = self._root / t
            if backup_dir.exists():
                entries = []
                for d in sorted(backup_dir.iterdir()):
                    if d.is_dir():
                        size = sum(f.stat().st_size for f in d.rglob("*") if f.is_file())
                        entries.append({"path": str(d), "timestamp": d.name, "size_bytes": size})
                result[t] = entries
        return result

    def restore(self, name: str, backup_timestamp: str) -> dict:
        src = self._root / name / backup_timestamp
        if not src.exists():
            return {"status": "ERROR", "reason": f"Backup not found: {src}"}
        if name not in self._targets:
            return {"status": "ERROR", "reason": f"Unknown target: {name}"}
        dest = self._targets[name]
        try:
            if dest.exists():
                if dest.is_dir():
                    shutil.rmtree(dest)
                else:
                    dest.unlink()
            backup_item = list(src.iterdir())[0]
            if backup_item.is_dir():
                shutil.copytree(backup_item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(backup_item, dest)
            return {"status": "OK", "name": name, "restored_from": backup_timestamp}
        except Exception as e:
            return {"status": "ERROR", "reason": str(e)}

    def _prune_old(self, name: str) -> None:
        backup_dir = self._root / name
        if not backup_dir.exists():
            return
        all_backups = sorted([d for d in backup_dir.iterdir() if d.is_dir()])
        while len(all_backups) > MAX_BACKUPS:
            oldest = all_backups.pop(0)
            shutil.rmtree(oldest)

    def health(self) -> dict[str, Any]:
        return {
            "root": str(self._root),
            "targets": list(self._targets.keys()),
            "max_backups": MAX_BACKUPS,
        }
