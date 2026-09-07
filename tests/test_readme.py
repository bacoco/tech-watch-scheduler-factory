"""Keep the public entry point usable by copying natural-language requests."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeTests(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / 'README.md').read_text(encoding='utf-8')

    def test_no_code_blocks_or_shell_commands(self):
        self.assertNotIn('```', self.text)
        self.assertIsNone(re.search(
            r'(?im)^\s*(?:python\d*\s|pip\s|git clone\s|gh\s|cd\s|\$\s)',
            self.text))
        self.assertNotIn('python', self.text.lower())

    def test_copyable_request_resolves_the_skill(self):
        self.assertIn('> Lis et applique le guide de génération', self.text)
        self.assertIn(
            'https://github.com/bacoco/tech-watch-scheduler-factory/blob/main/'
            'skills/generate-tech-watch/SKILL.md', self.text)
        self.assertTrue((ROOT / 'skills/generate-tech-watch/SKILL.md').is_file())

    def test_access_limits_and_lifecycle_remain_explicit(self):
        for required in ('accès', 'recherche externe approfondie',
                         'T0', 'mise à jour', 'ne crée pas une tâche planifiée',
                         'jamais prétendre', 'synthétiques'):
            self.assertIn(required, self.text)


if __name__ == '__main__':
    unittest.main()
