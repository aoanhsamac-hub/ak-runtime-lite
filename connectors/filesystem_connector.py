from __future__ import annotations

import os
from pathlib import Path
from typing import Any


BLOCKED_PATTERNS = (
    ".env",
    "credentials",
    "secrets",
    "sovereign/constitution",
    "sovereign/state_corpus",
    "governance/risk_kernel",
    "execution",
)


class FilesystemConnector:
    def __init__(self, base_path: str | Path | None = None):
        self.base_path = Path(base_path).resolve() if base_path else Path.cwd()

    def is_available(self) -> bool:
        return self.base_path.exists()

    def execute(self, action: str, path: str, content: str = "", **kwargs: Any) -> dict:
        if action == "read":
            return self.read(path)
        if action == "write":
            return self.write(path, content)
        if action == "list":
            return self.list_dir(path)
        if action == "exists":
            return {"success": True, "exists": self._resolve(path).exists(), "path": path}
        return {"success": False, "error": f"unsupported action: {action}"}

    def read(self, path: str) -> dict:
        resolved = self._resolve(path)
        if self._is_blocked(resolved):
            return {"success": False, "error": "access blocked: path is protected", "path": path}
        try:
            content = resolved.read_text(encoding="utf-8")
            return {"success": True, "content": content, "path": str(resolved)}
        except FileNotFoundError:
            return {"success": False, "error": f"file not found: {resolved}", "path": path}
        except Exception as e:
            return {"success": False, "error": str(e), "path": path}

    def write(self, path: str, content: str) -> dict:
        resolved = self._resolve(path)
        if self._is_blocked(resolved):
            return {"success": False, "error": "access blocked: path is protected", "path": path}
        if resolved.exists() and not resolved.is_file():
            return {"success": False, "error": "cannot write to existing directory", "path": path}
        try:
            resolved.parent.mkdir(parents=True, exist_ok=True)
            resolved.write_text(content, encoding="utf-8")
            return {"success": True, "path": str(resolved), "bytes": len(content.encode("utf-8"))}
        except Exception as e:
            return {"success": False, "error": str(e), "path": path}

    def list_dir(self, path: str) -> dict:
        resolved = self._resolve(path)
        if not resolved.exists():
            return {"success": False, "error": f"path not found: {resolved}", "path": path}
        if not resolved.is_dir():
            return {"success": False, "error": f"not a directory: {resolved}", "path": path}
        try:
            entries = sorted(
                [str(p.relative_to(self.base_path)) for p in resolved.iterdir()]
            )
            return {"success": True, "entries": entries, "path": str(resolved)}
        except Exception as e:
            return {"success": False, "error": str(e), "path": path}

    def _resolve(self, path: str) -> Path:
        p = Path(path)
        if p.is_absolute():
            return p.resolve()
        return (self.base_path / p).resolve()

    def _is_blocked(self, resolved: Path) -> bool:
        try:
            rel = str(resolved.relative_to(self.base_path)).replace("\\", "/").lower()
            for pattern in BLOCKED_PATTERNS:
                if rel == pattern or rel.startswith(pattern + "/") or rel.startswith(pattern + "\\"):
                    return True
            return False
        except ValueError:
            return True
