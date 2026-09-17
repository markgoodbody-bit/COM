import unittest
from discover_com import discover


def obj(number, body, **extra):
    return dict(id=number, number=number, body=body, updated_at="2026-09-17T19:44:18Z", **extra)


class DiscoveryTests(unittest.TestCase):
    def test_zero_comment_issue_on_second_page_is_delivered(self):
        def fetch(route):
            return [[]] if "issues/comments?" in route else [[obj(364, "old")], [obj(365, "CODEX: task", comments=0)]]
        result = discover("markgoodbody-bit/COM", "2026-09-17T19:00:00Z", fetch)
        self.assertEqual(result["surfaces"]["issues"]["objects"][1]["body"], "CODEX: task")
        self.assertEqual(result["surfaces"]["issues"]["pages"], 2)
        self.assertEqual(result["body_read_status"], "NOT_ESTABLISHED")

    def test_closed_and_pr_bodies_are_not_filtered(self):
        seen = []
        def fetch(route):
            seen.append(route)
            return [[]] if "comments?" in route else [[obj(1, "edited closed task", state="closed"), obj(2, "PR task", pull_request={})]]
        result = discover("markgoodbody-bit/COM", "2026-09-17T19:00:00Z", fetch)
        self.assertIn("state=all", seen[0])
        self.assertEqual(len(result["surfaces"]["issues"]["objects"]), 2)
        self.assertIn("18:58:00", result["effective_since"])

    def test_comment_failure_is_partial_not_empty_success(self):
        def fetch(route):
            if "comments?" in route:
                raise RuntimeError("page 2 failed")
            return [[obj(365, "task")]]
        result = discover("markgoodbody-bit/COM", "2026-09-17T19:00:00Z", fetch)
        self.assertEqual(result["status"], "PARTIAL")
        self.assertIn("issues", result["surfaces"])

    def test_missing_body_is_partial(self):
        result = discover("markgoodbody-bit/COM", fetch=lambda _: [[{"id": 365}]])
        self.assertEqual(result["status"], "PARTIAL")

    def test_bootstrap_does_not_claim_closed_history_or_reading(self):
        result = discover("markgoodbody-bit/COM", fetch=lambda _: [[]])
        self.assertEqual(result["closed_history"], "NOT_ESTABLISHED")
        self.assertEqual(result["status"], "DISCOVERY_RETRIEVED_NOT_READ")


if __name__ == "__main__":
    unittest.main()
