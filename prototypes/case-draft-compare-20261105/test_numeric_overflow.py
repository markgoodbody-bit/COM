import math
import unittest
import compare


class NumericOverflowTests(unittest.TestCase):
    def test_overflow_exponents_are_rejected_in_nested_rows(self):
        for token in (b'1e999', b'-1e999', b'2e999'):
            with self.subTest(token=token):
                with self.assertRaisesRegex(compare.CompareError, 'non-finite'):
                    compare.parse_json(b'{"claims":[{"value":' + token + b'}]}')

    def test_finite_extremes_and_large_integers_remain_accepted(self):
        data = compare.parse_json(b'{"value":1e308,"integer":123456789012345678901234567890}')
        self.assertTrue(math.isfinite(data['value']))
        self.assertEqual(data['integer'], 123456789012345678901234567890)

    def test_literal_nonfinite_constants_still_fail(self):
        for token in (b'NaN', b'Infinity', b'-Infinity'):
            with self.assertRaises(compare.CompareError):
                compare.parse_json(b'{"value":' + token + b'}')
