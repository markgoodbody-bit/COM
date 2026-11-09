"""Numeric preservation regressions using authored synthetic inputs only."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import compare


ROOT = Path(__file__).resolve().parent


class NumericPrecisionTests(unittest.TestCase):
    def test_distinct_long_decimals_cannot_silently_collapse(self):
        for value in (b'1.00000000000000001', b'1.00000000000000002'):
            with self.subTest(value=value):
                with self.assertRaises(compare.CompareError):
                    compare.parse_json(b'{"value":' + value + b'}')

    def test_nonzero_underflow_is_refused(self):
        for value in (b'1e-4000', b'-1e-4000'):
            with self.subTest(value=value):
                with self.assertRaises(compare.CompareError):
                    compare.parse_json(b'{"claims":[{"value":' + value + b'}]}')

    def test_rounded_fractional_integer_is_refused(self):
        with self.assertRaises(compare.CompareError):
            compare.parse_json(b'{"value":9007199254740993.0}')

    def test_roundtrippable_values_and_numeric_formatting_still_work(self):
        for value in (b'0.1', b'1.25', b'1e-5', b'1e308', b'5e-324', b'0e-4000'):
            with self.subTest(value=value):
                self.assertIsInstance(compare.parse_json(b'{"value":' + value + b'}')['value'], float)
        self.assertEqual(compare.changes(compare.parse_json(b'{"v":1.0}'),
                                         compare.parse_json(b'{"v":1.0000000000000000}')), [])

    def test_boolean_type_and_large_integer_preservation_remain(self):
        result = compare.changes(compare.parse_json(b'{"value":true}'),
                                 compare.parse_json(b'{"value":1}'))
        self.assertEqual(result[0][:2], ('CHANGED', '/value'))
        value = 123456789012345678901234567890
        self.assertEqual(compare.parse_json(('{"value":%d}' % value).encode())['value'], value)

    def test_text_and_html_cli_preserve_output_on_lossy_input(self):
        for script in ('compare.py', 'html_report.py'):
            for summary in (False, True):
                with self.subTest(script=script, summary=summary), tempfile.TemporaryDirectory() as tmp:
                    folder = Path(tmp)
                    before, after, report = (folder / name for name in ('before.json', 'after.json', 'report.txt'))
                    a = b'{"private_marker":"PRIVATE_NUMERIC_FIXTURE","value":1e-4000}'
                    b = b'{"private_marker":"PRIVATE_NUMERIC_FIXTURE","value":0.0}'
                    before.write_bytes(a); after.write_bytes(b); report.write_bytes(b'EXISTING_REPORT')
                    args = [sys.executable, str(ROOT / script), str(before), str(after), '--output', str(report)]
                    if summary:
                        args.append('--summary')
                    result = subprocess.run(args, capture_output=True, timeout=10)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(report.read_bytes(), b'EXISTING_REPORT')
                    self.assertEqual(before.read_bytes(), a)
                    self.assertEqual(after.read_bytes(), b)
                    self.assertNotIn(b'PRIVATE_NUMERIC_FIXTURE', result.stderr)
                    self.assertNotIn(b'1e-4000', result.stderr)
                    self.assertNotIn(b'NO_JSON_FIELD_CHANGE', result.stdout)

    def test_unrepresentable_exponent_fails_as_private_safe_input_error(self):
        with self.assertRaises(compare.CompareError):
            compare.parse_json(b'{"value":1e-999999999999999999999999999999}')


if __name__ == '__main__':
    unittest.main()
