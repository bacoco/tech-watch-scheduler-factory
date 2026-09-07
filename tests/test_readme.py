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
            r'(?im)^\s*(?:python\d*\s|pip\s|git clone\s|gh\s|cd\s|\$\s)',
            self.text))
        self.assertNotIn('python', self.text.lower())

    def test_exactly_two_copyable_requests_for_an_explicit_repo(self):
        self.assertEqual(len(self.prompts), 2)
        for prompt in self.prompts:
            self.assertIn('[LIEN_DU_REPO]', prompt)
            self.assertIn('ChatGPT', prompt)
        self.assertNotIn('dix dépôts', self.text)

    def test_first_request_fetches_factory_and_installs_only(self):
        prompt = self.prompts[0]
        self.assertIn(
            'https://github.com/bacoco/tech-watch-scheduler-factory/blob/main/'
            'skills/generate-tech-watch/SKILL.md', prompt)
        self.assertTrue((ROOT / 'skills/generate-tech-watch/SKILL.md').is_file())
        for required in ('recherche externe approfondie', 'scheduler-techno',
                         'ne lance pas encore le T0',
                         'ne crée aucune tâche planifiée'):
            self.assertIn(required, prompt)

    def test_second_request_creates_two_separate_weekly_tasks(self):
        prompt = self.prompts[1]
        for required in ('deux tâches planifiées distinctes', 'Veille —',
                         'Post-mortem —', 'lundi matin', 'vendredi matin',
                         'Europe/Paris', 'identifiant', 'état vérifiés',
                         'pas seulement leurs textes', 'simples rappels',
                         'réutilise-la', 'ne devront pas travailler à partir '
                         "d'une copie figée"):
            self.assertIn(required, prompt)

    def test_scheduled_lifecycle_and_access_remain_explicit(self):
        prompt = self.prompts[1]
        for required in ('T0 gelé', 'mises à jour', 'reliront les instructions',
                         'approbations requises', 'outil de planification',
                         "sans annoncer de création ou d'autonomie fictive"):
            self.assertIn(required, prompt)
        for required in ('accès', 'ne crée pas une tâche planifiée',
                         'jamais prétendre', 'synthétiques'):
            self.assertIn(required, self.text)

    def test_free_access_is_conditional_and_sourced(self):
        for required in ('comptes gratuits éligibles', 'avec des limites',
                         'https://help.openai.com/en/articles/10291617-',
                         'Ce n\'est pas une promesse de gratuité illimitée'):
            self.assertIn(required, self.text)

    def test_detailed_task_guide_matches_two_task_journey(self):
        text = (ROOT / 'docs/CHATGPT.md').read_text(encoding='utf-8')
        self.assertIn('deux tâches distinctes', text)
        self.assertIn('POST-MORTEM.md', text)
        self.assertIn('Ne pas fusionner ce second travail', text)
        self.assertNotIn('branche du même cycle', text)


if __name__ == '__main__':
    unittest.main()
