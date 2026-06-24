#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

RESERVED_KEYS = frozenset({'network', 'action'})

LOOPABLE_ACTIONS = frozenset({'like', 'share', 'delete'})
PLATFORM_ACTIONS = frozenset({'post', 'like', 'share', 'delete', 'video', 'authorize', 'template'})
FEED_ACTIONS = frozenset({'last-from-feed', 'random-from-feed'})
SCHEDULE_ACTIONS = frozenset({'schedule'})
UTILS_ACTIONS = FEED_ACTIONS | SCHEDULE_ACTIONS
ALL_ACTIONS = PLATFORM_ACTIONS | UTILS_ACTIONS

PLATFORM_PREFIXES = {
    'x': 'x-',
    'facebook': 'facebook-',
    'instagram': 'instagram-',
    'linkedin': 'linkedin-',
    'discord': 'discord-',
    'youtube': 'youtube-',
    'tiktok': 'tiktok-',
    'threads': 'threads-',
    'telegram': 'telegram-',
    'whatsapp': 'whatsapp-',
}

SHEETS_LEGACY_MAP = {
    'google-sheets-id': 'sheets-id',
    'google-sheets-name': 'sheets-name',
    'google-sheets-client-email': 'sheets-client-email',
    'google-sheets-private-key': 'sheets-private-key',
}

# Params that are passed through without platform-prefix stripping.
COMMON_PARAMS = frozenset({
    'text', 'link', 'image-1', 'image-2', 'image-3', 'image-4',
    'post-id', 'profile-id', 'video-url', 'video-title', 'video-description',
    'video-type', 'video-caption', 'video-id', 'title', 'description',
    'category-id', 'privacy', 'keywords', 'recipient', 'template-name',
    'language-code', 'template-components', 'parse-mode',
    'feed-url', 'max-count', 'post-lookback', 'max-post-age',
    'sheets-id', 'sheets-name', 'sheets-client-email', 'sheets-private-key',
    'allow-comments', 'allow-duet', 'allow-stitch', 'auto-add-music',
    'brand-organic', 'brand-content',
})


def normalize_network(network):
    if network == 'twitter':
        return 'x'
    return network


def is_utils_action(action):
    return action in UTILS_ACTIONS


def strip_platform_prefix(key, network):
    prefix = PLATFORM_PREFIXES.get(network, f'{network}-')
    if key.startswith(prefix):
        return key[len(prefix):]
    return key


def translate_params(params, network, action):
    normalized = {}
    for key, value in params.items():
        if key in RESERVED_KEYS or not value:
            continue
        if key in SHEETS_LEGACY_MAP:
            key = SHEETS_LEGACY_MAP[key]
        normalized[key] = value

    if is_utils_action(action):
        return normalized

    translated = {}
    prefix = PLATFORM_PREFIXES.get(network, f'{network}-')
    for key, value in normalized.items():
        if key in COMMON_PARAMS or not key.startswith(prefix):
            translated[key] = value
        else:
            translated[strip_platform_prefix(key, network)] = value

    if network == 'youtube' and action in ('like', 'delete') and 'post-id' in translated:
        translated['video-id'] = translated.pop('post-id')

    return translated


def build_argv(network, action, params):
    network = normalize_network(network)
    cli_params = translate_params(params, network, action)

    if action in FEED_ACTIONS:
        mode = 'last' if action == 'last-from-feed' else 'random'
        argv = ['utils', 'feed-publish', '--network', network, '--mode', mode]
    elif action in SCHEDULE_ACTIONS:
        argv = ['utils', 'schedule-run']
        if network:
            argv.extend(['--network', network])
    else:
        argv = [network, action]

    for key, value in cli_params.items():
        argv.extend([f'--{key}', value])
    return argv


def execute(network, action, params):
    from agoras.cli.main import main

    argv = build_argv(network, action, params)
    main(argv)


def parse_payload(payload):
    paramstore = {}
    for element in payload:
        parts = element.split('=', 1)
        if len(parts) != 2:
            continue
        param, value = parts
        value = value.replace('"', '')
        if param and value:
            paramstore[param] = value
    return paramstore


def validate_action(action):
    if action not in ALL_ACTIONS:
        raise ValueError(f'Invalid action "{action}"')


def run_from_payload(payload):
    paramstore = parse_payload(payload)
    network = paramstore.get('network', '')
    action = paramstore.get('action', '')
    validate_action(action)

    if action in LOOPABLE_ACTIONS:
        post_ids = paramstore.get('post-id', '')
        if not post_ids:
            raise ValueError(f'post-id is required for action "{action}"')
        for post_id in post_ids.split(','):
            params = dict(paramstore)
            params['post-id'] = post_id.strip()
            execute(network, action, params)
    else:
        execute(network, action, paramstore)


if __name__ == '__main__':
    run_from_payload(sys.argv[1:])
