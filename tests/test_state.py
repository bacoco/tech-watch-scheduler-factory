from pathlib import Path
import tempfile
import unittest
from support import profile, pack, receipt
from tech_watch.common import read_json
from tech_watch.state import freeze_t0, verify_t0


class Baseline(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = pack(self.temp.name)

    def test_freeze_once(self):
        r = receipt(self.root)
        state = freeze_t0(self.root, r)
        self.assertEqual(state['phase'], 'UPDATE_READY')
        verify_t0(self.root)
        with self.assertRaises(ValueError): freeze_t0(self.root, r)

    def test_incomplete_coverage_refused(self):
        r = receipt(self.root); r['coverage'].pop()
        with self.assertRaises(ValueError): freeze_t0(self.root, r)
        self.assertFalse((self.root / 'baseline').exists())

    def test_blocker_refused(self):
        r = receipt(self.root); r['blockers'] = ['required source unavailable']
        with self.assertRaises(ValueError): freeze_t0(self.root, r)

    def test_fake_delivery_refused(self):
        r = receipt(self.root); r['delivery']['status'] = 'unverified'
        with self.assertRaises(ValueError): freeze_t0(self.root, r)

    def test_changed_artifact_refused(self):
        r = receipt(self.root)
        (self.root / r['artifacts'][0]['path']).write_text('tampered')
        with self.assertRaises(ValueError): freeze_t0(self.root, r)

    def test_tampered_frozen_baseline_detected(self):
        r = receipt(self.root); freeze_t0(self.root, r)
        (self.root / 'baseline' / r['artifacts'][0]['path']).write_text('tampered')
        with self.assertRaises(ValueError): verify_t0(self.root)

    def test_added_baseline_file_detected(self):
        freeze_t0(self.root, receipt(self.root))
        (self.root / 'baseline' / 'extra.txt').write_text('unexpected')
        with self.assertRaises(ValueError): verify_t0(self.root)

    def test_locked_freeze_refused(self):
        (self.root / '.factory-lock').mkdir()
        with self.assertRaises(ValueError): freeze_t0(self.root, receipt(self.root))

    def test_artifact_other_run_refused(self):
        r = receipt(self.root); r['run_id'] = 'other-run'
        with self.assertRaises(ValueError): freeze_t0(self.root, r)

    def test_draft_cannot_freeze(self):
        p = profile(); p.update(status='draft', unknowns=['not understood'])
        root = pack(Path(self.temp.name) / 'draft', p)
        with self.assertRaises(ValueError): freeze_t0(root, receipt(root))

    def test_receipt_path_traversal(self):
        r = receipt(self.root); r['artifacts'][0]['path'] = 'runs/../private'
        with self.assertRaises(ValueError): freeze_t0(self.root, r)

    def test_no_baseline_to_verify(self):
        with self.assertRaises(ValueError): verify_t0(self.root)
