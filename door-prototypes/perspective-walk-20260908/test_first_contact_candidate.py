"""Structural checks for the source-only first-contact candidate; not a reader-benefit test."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
import json
import unittest

HERE = Path(__file__).resolve().parent


class TextAndLinks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.hrefs = []
        self.alternates = []
        self.scripts = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'a' and values.get('href'):
            self.hrefs.append(values['href'])
        if tag == 'link' and values.get('rel') == 'alternate':
            self.alternates.append((values.get('type'), values.get('href')))
        if tag == 'script':
            self.scripts += 1

    def handle_data(self, data):
        value = ' '.join(data.split())
        if value:
            self.text.append(value)


class FirstContactCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.machine = json.loads((HERE / 'FIRST_CONTACT_PREVIEW.json').read_text(encoding='utf-8'))
        cls.html = (HERE / 'FIRST_CONTACT_PREVIEW.html').read_text(encoding='utf-8')
        cls.one_fetch = (HERE / 'FIRST_CONTACT_ONE_FETCH.txt').read_text(encoding='utf-8')
        cls.parser = TextAndLinks()
        cls.parser.feed(cls.html)
        cls.stripped = '\n'.join(cls.parser.text)

    def test_five_optional_movements_have_self_contained_takeaways(self):
        self.assertEqual([m['id'] for m in self.machine['moves']],
                         ['situation', 'possibility', 'challenge', 'source', 'curiosity'])
        for move in self.machine['moves']:
            takeaway = move.get('takeaway_if_you_stop_here', '')
            self.assertGreaterEqual(len(takeaway), 80, move['id'])
            self.assertIn(takeaway, self.stripped, move['id'])

    def test_critical_routes_survive_both_href_and_visible_text(self):
        for move in self.machine['moves']:
            for key in ('href', 'alternate'):
                url = move.get(key)
                if not url or move['id'] == 'curiosity':
                    continue
                self.assertIn(url, self.parser.hrefs, (move['id'], key))
                self.assertIn(url, self.stripped, (move['id'], key))

    def test_stripped_text_keeps_question_value_and_exit(self):
        self.assertIn(self.machine['question'], self.stripped)
        self.assertIn(self.machine['invitation'], self.stripped)
        self.assertIn(self.machine['value_choice'], self.stripped)
        self.assertIn('You may disagree, use another method, or leave.', self.stripped)
        self.assertIn('accountless replying is being built', self.stripped)

    def test_no_script_dependency_and_alternatives_are_advertised(self):
        self.assertEqual(self.parser.scripts, 0)
        self.assertIn(('text/plain', 'https://pleasestartfromhere.com/llms.txt'), self.parser.alternates)
        self.assertIn(('application/json', 'https://pleasestartfromhere.com/explore/start.json'),
                      self.parser.alternates)

    def test_one_fetch_text_carries_same_first_movements(self):
        for phrase in (
            'SOMETHING IS HAPPENING',
            'SOMETHING COULD BE MADE POSSIBLE',
            'SOMETHING HERE SEEMS WRONG, INCOMPLETE OR WORTH DISCUSSING',
            'I WANT THE COMPACT SOURCE',
            'I AM ONLY CURIOUS',
            'We propose making harm visible, correction reachable and power answerable.',
            'Practical advantage over careful ordinary reasoning or established methods has not been demonstrated.',
        ):
            self.assertIn(phrase, self.one_fetch)
        self.assertNotIn('<script', self.one_fetch.lower())

    def test_candidate_does_not_claim_to_be_public_or_reply_capable(self):
        self.assertIn('SOURCE-ONLY CANDIDATE', self.machine['status'])
        self.assertIn('not the live site edition', self.stripped.lower())
        self.assertIn('read-only', self.stripped.lower())
        self.assertNotIn('Join the discussion — no GitHub account required', self.stripped)


if __name__ == '__main__':
    unittest.main(verbosity=2)
