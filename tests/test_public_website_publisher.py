import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'tools' / 'publish_public_website.py'
SPEC = importlib.util.spec_from_file_location('public_website_publisher', SCRIPT)
publisher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publisher)


class PublicWebsitePublisher(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for rel, text in {
            'index.html': '<h1>Latest</h1>',
            'archive/index.html': '<h1>Archive</h1>',
            'assets/style.css': 'body{}',
            '.nojekyll': '',
            'site.json': json.dumps({'schema_version': 1,
                'source_repository': 'example/image-product',
                'public_repository': 'example/image-product-website', 'editions': []}),
        }.items():
            path = self.root / rel; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')

    def test_site_inventory_and_identity(self):
        root, files = publisher.site_files(self.root)
        self.assertEqual(root, self.root.resolve())
        self.assertEqual(publisher.identity(root, files),
                         ('example/image-product', 'example/image-product-website'))

    def test_unexpected_file_is_refused(self):
        (self.root / 'secret.txt').write_text('no')
        with self.assertRaises(SystemExit):
            publisher.site_files(self.root)

    def test_wrong_public_repository_is_refused(self):
        manifest = json.loads((self.root / 'site.json').read_text())
        manifest['public_repository'] = 'example/other-public'
        (self.root / 'site.json').write_text(json.dumps(manifest))
        _, files = publisher.site_files(self.root)
        with self.assertRaises(SystemExit):
            publisher.identity(self.root, files)

    def test_dry_run_never_calls_github(self):
        with patch('sys.argv', ['publish_public_website.py', '--site-dir', str(self.root)]), \
                patch.object(publisher, 'request') as request, \
                contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(publisher.main(), 0)
        request.assert_not_called()
        self.assertIn('image-product-website', output.getvalue())


if __name__ == '__main__':
    unittest.main()
