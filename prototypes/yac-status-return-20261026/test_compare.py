"""Synthetic tests for key-free YAC status checkpoint comparison."""
import copy
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from compare import classify, main


OLD = {
    "http_status": 200,
    "result": {
        "profile": "PUBLIC",
        "daily_post_limit": 8,
        "daily_post_remaining": 7,
        "lifetime_post_remaining": 1023,
        "observed_at_utc": "2026-10-25T11:28:02Z",
        "database_now": 1792927682,
        "admission_open": True,
        "join_open": True,
    },
    "note": "Public read only; source status is time-bounded",
}


def pair():
    a = copy.deepcopy(OLD)
    b = copy.deepcopy(OLD)
    b["result"].update(
        observed_at_utc="2026-10-25T12:28:02Z",
        database_now=1792931282,
        daily_post_remaining=6,
        lifetime_post_remaining=1022,
    )
    return a, b


class ComparisonTests(unittest.TestCase):
    def test_budget_change_is_conditional_and_does_not_invent_visibility(self):
        a, b = pair()
        r = classify(a, b)
        self.assertEqual(r["classification"], "CONDITIONAL_BUDGET_CHANGE")
        self.assertEqual(r["lifetime_budget_units"], 1)
        self.assertEqual(r["daily_budget_units"], 1)
        self.assertIn("unverified", r["assumptions"].lower())
        self.assertNotIn("new posts", json.dumps(r).lower())
        self.assertIn("not", r["limits"].lower())

    def test_no_net_change_is_not_no_activity(self):
        a, b = pair()
        b["result"]["lifetime_post_remaining"] = 1023
        b["result"]["daily_post_remaining"] = 7
        b["result"]["admission_open"] = False
        r = classify(a, b)
        self.assertEqual(r["classification"], "NO_NET_COUNTER_CHANGE")
        self.assertIn("not proof", r["limits"].lower())

    def test_cross_date_does_not_compare_daily(self):
        a, b = pair()
        b["result"].update(observed_at_utc="2026-10-26T11:28:02Z", database_now=1793014082,
                           daily_post_remaining=8)
        r = classify(a, b)
        self.assertEqual(r["classification"], "CONDITIONAL_BUDGET_CHANGE")
        self.assertEqual(r["daily_comparison"], "NOT_COMPARABLE_DIFFERENT_UTC_DATES")
        self.assertIsNone(r["daily_budget_units"])

    def test_zero_is_unknown(self):
        a, b = pair()
        a["result"]["lifetime_post_remaining"] = 0
        self.assertEqual(classify(a, b)["classification"], "UNKNOWN")

    def test_increased_lifetime_is_unknown(self):
        a, b = pair()
        b["result"]["lifetime_post_remaining"] = 1024
        self.assertEqual(classify(a, b)["classification"], "UNKNOWN")

    def test_increased_same_day_daily_is_unknown(self):
        a, b = pair()
        b["result"]["daily_post_remaining"] = 8
        self.assertEqual(classify(a, b)["classification"], "UNKNOWN")

    def test_counter_disagreement_is_unknown(self):
        a, b = pair()
        b["result"]["daily_post_remaining"] = 5
        self.assertEqual(classify(a, b)["reason"], "INCONSISTENT_SAME_DAY_DELTAS")

    def test_profile_change_is_unknown(self):
        a, b = pair()
        b["result"]["profile"] = "NEW"
        self.assertEqual(classify(a, b)["reason"], "CONTRACT_VALUE_CHANGE")

    def test_daily_limit_change_is_unknown(self):
        a, b = pair()
        b["result"]["daily_post_limit"] = 20
        self.assertEqual(classify(a, b)["reason"], "CONTRACT_VALUE_CHANGE")

    def test_added_field_is_unknown(self):
        a, b = pair()
        b["result"]["router_hold"] = True
        self.assertEqual(classify(a, b)["reason"], "STATUS_FIELD_SET_CHANGED")

    def test_non_200_is_unknown(self):
        a, b = pair()
        b["http_status"] = None
        self.assertEqual(classify(a, b)["reason"], "HTTP_NOT_200")

    def test_invalid_non_integer_counters_unknown(self):
        for value in [True, -1, 2.5, "7", 10**20]:
            a, b = pair()
            b["result"]["daily_post_remaining"] = value
            self.assertEqual(classify(a, b)["classification"], "UNKNOWN")

    def test_response_not_object_unknown(self):
        a, b = pair()
        b["result"] = []
        self.assertEqual(classify(a, b)["classification"], "UNKNOWN")

    def test_invalid_iso_time_unknown(self):
        a, b = pair()
        b["result"]["observed_at_utc"] = "yesterday"
        self.assertEqual(classify(a, b)["reason"], "INVALID_CLOCK")

    def test_backward_service_clock_unknown(self):
        a, b = pair()
        b["result"]["observed_at_utc"] = "2026-10-24T12:28:02Z"
        self.assertEqual(classify(a, b)["reason"], "CLOCK_ORDER_UNVERIFIED")

    def test_backward_database_clock_unknown(self):
        a, b = pair()
        b["result"]["database_now"] = a["result"]["database_now"] - 10
        self.assertEqual(classify(a, b)["classification"], "UNKNOWN")

    def test_clock_skew_unknown(self):
        a, b = pair()
        b["result"]["database_now"] += 1000
        self.assertEqual(classify(a, b)["reason"], "CLOCK_DISAGREEMENT")

    def test_near_midnight_utc_unknown(self):
        a, b = pair()
        a["result"].update(observed_at_utc="2026-10-25T23:59:30Z", database_now=1792972770)
        b["result"].update(observed_at_utc="2026-10-26T00:01:30Z", database_now=1792972890)
        self.assertEqual(classify(a, b)["reason"], "NEAR_UTC_MIDNIGHT")

    def test_no_echo_of_untrusted_result_data(self):
        a, b = pair()
        a["result"]["untrusted_field"] = "X-YAC-Submission-Key=secret"
        b["result"]["untrusted_field"] = "another secret"
        s = json.dumps(classify(a, b))
        self.assertNotIn("secret", s)
        self.assertNotIn("X-YAC", s)


class FileTests(unittest.TestCase):
    def run_files(self, old, new):
        with tempfile.TemporaryDirectory() as t:
            p, q = Path(t) / "old.json", Path(t) / "new.json"
            p.write_text(old, encoding="utf-8")
            q.write_text(new, encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                rc = main([str(p), str(q)])
            return rc, json.loads(out.getvalue())

    def test_valid_files_exit_zero(self):
        a, b = pair()
        rc, data = self.run_files(json.dumps(a), json.dumps(b))
        self.assertEqual(rc, 0)
        self.assertEqual(data["classification"], "CONDITIONAL_BUDGET_CHANGE")

    def test_duplicate_key_refused(self):
        a, b = pair()
        malformed = json.dumps(a).replace('"http_status": 200', '"http_status": 200, "http_status": 200')
        rc, data = self.run_files(malformed, json.dumps(b))
        self.assertEqual((rc, data["classification"]), (2, "INPUT_REFUSED"))

    def test_nan_refused(self):
        a, b = pair()
        malformed = json.dumps(a).replace('"daily_post_remaining": 7', '"daily_post_remaining": NaN')
        rc, data = self.run_files(malformed, json.dumps(b))
        self.assertEqual((rc, data["classification"]), (2, "INPUT_REFUSED"))

    def test_large_input_refused(self):
        a, b = pair()
        rc, data = self.run_files(json.dumps(a) + " " * 70000, json.dumps(b))
        self.assertEqual((rc, data["classification"]), (2, "INPUT_REFUSED"))


if __name__ == "__main__":
    unittest.main()
