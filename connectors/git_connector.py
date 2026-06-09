from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any


class GitConnector:
    def __init__(self, repo_path: str | Path | None = None):
        self.repo_path = Path(repo_path).resolve() if repo_path else Path.cwd()

    def is_available(self) -> bool:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
                timeout=10,
            )
            return result.returncode == 0
        except Exception:
            return False

    def execute(self, action: str, **kwargs: Any) -> dict:
        allowed = {"status", "diff", "log", "branch"}
        if action not in allowed:
            return {"success": False, "error": f"action '{action}' not allowed; use one of: {', '.join(sorted(allowed))}"}
        if action == "status":
            return self.status()
        if action == "diff":
            return self.diff(kwargs.get("path", ""))
        if action == "log":
            return self.log(kwargs.get("count", 10))
        if action == "branch":
            return self.branch()
        return {"success": False, "error": f"unknown action: {action}"}

    def status(self) -> dict:
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
                timeout=10,
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout.strip() if result.returncode == 0 else result.stderr.strip(),
                "dirty": bool(result.stdout.strip()),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def diff(self, path: str = "") -> dict:
        try:
            cmd = ["git", "diff"]
            if path:
                cmd.append(path)
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.repo_path, timeout=10
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout.strip() if result.returncode == 0 else result.stderr.strip(),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def log(self, count: int = 10) -> dict:
        try:
            result = subprocess.run(
                ["git", "log", f"--max-count={count}", "--oneline"],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
                timeout=10,
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout.strip() if result.returncode == 0 else result.stderr.strip(),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def branch(self) -> dict:
        try:
            result = subprocess.run(
                ["git", "branch"],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
                timeout=10,
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout.strip() if result.returncode == 0 else result.stderr.strip(),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
