"""Structural regression only; not a claim that a reader understands the page."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import subprocess
import unittest
import hashlib
import json
from collections import Counter
import re

ROOT = Path(__file__).resolve().parents[1]
PUBLISHED = ROOT.parent / 'DEV' / 'campfire-door-pages'
BASELINE = '50caedc89646b7337a86a5610cef24426b518cf3'


class Reading(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.text, self.links, self.alternates, self.tags = [], [], [], []
        self.sections, self.open_sections = [], []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if tag == 'section':
            section = {'attrs': attrs, 'tags': [], 'text': []}
            self.sections.append(section)
            self.open_sections.append(section)
        for section in self.open_sections:
            section['tags'].append(tag)
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if tag == 'link' and attrs.get('rel') == 'alternate':
            self.alternates.append((attrs.get('type'), attrs.get('href')))

    def handle_data(self, data):
        self.text.append(data)
        for section in self.open_sections:
            section['text'].append(data)

    def handle_endtag(self, tag):
        if tag == 'section':
            self.open_sections.pop()


class FirstContactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / 'out/index.html').read_text(encoding='utf-8')
        cls.page = Reading(cls.html)
        cls.text = ' '.join(' '.join(cls.page.text).split())

    def test_primary_title_and_optional_attributed_artwork(self):
        self.assertEqual(self.html.count('<h1>'), 1)
        self.assertIn('<h1>Please Start From Here</h1>', self.html)
        self.assertIn('<p class="guiding-question">How can we make a better future?</p>', self.html)
        record = json.loads((ROOT / 'out/art/camp-fire.json').read_text(encoding='utf-8'))
        image = (ROOT / 'out/art/camp-fire.jpg').read_bytes()
        self.assertEqual(hashlib.sha256(image).hexdigest(), record['sha256'])
        self.assertEqual(len(image), record['bytes'])
        self.assertIn('src="/art/camp-fire-720.jpg"', self.html)
        self.assertIn('alt="' + record['alt'] + '"', self.html)
        self.assertIn('loading="eager"', self.html)
        self.assertIn('srcSet="', self.html)
        self.assertIn(' sizes="', self.html)
        self.assertLess(self.html.index('<figcaption'), self.html.index('<img'))
        # The editorial revision moves the same art into the opening composition.
        # Direct reading routes precede it; the original detailed choices remain.
        self.assertLess(self.html.index('aria-label="Reading routes"'), self.html.index('<figure'))
        self.assertLess(self.html.index('<figure'), self.html.index('class="first-movements"'))
        navigation = self.html.split('aria-label="Reading routes"')[1].split('</nav>')[0]
        for target in ['/explore/', '/resources/mechanical-ethics/MECHANICAL_ETHICS.pdf', '/discussion/']:
            self.assertIn(target, navigation)
        for link in [record['object_url'], record['rights_url'], record['biography_url'], '#winslow-homer', '/art/camp-fire.json']:
            self.assertIn(link, self.page.links)
        self.assertIn(record['credit'], self.text)
        manifest = json.loads((ROOT / 'out/manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['routes']['artwork'], '/art/camp-fire.json')
        self.assertEqual(manifest['provenance']['artwork']['image_sha256'], record['sha256'])
        self.assertNotIn('teaching_preview', manifest['provenance'])

    def test_editorial_layout_preserves_all_original_paragraphs_and_headings(self):
        original = subprocess.check_output(['git', 'show', 'e0d765b3d203035971b5fa544eb5f5b48cc0f518:index.html'], cwd=PUBLISHED).decode('utf-8')
        def blocks(html):
            # Compare substantive blocks independently of authorised relocation.
            values = []
            for block in re.findall(r'<(?:p|h[1-4])\b[^>]*>(.*?)</(?:p|h[1-4])>', html, re.S):
                text = ' '.join(' '.join(Reading(block).text).split())
                values.append(re.sub(r'Preview 0\.8(?:\.\d+)?', 'Preview [edition]', text))
            return Counter(values)
        before, after = blocks(original), blocks(self.html)
        # Only these explicitly reviewed art-provenance paragraphs may differ.
        old_credit = 'The image is reproduced without cropping or alteration from The Met’s original photograph , under its Open Access policy . Image source details . Its use here does not imply endorsement by the artist or museum.'
        new_credit = 'The painting is shown in smaller viewing copies without cropping, retouching or generative alteration. The unchanged local original comes from The Met’s original photograph , under its Open Access policy . Image source details . Its use here does not imply endorsement by the artist or museum.'
        record = json.loads((ROOT / 'out/art/camp-fire.json').read_text(encoding='utf-8'))
        interpretation = 'Why this spoke to us. ' + record['why_this_spoke_to_us']
        self.assertEqual(before[old_credit], 1)
        self.assertEqual(after[new_credit], 1)
        self.assertEqual(after[interpretation], 1)
        before.subtract([old_credit]); after.subtract([new_credit, interpretation])
        self.assertEqual(+before, +after)
        self.assertTrue(set(Reading(original).links).issubset(self.page.links))
        self.assertIn('href="#situation"', self.html.split('</header>')[0])

    def test_viewing_copies_and_offline_identity(self):
        from PIL import Image
        record = json.loads((ROOT / 'out/art/camp-fire.json').read_text(encoding='utf-8'))
        self.assertEqual(record['responsive']['parent_sha256'], record['sha256'])
        self.assertEqual(record['responsive']['parent_local_image'], record['local_image'])
        self.assertEqual([v['width'] for v in record['responsive']['variants']], [720, 1440])
        for variant in record['responsive']['variants']:
            file = ROOT / 'out' / variant['local_image'].lstrip('/')
            self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), variant['sha256'])
            self.assertEqual(file.stat().st_size, variant['bytes'])
            with Image.open(file) as image:
                self.assertEqual(image.size, (variant['width'], variant['height']))
            self.assertLess(variant['bytes'], record['bytes'])
            self.assertIn(f"{variant['local_image']} {variant['width']}w", self.html)
        self.assertIn(record['why_this_spoke_to_us'], self.text)
        offline = (ROOT / 'downloads/Campfire-preview.html').read_text(encoding='utf-8')
        self.assertNotRegex(offline, r'(?i)(?:srcset|imagesrcset|imagesizes)=')
        self.assertIn('src="data:image/jpeg;base64,', offline)
        self.assertNotIn('src="/art/', offline)

    def test_hero_white_text_has_a_conservative_image_contrast_floor(self):
        from PIL import Image
        css = (ROOT / 'app/globals.css').read_text(encoding='utf-8')
        self.assertIn('background: rgba(0,0,0,.74); color: #ffffff;', css)
        self.assertIn('background: #141b20;', css)
        self.assertNotIn('object-fit: cover', css)
        def linear(value):
            value /= 255
            return value / 12.92 if value <= .04045 else ((value + .055) / 1.055) ** 2.4
        record = json.loads((ROOT / 'out/art/camp-fire.json').read_text(encoding='utf-8'))
        for variant in record['responsive']['variants']:
            with Image.open(ROOT / 'out' / variant['local_image'].lstrip('/')) as image:
                # Upper-bound background luminance from actual channel maxima.
                # This is conservative across the complete image, including text
                # positions at other widths, not a measured browser paint result.
                maxima = [upper * .26 for lower, upper in image.getextrema()]
            lum = sum(weight * linear(value) for weight, value in zip((.2126, .7152, .0722), maxima))
            ratio = 1.05 / (lum + .05)
            self.assertGreaterEqual(ratio, 4.5)
            print(f"Hero contrast lower bound {variant['width']}px: {ratio:.2f}:1")

    def test_optional_movements_before_explanation_and_takeaway_before_link(self):
        headings = ['Something is happening', 'Something could be made possible',
                    'Something here seems wrong, incomplete or worth discussing',
                    'I want the compact source', 'I am only curious']
        positions = [self.text.index(h) for h in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertLess(positions[-1], self.text.index('Why this exists'))
        for name in ['situation', 'possibility', 'challenge', 'source', 'curiosity']:
            article = self.html.split(f'<article id="{name}">')[1].split('</article>')[0]
            before_link = Reading(article.split('<a ')[0])
            self.assertGreater(len(' '.join(before_link.text)), 160, name)

    def test_visible_absolute_routes_and_local_targets(self):
        for suffix in ['/explore/', '/explore/nodes/futures.html', '/discussion/',
                       '/explore/start.json', '/read/start.html', '/changes.html']:
            url = 'https://pleasestartfromhere.com' + suffix
            self.assertIn(url, self.text)
            self.assertIn(url, self.page.links)
        for href in self.page.links:
            url = urlparse(href)
            if url.netloc and url.netloc != 'pleasestartfromhere.com':
                continue
            name = url.path.lstrip('/') or 'index.html'
            if name.endswith('/'):
                name += 'index.html'
            self.assertTrue((ROOT / 'out' / name).is_file(), href)

    def test_meaning_changing_limits_and_no_dead_intake(self):
        for phrase in ['How can we make a better future?', 'Site Preview 0.8',
                       'No introduction or agreement is required.',
                       'This is a stated value choice',
                       'You may disagree, use another method, or leave.',
                       'read-only; it does not receive replies yet.',
                       'Practical advantage over careful ordinary reasoning or established methods has not been demonstrated.']:
            self.assertIn(phrase, self.text)
        self.assertTrue({'script', 'form', 'iframe'}.isdisjoint(self.page.tags))
        for mime, path in [('text/plain', '/llms.txt'), ('application/json', '/explore/start.json')]:
            self.assertIn((mime, 'https://pleasestartfromhere.com' + path), self.page.alternates)

    def test_optional_handoff_survives_text_extraction(self):
        self.assertRegex(self.text, r'Visual candidate|Working preview')
        self.assertNotIn('not published', self.text)
        self.assertRegex(self.text, r'(You can|If it helps,) read this yourself,? or hand this address to an AI')
        self.assertIn('No special prompt is required.', self.text)
        self.assertLess(self.text.index('I am only curious'), self.text.index('Another perspective'))
        self.assertLess(self.text.index('Another perspective'), self.text.index('This is a stated value choice'))
        self.assertIn('https://pleasestartfromhere.com/', self.page.links)

    def test_optional_small_loop_after_movements_and_in_machine_reading(self):
        self.assertLess(self.text.index('I am only curious'), self.text.index('Take one useful step'))
        self.assertLess(self.text.index('Take one useful step'), self.text.index('Why this exists'))
        cells = [s for s in self.page.sections if s['attrs'].get('aria-labelledby') == 'small-loop']
        self.assertEqual(len(cells), 1)
        cell = cells[0]
        cell_text = ' '.join(' '.join(cell['text']).split())
        self.assertEqual(cell['tags'].count('li'), 6)
        self.assertEqual(cell['tags'].count('ul'), 1)
        self.assertNotIn('ol', cell['tags'])
        # Explicit optional-use properties, not a general semantic evaluator.
        self.assertRegex(cell_text, r'not a procedure to complete|You do not need to work through all of these')
        self.assertRegex(cell_text, r'Start with whichever helps|Use the question that helps now; skip the rest')
        self.assertRegex(cell_text, r'[Tt]ake one useful piece and leave')
        self.assertIn('A description is not permission.', cell_text)
        disclosure = "These questions reflect this project's value choices, not neutral requirements for reasoning."
        self.assertIn(disclosure, cell_text)
        recurrence = 'The same questions can recur at another depth without requiring the same answer or the same amount of detail.'
        self.assertIn(recurrence, self.text)
        machine = (ROOT / 'out/llms.txt').read_text(encoding='utf-8')
        self.assertNotIn('not published', machine)
        machine_cell = machine.split('## Take one useful step')[1].split('## Project sources')[0]
        self.assertIn(disclosure, machine_cell)
        self.assertIn(recurrence, machine)
        self.assertIn('not a procedure to complete', machine)
        self.assertIn('A description is not permission.', machine)
        self.assertIn('You can take one useful piece and leave.', machine)
        for label in ['Notice', 'Choose', 'Decide', 'Responsibility', 'Repercussions', 'Check and correct']:
            self.assertIn(label + ':', machine)
            self.assertIn(label + '.', cell_text)
        edition = subprocess.check_output(['node', '--input-type=module', '-e', "import {SITE_EDITION} from './scripts/site-edition.mjs';process.stdout.write(SITE_EDITION)"], cwd=ROOT).decode()
        self.assertIn('Site edition: Preview ' + edition, machine)
        self.assertNotIn('Site edition: Preview 0.7', machine)
        self.assertIn('<title>Please Start From Here</title>', self.html)
        self.assertIn('A voluntary starting point for understanding, deciding, making and correcting under uncertainty.', self.html)

    def test_no_old_destination_dropped_and_history_preserved(self):
        def old(name):
            return subprocess.check_output(['git', 'show', BASELINE + ':' + name], cwd=PUBLISHED).decode('utf-8')
        self.assertTrue(set(Reading(old('index.html')).links).issubset(self.page.links))
        original = old('changes.md')
        current = (ROOT / 'public/changes.md').read_text(encoding='utf-8')
        self.assertEqual(current[current.index('Edition 0.5 adds D009'):], original[original.index('Edition 0.5 adds D009'):])


if __name__ == '__main__':
    unittest.main()
