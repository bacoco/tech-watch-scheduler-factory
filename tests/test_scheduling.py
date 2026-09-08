import json
from pathlib import Path
import unittest

from support import ROOT, profile
from tech_watch.scheduling import cadence_model, runtime_model


class AdaptiveCadence(unittest.TestCase):
    def fixture(self, name):
        return json.loads((ROOT / f'examples/{name}.json').read_text())

    def test_fast_domain_separates_watch_and_postmortem(self):
        cadence = cadence_model(self.fixture('cadence-fast'))
        self.assertEqual(cadence['watch']['interval_days'], 1)
        self.assertEqual(cadence['postmortem']['interval_days'], 14)
        self.assertNotEqual(cadence['watch']['recommendation'],
                            cadence['postmortem']['recommendation'])

    def test_slow_domain_matches_ay11_shape(self):
        cadence = cadence_model(self.fixture('cadence-slow'))
        self.assertEqual(cadence['watch']['interval_days'], 14)
        self.assertEqual(cadence['postmortem']['interval_days'], 30)
        self.assertEqual(cadence['adaptation']['min_runs_before_change'], 3)

    def test_legacy_flat_profile_does_not_force_weekly_postmortem(self):
        cadence = cadence_model(profile()['cadence'])
        self.assertTrue(cadence['legacy_flat'])
        self.assertEqual(cadence['watch']['interval_days'], 7)
        self.assertEqual(cadence['postmortem']['interval_days'], 30)

    def test_hysteresis_rejects_too_early_decrease(self):
        value = self.fixture('cadence-slow')
        value['adaptation']['min_runs_before_change'] = 4
        value['adaptation']['decrease_after_consecutive_low_value'] = 3
        with self.assertRaises(ValueError):
            cadence_model(value)

    def test_multiplex_runtime_requires_canonical_registry_repo(self):
        p = profile()
        p['runtime'] = {'mode': 'multiplexed', 'reason': 'save task slots',
                        'group_id': 'shared-watch'}
        with self.assertRaises((ValueError, TypeError)):
            runtime_model(p)
        p['runtime']['registry_repository'] = 'example/watch-runtime'
        self.assertEqual(runtime_model(p)['registry_repository'], 'example/watch-runtime')

    def test_dedicated_is_backward_compatible(self):
        runtime = runtime_model(profile())
        self.assertEqual(runtime['mode'], 'dedicated')


if __name__ == '__main__':
    unittest.main()
