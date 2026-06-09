"""Credential Validator - Validates credentials before use."""

import re
import os
from typing import Any


class CredentialValidator:
    PLAINTEXT_PATTERNS = [
        r"(?i)token\s*=\s*['\"][a-zA-Z0-9:_-]{30,}['\"]",
        r"(?i)password\s*=\s*['\"][^'\"]{6,}['\"]",
        r"(?i)api_key\s*=\s*['\"][a-zA-Z0-9]{20,}['\"]",
        r"(?i)secret\s*=.*['\"][a-zA-Z0-9+/=]{20,}['\"]",
    ]

    FORBIDDEN_STORAGE = [
        ".env",
        "config.json",
        "settings.py",
        "credentials.txt",
        "secrets.txt",
    ]

    def validate_token_format(self, token: str, token_type: str = "telegram") -> dict:
        if token_type == "telegram":
            parts = token.split(":")
            if len(parts) != 2:
                return {"valid": False, "reason": "Must contain exactly one colon"}
            if not parts[0].isdigit():
                return {"valid": False, "reason": "Prefix must be numeric"}
            if len(parts[1]) < 30:
                return {"valid": False, "reason": "Token suffix too short (< 30 chars)"}
            return {"valid": True}
        if token_type == "api_key":
            if len(token) < 16:
                return {"valid": False, "reason": "API key too short (< 16 chars)"}
            return {"valid": True}
        return {"valid": len(token) > 0, "reason": "Unknown token type"}

    def scan_for_plaintext(self, file_path: str) -> list[dict]:
        findings = []
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                for i, line in enumerate(f, 1):
                    for pattern in self.PLAINTEXT_PATTERNS:
                        if re.search(pattern, line):
                            findings.append({
                                "file": file_path,
                                "line": i,
                                "pattern": pattern[:40],
                                "severity": "HIGH",
                            })
        except Exception:
            pass
        return findings

    def validate_file_permissions(self, file_path: str) -> dict:
        try:
            stat = os.stat(file_path)
            if stat.st_mode & 0o007:
                return {"valid": False, "reason": f"World-readable permissions: {oct(stat.st_mode)}"}
            return {"valid": True}
        except Exception as e:
            return {"valid": False, "reason": str(e)}

    def check_credential_in_code(self, source_paths: list[str]) -> list[dict]:
        all_findings = []
        for fpath in source_paths:
            if any(fname in fpath for fname in self.FORBIDDEN_STORAGE):
                all_findings.extend(self.scan_for_plaintext(fpath))
        return all_findings

    def health(self) -> dict:
        return {
            "plaintext_patterns": len(self.PLAINTEXT_PATTERNS),
            "forbidden_storage": self.FORBIDDEN_STORAGE,
        }
