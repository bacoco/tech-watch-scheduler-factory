from pathlib import Path
import base64
import tempfile
import unittest
from unittest.mock import patch
from tech_watch.github import GitHub, NoRedirect
from tech_watch.snapshot import safe_candidate, snapshot


class FakeClient:
    def metadata(self, repo):
        return {'default_branch': 'trunk', 'archived': False, 'private': True,
                'fork': False, 'pushed_at': '2026-09-07T00:00:00Z'}

    def head(self, repo, branch):
        return 'b' * 40

    def get(self, endpoint, **params):
        if '/git/trees/' in endpoint:
            return {'tree': [{'path': 'README.md', 'type': 'blob', 'mode': '100644',
                              'sha': 'c' * 40, 'size': 12}], 'truncated': False}
        if '/git/blobs/' in endpoint:
            return {'content': base64.b64encode(b'# Example\n').decode(), 'encoding': 'base64'}
        return []


class GitHubReads(unittest.TestCase):
    def test_sensitive_paths_excluded(self):
        for path in ['.env', 'data/customer.json', 'secrets/key.md', 'private_key.py',
                     'src/credentials.yml', 'uploads/file.md']:
            self.assertFalse(safe_candidate(path), path)

    def test_source_path_allowed(self):
        self.assertTrue(safe_candidate('src/image_service.py'))

    def test_snapshot_is_not_analysis(self):
        with tempfile.TemporaryDirectory() as temp:
            data = snapshot(FakeClient(), 'example/image-product', Path(temp) / 'snapshot')
            self.assertFalse(data['semantic_analysis_done'])
            self.assertEqual(data['default_branch'], 'trunk')
            self.assertEqual(data['files'][0]['path'], 'README.md')

    def test_reject_truncated_tree(self):
        client = FakeClient()
        with patch.object(client, 'get', return_value={'tree': [], 'truncated': True}):
            with tempfile.TemporaryDirectory() as temp:
                with self.assertRaises(ValueError):
                    snapshot(client, 'example/image-product', Path(temp) / 'snapshot')

    def test_redirect_refused(self):
        with self.assertRaises(ValueError):
            NoRedirect().redirect_request(None, None, 302, '', {}, 'https://evil.invalid')

    def test_public_discovery_marked(self):
        with patch.dict('os.environ', {}, clear=True):
            client = GitHub()
            row = {'owner': {'login': 'example'}, 'name': 'repo', 'archived': False,
                   'full_name': 'example/repo'}
            with patch.object(client, 'get', return_value=[row]):
                result = client.discover('example', 10)
            self.assertEqual(result['visibility'], 'public-only')
            self.assertEqual(len(result['repositories']), 1)
