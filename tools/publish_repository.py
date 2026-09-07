"""Explicitly publish this checkout using the owner's already-authenticated gh CLI."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(args, check=True):
    p = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=120)
    if check and p.returncode:
        # gh/git errors may contain account details; never print environment or tokens.
        raise RuntimeError(f'{args[0]} command failed (exit {p.returncode}): {p.stderr[-1200:]}')
    return p


def git(*args, check=True):
    return run(['git', '-c', 'credential.helper=',
                '-c', 'credential.helper=!gh auth git-credential', *args], check=check)


def require_allowed_visibility(metadata, allow_public=False):
    """Public delivery requires an explicit flag, never an inferred permission."""
    if not isinstance(metadata, dict) or type(metadata.get('private')) is not bool:
        raise RuntimeError('unknown destination visibility; refusing publication')
    if not metadata['private'] and not allow_public:
        raise RuntimeError('destination is public; inspect the files then explicitly use --allow-public')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--owner', default='bacoco')
    p.add_argument('--name', default='tech-watch-scheduler-factory')
    p.add_argument('--apply', action='store_true')
    p.add_argument('--allow-public', action='store_true',
                   help='Allow an existing public destination after reviewing the publication inventory')
    a = p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*', a.owner):
        raise ValueError('invalid owner')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', a.name):
        raise ValueError('invalid repo name')
    full = f'{a.owner}/{a.name}'
    if not a.apply:
        print(f'PREVIEW: validate, create private {full} if absent, push main, verify exact SHA.')
        print('Existing public destination permitted: ' + str(a.allow_public))
        print('No remote operation. Add --apply to authorize these effects.')
        return 0
    if not shutil.which('gh') or not shutil.which('git'):
        raise RuntimeError('git and authenticated gh are required; no credentials are embedded')
    run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'])
    run([sys.executable, 'tools/check_repository.py'])
    login = run(['gh', 'api', 'user', '--jq', '.login']).stdout.strip()
    if login.lower() != a.owner.lower():
        raise RuntimeError(f'authenticated owner differs from {a.owner}; no write performed')
    inventory = json.loads((ROOT / 'tools/publish-files.json').read_text())
    if (ROOT / '.git').exists():
        top = Path(git('rev-parse', '--show-toplevel').stdout.strip()).resolve()
        if top != ROOT.resolve(): raise RuntimeError('checkout is nested in another repository')
        if git('branch', '--show-current').stdout.strip() != 'main':
            raise RuntimeError('refusing to change a non-main checkout')
        tracked = set(git('ls-files').stdout.splitlines())
        if not tracked <= set(inventory): raise RuntimeError('unexpected tracked files; inspect first')
    else:
        # Refuse an enclosing Git checkout: do not stage files in a different project.
        parent_check = run(['git', '-C', str(ROOT.parent), 'rev-parse', '--show-toplevel'], check=False)
        if parent_check.returncode == 0: raise RuntimeError('extract outside another Git checkout')
        git('init', '-b', 'main')
    if git('config', 'user.name', check=False).returncode:
        git('config', 'user.name', 'Tech Watch Factory')
    if git('config', 'user.email', check=False).returncode:
        git('config', 'user.email', 'noreply@users.noreply.github.com')
    git('add', '--', *inventory)
    if git('diff', '--cached', '--quiet', check=False).returncode:
        git('commit', '-m', 'feat: repository-specific tech-watch scheduler factory')
    local_sha = git('rev-parse', 'HEAD').stdout.strip()
    origin = git('remote', 'get-url', 'origin', check=False)
    url = f'https://github.com/{full}.git'
    if origin.returncode == 0 and origin.stdout.strip() != url:
        raise RuntimeError('origin differs from requested destination; no remote write performed')
    existing = run(['gh', 'api', f'repos/{full}'], check=False)
    if existing.returncode:
        if '404' not in existing.stderr: raise RuntimeError('repository lookup failed; not assumed absent')
        run(['gh', 'repo', 'create', full, '--private', '--description',
             'Repository-specific technology watch instruction factory: T0 then updates'])
    else:
        require_allowed_visibility(json.loads(existing.stdout), a.allow_public)
    if origin.returncode:
        git('remote', 'add', 'origin', url)
    heads = git('ls-remote', '--heads', 'origin').stdout.strip()
    expected = f'{local_sha}\trefs/heads/main'
    if heads and heads != expected:
        raise RuntimeError('remote is not empty or identical; refusing to overwrite/reconcile blindly')
    if not heads:
        git('push', '--set-upstream', 'origin', 'HEAD:refs/heads/main')
    remote_sha = git('ls-remote', 'origin', 'refs/heads/main').stdout.split()[0]
    if remote_sha != local_sha: raise RuntimeError('remote SHA verification failed')
    raw = run(['gh', 'api', f'repos/{full}/contents/README.md?ref={remote_sha}']).stdout
    if not json.loads(raw).get('sha'): raise RuntimeError('remote README not verified')
    print(json.dumps({'status': 'published-and-reread', 'repository': full,
                      'url': f'https://github.com/{full}', 'sha': remote_sha,
                      'task_created': False}, indent=2))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, OSError, subprocess.TimeoutExpired) as exc:
        print(f'BLOCKED: {exc}', file=sys.stderr)
        raise SystemExit(2)
