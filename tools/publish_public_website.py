#!/usr/bin/env python3
"""Publish one rendered static site atomically to its separate public GitHub repo."""
import argparse
import json
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

API = 'https://api.github.com'
ALLOWED_SUFFIXES = {'.html', '.css', '.json'}
REQUIRED = {'index.html', 'archive/index.html', 'assets/style.css', '.nojekyll', 'site.json'}


def request(method, path, payload=None, allow_404=False):
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        raise SystemExit('BLOCKED: GITHUB_TOKEN is required for publication')
    data = None if payload is None else json.dumps(payload).encode()
    req = Request(API + path, data=data, method=method, headers={
        'Accept': 'application/vnd.github+json', 'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'tech-watch-scheduler-factory'})
    try:
        with urlopen(req, timeout=30) as response:
            raw = response.read().decode()
            return response.status, json.loads(raw) if raw else {}
    except HTTPError as exc:
        raw = exc.read().decode()
        if allow_404 and exc.code == 404:
            return 404, {}
        raise SystemExit(f'BLOCKED: GitHub API {exc.code}: {raw[:1000] or exc.reason}') from exc


def site_files(root):
    root = Path(root).resolve()
    if not root.is_dir():
        raise SystemExit('BLOCKED: site directory is missing')
    result = {}
    for path in root.rglob('*'):
        if path.is_symlink():
            raise SystemExit(f'BLOCKED: symlink refused: {path}')
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel != '.nojekyll' and path.suffix not in ALLOWED_SUFFIXES:
            raise SystemExit(f'BLOCKED: unexpected public file: {rel}')
        data = path.read_bytes()
        if len(data) > 1_000_000:
            raise SystemExit(f'BLOCKED: public file too large: {rel}')
        try:
            result[rel] = data.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise SystemExit(f'BLOCKED: non-text public file: {rel}') from exc
    missing = REQUIRED - set(result)
    if missing:
        raise SystemExit(f'BLOCKED: incomplete site: {sorted(missing)}')
    return root, result


def identity(root, files):
    manifest = json.loads(files['site.json'])
    source = manifest.get('source_repository')
    target = manifest.get('public_repository')
    if not isinstance(source, str) or source.count('/') != 1:
        raise SystemExit('BLOCKED: invalid source_repository in site.json')
    if not isinstance(target, str) or target.count('/') != 1:
        raise SystemExit('BLOCKED: invalid public_repository in site.json')
    owner, name = source.split('/', 1)
    expected = f'{owner}/{name}-website'
    if target != expected:
        raise SystemExit(f'BLOCKED: public repository mismatch: expected {expected}')
    return source, target


def blob(repo, text):
    owner, name = repo.split('/', 1)
    _, result = request('POST', f'/repos/{quote(owner)}/{quote(name)}/git/blobs',
                        {'content': text, 'encoding': 'utf-8'})
    return result['sha']


def publish(repo, files):
    owner, name = repo.split('/', 1)
    prefix = f'/repos/{quote(owner)}/{quote(name)}'
    status, meta = request('GET', prefix, allow_404=True)
    if status == 404:
        raise SystemExit('BLOCKED: public repository does not exist; create it first')
    if meta.get('private') is not False:
        raise SystemExit('BLOCKED: website repository must be public')
    status, ref = request('GET', prefix + '/git/ref/heads/main', allow_404=True)
    parent = None
    base_tree = None
    if status != 404:
        parent = ref['object']['sha']
        _, commit = request('GET', prefix + f'/git/commits/{parent}')
        base_tree = commit['tree']['sha']
    entries = [{'path': path, 'mode': '100644', 'type': 'blob', 'sha': blob(repo, text)}
               for path, text in sorted(files.items())]
    payload = {'tree': entries}
    if base_tree:
        payload['base_tree'] = base_tree
    _, tree = request('POST', prefix + '/git/trees', payload)
    if base_tree and tree['sha'] == base_tree:
        return {'status': 'unchanged', 'commit': parent}
    commit_payload = {'message': 'publish: update public watch site', 'tree': tree['sha'],
                      'parents': [parent] if parent else []}
    _, commit = request('POST', prefix + '/git/commits', commit_payload)
    if parent:
        request('PATCH', prefix + '/git/refs/heads/main', {'sha': commit['sha'], 'force': False})
    else:
        request('POST', prefix + '/git/refs', {'ref': 'refs/heads/main', 'sha': commit['sha']})
    return {'status': 'published', 'commit': commit['sha']}


def enable_pages(repo):
    owner, name = repo.split('/', 1)
    prefix = f'/repos/{quote(owner)}/{quote(name)}'
    status, pages = request('GET', prefix + '/pages', allow_404=True)
    if status == 404:
        _, pages = request('POST', prefix + '/pages', {'source': {'branch': 'main', 'path': '/'}})
    return {'status': 'enabled', 'url': pages.get('html_url')}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site-dir', required=True)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--enable-pages', action='store_true')
    args = parser.parse_args()
    root, files = site_files(args.site_dir)
    source, target = identity(root, files)
    result = {'source_repository': source, 'public_repository': target,
              'file_count': len(files), 'apply': args.apply}
    if not args.apply:
        print(json.dumps(result, ensure_ascii=False, indent=2)); return 0
    result.update(publish(target, files))
    if args.enable_pages:
        try:
            result['pages'] = enable_pages(target)
        except SystemExit as exc:
            result['pages'] = {'status': 'blocked', 'reason': str(exc)}
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0


if __name__ == '__main__':
    raise SystemExit(main())
