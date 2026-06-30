#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr
from unittest.mock import patch

from agoras.core.auth.storage import SecureTokenStorage
from refresh_credentials import (
    extract_refresh_token_value,
    process_platform,
    run_refresh,
    seed_platform_storage,
)


class TestRefreshCredentials(unittest.TestCase):
    def setUp(self):
        self.storage_dir = tempfile.mkdtemp(prefix="agoras-test-storage-")
        self.env_patch = patch.dict(os.environ, {"AGORAS_STORAGE_DIR": self.storage_dir})
        self.env_patch.start()
        self.addCleanup(self.env_patch.stop)

    def _facebook_env(self, refresh_token="fb-refresh"):  # nosec B107
        return {
            "FACEBOOK_CLIENT_ID": "cid",
            "FACEBOOK_CLIENT_SECRET": "sec",
            "FACEBOOK_OBJECT_ID": "oid",
            "FACEBOOK_REFRESH_TOKEN": refresh_token,
        }

    @patch("refresh_credentials.put_repository_secret")
    @patch("refresh_credentials.refresh_platform_token", return_value=True)
    def test_unchanged_token_logs_ok(self, _mock_refresh, mock_put):
        storage = SecureTokenStorage()
        seed_platform_storage(storage, "facebook", self._facebook_env())
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            status = process_platform(
                "facebook",
                self._facebook_env(),
                "FB_REFRESH",
                "ghp_test",
                storage,
            )
        self.assertEqual(status, "ok")
        mock_put.assert_not_called()
        self.assertIn("status=ok", stderr.getvalue())
        self.assertNotIn("fb-refresh", stderr.getvalue())

    @patch("refresh_credentials.put_repository_secret")
    @patch("refresh_credentials.refresh_platform_token", return_value=True)
    def test_rotated_token_triggers_github_put(self, mock_refresh, mock_put):
        storage = SecureTokenStorage()
        seed_platform_storage(storage, "facebook", self._facebook_env("old-token"))
        mock_refresh.side_effect = lambda platform, env, stor: (
            seed_platform_storage(stor, platform, self._facebook_env("new-token")) or True
        )

        stderr = io.StringIO()
        with redirect_stderr(stderr):
            status = process_platform(
                "facebook",
                self._facebook_env("old-token"),
                "FB_REFRESH",
                "ghp_test",
                storage,
            )
        self.assertEqual(status, "updated")
        mock_put.assert_called_once_with("FB_REFRESH", "new-token", token="ghp_test")
        self.assertIn("status=updated", stderr.getvalue())

    @patch("refresh_credentials.put_repository_secret", side_effect=RuntimeError("network"))
    @patch("refresh_credentials.refresh_platform_token", return_value=True)
    def test_github_write_runtime_error_returns_failed(self, _mock_refresh, _mock_put):
        storage = SecureTokenStorage()
        seed_platform_storage(storage, "facebook", self._facebook_env("old-token"))

        def rotate(_platform, env, stor):
            seed_platform_storage(stor, "facebook", self._facebook_env("new-token"))
            return True

        with patch("refresh_credentials.refresh_platform_token", side_effect=rotate):
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                status = process_platform(
                    "facebook",
                    self._facebook_env("old-token"),
                    "FB_REFRESH",
                    "ghp_test",
                    storage,
                )
        self.assertEqual(status, "failed")
        self.assertIn("github_write", stderr.getvalue())

    @patch("refresh_credentials.put_repository_secret")
    @patch("refresh_credentials.refresh_platform_token", return_value=True)
    def test_missing_secret_mapping_skipped(self, _mock_refresh, mock_put):
        storage = SecureTokenStorage()
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            status = process_platform(
                "facebook",
                self._facebook_env(),
                None,
                "ghp_test",
                storage,
            )
        self.assertEqual(status, "skipped")
        mock_put.assert_not_called()
        self.assertIn("no_secret_mapping", stderr.getvalue())

    @patch("refresh_credentials.put_repository_secret")
    @patch("refresh_credentials.refresh_platform_token", return_value=True)
    def test_tiktok_access_only_skipped(self, _mock_refresh, mock_put):
        storage = SecureTokenStorage()
        env = {
            "TIKTOK_USERNAME": "user",
            "TIKTOK_CLIENT_KEY": "key",
            "TIKTOK_CLIENT_SECRET": "sec",
            "TIKTOK_REFRESH_TOKEN": "access_only_token",
        }
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            status = process_platform("tiktok", env, "TIKTOK_RT", "ghp_test", storage)
        self.assertEqual(status, "skipped")
        mock_put.assert_not_called()
        self.assertIn("access_only_token", stderr.getvalue())

    @patch("refresh_credentials.process_platform")
    def test_run_refresh_non_zero_when_any_failed(self, mock_process):
        mock_process.side_effect = ["ok", "failed"]
        code = run_refresh(
            {
                "facebook": self._facebook_env(),
                "instagram": self._facebook_env(),
            },
            {"facebook": "FB", "instagram": "IG"},
            "ghp_test",
        )
        self.assertEqual(code, 1)

    def test_extract_refresh_token_value_threads(self):
        storage = SecureTokenStorage()
        seed_platform_storage(
            storage,
            "threads",
            {
                "THREADS_APP_ID": "app",
                "THREADS_APP_SECRET": "sec",
                "THREADS_USER_ID": "uid",
                "THREADS_REFRESH_TOKEN": "threads-token",
            },
        )
        value = extract_refresh_token_value("threads", storage)
        self.assertEqual(value, "threads-token")


if __name__ == "__main__":
    unittest.main()
