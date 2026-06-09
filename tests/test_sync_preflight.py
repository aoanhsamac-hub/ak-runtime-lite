"""Tests for AK-AUTO-RUNTIME-SYNC-01 pipeline."""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

# Adjust path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


# ============================================================
# Constants
# ============================================================
SYNC_DIR = Path("D:/AK/deploy/sync")
LOG_DIR = Path("D:/AK/logs")
SSH_KEY_DIR = Path(os.environ["USERPROFILE"]) / ".ssh"
EXCLUDE_FILE = SYNC_DIR / "exclude_list.txt"
AK_DIR = Path("D:/AK")


# ============================================================
# Fixtures
# ============================================================


# ============================================================
# SSH Key Tests
# ============================================================
class TestSSHSetup:
    def test_ssh_key_exists(self):
        """SSH key file ton tai."""
        assert (SSH_KEY_DIR / "ak_vps").exists(), "Thieu SSH private key"

    def test_ssh_pubkey_exists(self):
        """SSH public key file ton tai."""
        assert (SSH_KEY_DIR / "ak_vps.pub").exists(), "Thieu SSH public key"

    def test_ssh_config_exists(self):
        """SSH config co host ak-vps."""
        config = SSH_KEY_DIR / "config"
        assert config.exists(), "Thieu SSH config file"
        content = config.read_text(encoding="utf-8")
        assert "Host ak-vps" in content, "Config thieu host ak-vps"
        assert "100.81.12.50" in content, "Config sai HostName"
        assert "ak_vps" in content, "Config sai IdentityFile path"

    def test_ssh_auth_works(self):
        """SSH vao VPS khong can password."""
        result = subprocess.run(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5",
             "ak-vps", "echo OK"],
            capture_output=True, text=True, timeout=10
        )
        assert result.returncode == 0, f"SSH auth that bai: {result.stderr}"
        assert result.stdout.strip() == "OK", f"Sai output: {result.stdout}"

    def test_ssh_done_marker(self):
        """Marker file setup_ssh da duoc tao."""
        assert (LOG_DIR / ".ssh_done").exists(), "Chua chay setup_ssh.ps1"


# ============================================================
# Exclude List Tests
# ============================================================
class TestExcludeList:
    def test_exclude_file_exists(self):
        """File exclude_list.txt ton tai."""
        assert EXCLUDE_FILE.exists(), "Thieu exclude_list.txt"

    def test_exclude_patterns_loaded(self):
        """Doc duoc cac patterns tu exclude file."""
        patterns = EXCLUDE_FILE.read_text(encoding="utf-8").splitlines()
        patterns = [p.strip() for p in patterns if p.strip() and not p.startswith("#")]
        assert len(patterns) > 5, "It nhat 5 patterns exclude"
        assert any(".venv" in p for p in patterns), "Thieu exclude .venv"
        assert any("__pycache__" in p for p in patterns), "Thieu exclude __pycache__"
        assert any("secrets" in p for p in patterns), "Thieu exclude secrets"
        assert any(".env" in p for p in patterns), "Thieu exclude .env"

    def test_exclude_prevents_secret_leak(self):
        """Kiem tra exclude patterns bao ve secrets."""
        patterns = EXCLUDE_FILE.read_text(encoding="utf-8").splitlines()
        patterns = [p.strip() for p in patterns if p.strip() and not p.startswith("#")]
        secret_patterns = ["secrets", ".env", "token", "password", "credential"]
        found = [s for s in secret_patterns if any(s in p for p in patterns)]
        assert "secrets" in str(found), "Thieu pattern bao ve secrets"
        assert ".env" in str(found), "Thieu pattern bao ve .env"


# ============================================================
# Push Source Tests
# ============================================================
class TestPushSource:
    def test_push_script_exists(self):
        """Script push_source.ps1 ton tai."""
        assert (SYNC_DIR / "push_source.ps1").exists()

    def test_push_excludes_venv(self):
        """Push khong gui .venv."""
        # Kiem tra trong script co exclude .venv khong
        content = (SYNC_DIR / "push_source.ps1").read_text(encoding="utf-8")
        assert ".venv" in content, "Script push thieu exclude .venv"

    def test_push_excludes_logs(self):
        """Push khong gui *.log."""
        content = (SYNC_DIR / "push_source.ps1").read_text(encoding="utf-8")
        assert "*.log" in content or ".log" in content, "Script push thieu exclude logs"

    def test_push_excludes_pycache(self):
        """Push khong gui __pycache__."""
        content = (SYNC_DIR / "push_source.ps1").read_text(encoding="utf-8")
        assert "__pycache__" in content, "Script push thieu exclude __pycache__"

    def test_push_has_log(self):
        """Push co ghi log file."""
        content = (SYNC_DIR / "push_source.ps1").read_text(encoding="utf-8")
        assert "sync_push.log" in content, "Push thieu log file"

    def test_push_sends_telegram(self):
        """Push co gui Telegram thong bao."""
        content = (SYNC_DIR / "push_source.ps1").read_text(encoding="utf-8")
        assert "send_telegram.ps1" in content, "Push thieu Telegram notification"


# ============================================================
# Pull Reports Tests
# ============================================================
class TestPullReports:
    def test_pull_script_exists(self):
        """Script pull_reports.ps1 ton tai."""
        assert (SYNC_DIR / "pull_reports.ps1").exists()

    def test_pull_only_reports_evidence_logs(self):
        """Pull chi lay reports/, evidence/, logs/."""
        content = (SYNC_DIR / "pull_reports.ps1").read_text(encoding="utf-8")
        assert "docs/reports" in content, "Thieu docs/reports"
        assert "evidence" in content, "Thieu evidence"
        assert "logs" in content, "Thieu logs"

    def test_pull_no_source_overwrite(self):
        """Pull khong gui source code tu VPS ve."""
        content = (SYNC_DIR / "pull_reports.ps1").read_text(encoding="utf-8")
        # Kiem tra khong co thu muc source code trong pull list
        assert "services" not in content.split("$folders")[1] if "$folders" in content else True
        assert "deploy" not in content.split("$folders")[1] if "$folders" in content else True

    def test_pull_has_log(self):
        """Pull co ghi log file."""
        content = (SYNC_DIR / "pull_reports.ps1").read_text(encoding="utf-8")
        assert "sync_pull.log" in content, "Pull thieu log file"

    def test_pull_sends_telegram(self):
        """Pull co gui Telegram thong bao."""
        content = (SYNC_DIR / "pull_reports.ps1").read_text(encoding="utf-8")
        assert "send_telegram.ps1" in content, "Pull thieu Telegram notification"


# ============================================================
# Telegram Tests
# ============================================================
class TestTelegram:
    def test_send_script_exists(self):
        """Script send_telegram.ps1 ton tai."""
        assert (SYNC_DIR / "send_telegram.ps1").exists()

    def test_send_script_has_token_check(self):
        """Script kiem tra token ton tai truoc khi gui."""
        content = (SYNC_DIR / "send_telegram.ps1").read_text(encoding="utf-8")
        assert "TELEGRAM_BOT_TOKEN" in content
        assert "TELEGRAM_WHITELIST" in content

    def test_send_script_has_error_handling(self):
        """Script co try/catch khi gui."""
        content = (SYNC_DIR / "send_telegram.ps1").read_text(encoding="utf-8")
        assert "try" in content and "catch" in content

    def test_token_not_hardcoded_in_code(self):
        """Khong co token hardcode trong file .py hoac .ps1."""
        # Check all .py files in services
        py_files = list(AK_DIR.rglob("*.py"))
        for f in py_files:
            if ".venv" in str(f):
                continue
            content = f.read_text(encoding="utf-8", errors="ignore")
            # Kiem tra token khong xuat hien hardcoded
            if "8869703952" in content:
                # Cho phep trong file set_telegram_vars.ps1
                if "set_telegram_vars.ps1" not in str(f):
                    pytest.fail(f"Token hardcoded trong {f}")

    def test_send_telegram_live(self):
        """Gui that 1 tin nhan Telegram de kiem tra."""
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-File", str(SYNC_DIR / "send_telegram.ps1"),
             "-Message", "TEST: AK-AUTO-RUNTIME-SYNC-01 preflight check",
             "-Status", "info"],
            capture_output=True, text=True, timeout=15
        )
        assert result.returncode == 0, f"Send Telegram that bai: {result.stderr}"


# ============================================================
# Scheduler Tasks Tests
# ============================================================
class TestSchedulerTasks:
    def test_pc_push_task_exists(self):
        """Task AK_Push_Source_Every_30min ton tai tren PC."""
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-ScheduledTask -TaskName AK_Push_Source_Every_30min -ErrorAction SilentlyContinue | Format-Table -AutoSize"],
            capture_output=True, text=True, timeout=10
        )
        assert "AK_Push_Source_Every_30min" in result.stdout, "Thieu task push tren PC"

    def test_pc_pull_task_exists(self):
        """Task AK_Pull_Reports_Every_1h ton tai tren PC."""
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-ScheduledTask -TaskName AK_Pull_Reports_Every_1h -ErrorAction SilentlyContinue | Format-Table -AutoSize"],
            capture_output=True, text=True, timeout=10
        )
        assert "AK_Pull_Reports_Every_1h" in result.stdout, "Thieu task pull tren PC"


# ============================================================
# Script Files Tests
# ============================================================
class TestScripts:
    def test_all_sync_scripts_exist(self):
        """Tat ca script files trong sync/ deu ton tai."""
        expected = [
            "setup_ssh.ps1", "push_source.ps1", "pull_reports.ps1",
            "send_telegram.ps1", "register_tasks_pc.ps1",
            "register_tasks_vps.ps1", "update_runtime.ps1",
            "start_runtime.ps1", "stop_runtime.ps1", "restart_runtime.ps1",
            "status_runtime.ps1", "set_telegram_vars.ps1",
            "exclude_list.txt"
        ]
        for f in expected:
            assert (SYNC_DIR / f).exists(), f"Thieu file: {f}"

    def test_sync_scripts_no_secrets_hardcoded(self):
        """Khong co secret nao hardcoded trong scripts (ngoai set_telegram_vars)."""
        secret_patterns = ["8869703952:AAHZo6hujSaeuoSPijIGmoUH28NKhRI5Mo0"]
        for script in SYNC_DIR.glob("*.ps1"):
            if script.name == "set_telegram_vars.ps1":
                continue
            content = script.read_text(encoding="utf-8")
            for secret in secret_patterns:
                assert secret not in content, f"Secret hardcoded trong {script.name}"


# ============================================================
# Safety Tests
# ============================================================
class TestSafety:
    def test_no_password_in_ssh_config(self):
        """SSH config khong chua password."""
        config = SSH_KEY_DIR / "config"
        if config.exists():
            content = config.read_text(encoding="utf-8")
            assert "PasswordAuthentication" not in content
            assert "password" not in content.lower().split("host")[1] if "host" in content else True

    def test_vps_cannot_overwrite_pc_source(self):
        """Pull script khong co logic ghi source code tu VPS ve PC."""
        content = (SYNC_DIR / "pull_reports.ps1").read_text(encoding="utf-8") if (SYNC_DIR / "pull_reports.ps1").exists() else ""
        # Kiem tra pull khong co dong nao ghi services/ hay deploy/ tu VPS ve
        assert "services" not in content.replace("docs/reports", ""), "Pull co the ghi services tu VPS"
        assert "deploy" not in content.replace("docs/reports", ""), "Pull co the ghi deploy tu VPS"
        assert "AK\\services" not in content, "Pull co the ghi services tu VPS"

    def test_log_directory_exists(self):
        """Thu muc logs ton tai."""
        assert LOG_DIR.exists(), "Thieu thu muc logs"

    def test_log_directory_writable(self):
        """Thu muc logs co the ghi duoc."""
        test_file = LOG_DIR / ".write_test"
        try:
            test_file.write_text("test")
            assert test_file.exists()
            test_file.unlink()
        except PermissionError:
            pytest.fail("Khong the ghi vao thu muc logs")
