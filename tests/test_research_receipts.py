"""Every successful cycle needs fresh, linked, hashed research evidence."""
import tempfile
import unittest
from support import pack, receipt
from tech_watch.common import atomic_json, digest, read_json
from tech_watch.state import freeze_t0, verify_t0
from tech_watch.updates import record_update


class ResearchReceipts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = pack(self.temp.name)

    def change_research(self, r, edit):
        target = self.root / r['research']
        d = read_json(target); edit(d); atomic_json(target, d)
        for a in r['artifacts']:
            if a['path'] == r['research']: a['sha256'] = digest(target.read_bytes())

    def test_t0_requires_external_research_record(self):
        r = receipt(self.root); r.pop('research')
        with self.assertRaises(ValueError): freeze_t0(self.root, r)
        self.assertFalse((self.root / 'baseline').exists())

    def test_t0_cannot_reuse_generation_stage(self):
        r = receipt(self.root)
        self.change_research(r, lambda d: d.update(stage='generation'))
        with self.assertRaises(ValueError): freeze_t0(self.root, r)

    def test_t0_research_is_frozen_with_other_evidence(self):
        r = receipt(self.root); freeze_t0(self.root, r)
        self.assertTrue((self.root / 'baseline' / r['research']).is_file())
        verify_t0(self.root)

    def test_update_with_unchanged_code_still_requires_research(self):
        freeze_t0(self.root, receipt(self.root))
        r = receipt(self.root, 'update', 'update-1'); r.pop('research')
        with self.assertRaises(ValueError): record_update(self.root, r)
        self.assertIsNone(read_json(self.root / 'state.json')['last_completed_update'])

    def test_partial_web_research_cannot_advance(self):
        freeze_t0(self.root, receipt(self.root))
        r = receipt(self.root, 'update', 'update-1')
        self.change_research(r, lambda d: d.update(status='partial'))
        with self.assertRaises(ValueError): record_update(self.root, r)
        self.assertIsNone(read_json(self.root / 'state.json')['last_completed_update'])

    def test_stale_research_window_refused(self):
        r = receipt(self.root)
        self.change_research(r, lambda d: d.update(started_at='2026-09-06T08:00:00+02:00'))
        with self.assertRaises(ValueError): freeze_t0(self.root, r)

    def test_unhashed_journal_refused(self):
        r = receipt(self.root)
        r['artifacts'] = [a for a in r['artifacts'] if a['path'] != r['research']]
        with self.assertRaises(ValueError): freeze_t0(self.root, r)

    def test_tampered_research_refused(self):
        r = receipt(self.root)
        (self.root / r['research']).write_text('{}')
        with self.assertRaises(ValueError): freeze_t0(self.root, r)
