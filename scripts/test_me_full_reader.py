"""PSFH first-screen and full released Mechanical Ethics reader: integrated source custody."""
import hashlib
from html.parser import HTMLParser
from html import unescape
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import render_me_full as render

class Tags(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.images, self.headings, self.ids, self.links, self.tags = [], [], set(), [], []
        self.current_h = None
        self.buffer = []
    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        self.tags.append(tag)
        if "id" in props:
            if props["id"] in self.ids:
                raise AssertionError("Duplicate HTML id: " + props["id"])
            self.ids.add(props["id"])
        if tag == "img":
            self.images.append(props)
        if tag == "a":
            self.links.append(props.get("href",""))
        if tag in ("h1","h2","h3"):
            self.current_h = tag
            self.buffer = []
    def handle_data(self, text):
        if self.current_h:
            self.buffer.append(text)
    def handle_endtag(self, tag):
        if tag == self.current_h:
            self.headings.append((tag, "".join(self.buffer).strip()))
            self.current_h = None

class CompleteBook(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT/"out/read/me-v0.8.html").read_text(encoding="utf-8")
        cls.parsed = Tags()
        cls.parsed.feed(cls.html)
        cls.md = render.SOURCE.read_text(encoding="utf-8")

    def test_exact_source_and_deterministic_render(self):
        self.assertEqual(hashlib.sha256(render.SOURCE.read_bytes()).hexdigest(), render.BOOK_SHA256)
        self.assertEqual(render.produce()[0], (ROOT/"out/read/me-v0.8.html").read_bytes())
        with tempfile.TemporaryDirectory() as tmp:
            changed = Path(tmp)/"altered.md"
            changed.write_text(self.md + "\nUnexpected new words\n",encoding="utf-8")
            with patch.object(render,"SOURCE",changed):
                with self.assertRaisesRegex(ValueError,"Released Mechanical Ethics Markdown changed"):
                    render.produce()

    def test_all_original_headings_and_complete_human_reader(self):
        source_h1 = re.findall(r"^# (.+)$",self.md,re.M)
        source_h2 = re.findall(r"^## (.+)$",self.md,re.M)
        rendered_h1 = [x for h,x in self.parsed.headings if h=="h1"]
        rendered_h2 = [x for h,x in self.parsed.headings if h=="h2"]
        self.assertEqual(rendered_h1,source_h1)
        self.assertEqual(rendered_h2,source_h2)
        self.assertEqual(len(rendered_h1)+len(rendered_h2),55)
        self.assertEqual(rendered_h1[0],"Safety note for a reader inside harm")
        for phrase in ("Author's Note - How This Began","Appendix C - Status, Sources, and the Two-Artifact Pair",
                       "The Saturday Workshop","Privacy Without Dishonesty","A Human Standard for Answerability"):
            self.assertIn(phrase,unescape(self.html))
        self.assertLess(self.html.index("Safety note for a reader inside harm"),
                        self.html.index("Mechanical Ethics: When Correction Arrives Too Late"))

    def test_four_released_diagrams_not_recreated_or_lost(self):
        self.assertEqual(len(self.parsed.images),4)
        for img in self.parsed.images:
            self.assertTrue(img.get("alt"))
            self.assertTrue(img["src"].startswith("/resources/mechanical-ethics/figures/"))
            path=ROOT/"out"/img["src"].lstrip("/")
            self.assertTrue(path.is_file(),str(path))
        self.assertEqual(len(set(x["src"] for x in self.parsed.images)),4)
        for n in range(1,5):
            self.assertIn("Figure "+str(n)+".",self.html)

    def test_nested_book_contents_lists_are_structural_not_only_visual(self):
        class BookListTree(HTMLParser):
            def __init__(self):
                super().__init__()
                self.open = []
                self.nested = 0
            def handle_starttag(self, tag, attrs):
                if tag == "ul":
                    if self.open and self.open[-1] != "li":
                        raise AssertionError("Nested UL has no LI parent")
                    if self.open:
                        self.nested += 1
                    self.open.append("ul")
                elif tag == "li":
                    if not self.open or self.open[-1] != "ul":
                        raise AssertionError("LI missing UL parent")
                    self.open.append("li")
            def handle_endtag(self, tag):
                if tag in ("li", "ul"):
                    if not self.open or self.open[-1] != tag:
                        raise AssertionError("Unbalanced list hierarchy")
                    self.open.pop()
        source = self.html.split('<article aria-label=', 1)[1].split("</article>", 1)[0]
        tree = BookListTree()
        tree.feed(source)
        self.assertEqual(tree.open, [])
        self.assertGreaterEqual(tree.nested, 1)
        self.assertIn("<li>Part I - The Door\n<ul>\n<li>1. A Door You Cannot Reach", source)

    def test_reader_structure_and_no_active_resources(self):
        for bad in ("script","form","iframe","video","audio"):
            self.assertNotIn(bad,self.parsed.tags)
        self.assertIn("#book",self.parsed.links)
        self.assertIn("book",self.parsed.ids)
        self.assertIn("RELEASED BASELINE",self.html)
        self.assertIn("NOT VALIDATED",self.html)
        self.assertIn("v0.8.0",self.html)
        self.assertIn(render.BOOK_COMMIT,self.html)
        self.assertIn("@media print",self.html)
        self.assertIn("@media(max-width:680px)",self.html)
        for link in self.parsed.links:
            if link.startswith("#"):
                self.assertIn(link[1:],self.parsed.ids)

class HumanFirstDoor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home=(ROOT/"out/index.html").read_text(encoding="utf-8")
        cls.css=(ROOT/"out/style.css").read_text(encoding="utf-8")
    def test_original_painting_first_and_orientation_before_story(self):
        h=self.home
        self.assertEqual(h.count('id="human-door-title"'),1)
        art=h.index('class="art-hero"')
        title=h.index('Please Start From <em>Here</em>')
        credit=h.index('id="camp-fire-credit"')
        door=h.index('class="human-first-door"')
        story=h.index('id="step-story"')
        self.assertLess(art, credit)
        self.assertLess(credit, door)
        self.assertLess(title, door)
        self.assertLess(door, story)
        self.assertEqual(h.count('<h1>Please Start From <em>Here</em></h1>'),1)
        self.assertIn('href="/read/me-v0.8.html"',h)
        self.assertIn('>Complete HTML book</a>',h)
        self.assertIn('>Original Markdown</a>',h)
        for target in ('#step-story','#project','/llms.txt'):
            self.assertIn('href="'+target+'"',h)

    def test_reachable_support_status_are_after_art_and_before_story(self):
        h=self.home
        art=h.index('class="art-hero"')
        details=h.index('id="human-door-limits"')
        story=h.index('id="step-story"')
        self.assertLess(art,details)
        self.assertLess(details,story)
        self.assertIn('<summary>Limits, source status, and help with a housing problem now</summary>',h)
        self.assertIn('Shelter: damp and mould',h)
        self.assertIn('GOV.UK: guidance for English social landlords',h)
        self.assertIn('not validated methods',h)
        self.assertNotIn('General writes are currently open',h)

    def test_original_art_story_and_machine_routes_survive(self):
        for s in ('id="camp-fire-credit"','id="step-story"','id="project"',
                  'href="/explore/"','href="/works/"','href="https://pleasestartfromhere.com/manifest.json"',
                  'href="/llms.txt"','Two flats, one wall'):
            self.assertIn(s,self.home)
        self.assertIn('srcSet=',self.home)
        self.assertIn('height=',self.home)
        self.assertIn('A composite scene',self.home)
    def test_no_unsupported_privacy_or_live_service_claim(self):
        self.assertIn('Mechanical Ethics v0.8.0 is the released book',self.home)
        self.assertIn('https://yetanotherclearing.com/',self.home)
        self.assertIn('https://thehumanrecord.net/',self.home)
        self.assertIn('Reading grants no permission',self.home)
        self.assertNotIn('No information about you is collected',self.home)
        journey=(ROOT/"out/journey.js").read_text(encoding="utf-8")
        for forbidden in ("fetch(","sendBeacon","localStorage","sessionStorage","document.cookie"):
            self.assertNotIn(forbidden,journey)
    def test_responsive_source_and_mobile_reading_route(self):
        self.assertIn('@media(max-width:690px)',self.css)
        self.assertIn('.human-door-routes{grid-template-columns:1fr',self.css)
        self.assertNotIn('body:has(.human-first-door) .art-hero{width:',self.css)
        self.assertIn('human-door-lead',self.home)

if __name__ == "__main__":
    unittest.main()
