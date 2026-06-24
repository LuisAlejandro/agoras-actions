#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch

from execute import (
    build_argv,
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
    def test_x_post_platform_command(self):
        argv = build_argv('x', 'post', {
            'network': 'x',
            'action': 'post',
            'x-consumer-key': 'key',
            'text': 'hello',
        })
        self.assertEqual(argv[:3], ['x', 'post', '--consumer-key'])
        self.assertIn('--text', argv)
        self.assertIn('hello', argv)
        self.assertNotIn('--x-consumer-key', argv)

    def test_feed_publish_utils_command(self):
        argv = build_argv('facebook', 'last-from-feed', {
            'network': 'facebook',
            'action': 'last-from-feed',
            'feed-url': 'https://example.com/feed.xml',
            'facebook-object-id': '123',
        })
        self.assertEqual(argv[:6], ['utils', 'feed-publish', '--network', 'facebook', '--mode', 'last'])
        self.assertIn('--feed-url', argv)
        self.assertIn('--facebook-object-id', argv)
        self.assertIn('123', argv)

    def test_schedule_run(self):
        argv = build_argv('', 'schedule', {
            'action': 'schedule',
            'sheets-id': 'sheet123',
            'sheets-name': 'Schedule',
            'sheets-client-email': 'svc@example.com',
            'sheets-private-key': 'key',
        })
        self.assertEqual(argv[0], 'utils')
        self.assertEqual(argv[1], 'schedule-run')
        self.assertIn('--sheets-id', argv)

    def test_youtube_like_maps_post_id_to_video_id(self):
        params = translate_params(
            {'post-id': 'abc123'},
            'youtube',
            'like',
        )
        self.assertEqual(params, {'video-id': 'abc123'})


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
        execute('x', 'post', {
            'network': 'x',
            'action': 'post',
            'x-consumer-key': 'key',
            'text': 'hello',
        })
        mock_main.assert_called_once()
        argv = mock_main.call_args[0][0]
        self.assertEqual(argv[:2], ['x', 'post'])
        self.assertIn('--consumer-key', argv)
        self.assertIn('key', argv)
        self.assertIn('--text', argv)
        self.assertIn('hello', argv)
        self.assertNotIn('--x-consumer-key', argv)


class TestRunFromPayload(unittest.TestCase):
    @patch('agoras.cli.main.main')
    def test_run_from_payload_github_style_quoted_args(self, mock_main):
        run_from_payload([
            'network=x',
            'action=post',
            'text="hello"',
            'x-consumer-key="key"',
        ])
        mock_main.assert_called_once()
        argv = mock_main.call_args[0][0]
        self.assertEqual(argv[:2], ['x', 'post'])
        self.assertIn('--text', argv)
        self.assertIn('hello', argv)
        self.assertIn('--consumer-key', argv)
        self.assertIn('key', argv)


class TestValidateAction(unittest.TestCase):
    def test_invalid_action_raises(self):
        with self.assertRaisesRegex(ValueError, 'not-real'):
            validate_action('not-real')


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
