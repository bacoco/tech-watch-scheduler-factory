import unittest
from support import profile
from tech_watch.profile import validate_profile


class Profiles(unittest.TestCase):
    def test_valid(self):
        validate_profile(profile())

    def test_arxiv_must_be_decided(self):
        p = profile(); p['channels'] = [c for c in p['channels'] if c['id'] != 'arxiv']
        with self.assertRaises(ValueError): validate_profile(p)

    def test_arxiv_may_be_excluded(self):
        p = profile(); p['channels'][0].update(mode='excluded', queries=[], targets=[])
        validate_profile(p)

    def test_unknown_evidence(self):
        p = profile(); p['questions'][0]['evidence_ids'] = ['nonexistent']
        with self.assertRaises(ValueError): validate_profile(p)

    def test_ready_with_unknowns_refused(self):
        p = profile(); p['unknowns'] = ['purpose not understood']
        with self.assertRaises(ValueError): validate_profile(p)

    def test_draft_allowed(self):
        p = profile(); p.update(status='draft', unknowns=['need more source reading'])
        validate_profile(p)

    def test_path_traversal(self):
        p = profile(); p['evidence'][0]['path'] = '../secrets'
        with self.assertRaises(ValueError): validate_profile(p)

    def test_timezone_required(self):
        p = profile(); p['analyzed_at'] = '2026-09-07T08:00:00'
        with self.assertRaises(ValueError): validate_profile(p)

    def test_invalid_issue_budget(self):
        p = profile(); p['cadence']['max_new_issues'] = True
        with self.assertRaises(ValueError): validate_profile(p)

    def test_duplicate_source(self):
        p = profile(); p['channels'][0] = p['channels'][1]
        with self.assertRaises(ValueError): validate_profile(p)

    def test_existing_requires_pointer(self):
        p = profile(); p['integration']['mode'] = 'reuse-existing'
        with self.assertRaises(ValueError): validate_profile(p)
