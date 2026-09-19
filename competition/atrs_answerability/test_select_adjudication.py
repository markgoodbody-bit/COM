import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("atrs_select", ROOT / "select_adjudication.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


def row(url, *, present=True, token=False, matches=1):
    return {
        "title": url.rsplit('/', 1)[-1],
        "url": url,
        "source_sha256": "a" * 64,
        "source_snapshot": "a.html",
        "fetched_at_utc": "2026-09-17T00:00:00+00:00",
        "fields": {
            "appeals_review": {
                "section_present": present,
                "match_count": matches if present else 0,
                "syntactic_contact_token_present": token if present else False,
                "matches": [],
            }
        },
    }


class SelectionTests(unittest.TestCase):
    def test_positive_is_census_not_sample(self):
        report={"records":[
            row("https://www.gov.uk/algorithmic-transparency-records/a", token=True),
            row("https://www.gov.uk/algorithmic-transparency-records/b", token=True),
            row("https://www.gov.uk/algorithmic-transparency-records/c", token=False),
        ]}
        result=mod.select(report, negative_sample_size=1)
        self.assertEqual(len(result["token_positive_census"]), 2)
        self.assertEqual(len(result["token_negative_sample"]), 1)

    def test_negative_sample_is_sha256_url_order(self):
        urls=[f"https://www.gov.uk/algorithmic-transparency-records/{x}" for x in "abcdef"]
        report={"records":[row(url) for url in urls]}
        result=mod.select(report, negative_sample_size=3)
        expected=sorted(urls, key=mod.url_digest)[:3]
        self.assertEqual([x["url"] for x in result["token_negative_sample"]], expected)

    def test_missing_and_multiple_are_additional_checks(self):
        report={"records":[
            row("https://www.gov.uk/algorithmic-transparency-records/missing", present=False),
            row("https://www.gov.uk/algorithmic-transparency-records/multi", matches=2),
        ]}
        result=mod.select(report)
        self.assertEqual(len(result["section_not_observed_checks"]), 1)
        self.assertEqual(len(result["multiple_match_checks"]), 1)

    def test_selection_carries_source_identity(self):
        report={"records":[row("https://www.gov.uk/algorithmic-transparency-records/a", token=True)]}
        selected=mod.select(report)["token_positive_census"][0]
        self.assertEqual(selected["source_sha256"], "a" * 64)
        self.assertEqual(selected["source_snapshot"], "a.html")


if __name__ == "__main__":
    unittest.main()
