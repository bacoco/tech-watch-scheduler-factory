import tempfile
import unittest
from support import pack, receipt
from tech_watch.common import read_json
from tech_watch.state import freeze_t0, verify_t0
from tech_watch.updates import record_update


class Updates(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = pack(self.temp.name)
        freeze_t0(self.root, receipt(self.root))

    def test_idempotent_receipt(self):
        r = receipt(self.root, 'update', 'update-1')
        self.assertEqual(record_update(self.root, r)['status'], 'recorded-locally')
        self.assertEqual(record_update(self.root, r)['status'], 'unchanged')
        verify_t0(self.root)

    def test_stale_parent_refused(self):
        record_update(self.root, receipt(self.root, 'update', 'update-1'))
        with self.assertRaises(ValueError):
            record_update(self.root, receipt(self.root, 'update', 'update-2'))

    def test_partial_does_not_advance(self):
        r = receipt(self.root, 'update', 'update-1'); r['status'] = 'partial'
        with self.assertRaises(ValueError): record_update(self.root, r)
        self.assertIsNone(read_json(self.root / 'state.json')['last_completed_update'])

    def test_old_paper_allowed(self):
        before = (self.root / 'baseline/manifest.json').read_bytes()
        r = receipt(self.root, 'update', 'update-1')
        r['findings'] = [{'kind': 'newly_discovered_historical', 'published_at': '2018-01-01',
                          'first_seen_at': '2026-09-07T09:00:00+02:00'}]
        record_update(self.root, r)
        self.assertEqual(before, (self.root / 'baseline/manifest.json').read_bytes())

    def test_omitted_source_preserved(self):
        record_update(self.root, receipt(self.root, 'update', 'update-1'))
        r = receipt(self.root, 'update', 'update-2')
        r.update(previous_run_id='update-1', source_checkpoints={'official': {'cursor': 'second'}})
        state = record_update(self.root, r)['state']
        self.assertEqual(state['source_checkpoints']['github']['cursor'], 'test-only')

    def test_excluded_source_cursor_refused(self):
        r = receipt(self.root, 'update', 'update-1'); r['source_checkpoints'] = {'personal': 'no'}
        with self.assertRaises(ValueError): record_update(self.root, r)

    def test_historical_run_id_cannot_be_reused(self):
        first = receipt(self.root, 'update', 'update-1')
        record_update(self.root, first)
        second = receipt(self.root, 'update', 'update-2')
        second['previous_run_id'] = 'update-1'
        record_update(self.root, second)
        first['previous_run_id'] = 'update-2'
        with self.assertRaises(ValueError): record_update(self.root, first)

    def test_time_cannot_move_backwards(self):
        r = receipt(self.root, 'update', 'update-1')
        r['started_at'] = '2025-01-01T00:00:00Z'
        r['finished_at'] = '2025-01-01T01:00:00Z'
        with self.assertRaises(ValueError): record_update(self.root, r)
