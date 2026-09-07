"""Usage-driven research must be evidenced, not inferred from a stack label."""
import json
from copy import deepcopy
import unittest
from support import ROOT, profile
from tech_watch.profile import validate_profile
from tech_watch.render import render_files
from tech_watch.snapshot import priority


class UsageResearch(unittest.TestCase):
    def reject(self, p):
        with self.assertRaises((ValueError, KeyError, TypeError)):
            validate_profile(p)

    def test_v1_cannot_be_relabelled_as_complete_research(self):
        p = profile(); p['schema_version'] = 1
        self.reject(p)

    def test_stack_only_profile_refused(self):
        p = profile(); p.pop('usage')
        self.reject(p)

    def test_unrelated_question_refused(self):
        p = profile(); p['questions'][0]['usage_ids'] = []
        self.reject(p)

    def test_unknown_usage_refused(self):
        p = profile(); p['questions'][0]['usage_ids'] = ['ghost']
        self.reject(p)

    def test_code_is_not_runtime_observation(self):
        p = profile(); p['usage']['journeys'][0]['status'] = 'observed'
        self.reject(p)

    def test_documented_usage_with_explicit_limits_is_valid(self):
        validate_profile(profile())

    def test_observed_requires_reference(self):
        p = profile(); p['usage']['journeys'][0].update(
            status='observed', observation_refs=['SYNTHETIC authorized observation fixture'])
        validate_profile(p)

    def test_information_watch_without_code_change(self):
        p = json.loads((ROOT / 'examples/domain-watch.json').read_text())
        validate_profile(p)
        text = render_files(p)['USAGES.md']
        self.assertIn('domain_intelligence', text)
        self.assertIn('aucune issue de développement', text)
        self.assertTrue(all(e['kind'] != 'code' for e in p['evidence']))

    def test_same_stack_different_usage_gives_different_instructions(self):
        a = profile()
        b = json.loads((ROOT / 'examples/domain-watch.json').read_text())
        self.assertEqual(a['evidence'], b['evidence'])
        self.assertEqual(a['analyzed_sha'], b['analyzed_sha'])
        self.assertNotEqual(render_files(a)['USAGES.md'], render_files(b)['USAGES.md'])
        self.assertNotEqual(render_files(a)['QUESTIONS.md'], render_files(b)['QUESTIONS.md'])

    def test_both_purposes_need_both_question_types(self):
        p = profile(); p['usage']['watch_purpose'] = 'both'
        self.reject(p)
        p['questions'][0]['intent'] = 'domain_information'
        validate_profile(p)

    def test_source_plan_alone_is_not_research(self):
        p = profile(); p.pop('discovery')
        self.reject(p)

    def test_all_sources_only_candidates_refused(self):
        p = profile()
        for s in p['discovery']['sources']: s['status'] = 'candidate'
        self.reject(p)

    def test_missing_browse_access_blocks_ready(self):
        p = profile(); p['discovery']['status'] = 'blocked'
        self.reject(p)
        p.update(status='draft', unknowns=['Internet access blocked'])
        validate_profile(p)

    def test_closed_seed_list_refused(self):
        p = profile()
        for s in p['discovery']['sources']: s['origin'] = 'seed'
        self.reject(p)

    def test_missing_expansion_refused(self):
        p = profile(); p['discovery']['searches'].pop(1)
        self.reject(p)

    def test_missing_challenge_refused(self):
        p = profile(); p['discovery']['searches'].pop()
        self.reject(p)

    def test_missing_search_trace_refused(self):
        p = profile(); p['discovery']['searches'][0]['trace'] = ''
        self.reject(p)

    def test_no_new_ideas_can_be_honest_result(self):
        p = profile(); p['discovery']['new_directions'] = []
        validate_profile(p)

    def test_one_publisher_repeated_is_not_diversity(self):
        p = profile(); p['discovery']['sources'][1]['publisher'] = 'Catalogue Fixture'
        self.reject(p)

    def test_github_and_arxiv_only_refused(self):
        p = profile()
        for s, family in zip(p['discovery']['sources'], ['github', 'arxiv']):
            s.update(family=family, url=f'https://{family}.com/fixture')
        self.reject(p)

    def test_duplicate_url_refused(self):
        p = profile(); p['discovery']['sources'][1]['url'] = p['discovery']['sources'][0]['url']
        self.reject(p)

    def test_wrong_repo_revision_refused(self):
        p = profile(); p['discovery']['repo_sha'] = 'b' * 40
        self.reject(p)

    def test_real_profile_cannot_use_synthetic_example(self):
        p = profile(); p['repository'] = 'bacoco/actual-product'
        self.reject(p)

    def test_example_cannot_claim_real_web_access(self):
        p = profile(); p['discovery']['synthetic'] = False
        self.reject(p)

    def test_custom_source_family_is_supported(self):
        p = profile(); c = deepcopy(p['channels'][-1]); c['id'] = 'museum-practice'
        p['channels'].append(c)
        validate_profile(p)

    def test_open_web_cannot_be_excluded(self):
        p = profile(); p['channels'][-1].update(mode='excluded', queries=[], targets=[])
        self.reject(p)

    def test_usage_guides_read_before_dependency_manifests(self):
        self.assertLess(priority('docs/user-guide.md'), priority('package.json'))

    def test_pack_carries_usage_and_deep_research_protocol(self):
        files = render_files(profile())
        for name in ['USAGES.md', 'RECHERCHE.md', 'RECHERCHE-INITIALE.md', 'discovery.json']:
            self.assertIn(name, files)
        for name in ['T0.md', 'UPDATE.md', 'INSTRUCTIONS.md', 'CHATGPT-TASK.md']:
            self.assertIn('RECHERCHE.md', files[name])
        self.assertIn('SYNTHÉTIQUE', files['RECHERCHE-INITIALE.md'])

    def test_generation_not_misrepresented_as_t0(self):
        p = profile(); p['discovery']['stage'] = 't0'
        self.reject(p)
