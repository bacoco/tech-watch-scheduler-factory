from pathlib import Path
import tempfile
import unittest
from support import pack, checkout, profile
from tech_watch.install import install, origin_repository, git


class Installation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = checkout(self.root / 'target')
        p = profile(); p['analyzed_sha'] = git(self.repo, 'rev-parse', 'HEAD')
        self.pack = pack(self.root, p)

    def test_preview_no_effect(self):
        self.assertEqual(install(self.pack, self.repo)['status'], 'preview')
        self.assertFalse((self.repo / 'scheduler-techno').exists())

    def test_apply_only_directory(self):
        before = (self.repo / 'product.txt').read_bytes()
        self.assertEqual(install(self.pack, self.repo, True)['status'], 'installed-locally')
        self.assertEqual(before, (self.repo / 'product.txt').read_bytes())
        self.assertEqual(install(self.pack, self.repo, True)['status'], 'unchanged')

    def test_target_mismatch(self):
        other = checkout(self.root / 'wrong', 'example/other')
        with self.assertRaises(ValueError): install(self.pack, other, True)
        self.assertFalse((other / 'scheduler-techno').exists())

    def test_existing_human_file_protected(self):
        dest = self.repo / 'scheduler-techno'; dest.mkdir()
        (dest / 'human.md').write_text('keep this')
        with self.assertRaises(ValueError): install(self.pack, self.repo, True)
        self.assertEqual((dest / 'human.md').read_text(), 'keep this')

    def test_extra_payload_refused(self):
        (self.pack / '.env').write_text('do not install')
        with self.assertRaises(ValueError): install(self.pack, self.repo, True)

    def test_symlink_target_refused(self):
        (self.repo / 'scheduler-techno').symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError): install(self.pack, self.repo, True)

    def test_origin_forms(self):
        for value in ['git@github.com:example/image-product.git',
                      'https://github.com/example/image-product.git',
                      'ssh://git@github.com/example/image-product.git']:
            self.assertEqual(origin_repository(value), 'example/image-product')

    def test_malicious_origin(self):
        for value in ['https://github.com.evil/example/image-product',
                      'https://github.com/example/image-product/../other',
                      'https://github.com/example/image-product?bad=true']:
            with self.assertRaises(ValueError): origin_repository(value)

    def test_unrelated_symlinks_in_product_are_not_our_scope(self):
        (self.repo / 'linked-product.txt').symlink_to(self.repo / 'product.txt')
        self.assertEqual(install(self.pack, self.repo, True)['status'], 'installed-locally')

    def test_changed_checkout_refused(self):
        (self.repo / 'product.txt').write_text('unreviewed local changes')
        with self.assertRaises(ValueError): install(self.pack, self.repo, True)

    def test_stale_profile_refused(self):
        stale = pack(self.root / 'stale', profile())
        with self.assertRaises(ValueError): install(stale, self.repo, True)
