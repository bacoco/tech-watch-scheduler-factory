"""Protect the short two-copy-paste ChatGPT entry point and canonical prompts."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeTests(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.prompts = re.findall(r'^> (.+)$', self.text, re.MULTILINE)
        self.prepare = (ROOT / 'prompts/PREPARE.md').read_text(encoding='utf-8')
        self.activate = (ROOT / 'prompts/ACTIVATE.md').read_text(encoding='utf-8')

    def test_no_code_blocks_or_shell_commands(self):
        self.assertNotIn('```', self.text)
        self.assertIsNone(re.search(
            r'(?im)^\s*(?:python\d*\s|pip\s|git clone\s|gh\s|cd\s|\$\s)', self.text))
        self.assertNotIn('python', self.text.lower())

    def test_exactly_two_short_copyable_requests(self):
        self.assertEqual(len(self.prompts), 2)
        for prompt in self.prompts:
            self.assertIn('[LIEN_DU_REPO]', prompt)
            self.assertIn('ChatGPT', prompt)
            self.assertIn('TARGET_REPOSITORY', prompt)
            self.assertLess(len(prompt), 450)
        self.assertIn('/prompts/PREPARE.md', self.prompts[0])
        self.assertIn('/prompts/ACTIVATE.md', self.prompts[1])

    def test_prepare_prompt_carries_full_generation_contract(self):
        for required in ('skills/generate-tech-watch/SKILL.md',
                         'recherche externe approfondie', 'scheduler-techno/',
                         'cadence.watch', 'cadence.postmortem', 'dedicated',
                         'multiplexed', 'registry_repository', 'RUNTIME.md',
                         'multiplex-jobs.json', 'WEBSITE.md', 'website.json',
                         'ne lance pas le T0'):
            self.assertIn(required, self.prepare)

    def test_activate_prompt_carries_runtime_and_website_contract(self):
        for required in ('runtime.mode', 'Veille —', 'Post-mortem —',
                         'Tech Watch Orchestrator', 'Tech Watch Worker',
                         'dedicated_tasks_disabled=true', 'dispatch_id',
                         'retry borné', 'registre canonique', 'RECHERCHE.md',
                         'repo PUBLIC séparé `*-website`', 'GitHub Pages',
                         'home + archive', 'watch_status', 'website_status'):
            self.assertIn(required, self.activate)

    def test_readme_explicitly_says_website_is_generated_and_updated(self):
        for required in ('site public généré puis mis à jour automatiquement',
                         'génère le site puis le met à jour',
                         'À chaque exécution suivante validée',
                         'reconstruire la home + l\'archive'):
            self.assertIn(required, self.text)

    def test_canonical_prompt_files_exist(self):
        for path in ('prompts/README.md', 'prompts/PREPARE.md', 'prompts/ACTIVATE.md',
                     'docs/WEBSITE.md', 'templates/watch/WEBSITE.md',
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
