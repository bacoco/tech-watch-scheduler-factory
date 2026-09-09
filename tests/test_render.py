from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import json
import tempfile
import unittest
from support import ROOT, profile, pack
from tech_watch.cli import main
from tech_watch.common import atomic_json, read_json
from tech_watch.render import generate, validate_pack


class Rendering(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_idempotent(self):
        first, _ = generate(profile(), self.root)
        second, status = generate(profile(), self.root)
        self.assertEqual(first, second); self.assertEqual(status, 'unchanged')

    def test_context_and_queries_specific(self):
        root = pack(self.root)
        self.assertIn('rayures', (root / 'CONTEXTE.md').read_text())
        self.assertIn('image editing preservation', (root / 'SOURCES.md').read_text())
        self.assertIn('signatures', (root / 'QUESTIONS.md').read_text())
        self.assertIn('example/image-product', (root / 'CHATGPT-TASK.md').read_text())

    def test_legacy_profile_renders_distinct_dedicated_cadences(self):
        root = pack(self.root)
        runtime = read_json(root / 'runtime.json')
        self.assertEqual(runtime['mode'], 'dedicated')
        self.assertEqual(runtime['cadence']['watch']['interval_days'], 7)
        self.assertEqual(runtime['cadence']['postmortem']['interval_days'], 30)
        self.assertTrue(runtime['recovery']['enabled'])
        self.assertEqual(runtime['recovery']['interval_hours'], 6)
        self.assertTrue(runtime['recovery']['only_when_incomplete'])
        text = (root / 'CHATGPT-TASK.md').read_text()
        self.assertIn('## Veille', text)
        self.assertIn('## Reprise', text)
        self.assertIn('## Post-mortem', text)
        self.assertIn('toutes les 6 heures', text)
        self.assertEqual(read_json(root / 'multiplex-jobs.json')['jobs'], [])

    def test_multiplex_profile_generates_two_logical_jobs_and_restore_prompts(self):
        p = profile()
        p['cadence'] = json.loads((ROOT / 'examples/cadence-slow.json').read_text())
        p['runtime'] = {'mode': 'multiplexed', 'reason': 'share physical task slots',
                        'group_id': 'example-watch',
                        'registry_repository': 'example/watch-runtime'}
        root = pack(self.root, p)
        runtime = read_json(root / 'runtime.json')
        jobs = read_json(root / 'multiplex-jobs.json')['jobs']
        self.assertEqual(runtime['mode'], 'multiplexed')
        self.assertNotIn('recovery', runtime)
        self.assertEqual(len(jobs), 2)
        self.assertEqual({j['kind'] for j in jobs}, {'watch', 'postmortem'})
        self.assertIn('Orchestrator', (root / 'MULTIPLEX-TASKS.md').read_text())
        self.assertIn('Worker', (root / 'MULTIPLEX-TASKS.md').read_text())
        self.assertIn('Ne crée PAS deux tâches', (root / 'CHATGPT-TASK.md').read_text())

    def test_no_fake_baseline_or_task(self):
        root = pack(self.root); state = read_json(root / 'state.json')
        self.assertEqual(state['phase'], 'T0_REQUIRED')
        self.assertIsNone(state['baseline'])
        self.assertEqual(state['external_task']['status'], 'not_created')
        self.assertEqual(state['runtime']['status'], 'not_activated')
        self.assertFalse((root / 'baseline').exists())

    def test_existing_research_not_duplicated(self):
        p = profile(); p['integration'].update(mode='reuse-existing', paths=['operator/research.yml'])
        root = pack(self.root, p)
        self.assertEqual(read_json(root / 'state.json')['phase'], 'INTEGRATION_REQUIRED')

    def test_changed_profile_never_overwrites(self):
        generate(profile(), self.root)
        p = profile(); p['objective'] = 'different objective'
        with self.assertRaises(ValueError): generate(p, self.root)

    def test_modified_instruction_detected(self):
        root = pack(self.root); (root / 'UPDATE.md').write_text('Changed')
        with self.assertRaises(ValueError): validate_pack(root)

    def test_symlink_refused(self):
        (self.root / 'link').symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError): generate(profile(), self.root / 'link')

    def test_partial_batch_continues(self):
        profiles = self.root / 'profiles'; profiles.mkdir()
        atomic_json(profiles / 'a-valid.json', profile()); atomic_json(profiles / 'b-invalid.json', {})
        with redirect_stdout(StringIO()):
            code = main(['generate', '--profile-dir', str(profiles), '--out', str(self.root / 'out')])
        self.assertEqual(code, 2)
        report = read_json(self.root / 'out/generation-report.json')
        self.assertEqual([r['status'] for r in report['results']], ['generated', 'blocked'])

    def test_files_are_short(self):
        root = pack(self.root)
        for path in root.iterdir():
            self.assertLessEqual(len(path.read_text().splitlines()), 200, path.name)


if __name__ == '__main__':
    unittest.main()
