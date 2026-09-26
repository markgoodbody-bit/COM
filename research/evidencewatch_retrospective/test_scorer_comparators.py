"""Offline negative-input regressions; no owner data or provider calls."""
import unittest

import score_brierley_unblinded as scorer
from score_trivial_baselines import METRICS, auc, roc_points


def fixture():
    rows = [dict(preprint_doi=str(i), owner_label=scorer.POSITIVE if i < 22 else scorer.CONTROL,
                 published_abstract_available=True,
                 scores={name: i / 44 for name in METRICS}) for i in range(44)]
    metrics = {name: dict(complete_positive_n=22, complete_control_n=22,
                         missing_positive_n=0, missing_control_n=0,
                         auc=auc([r['scores'][name] for r in rows[:22]],
                                 [r['scores'][name] for r in rows[22:]]),
                         roc_points=roc_points(rows, name)) for name in METRICS}
    return dict(schema=scorer.BASELINE_SCHEMA, status='PRE_MODEL_TRIVIAL_BASELINE',
                rows=rows, metrics=metrics)


def comparisons(sensitivity=0.2, far=0.0):
    return {name: {'best_at_or_below_model_strict_far': {
        'sensitivity': sensitivity, 'false_alert_rate': far,
        'positive_n': 22, 'control_n': 22}} for name in METRICS}


class ComparatorTests(unittest.TestCase):
    def test_valid_generated_fixture(self):
        self.assertEqual(len(scorer.validate_baselines(fixture())), 44)

    def test_missing_empty_partial_extra_metrics(self):
        for replacement in (None, {}, {'unknown': {}}, {next(iter(METRICS)): {}}):
            with self.subTest(replacement=replacement):
                data = fixture()
                data['metrics'] = replacement
                with self.assertRaises(AssertionError):
                    scorer.validate_baselines(data)

    def test_invalid_case_scores(self):
        for value in (None, True, float('nan'), float('inf'), -0.1, 1.1, '0.5'):
            with self.subTest(value=value):
                data = fixture()
                data['rows'][0]['scores'][next(iter(METRICS))] = value
                with self.assertRaises(AssertionError):
                    scorer.validate_baselines(data)

    def test_corrupt_summary_rejected(self):
        for key, value in [('roc_points', []), ('roc_points', None),
                           ('auc', float('nan')), ('auc', 1.0),
                           ('complete_positive_n', 21), ('missing_control_n', 1)]:
            with self.subTest(key=key, value=value):
                data = fixture()
                data['metrics'][next(iter(METRICS))][key] = value
                with self.assertRaises(AssertionError):
                    scorer.validate_baselines(data)

    def test_changed_roc_rejected(self):
        data = fixture()
        data['metrics'][next(iter(METRICS))]['roc_points'][1]['sensitivity'] = 0.9
        with self.assertRaises(AssertionError):
            scorer.validate_baselines(data)

    def test_owner_coverage_rejected(self):
        data = fixture()
        data['rows'][0]['owner_label'] = scorer.CONTROL
        with self.assertRaises(AssertionError):
            scorer.validate_baselines(data)

    def test_missing_comparison_never_survives(self):
        values = [{}, {next(iter(METRICS)): {}}, dict.fromkeys(METRICS), comparisons()]
        values[-1][next(iter(METRICS))]['best_at_or_below_model_strict_far'] = None
        for value in values:
            self.assertEqual(scorer.decision_route(
                {'sensitivity': 0.5, 'false_alert_rate': 0.1}, 0, value)['route'],
                'INVALID_OR_UNSCORABLE')

    def test_invalid_operating_points(self):
        for field, value in [('sensitivity', float('nan')), ('false_alert_rate', 2),
                             ('positive_n', 21), ('false_alert_rate', 0.5)]:
            data = comparisons()
            data[next(iter(METRICS))]['best_at_or_below_model_strict_far'][field] = value
            self.assertEqual(scorer.decision_route(
                {'sensitivity': 0.5, 'false_alert_rate': 0.1}, 0, data)['route'],
                'INVALID_OR_UNSCORABLE')

    def test_three_substantive_routes(self):
        rates = {'sensitivity': 0.5, 'false_alert_rate': 0.1}
        self.assertEqual(scorer.decision_route(rates, 1, comparisons(0.5))['route'],
                         'INCONCLUSIVE_PROVIDER_OR_ANALYSIS_FAILURE')
        self.assertEqual(scorer.decision_route(rates, 0, comparisons(0.5))['route'],
                         'NARROW_OR_STOP_SEMANTIC_VALUE_CLAIM')
        self.assertEqual(scorer.decision_route(rates, 0, comparisons())['route'],
                         'RETROSPECTIVE_SIGNAL_SURVIVED')

    def test_zero_far_has_always_quiet_endpoint(self):
        data = fixture()
        scorer.validate_baselines(data)
        point = scorer.best_baseline_at_far(data['metrics'][next(iter(METRICS))], 0)
        self.assertEqual((point['sensitivity'], point['false_alert_rate']), (0, 0))
        self.assertIsNone(point['threshold'])


if __name__ == '__main__':
    unittest.main()
