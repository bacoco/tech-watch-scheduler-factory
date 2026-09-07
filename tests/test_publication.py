"""Publication visibility guard: no network or authenticated Git is used."""
import contextlib
import importlib.util
import io
from pathlib import Path
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'tools' / 'publish_repository.py'
SPEC = importlib.util.spec_from_file_location('publication_helper', SCRIPT)
publication = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publication)


class PublicationVisibility(unittest.TestCase):
    def test_private_allowed_by_default(self):
        publication.require_allowed_visibility({'private': True})

    def test_public_denied_by_default(self):
        with self.assertRaisesRegex(RuntimeError, '--allow-public'):
            publication.require_allowed_visibility({'private': False})

    def test_public_allowed_only_by_explicit_flag(self):
        publication.require_allowed_visibility({'private': False}, True)

    def test_private_still_allowed_with_public_flag(self):
        publication.require_allowed_visibility({'private': True}, True)

    def test_missing_visibility_refused(self):
        with self.assertRaisesRegex(RuntimeError, 'unknown'):
            publication.require_allowed_visibility({}, True)

    def test_non_boolean_visibility_refused(self):
        for value in ('false', 0, None, [], {}):
            with self.subTest(value=value), self.assertRaises(RuntimeError):
                publication.require_allowed_visibility({'private': value}, True)

    def test_non_object_metadata_refused(self):
        with self.assertRaises(RuntimeError):
            publication.require_allowed_visibility(None, True)

    def test_public_preview_never_runs_remote_commands(self):
        with patch('sys.argv', ['publish_repository.py', '--allow-public']), \
                patch.object(publication, 'run') as run, \
                contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(publication.main(), 0)
        run.assert_not_called()
        self.assertIn('public destination permitted: True', output.getvalue())


if __name__ == '__main__':
    unittest.main()
