"""Tests for the Telegram Gateway, Command Router, and Notification Service."""

import os
import time
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone


class TestTelegramGatewayReal(unittest.TestCase):
    def setUp(self):
        self.env_patcher = patch.dict(os.environ, {
            "TELEGRAM_BOT_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
            "TELEGRAM_WHITELIST": "12345678,87654321",
        })
        self.env_patcher.start()

    def tearDown(self):
        self.env_patcher.stop()

    def test_create_gateway(self):
        from services.telegram_gateway import TelegramGateway
        gw = TelegramGateway()
        self.assertTrue(gw.has_token)

    def test_gateway_no_token(self):
        with patch.dict(os.environ, {"TELEGRAM_WHITELIST": "123"}, clear=True):
            from services.telegram_gateway import TelegramGateway
            gw = TelegramGateway(token="")
            self.assertFalse(gw.has_token)

    def test_validate_token_format(self):
        from services.telegram_gateway import TelegramGateway
        gw = TelegramGateway(token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
        self.assertTrue(gw.validate_token_format())

    def test_validate_token_format_invalid(self):
        from services.telegram_gateway import TelegramGateway
        gw = TelegramGateway(token="invalid-token")
        self.assertFalse(gw.validate_token_format())

    def test_process_command_authorized(self):
        from services.telegram_gateway import TelegramGateway, is_authorized
        gw = TelegramGateway(token="123456:test")
        result = gw.process_command(12345678, "/status")
        self.assertEqual(result["status"], "OK")

    def test_register_handler(self):
        from services.telegram_gateway import TelegramGateway
        gw = TelegramGateway()
        handler = Mock(return_value="handled")
        gw.register_handler("/custom", handler)
        result = gw.process_command(12345678, "/custom")
        self.assertEqual(result["status"], "OK")

    def test_start_stop(self):
        from services.telegram_gateway import TelegramGateway
        gw = TelegramGateway(token="test:token")
        result = gw.start()
        self.assertEqual(result["status"], "OK")
        self.assertTrue(gw.is_running)
        result = gw.stop()
        self.assertFalse(gw.is_running)

    def test_health(self):
        from services.telegram_gateway import TelegramGateway
        gw = TelegramGateway(token="test:token")
        h = gw.health()
        self.assertIn("running", h)
        self.assertIn("token_configured", h)

    def test_whitelist_auth(self):
        from services.telegram_gateway import is_authorized
        byp = patch("services.telegram_gateway.WHITELISTED_USERS", {12345, 67890})
        byp.start()
        self.assertTrue(is_authorized(12345))
        self.assertFalse(is_authorized(99999))
        byp.stop()

    def test_audit_log(self):
        from services.telegram_gateway import TelegramGateway
        gw = TelegramGateway(token="test:token")
        gw.process_command(12345678, "/help")
        log = gw.get_audit_log()
        self.assertGreater(len(log), 0)

    def test_get_whitelist(self):
        from services.telegram_gateway import TelegramGateway
        gw = TelegramGateway(token="test:token")
        wl = gw.get_whitelist()
        self.assertIn(12345678, wl)
        self.assertIn(87654321, wl)


class TestTelegramCommandRouter(unittest.TestCase):
    def setUp(self):
        self.router_patch = patch("services.telegram_command_router.CommandRouter")
        self.mock_router = self.router_patch.start()
        self.router = self.mock_router()

    def tearDown(self):
        self.router_patch.stop()

    def test_register_handler(self):
        mock_fn = Mock()
        self.router.register("test", mock_fn)
        self.router.register.assert_called_with("test", mock_fn)

    def test_route_known(self):
        mock_handler = Mock(return_value="handled")
        self.router.register("status", mock_handler)
        self.router.route.assert_not_called()


class TestTelegramNotificationService(unittest.TestCase):
    def setUp(self):
        self.notif_patch = patch("services.telegram_notification_service.NotificationService")
        self.mock_notif = self.notif_patch.start()
        self.service = self.mock_notif()

    def tearDown(self):
        self.notif_patch.stop()

    def test_broadcast(self):
        self.service.broadcast("test message")
        self.service.broadcast.assert_called_with("test message")

    def test_broadcast_to_user(self):
        self.service.send_to_user.assert_not_called()


if __name__ == "__main__":
    unittest.main()
