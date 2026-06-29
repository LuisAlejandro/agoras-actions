#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
from unittest.mock import patch

from execute import (
    build_argv,
    build_env,
    execute,
    normalize_network,
    parse_payload,
    run_from_payload,
    translate_params,
    validate_action,
)


class TestNormalizeNetwork(unittest.TestCase):
    def test_twitter_maps_to_x(self):
        self.assertEqual(normalize_network('twitter'), 'x')

    def test_x_unchanged(self):
        self.assertEqual(normalize_network('x'), 'x')


class TestBuildArgv(unittest.TestCase):
    def test_x_post_omits_auth_flags_from_argv(self):
        argv = build_argv('x', 'post', {
            'network': 'x',
            'action': 'post',
            'x-consumer-key': 'key',
            'text': 'hello',
        })
        self.assertEqual(argv, ['x', 'post', '--text', 'hello'])
        self.assertNotIn('--consumer-key', argv)

    def test_x_post_maps_auth_to_env(self):
        env = build_env('x', 'post', {
            'x-consumer-key': 'key',
            'x-consumer-secret': 'sec',
            'x-oauth-token': 'tok',
            'x-oauth-secret': 'osec',
        })
        self.assertEqual(env, {
            'TWITTER_CONSUMER_KEY': 'key',
            'TWITTER_CONSUMER_SECRET': 'sec',
            'TWITTER_OAUTH_TOKEN': 'tok',
            'TWITTER_OAUTH_SECRET': 'osec',
        })

    def test_youtube_like_maps_post_id_to_video_id(self):
        params = translate_params(
            {'post-id': 'abc123'},
            'youtube',
            'like',
        )
        self.assertEqual(params, {'video-id': 'abc123'})

    def test_facebook_post_omits_auth_flags_from_argv(self):
        argv = build_argv('facebook', 'post', {
            'network': 'facebook',
            'action': 'post',
            'text': 'hello',
            'image-1': 'http://img',
            'facebook-client-id': 'cid',
            'facebook-client-secret': 'sec',
            'facebook-object-id': 'oid',
            'facebook-refresh-token': 'tok',
        })
        self.assertEqual(argv[:2], ['facebook', 'post'])
        self.assertIn('--text', argv)
        self.assertIn('--image-1', argv)
        self.assertNotIn('--client-id', argv)
        self.assertNotIn('--client-secret', argv)
        self.assertNotIn('--object-id', argv)
        self.assertNotIn('--refresh-token', argv)

    def test_facebook_post_maps_auth_to_env(self):
        env = build_env('facebook', 'post', {
            'facebook-client-id': 'cid',
            'facebook-client-secret': 'sec',
            'facebook-object-id': 'oid',
            'facebook-refresh-token': 'tok',
        })
        self.assertEqual(env, {
            'FACEBOOK_CLIENT_ID': 'cid',
            'FACEBOOK_CLIENT_SECRET': 'sec',
            'FACEBOOK_OBJECT_ID': 'oid',
            'FACEBOOK_REFRESH_TOKEN': 'tok',
        })

    def test_linkedin_post_omits_auth_flags_from_argv(self):
        argv = build_argv('linkedin', 'post', {
            'text': 'hello',
            'linkedin-client-id': 'cid',
            'linkedin-client-secret': 'sec',
            'linkedin-object-id': 'oid',
            'linkedin-refresh-token': 'tok',
        })
        self.assertEqual(argv, ['linkedin', 'post', '--text', 'hello'])
        self.assertEqual(build_env('linkedin', 'post', {
            'linkedin-client-id': 'cid',
            'linkedin-client-secret': 'sec',
            'linkedin-object-id': 'oid',
            'linkedin-refresh-token': 'tok',
        }), {
            'LINKEDIN_CLIENT_ID': 'cid',
            'LINKEDIN_CLIENT_SECRET': 'sec',
            'LINKEDIN_OBJECT_ID': 'oid',
            'LINKEDIN_REFRESH_TOKEN': 'tok',
        })

    def test_discord_post_maps_auth_to_env(self):
        argv = build_argv('discord', 'post', {
            'text': 'hello',
            'discord-bot-token': 'token',
            'discord-server-name': 'srv',
            'discord-channel-name': 'chan',
        })
        self.assertEqual(argv, ['discord', 'post', '--text', 'hello'])
        self.assertEqual(build_env('discord', 'post', {
            'discord-bot-token': 'token',
            'discord-server-name': 'srv',
            'discord-channel-name': 'chan',
        }), {
            'DISCORD_BOT_TOKEN': 'token',
            'DISCORD_SERVER_NAME': 'srv',
            'DISCORD_CHANNEL_NAME': 'chan',
        })


class TestParsePayload(unittest.TestCase):
    def test_parses_key_value_pairs(self):
        result = parse_payload(['network=x', 'action=post', 'text=hello'])
        self.assertEqual(result['network'], 'x')
        self.assertEqual(result['action'], 'post')
        self.assertEqual(result['text'], 'hello')

    def test_skips_empty_values(self):
        result = parse_payload(['network=x', 'action=post', 'text='])
        self.assertNotIn('text', result)


class TestExecute(unittest.TestCase):
    @patch('agoras.cli.main.main')
    def test_execute_delegates_to_agoras_main(self, mock_main):
        seen = {}

        def capture_env(argv):
            seen['argv'] = argv
            seen['env'] = os.environ.get('TWITTER_CONSUMER_KEY')

        mock_main.side_effect = capture_env
        execute('x', 'post', {
            'network': 'x',
            'action': 'post',
            'x-consumer-key': 'key',
            'text': 'hello',
        })
        mock_main.assert_called_once()
        self.assertEqual(seen['argv'], ['x', 'post', '--text', 'hello'])
        self.assertEqual(seen['env'], 'key')
        self.assertIsNone(os.environ.get('TWITTER_CONSUMER_KEY'))

    @patch('agoras.cli.main.main')
    def test_execute_sets_facebook_auth_env(self, mock_main):
        seen = {}

        def capture_env(argv):
            seen['argv'] = argv
            seen['env'] = {
                'FACEBOOK_CLIENT_ID': os.environ.get('FACEBOOK_CLIENT_ID'),
                'FACEBOOK_OBJECT_ID': os.environ.get('FACEBOOK_OBJECT_ID'),
            }

        mock_main.side_effect = capture_env
        execute('facebook', 'post', {
            'text': 'hello',
            'facebook-client-id': 'cid',
            'facebook-client-secret': 'sec',
            'facebook-object-id': 'oid',
            'facebook-refresh-token': 'tok',
        })
        mock_main.assert_called_once()
        self.assertEqual(seen['argv'], ['facebook', 'post', '--text', 'hello'])
        self.assertEqual(seen['env']['FACEBOOK_CLIENT_ID'], 'cid')
        self.assertEqual(seen['env']['FACEBOOK_OBJECT_ID'], 'oid')
        self.assertIsNone(os.environ.get('FACEBOOK_CLIENT_ID'))


class TestRunFromPayload(unittest.TestCase):
    @patch('agoras.cli.main.main')
    def test_run_from_payload_github_style_quoted_args(self, mock_main):
        seen = {}

        def capture_env(argv):
            seen['argv'] = argv
            seen['env'] = os.environ.get('TWITTER_CONSUMER_KEY')

        mock_main.side_effect = capture_env
        run_from_payload([
            'network=x',
            'action=post',
            'text="hello"',
            'x-consumer-key="key"',
        ])
        mock_main.assert_called_once()
        self.assertEqual(seen['argv'], ['x', 'post', '--text', 'hello'])
        self.assertEqual(seen['env'], 'key')


class TestValidateAction(unittest.TestCase):
    def test_invalid_action_raises(self):
        with self.assertRaisesRegex(ValueError, 'not-real'):
            validate_action('not-real')

    def test_rejects_authorize_action(self):
        with self.assertRaisesRegex(ValueError, 'authorize'):
            validate_action('authorize')

    def test_rejects_feed_action(self):
        with self.assertRaisesRegex(ValueError, 'last-from-feed'):
            validate_action('last-from-feed')

    def test_rejects_schedule_action(self):
        with self.assertRaisesRegex(ValueError, 'schedule'):
            validate_action('schedule')


class TestLoopableActions(unittest.TestCase):
    @patch('agoras.cli.main.main')
    def test_like_invokes_main_per_post_id(self, mock_main):
        run_from_payload([
            'network=x',
            'action=like',
            'post-id="a,b,c"',
            'x-consumer-key="key"',
        ])
        self.assertEqual(mock_main.call_count, 3)
        post_ids = [call.args[0][call.args[0].index('--post-id') + 1]
                    for call in mock_main.call_args_list]
        self.assertEqual(post_ids, ['a', 'b', 'c'])

    @patch('agoras.cli.main.main')
    def test_loopable_without_post_id_raises(self, mock_main):
        with self.assertRaisesRegex(ValueError, 'post-id is required'):
            run_from_payload([
                'network=x',
                'action=like',
                'x-consumer-key="key"',
            ])
        mock_main.assert_not_called()


class TestAgorasImportSmoke(unittest.TestCase):
    def test_agoras_main_is_callable(self):
        from agoras.cli.main import main
        self.assertTrue(callable(main))


if __name__ == '__main__':
    unittest.main()
