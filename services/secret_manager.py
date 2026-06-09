"""Secret Manager - Secure credential storage for AK-RUNTIME-LITE."""

import os
import json
import base64
import hashlib
from pathlib import Path
from typing import Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


SECRETS_DIR = Path(__file__).resolve().parent.parent / "data" / "secrets"
ENCRYPTED_FILE = SECRETS_DIR / "secrets.enc"
SALT_FILE = SECRETS_DIR / ".salt"


def _derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600000)
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))


def _load_or_create_salt() -> bytes:
    if SALT_FILE.exists():
        return SALT_FILE.read_bytes()
    SECRETS_DIR.mkdir(parents=True, exist_ok=True)
    salt = os.urandom(16)
    SALT_FILE.write_bytes(salt)
    return salt


REQUIRED_SECRETS = {
    "TELEGRAM_BOT_TOKEN": "Telegram bot token for command gateway",
    "TELEGRAM_WHITELIST": "Comma-separated Telegram user IDs",
    "MT5_LOGIN": "MT5 account login",
    "MT5_PASSWORD": "MT5 account password",
    "MT5_SERVER": "MT5 server name",
    "ROUTER9_API_KEY": "9router API key for LLM routing",
    "TAILSCALE_AUTH_KEY": "Tailscale auth key (if needed)",
}


class SecretManager:
    def __init__(self, master_password: str | None = None):
        self._master = master_password or os.environ.get("AK_MASTER_SECRET", "")
        self._secrets: dict[str, str] = {}
        self._unlocked = False

    @property
    def is_unlocked(self) -> bool:
        return self._unlocked

    def is_configured(self) -> bool:
        return bool(self._master)

    def unlock(self) -> dict:
        if not self._master:
            return {"status": "ERROR", "message": "Master password not configured"}
        if not ENCRYPTED_FILE.exists():
            self._secrets = {}
            self._unlocked = True
            return {"status": "OK", "message": "New vault initialized (empty)"}
        try:
            salt = _load_or_create_salt()
            key = _derive_key(self._master, salt)
            f = Fernet(key)
            encrypted = ENCRYPTED_FILE.read_bytes()
            decrypted = f.decrypt(encrypted)
            self._secrets = json.loads(decrypted)
            self._unlocked = True
            return {"status": "OK", "message": f"Unlocked {len(self._secrets)} secrets"}
        except Exception as e:
            self._unlocked = False
            return {"status": "ERROR", "message": f"Failed to unlock: {e}"}

    def lock(self) -> dict:
        self._secrets = {}
        self._unlocked = False
        return {"status": "OK", "message": "Vault locked"}

    def get(self, key: str) -> str | None:
        if not self._unlocked:
            return None
        return self._secrets.get(key)

    def set(self, key: str, value: str) -> dict:
        if not self._unlocked:
            return {"status": "ERROR", "message": "Vault locked"}
        self._secrets[key] = value
        return {"status": "OK", "key": key}

    def delete(self, key: str) -> dict:
        if not self._unlocked:
            return {"status": "ERROR", "message": "Vault locked"}
        self._secrets.pop(key, None)
        return {"status": "OK", "key": key}

    def persist(self) -> dict:
        if not self._unlocked:
            return {"status": "ERROR", "message": "Vault locked"}
        try:
            SECRETS_DIR.mkdir(parents=True, exist_ok=True)
            salt = _load_or_create_salt()
            key = _derive_key(self._master, salt)
            f = Fernet(key)
            encrypted = f.encrypt(json.dumps(self._secrets).encode())
            ENCRYPTED_FILE.write_bytes(encrypted)
            return {"status": "OK", "path": str(ENCRYPTED_FILE)}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def has_secret(self, key: str) -> bool:
        return key in self._secrets if self._unlocked else False

    def list_keys(self) -> list[str]:
        return list(self._secrets.keys()) if self._unlocked else []

    def validate_all_required(self) -> dict:
        if not self._unlocked:
            return {"status": "LOCKED", "required": list(REQUIRED_SECRETS.keys())}
        missing = [k for k in REQUIRED_SECRETS if k not in self._secrets]
        return {
            "status": "INCOMPLETE" if missing else "COMPLETE",
            "total": len(REQUIRED_SECRETS),
            "present": len(REQUIRED_SECRETS) - len(missing),
            "missing": missing,
        }

    def get_from_env(self, key: str) -> str | None:
        return os.environ.get(key) or self.get(key)
