#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import os
import shutil
import sys
import tempfile

from agoras.cli.utils.unattended_format import (
    PLATFORM_SECTION_BY_NAME,
    load_platform_token,
)
from agoras.core.auth.storage import SecureTokenStorage
from github_secrets import put_repository_secret

REFRESH_CAPABLE_PLATFORMS = (
    "youtube",
    "facebook",
    "instagram",
    "linkedin",
    "tiktok",
    "threads",
)

PLATFORM_TOKEN_BUILDERS = {
    "youtube": lambda env: {
        "client_id": env["YOUTUBE_CLIENT_ID"],
        "client_secret": env["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": env["YOUTUBE_REFRESH_TOKEN"],
    },
    "facebook": lambda env: {
        "client_id": env["FACEBOOK_CLIENT_ID"],
        "client_secret": env["FACEBOOK_CLIENT_SECRET"],
        "user_id": env["FACEBOOK_OBJECT_ID"],
        "refresh_token": env["FACEBOOK_REFRESH_TOKEN"],
    },
    "instagram": lambda env: {
        "client_id": env["INSTAGRAM_CLIENT_ID"],
        "client_secret": env["INSTAGRAM_CLIENT_SECRET"],
        "user_id": env["INSTAGRAM_OBJECT_ID"],
        "refresh_token": env["INSTAGRAM_REFRESH_TOKEN"],
    },
    "linkedin": lambda env: {
        "client_id": env["LINKEDIN_CLIENT_ID"],
        "client_secret": env["LINKEDIN_CLIENT_SECRET"],
        "user_id": env["LINKEDIN_OBJECT_ID"],
        "refresh_token": env["LINKEDIN_REFRESH_TOKEN"],
    },
    "tiktok": lambda env: {
        "username": env["TIKTOK_USERNAME"],
        "client_key": env["TIKTOK_CLIENT_KEY"],
        "client_secret": env["TIKTOK_CLIENT_SECRET"],
        "refresh_token": env["TIKTOK_REFRESH_TOKEN"],
    },
    "threads": lambda env: {
        "app_id": env["THREADS_APP_ID"],
        "app_secret": env["THREADS_APP_SECRET"],
        "user_id": env["THREADS_USER_ID"],
        "refresh_token": env["THREADS_REFRESH_TOKEN"],
    },
}

PLATFORM_IDENTIFIERS = {
    "youtube": lambda env: env["YOUTUBE_CLIENT_ID"],
    "facebook": lambda env: env["FACEBOOK_CLIENT_ID"],
    "instagram": lambda env: env["INSTAGRAM_CLIENT_ID"],
    "linkedin": lambda env: env["LINKEDIN_CLIENT_ID"],
    "tiktok": lambda env: env["TIKTOK_USERNAME"],
    "threads": lambda env: env["THREADS_APP_ID"],
}


def _log_status(platform, secret_name, status, reason=None):
    line = f"platform={platform} secret={secret_name or '-'} status={status}"
    if reason:
        line = f"{line} reason={reason}"
    print(line, file=sys.stderr)


def extract_refresh_token_value(platform, storage):
    token_data = load_platform_token(storage, platform)
    if not token_data:
        return None
    section = PLATFORM_SECTION_BY_NAME.get(platform)
    if not section:
        return None
    for env_name, getter in section.env_vars:
        if env_name.endswith("_REFRESH_TOKEN"):
            return getter(token_data)
    return None


def seed_platform_storage(storage, platform, env):
    builder = PLATFORM_TOKEN_BUILDERS[platform]
    token_data = builder(env)
    identifier = PLATFORM_IDENTIFIERS[platform](env)
    storage.save_token(platform, identifier, token_data)
    storage.save_token(platform, "default", token_data)


def _create_auth_manager(platform, env):
    if platform == "youtube":
        from agoras.platforms.youtube.auth import YouTubeAuthManager

        return YouTubeAuthManager(
            client_id=env["YOUTUBE_CLIENT_ID"],
            client_secret=env["YOUTUBE_CLIENT_SECRET"],
            refresh_token=env["YOUTUBE_REFRESH_TOKEN"],
        )
    if platform == "facebook":
        from agoras.platforms.facebook.auth import FacebookAuthManager

        return FacebookAuthManager(
            user_id=env["FACEBOOK_OBJECT_ID"],
            client_id=env["FACEBOOK_CLIENT_ID"],
            client_secret=env["FACEBOOK_CLIENT_SECRET"],
            refresh_token=env["FACEBOOK_REFRESH_TOKEN"],
        )
    if platform == "instagram":
        from agoras.platforms.instagram.auth import InstagramAuthManager

        return InstagramAuthManager(
            user_id=env["INSTAGRAM_OBJECT_ID"],
            client_id=env["INSTAGRAM_CLIENT_ID"],
            client_secret=env["INSTAGRAM_CLIENT_SECRET"],
            refresh_token=env["INSTAGRAM_REFRESH_TOKEN"],
        )
    if platform == "linkedin":
        from agoras.platforms.linkedin.auth import LinkedInAuthManager

        return LinkedInAuthManager(
            user_id=env["LINKEDIN_OBJECT_ID"],
            client_id=env["LINKEDIN_CLIENT_ID"],
            client_secret=env["LINKEDIN_CLIENT_SECRET"],
            refresh_token=env["LINKEDIN_REFRESH_TOKEN"],
        )
    if platform == "tiktok":
        from agoras.platforms.tiktok.auth import TikTokAuthManager

        return TikTokAuthManager(
            username=env["TIKTOK_USERNAME"],
            client_key=env["TIKTOK_CLIENT_KEY"],
            client_secret=env["TIKTOK_CLIENT_SECRET"],
            refresh_token=env["TIKTOK_REFRESH_TOKEN"],
        )
    if platform == "threads":
        from agoras.platforms.threads.auth import ThreadsAuthManager

        return ThreadsAuthManager(
            app_id=env["THREADS_APP_ID"],
            app_secret=env["THREADS_APP_SECRET"],
            refresh_token=env["THREADS_REFRESH_TOKEN"],
        )
    raise ValueError(f"unsupported platform: {platform}")


async def _refresh_platform(platform, env, storage):
    seed_platform_storage(storage, platform, env)
    previous = {key: os.environ.get(key) for key in env}
    try:
        os.environ.update(env)
        manager = _create_auth_manager(platform, env)
        return await manager.authenticate()
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def refresh_platform_token(platform, env, storage):
    return asyncio.run(_refresh_platform(platform, env, storage))


def process_platform(platform, env, secret_name, write_token, storage):
    refresh_token = _refresh_token_from_env(env, platform)
    if platform == "tiktok" and refresh_token and refresh_token.startswith("access_only_"):
        _log_status(platform, secret_name, "skipped", "access_only_token")
        return "skipped"

    if not secret_name:
        _log_status(platform, secret_name, "skipped", "no_secret_mapping")
        return "skipped"

    original_value = _refresh_token_from_env(env, platform)
    if not original_value:
        _log_status(platform, secret_name, "skipped", "missing_refresh_token")
        return "skipped"

    try:
        if not refresh_platform_token(platform, env, storage):
            _log_status(platform, secret_name, "failed", "oauth_refresh")
            return "failed"
    except Exception:
        _log_status(platform, secret_name, "failed", "oauth_refresh")
        return "failed"

    new_value = extract_refresh_token_value(platform, storage)
    if not new_value:
        _log_status(platform, secret_name, "failed", "token_readback")
        return "failed"

    if new_value == original_value:
        _log_status(platform, secret_name, "ok")
        return "ok"

    try:
        put_repository_secret(secret_name, new_value, token=write_token)
    except Exception:
        _log_status(platform, secret_name, "failed", "github_write")
        return "failed"

    _log_status(platform, secret_name, "updated")
    return "updated"


def _refresh_env_key(platform):
    return {
        "youtube": "YOUTUBE_REFRESH_TOKEN",
        "facebook": "FACEBOOK_REFRESH_TOKEN",
        "instagram": "INSTAGRAM_REFRESH_TOKEN",
        "linkedin": "LINKEDIN_REFRESH_TOKEN",
        "tiktok": "TIKTOK_REFRESH_TOKEN",
        "threads": "THREADS_REFRESH_TOKEN",
    }[platform]


def _refresh_token_from_env(env, platform):
    return env.get(_refresh_env_key(platform))


def run_refresh(platform_envs, secret_names, write_token):
    storage_dir = tempfile.mkdtemp(prefix="agoras-refresh-")
    previous_storage = os.environ.get("AGORAS_STORAGE_DIR")
    os.environ["AGORAS_STORAGE_DIR"] = storage_dir
    storage = SecureTokenStorage()
    any_failed = False

    try:
        for platform, env in platform_envs.items():
            secret_name = secret_names.get(platform)
            status = process_platform(platform, env, secret_name, write_token, storage)
            if status == "failed":
                any_failed = True
    finally:
        if previous_storage is None:
            os.environ.pop("AGORAS_STORAGE_DIR", None)
        else:
            os.environ["AGORAS_STORAGE_DIR"] = previous_storage
        shutil.rmtree(storage_dir, ignore_errors=True)

    return 1 if any_failed else 0
