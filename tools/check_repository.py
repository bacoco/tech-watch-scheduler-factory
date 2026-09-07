"""Validate the checkout without dependencies or network."""
from pathlib import Path
import ast
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', '__pycache__', 'work', 'dist', '.venv'}


def files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
                  and not any(x in SKIP or x.endswith('.egg-info') for x in p.relative_to(ROOT).parts))


def main():
    errors = []
    paths = files()
    for p in paths:
        if p.is_symlink():
            errors.append(f'symlink: {p.relative_to(ROOT)}'); continue
        if p.suffix not in {'.md', '.py', '.json', '.yml', '.yaml', '.toml'}:
            continue
        text = p.read_text(encoding='utf-8')
        if len(text.splitlines()) > 200:
            errors.append(f'PD >200 lines: {p.relative_to(ROOT)}')
        if p.suffix == '.py':
            try: ast.parse(text, filename=str(p))
            except SyntaxError as exc: errors.append(str(exc))
        if p.suffix == '.json':
            try: json.loads(text)
            except ValueError as exc: errors.append(f'{p}: {exc}')
        if p.suffix == '.md' and 'templates' not in p.relative_to(ROOT).parts:
            for url in re.findall(r'\]\(([^)]+)\)', text):
                if '://' in url or url.startswith('#'):
                    continue
                target = p.parent / url.split('#')[0]
                if not target.exists(): errors.append(f'broken link: {p.relative_to(ROOT)} -> {url}')
    manifest = ROOT / 'tools/publish-files.json'
    if manifest.exists():
        allowed = set(json.loads(manifest.read_text()))
        actual = {p.relative_to(ROOT).as_posix() for p in paths}
        if actual != allowed:
            errors.append(f'publication inventory mismatch: {sorted(actual ^ allowed)}')
    for directory in ('tech_watch', 'docs', 'tests', 'tools', 'skills', 'examples', 'templates'):
        if not (ROOT / directory / 'README.md').exists(): errors.append('missing index: ' + directory)
    if errors:
        print('\n'.join(errors), file=sys.stderr); return 2
    print(f'PASS: {len(paths)} files; Python syntax, JSON, local links, <=200 lines, inventory.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
