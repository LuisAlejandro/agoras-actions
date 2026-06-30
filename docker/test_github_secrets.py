#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import unittest
from unittest.mock import patch

from github_secrets import GitHubSecretsError, encrypt_secret, put_repository_secret


class TestEncryptSecret(unittest.TestCase):
    def test_encrypt_secret_roundtrip_shape(self):
        from nacl import public

        private_key = public.PrivateKey.generate()
        public_key_b64 = base64.b64encode(bytes(private_key.public_key)).decode("utf-8")
        encrypted = encrypt_secret(public_key_b64, "secret-value")
        self.assertTrue(encrypted)


class TestPutRepositorySecret(unittest.TestCase):
    @patch("github_secrets._api_request")
    def test_put_repository_secret_calls_github_api(self, mock_api):
        mock_api.side_effect = [
            {"key": base64.b64encode(b"0" * 32).decode("utf-8"), "key_id": "kid"},
            {},
        ]
        put_repository_secret(
            "FB_REFRESH_TOKEN",
            "rotated-token",
            token="ghp_test",
            repository="owner/repo",
            api_url="https://api.github.com",
        )
        self.assertEqual(mock_api.call_count, 2)
        put_call = mock_api.call_args_list[1]
        self.assertEqual(put_call.args[0], "PUT")
        payload = put_call.args[3]
        self.assertEqual(payload["key_id"], "kid")
        self.assertIn("encrypted_value", payload)

    @patch("github_secrets._api_request")
    def test_put_repository_secret_http_error(self, mock_api):
        mock_api.side_effect = GitHubSecretsError("HTTP 403")
        with self.assertRaises(GitHubSecretsError):
            put_repository_secret(
                "FB_REFRESH_TOKEN",
                "rotated-token",
                token="ghp_test",
                repository="owner/repo",
            )

    def test_put_repository_secret_rejects_invalid_name(self):
        with self.assertRaises(GitHubSecretsError):
            put_repository_secret(
                "../evil",
                "rotated-token",
                token="ghp_test",
                repository="owner/repo",
            )


if __name__ == "__main__":
    unittest.main()
