from pathlib import Path
import tempfile
import unittest

from tech_watch.common import read_json
from tech_watch.website import render_public_site, website_repository


class WebsiteRendering(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def edition(self, date='2026-09-08', slug='watch-2026-09-08'):
        return {'slug': slug, 'date': date, 'title': f'Watch {date}',
                'excerpt': 'Material changes only.',
                'body_html': '<h2>Changes</h2><p>Verified public result.</p>'}

    def test_target_name_is_separate_public_repo(self):
        self.assertEqual(website_repository('example/image-product'),
                         'example/image-product-website')

    def test_render_builds_navigable_root(self):
        result = render_public_site('example/image-product', self.edition(), self.root)
        self.assertEqual(result['edition_count'], 1)
        for path in ('.nojekyll', 'index.html', 'archive/index.html',
                     'assets/style.css', 'watch-2026-09-08/index.html', 'site.json'):
            self.assertTrue((self.root / path).exists(), path)
        manifest = read_json(self.root / 'site.json')
        self.assertEqual(manifest['public_repository'], 'example/image-product-website')
        self.assertNotIn('scheduler-techno', (self.root / 'index.html').read_text())

    def test_idempotent_same_edition(self):
        first = render_public_site('example/image-product', self.edition(), self.root)
        second = render_public_site('example/image-product', self.edition(), self.root)
        self.assertEqual(first['edition_count'], second['edition_count'])

    def test_archive_preserves_multiple_editions(self):
        render_public_site('example/image-product', self.edition('2026-09-07', 'watch-2026-09-07'), self.root)
        render_public_site('example/image-product', self.edition(), self.root)
        archive = (self.root / 'archive/index.html').read_text()
        self.assertIn('watch-2026-09-07', archive)
        self.assertIn('watch-2026-09-08', archive)
        self.assertEqual(read_json(self.root / 'site.json')['editions'][0]['date'], '2026-09-08')

    def test_active_html_is_rejected(self):
        bad = self.edition(); bad['body_html'] = '<script>alert(1)</script>'
        with self.assertRaises(ValueError):
            render_public_site('example/image-product', bad, self.root)

    def test_existing_slug_is_immutable(self):
        render_public_site('example/image-product', self.edition(), self.root)
        changed = self.edition(); changed['body_html'] = '<p>Different</p>'
        with self.assertRaises(ValueError):
            render_public_site('example/image-product', changed, self.root)


if __name__ == '__main__':
    unittest.main()
