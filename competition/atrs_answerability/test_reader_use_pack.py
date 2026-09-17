"""Offline method checks; these do not establish human reader benefit."""
import re
import unittest
from collections import Counter, defaultdict
from html import unescape

from reader_use_pack import CASES, CONDITIONS, build_schedules, excerpt_surface, lens_surface


class ScheduleTests(unittest.TestCase):
    def setUp(self):
        self.cases = [case for case in CASES if case["primary_scored"]]
        self.schedules = build_schedules(self.cases)

    def test_each_case_once_per_schedule_and_three_per_condition(self):
        expected_ids = {case["case_id"] for case in self.cases}
        self.assertEqual(len(self.schedules), 6)
        for schedule in self.schedules:
            rows = schedule["cases"]
            self.assertEqual(len(rows), 9)
            self.assertEqual({r["case_id"] for r in rows}, expected_ids)
            self.assertEqual([r["position"] for r in rows], list(range(1, 10)))
            self.assertEqual(Counter(r["condition"] for r in rows),
                             Counter({condition: 3 for condition in CONDITIONS}))

    def test_each_case_twice_in_each_condition(self):
        counts = defaultdict(Counter)
        for schedule in self.schedules:
            for row in schedule["cases"]:
                counts[row["case_id"]][row["condition"]] += 1
        for value in counts.values():
            self.assertEqual(value, Counter({condition: 2 for condition in CONDITIONS}))

    def test_each_position_twice_in_each_condition(self):
        counts = defaultdict(Counter)
        for schedule in self.schedules:
            for row in schedule["cases"]:
                counts[row["position"]][row["condition"]] += 1
        self.assertEqual(set(counts), set(range(1, 10)))
        for position, value in counts.items():
            with self.subTest(position=position):
                self.assertEqual(value, Counter({condition: 2 for condition in CONDITIONS}))

    def test_repeatable_without_mutating_input(self):
        before = [case["case_id"] for case in self.cases]
        self.assertEqual(self.schedules, build_schedules(self.cases))
        self.assertEqual(before, [case["case_id"] for case in self.cases])


class SurfaceParityTests(unittest.TestCase):
    def surfaces(self, tokens):
        case = {"title": "Synthetic field-only fixture"}
        row = {"fields": {"appeals_review": {
            "section_present": True,
            "matches": [{"text": "Ask your clinician for review; a route need not be a URL.",
                         "contact_tokens": tokens}],
        }}}
        return [render(case, row).decode("utf-8")
                for render in (excerpt_surface, lens_surface)]

    def test_no_lens_only_absence_or_interpretation_cues(self):
        excerpt, lens = self.surfaces({})
        for cue in ("No link, URL, email or phone-like token was observed",
                    "This does not mean no route exists",
                    "it is not an appeal-right or route-effectiveness classification"):
            self.assertNotIn(cue, lens)
        # All prose paragraphs, including the common instruction, must be equal.
        paragraphs = lambda doc: re.findall(r"<p\b[^>]*>(.*?)</p>", doc, re.S)
        self.assertEqual(paragraphs(excerpt), paragraphs(lens))

    def test_source_passage_and_contact_values_preserved(self):
        tokens = {"hrefs": ["https://example.org/help?a=1&b=2"],
                  "urls_in_text": ["https://example.org/help"],
                  "emails": ["help@example.org"], "phones": ["01234 567890"]}
        excerpt, lens = self.surfaces(tokens)
        source = lambda doc: re.findall(r"<p class='source'>(.*?)</p>", doc, re.S)
        values = lambda doc: [unescape(v) for v in re.findall(r"<code>(.*?)</code>", doc)]
        self.assertEqual(source(excerpt), source(lens))
        self.assertEqual(values(excerpt), values(lens))
        self.assertEqual(values(lens), [v for group in tokens.values() for v in group])


if __name__ == "__main__":
    unittest.main()
