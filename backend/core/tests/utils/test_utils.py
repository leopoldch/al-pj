import unittest
from unittest.mock import patch, MagicMock
from core.utils import send_email, send_formatted_mail



class TestUtils(unittest.TestCase):

    @patch("core.utils.smtplib.SMTP")
    def test_send_email_success(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        send_email(
            subject="Test Subject",
            html_body="<p>Test Body</p>",
            sender_email="sender@example.com",
            sender_password="password",
            recipient_email="recipient@example.com",
            smtp_server="smtp.example.com",
            smtp_port=587,
        )

        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_with("sender@example.com", "password")
        mock_server.send_message.assert_called_once()

    @patch("core.utils.smtplib.SMTP")
    def test_send_email_failure(self, mock_smtp):
        # Setup mock to raise an exception
        mock_smtp.return_value.__enter__.side_effect = Exception(
            "SMTP Connection Failed"
        )

        # Should catch exception and print error (not crash)
        send_email(
            subject="Test Subject",
            html_body="<p>Test Body</p>",
            sender_email="sender@example.com",
            sender_password="password",
            recipient_email="recipient@example.com",
            smtp_server="smtp.example.com",
            smtp_port=587,
        )

    @patch("core.utils.send_email")
    @patch("core.utils.os.getenv")
    def test_send_formatted_mail(self, mock_getenv, mock_send_email):
        # Mock env vars
        def getenv_side_effect(key, default=None):
            env_vars = {
                "MAIL_USERNAME": "sender@example.com",
                "MAIL_PASSWORD": "password",
                "MAIL_HOST": "smtp.example.com",
                "MAIL_PORT": "587",
            }
            return env_vars.get(key, default)

        mock_getenv.side_effect = getenv_side_effect

        send_formatted_mail(receiver="recipient@example.com", name="John Doe")

        mock_send_email.assert_called_once()
        call_args = mock_send_email.call_args
        self.assertEqual(
            call_args[0][0], "[Aurianne Léo] - Nouveau message reçu sur le site"
        )  # subject
        self.assertIn("Bonjour John Doe", call_args[0][1])  # html_body contains name
        self.assertEqual(call_args[0][2], "sender@example.com")  # sender
        self.assertEqual(call_args[0][3], "password")  # password
        self.assertEqual(call_args[0][4], "recipient@example.com")  # receiver
        self.assertEqual(call_args[0][5], "smtp.example.com")  # server
        self.assertEqual(call_args[0][6], 587)  # port (cast to int in utils)

        # Check that the port passed to send_email is actually an int as expected by the function signature,
        # but my mock returns string '587'. verify utils.py line 112: int(os.getenv(..., 587))
        # Ah my mock returns '587', int('587') is 587. Good.
