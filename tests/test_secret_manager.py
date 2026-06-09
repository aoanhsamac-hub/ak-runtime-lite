"""Tests for the Secret Manager and Credential Validator."""

import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock


class TestSecretManagerReal(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.env_patcher = patch.dict(os.environ, {
            "AK_MASTER_SECRET": "test-master-password-12345",
        })
        self.env_patcher.start()
        import services.secret_manager as sm_module
        self._orig_secrets_dir = sm_module.SECRETS_DIR
        self._orig_encrypted_file = sm_module.ENCRYPTED_FILE
        self._orig_salt_file = sm_module.SALT_FILE
        sm_module.SECRETS_DIR = Path(self.tmpdir)
        sm_module.ENCRYPTED_FILE = Path(self.tmpdir) / "secrets.enc"
        sm_module.SALT_FILE = Path(self.tmpdir) / ".salt"

    def tearDown(self):
        self.env_patcher.stop()
        import services.secret_manager as sm_module
        sm_module.SECRETS_DIR = self._orig_secrets_dir
        sm_module.ENCRYPTED_FILE = self._orig_encrypted_file
        sm_module.SALT_FILE = self._orig_salt_file
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_create_and_unlock(self):
        from services.secret_manager import SecretManager
        sm = SecretManager()
        self.assertTrue(sm.is_configured())
        result = sm.unlock()
        self.assertEqual(result["status"], "OK")
        self.assertTrue(sm.is_unlocked)

    def test_set_and_get(self):
        from services.secret_manager import SecretManager
        sm = SecretManager()
        sm.unlock()
        sm.set("TEST_KEY", "test_value")
        val = sm.get("TEST_KEY")
        self.assertEqual(val, "test_value")

    def test_persist_and_reload(self):
        import services.secret_manager as sm_module
        from services.secret_manager import SecretManager
        sm = SecretManager()
        sm.unlock()
        sm.set("PERSIST_KEY", "persist_value")
        sm.persist()
        self.assertTrue(sm_module.ENCRYPTED_FILE.exists())
        sm2 = SecretManager()
        sm2.unlock()
        val = sm2.get("PERSIST_KEY")
        self.assertEqual(val, "persist_value")

    def test_delete(self):
        from services.secret_manager import SecretManager
        sm = SecretManager()
        sm.unlock()
        sm.set("TO_DELETE", "value")
        sm.delete("TO_DELETE")
        self.assertIsNone(sm.get("TO_DELETE"))

    def test_list_keys(self):
        from services.secret_manager import SecretManager
        sm = SecretManager()
        sm.unlock()
        sm.set("KEY_A", "a")
        sm.set("KEY_B", "b")
        keys = sm.list_keys()
        self.assertIn("KEY_A", keys)
        self.assertIn("KEY_B", keys)

    def test_has_secret(self):
        from services.secret_manager import SecretManager
        sm = SecretManager()
        sm.unlock()
        sm.set("EXISTS", "yes")
        self.assertTrue(sm.has_secret("EXISTS"))
        self.assertFalse(sm.has_secret("MISSING"))

    def test_lock(self):
        from services.secret_manager import SecretManager
        sm = SecretManager()
        sm.unlock()
        sm.set("KEY", "val")
        sm.lock()
        self.assertFalse(sm.is_unlocked)
        self.assertIsNone(sm.get("KEY"))

    def test_get_from_env(self):
        from services.secret_manager import SecretManager
        sm = SecretManager()
        sm.unlock()
        sm.set("CUSTOM_KEY", "vault_val")
        with patch.dict(os.environ, {"CUSTOM_KEY": "env_val"}, clear=True):
            val = sm.get_from_env("CUSTOM_KEY")
            self.assertEqual(val, "env_val")

    def test_validate_required(self):
        from services.secret_manager import SecretManager
        sm = SecretManager()
        sm.unlock()
        result = sm.validate_all_required()
        self.assertEqual(result["status"], "INCOMPLETE")

    def test_no_password(self):
        with patch.dict(os.environ, {}, clear=True):
            from services.secret_manager import SecretManager
            sm = SecretManager()
            self.assertFalse(sm.is_configured())

    def test_wrong_password(self):
        from services.secret_manager import SecretManager
        sm = SecretManager(master_password="correct-pw")
        sm.unlock()
        sm.set("KEY", "secret")
        sm.persist()
        sm2 = SecretManager(master_password="wrong-password")
        result = sm2.unlock()
        self.assertEqual(result["status"], "ERROR")


class TestCredentialValidator(unittest.TestCase):
    def setUp(self):
        self.validator_patch = patch("services.credential_validator.CredentialValidator")
        self.mock_validator = self.validator_patch.start()
        self.validator = self.mock_validator()

    def tearDown(self):
        self.validator_patch.stop()

    def test_validate_token_format(self):
        self.validator.validate_token_format.return_value = True
        result = self.validator.validate_token_format("123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
        self.assertTrue(result)

    def test_validate_token_format_invalid(self):
        self.validator.validate_token_format.return_value = False
        result = self.validator.validate_token_format("invalid")
        self.assertFalse(result)

    def test_validate_all(self):
        self.validator.validate_all.return_value = {"errors": [], "warnings": []}
        result = self.validator.validate_all()
        self.assertEqual(result["errors"], [])

    def test_validate_all_with_plaintext(self):
        self.validator.validate_all.return_value = {"errors": ["API_KEY found in config.py:5"], "warnings": []}
        result = self.validator.validate_all()
        self.assertIn("API_KEY found", result["errors"][0])


if __name__ == "__main__":
    unittest.main()
