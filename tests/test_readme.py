"""Protect the two-copy-paste ChatGPT-only public entry point."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeTests(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.prompts = re.findall(r'^> (.+)$', self.text, re.MULTILINE)

    def test_no_code_blocks_or_shell_commands(self):
        self.assertNotIn('```', self.text)
        self.assertIsNone(re.search(
            r'(?im)^\s*(?:python\d*\s|pip\s|git clone\s|gh\s|cd\s|\$\s)', self.text))
        self.assertNotIn('python', self.text.lower())

    def test_exactly_two_copyable_requests_for_an_explicit_repo(self):
        self.assertEqual(len(self.prompts), 2)
        for prompt in self.prompts:
            self.assertIn('[LIEN_DU_REPO]', prompt)
            self.assertIn('ChatGPT', prompt)

    def test_first_request_generates_cadence_runtime_and_site_contracts(self):
        prompt = self.prompts[0]
        self.assertIn('https://github.com/bacoco/tech-watch-scheduler-factory/blob/main/'
                      'skills/generate-tech-watch/SKILL.md', prompt)
        for required in ('recherche externe approfondie', 'scheduler-techno',
                         'cadence de veille', 'cadence de post-mortem',
                         'runtime.mode=dedicated', 'multiplexed', 'registry_repository',
                         'RUNTIME', 'multiplex-jobs.json', 'WEBSITE.md',
                         'ne lance pas le T0'):
            self.assertIn(required, prompt)
        self.assertNotIn('chaque lundi', prompt)

    def test_second_request_activates_exact_declared_runtime(self):
        prompt = self.prompts[1]
        for required in ('runtime.mode=dedicated', 'runtime.mode=multiplexed',
                         'Veille —', 'Post-mortem —', 'Tech Watch Orchestrator',
                         'Tech Watch Worker', 'dedicated_tasks_disabled=true',
                         'dispatch déterministe', 'retry borné',
                         'résolution du chemin uniquement depuis le registre canonique'):
            self.assertIn(required, prompt)
        self.assertIn('cadence `watch`', prompt)
        self.assertIn('cadence `postmortem`', prompt)
        self.assertNotIn('chaque lundi matin', prompt)
        self.assertNotIn('chaque vendredi matin', prompt)

    def test_public_website_remains_separate(self):
        first, second = self.prompts
        self.assertIn('nom-du-repo-website', first)
        for required in ('repo public `*-website`', 'GitHub Pages', 'main et /(root)',
                         'ne rends jamais public le repo source'):
            self.assertIn(required, second)
        for path in ('docs/WEBSITE.md', 'templates/watch/WEBSITE.md',
                     'tools/render_public_website.py', 'tools/create_public_website_repo.py',
                     'tools/publish_public_website.py'):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_runtime_and_cadence_examples_exist(self):
        for path in ('examples/cadence-fast.json', 'examples/cadence-slow.json',
                     'examples/multiplex-registry.json', 'docs/RUNTIME.md',
                     'templates/watch/RUNTIME.md'):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_access_and_proof_language_remains_explicit(self):
        for required in ('comptes gratuits éligibles', 'avec des limites',
                         'permissions', 'ne prouvent pas', 'synthétiques'):
            self.assertIn(required, self.text)
        self.assertIn('https://help.openai.com/en/articles/10291617-', self.text)

    def test_detailed_task_guide_is_runtime_aware(self):
        text = (ROOT / 'docs/CHATGPT.md').read_text(encoding='utf-8')
        self.assertIn('dedicated', text)
        self.assertIn('multiplexed', text)
        self.assertIn('Orchestrator', text)
        self.assertIn('Worker', text)
        self.assertIn('POST-MORTEM.md', text)


if __name__ == '__main__':
    unittest.main()
