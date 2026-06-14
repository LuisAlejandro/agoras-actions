#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from execute import build_argv, normalize_network, parse_payload, translate_params


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


if __name__ == '__main__':
    unittest.main()
