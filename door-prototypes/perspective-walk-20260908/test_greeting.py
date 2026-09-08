"""Greeting placement and preservation checks, not an engagement experiment."""
from __future__ import annotations
import hashlib
import html
import json
import unittest
from unittest.mock import patch
import build


class GreetingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, _ = build.generate()
        cls.start = json.loads(cls.files['explore/start.json'])

    def test_same_greeting_in_machine_and_text_entrances(self):
        self.assertEqual(build.GREETING, self.start['greeting'])
        for name in ('index.md', 'index.txt', 'index.html', 'llms.txt'):
            text = self.files['explore/' + name].decode('utf-8')
            for value in build.GREETING.values():
                self.assertEqual(text.count(value), 1, (name, value))

    def test_question_is_an_invitation_not_required_identity(self):
        self.assertEqual('Hello. What are you trying to understand, change, or keep possible?',
                         self.start['greeting']['question'])
        self.assertIn('No introduction or agreement is required.',
                      self.start['greeting']['invitation'])
        self.assertIn('A reader may stop, disagree or use a better account.', self.start['boundary'])

    def test_reply_boundary_keeps_actual_access_limits(self):
        self.assertIn('does not receive replies', self.start['greeting']['reply_boundary'])
        self.assertEqual(self.start['routes']['challenge'], 'challenge.md')
        challenge = self.files['explore/challenge.md'].decode('utf-8')
        self.assertIn('posting needs a GitHub account', challenge)
        self.assertIn('No response time is promised', challenge)

    def test_greeting_does_not_change_prior_arrival_fields(self):
        previous = {k: v for k, v in self.start.items() if k != 'greeting'}
        # The exact preceding start.json from source 323a3fa9, not a prose comparison.
        expected = '69b9b3c8b2f26e91bb73e4912010342658b58b6f057926b81cb33c07a9d69024'
        self.assertEqual(hashlib.sha256(build.encode(previous)).hexdigest(), expected)
        self.assertLessEqual(len(self.files['explore/start.json']), 2048)

    def test_packets_remain_byte_identical(self):
        expected = {
            'packet.json': 'ba80aefb5756aad5d85a626fd1c4ed49f09088906547d3db5ede5805efb0c279',
            'packet.md': '0800e408b7d73bc674ddcfee0c403f51a91ebd51c253362ddd9f91a96d102a76',
        }
        for name, digest in expected.items():
            self.assertEqual(hashlib.sha256(self.files['explore/' + name]).hexdigest(), digest)

    def test_oversized_welcome_is_rejected_not_truncated(self):
        with patch.dict(build.GREETING, {'question': 'x' * 2500}):
            with self.assertRaisesRegex(ValueError, 'Small-entry byte budget exceeded'):
                build.generate()

    def test_html_welcome_is_escaped(self):
        payload = '<script>alert("not executed")</script>'
        with patch.dict(build.GREETING, {'question': payload}):
            files, _ = build.generate()
        rendered = files['explore/index.html'].decode('utf-8')
        self.assertNotIn(payload, rendered)
        self.assertIn(html.escape(payload), rendered)
        self.assertEqual(json.loads(files['explore/start.json'])['greeting']['question'], payload)


if __name__ == '__main__':
    unittest.main(verbosity=2)
