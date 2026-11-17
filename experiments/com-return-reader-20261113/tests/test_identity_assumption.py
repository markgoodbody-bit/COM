import unittest
from return_reader import audit


class IdentityAssumptionTests(unittest.TestCase):
    def test_missing_status_is_distinguished_from_explicit_preserved(self):
        rows = [
            {"source": "a", "event_id": "one", "kind": "TASK", "status": "ATTEMPTED", "task_id": "x"},
            {"source": "a", "event_id": "two", "kind": "TASK", "status": "ATTEMPTED", "task_id": "y", "identity_status": "PRESERVED"},
            {"source": "a", "event_id": "three", "kind": "TASK", "status": "ATTEMPTED", "task_id": "z", "identity_status": "UNKNOWN"},
            {"kind": "RETURN", "status": "UNKNOWN"},
        ]
        result = audit({"events": rows})
        self.assertEqual(result["identity_status_defaulted_records"], 2)
        self.assertEqual(result["identity_status_defaulted_grouped_records"], 1)
        self.assertIn("not verified", result["identity_default_caveat"])

    def test_explicit_statuses_do_not_default(self):
        rows = [{"source": "a", "event_id": "one", "kind": "TASK", "status": "ATTEMPTED", "identity_status": "PRESERVED"}]
        result = audit({"events": rows})
        self.assertEqual(result["identity_status_defaulted_records"], 0)
        self.assertEqual(result["identity_status_defaulted_grouped_records"], 0)
