#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

RESERVED_KEYS = frozenset({"network", "action"})

LOOPABLE_ACTIONS = frozenset({"like", "share", "delete"})
PLATFORM_ACTIONS = frozenset({"post", "like", "share", "delete", "video", "template"})
REFRESH_ACTION = "refresh-credentials"
ALL_ACTIONS = PLATFORM_ACTIONS | {REFRESH_ACTION}

REFRESH_CAPABLE_PLATFORMS = (
    "youtube",
    "facebook",
    "instagram",
    "linkedin",
    "tiktok",
    "threads",
)

REFRESH_TOKEN_SECRET_NAME_INPUT = {
    platform: f"{platform}-refresh-token-secret-name" for platform in REFRESH_CAPABLE_PLATFORMS
}

PLATFORM_REFRESH_REQUIRED_ENV = {
    "youtube": (
        "YOUTUBE_CLIENT_ID",
        "YOUTUBE_CLIENT_SECRET",
        "YOUTUBE_REFRESH_TOKEN",
    ),
    "facebook": (
        "FACEBOOK_CLIENT_ID",
        "FACEBOOK_CLIENT_SECRET",
        "FACEBOOK_OBJECT_ID",
        "FACEBOOK_REFRESH_TOKEN",
    ),
    "instagram": (
        "INSTAGRAM_CLIENT_ID",
        "INSTAGRAM_CLIENT_SECRET",
        "INSTAGRAM_OBJECT_ID",
        "INSTAGRAM_REFRESH_TOKEN",
    ),
    "linkedin": (
        "LINKEDIN_CLIENT_ID",
        "LINKEDIN_CLIENT_SECRET",
        "LINKEDIN_OBJECT_ID",
        "LINKEDIN_REFRESH_TOKEN",
    ),
    "tiktok": (
        "TIKTOK_CLIENT_KEY",
        "TIKTOK_CLIENT_SECRET",
        "TIKTOK_USERNAME",
        "TIKTOK_REFRESH_TOKEN",
    ),
    "threads": (
        "THREADS_APP_ID",
        "THREADS_APP_SECRET",
        "THREADS_USER_ID",
        "THREADS_REFRESH_TOKEN",
    ),
}

PLATFORM_PREFIXES = {
    "x": "x-",
    "facebook": "facebook-",
    "instagram": "instagram-",
    "linkedin": "linkedin-",
    "discord": "discord-",
    "youtube": "youtube-",
    "tiktok": "tiktok-",
    "threads": "threads-",
    "telegram": "telegram-",
    "whatsapp": "whatsapp-",
}

# Params that are passed through without platform-prefix stripping.
COMMON_PARAMS = frozenset(
    {
        "text",
        "link",
        "image-1",
        "image-2",
        "image-3",
        "image-4",
        "post-id",
        "profile-id",
        "video-url",
        "video-title",
        "video-description",
        "video-type",
        "video-caption",
        "video-id",
        "title",
        "description",
        "category-id",
        "privacy",
        "keywords",
        "recipient",
        "template-name",
        "language-code",
        "template-components",
        "parse-mode",
        "allow-comments",
        "allow-duet",
        "allow-stitch",
        "auto-add-music",
        "brand-organic",
        "brand-content",
        "github-secret-update-token",
        "platforms",
        *REFRESH_TOKEN_SECRET_NAME_INPUT.values(),
    }
)

# Agoras 2.x reads platform credentials from env on unattended actions.
AUTH_PARAM_ENV_VARS = {
    "x": {
        "consumer-key": "TWITTER_CONSUMER_KEY",
        "consumer-secret": "TWITTER_CONSUMER_SECRET",
        "oauth-token": "TWITTER_OAUTH_TOKEN",
        "oauth-secret": "TWITTER_OAUTH_SECRET",
    },
    "facebook": {
        "client-id": "FACEBOOK_CLIENT_ID",
        "client-secret": "FACEBOOK_CLIENT_SECRET",
        "refresh-token": "FACEBOOK_REFRESH_TOKEN",
        "object-id": "FACEBOOK_OBJECT_ID",
        "app-id": "FACEBOOK_APP_ID",
        "access-token": "FACEBOOK_ACCESS_TOKEN",
    },
    "instagram": {
        "client-id": "INSTAGRAM_CLIENT_ID",
        "client-secret": "INSTAGRAM_CLIENT_SECRET",
        "refresh-token": "INSTAGRAM_REFRESH_TOKEN",
        "object-id": "INSTAGRAM_OBJECT_ID",
        "access-token": "INSTAGRAM_ACCESS_TOKEN",
    },
    "linkedin": {
        "client-id": "LINKEDIN_CLIENT_ID",
        "client-secret": "LINKEDIN_CLIENT_SECRET",
        "refresh-token": "LINKEDIN_REFRESH_TOKEN",
        "object-id": "LINKEDIN_OBJECT_ID",
        "access-token": "LINKEDIN_ACCESS_TOKEN",
    },
    "discord": {
        "bot-token": "DISCORD_BOT_TOKEN",
        "server-name": "DISCORD_SERVER_NAME",
        "channel-name": "DISCORD_CHANNEL_NAME",
    },
    "youtube": {
        "client-id": "YOUTUBE_CLIENT_ID",
        "client-secret": "YOUTUBE_CLIENT_SECRET",
        "refresh-token": "YOUTUBE_REFRESH_TOKEN",
        "access-token": "YOUTUBE_ACCESS_TOKEN",
    },
    "tiktok": {
        "client-key": "TIKTOK_CLIENT_KEY",
        "client-secret": "TIKTOK_CLIENT_SECRET",
        "refresh-token": "TIKTOK_REFRESH_TOKEN",
        "username": "TIKTOK_USERNAME",
        "access-token": "TIKTOK_ACCESS_TOKEN",
    },
    "threads": {
        "app-id": "THREADS_APP_ID",
        "app-secret": "THREADS_APP_SECRET",
        "refresh-token": "THREADS_REFRESH_TOKEN",
        "user-id": "THREADS_USER_ID",
        "access-token": "THREADS_ACCESS_TOKEN",
    },
    "telegram": {
        "bot-token": "TELEGRAM_BOT_TOKEN",
        "chat-id": "TELEGRAM_CHAT_ID",
    },
    "whatsapp": {
        "access-token": "WHATSAPP_ACCESS_TOKEN",
        "phone-number-id": "WHATSAPP_PHONE_NUMBER_ID",
        "business-account-id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
    },
}


def normalize_network(network):
    if network == "twitter":
        return "x"
    return network


def strip_platform_prefix(key, network):
    prefix = PLATFORM_PREFIXES.get(network, f"{network}-")
    if key.startswith(prefix):
        return key[len(prefix) :]
    return key


def translate_params(params, network, action):
    normalized = {}
    for key, value in params.items():
        if key in RESERVED_KEYS or not value:
            continue
        normalized[key] = value

    translated = {}
    prefix = PLATFORM_PREFIXES.get(network, f"{network}-")
    for key, value in normalized.items():
        if key in COMMON_PARAMS or not key.startswith(prefix):
            translated[key] = value
        else:
            translated[strip_platform_prefix(key, network)] = value

    if network == "youtube" and action in ("like", "delete") and "post-id" in translated:
        translated["video-id"] = translated.pop("post-id")

    return translated


def split_cli_and_env_params(network, cli_params):
    env_map = AUTH_PARAM_ENV_VARS.get(network, {})
    cli_only = {}
    env_vars = {}
    for key, value in cli_params.items():
        env_key = env_map.get(key)
        if env_key:
            env_vars[env_key] = value
        else:
            cli_only[key] = value
    return cli_only, env_vars


def build_argv(network, action, params):
    network = normalize_network(network)
    cli_params, _env_vars = prepare_cli_and_env(network, action, params)

    argv = [network, action]
    for key, value in cli_params.items():
        argv.extend([f"--{key}", value])
    return argv


def prepare_cli_and_env(network, action, params):
    network = normalize_network(network)
    cli_params = translate_params(params, network, action)
    return split_cli_and_env_params(network, cli_params)


def build_env(network, action, params):
    _cli_params, env_vars = prepare_cli_and_env(network, action, params)
    return env_vars


def execute(network, action, params):
    from agoras.cli.main import main

    network = normalize_network(network)
    argv = build_argv(network, action, params)
    env_vars = build_env(network, action, params)

    previous = {key: os.environ.get(key) for key in env_vars}
    try:
        os.environ.update(env_vars)
        main(argv)
    finally:
        for key in env_vars:
            if previous[key] is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = previous[key]


def parse_payload(payload):
    paramstore = {}
    for element in payload:
        parts = element.split("=", 1)
        if len(parts) != 2:
            continue
        param, value = parts
        value = value.replace('"', "")
        if param and value:
            paramstore[param] = value
    return paramstore


def validate_action(action):
    if action not in ALL_ACTIONS:
        raise ValueError(f'Invalid action "{action}"')


def parse_platforms_filter(params):
    raw = params.get("platforms", "").strip()
    if not raw:
        return None
    platforms = {normalize_network(p.strip()) for p in raw.split(",") if p.strip()}
    return platforms


def parse_secret_name_mappings(params):
    mappings = {}
    for platform, input_name in REFRESH_TOKEN_SECRET_NAME_INPUT.items():
        value = params.get(input_name, "").strip()
        if value:
            mappings[platform] = value
    return mappings


def collect_refresh_env(params):
    platform_envs = {platform: {} for platform in REFRESH_CAPABLE_PLATFORMS}
    for platform in REFRESH_CAPABLE_PLATFORMS:
        prefix = PLATFORM_PREFIXES[platform]
        scoped = {}
        for key, value in params.items():
            if key.startswith(prefix):
                scoped[strip_platform_prefix(key, platform)] = value
        _cli_only, env_vars = split_cli_and_env_params(platform, scoped)
        platform_envs[platform].update(env_vars)
    return platform_envs


def platform_refresh_complete(platform, env):
    required = PLATFORM_REFRESH_REQUIRED_ENV[platform]
    return all(env.get(key) for key in required)


def mask_sensitive_values(params):
    write_token = params.get("github-secret-update-token")
    if write_token:
        print(f"::add-mask::{write_token}")
    for platform in REFRESH_CAPABLE_PLATFORMS:
        prefix = PLATFORM_PREFIXES[platform]
        refresh_key = f"{prefix}refresh-token"
        value = params.get(refresh_key)
        if value:
            print(f"::add-mask::{value}")


def run_refresh_credentials(params):
    from refresh_credentials import run_refresh

    mask_sensitive_values(params)
    platform_envs = collect_refresh_env(params)
    secret_names = parse_secret_name_mappings(params)
    write_token = params.get("github-secret-update-token", "").strip()
    platforms_filter = parse_platforms_filter(params)

    network = params.get("network", "").strip()
    if network:
        network = normalize_network(network)
        if platforms_filter is None:
            platforms_filter = {network}
        else:
            platforms_filter = platforms_filter | {network}

    if secret_names and not write_token:
        raise ValueError("github-secret-update-token is required when refresh-token secret names are configured")

    eligible = {}
    eligible_secrets = {}
    for platform in REFRESH_CAPABLE_PLATFORMS:
        env = platform_envs[platform]
        if platforms_filter and platform not in platforms_filter:
            continue
        if not platform_refresh_complete(platform, env):
            continue
        eligible[platform] = env
        eligible_secrets[platform] = secret_names.get(platform)

    requested_filter = bool(platforms_filter) or bool(network)
    if requested_filter and not eligible:
        raise ValueError("No refresh-capable platforms matched the filter with complete credentials")

    return run_refresh(eligible, eligible_secrets, write_token)


def run_from_payload(payload):
    paramstore = parse_payload(payload)
    action = paramstore.get("action", "")
    validate_action(action)

    if action == REFRESH_ACTION:
        exit_code = run_refresh_credentials(paramstore)
        if exit_code:
            sys.exit(exit_code)
        return

    network = paramstore.get("network", "")
    if not network:
        raise ValueError("network is required for social actions")

    if action in LOOPABLE_ACTIONS:
        post_ids = paramstore.get("post-id", "")
        if not post_ids:
            raise ValueError(f'post-id is required for action "{action}"')
        for post_id in post_ids.split(","):
            params = dict(paramstore)
            params["post-id"] = post_id.strip()
            execute(network, action, params)
    else:
        execute(network, action, paramstore)


if __name__ == "__main__":
    run_from_payload(sys.argv[1:])
