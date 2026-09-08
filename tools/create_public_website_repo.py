#!/usr/bin/env python3
"""Explicit GitHub REST helper for creating the separate public website repo."""
import argparse
import json
import os
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

API = 'https://api.github.com'


def request(method, path, payload=None, allow_404=False):
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        raise SystemExit('BLOCKED: GITHUB_TOKEN is required for this local helper')
    data = None if payload is None else json.dumps(payload).encode()
    req = Request(API + path, data=data, method=method, headers={
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'tech-watch-scheduler-factory'})
    try:
        with urlopen(req, timeout=30) as response:
            raw = response.read().decode()
            return response.status, json.loads(raw) if raw else {}
    except HTTPError as exc:
        raw = exc.read().decode()
        if allow_404 and exc.code == 404:
            return 404, {}
        message = raw[:1000] if raw else exc.reason
        raise SystemExit(f'BLOCKED: GitHub API {exc.code}: {message}') from exc


def target_name(source):
    if source.count('/') != 1:
        raise SystemExit('BLOCKED: source must be owner/name')
    owner, name = source.split('/', 1)
    return owner, f'{name}-website'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-repo', required=True)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--enable-pages', action='store_true')
    args = parser.parse_args()
    owner, name = target_name(args.source_repo)
    target = f'{owner}/{name}'
    plan = {'source_repository': args.source_repo, 'public_repository': target,
            'visibility': 'public', 'default_branch': 'main',
            'pages_source': 'main:/(root)', 'apply': args.apply}
    if not args.apply:
        print(json.dumps(plan, indent=2))
        return 0
    _, viewer = request('GET', '/user')
    status, repo = request('GET', f'/repos/{quote(owner)}/{quote(name)}', allow_404=True)
    if status == 404:
        endpoint = '/user/repos' if viewer.get('login') == owner else f'/orgs/{quote(owner)}/repos'
        _, repo = request('POST', endpoint, {
            'name': name, 'private': False, 'auto_init': True,
            'description': f'Public static watch site for {args.source_repo}'})
    elif repo.get('private'):
        raise SystemExit('BLOCKED: target repository already exists but is private')
    result = {'public_repository': target, 'html_url': repo.get('html_url'),
              'created_or_verified_public': True,
              'pages_settings_url': f'https://github.com/{target}/settings/pages'}
    if args.enable_pages:
        try:
            page_status, pages = request('GET',
                f'/repos/{quote(owner)}/{quote(name)}/pages', allow_404=True)
            if page_status == 404:
                _, pages = request('POST', f'/repos/{quote(owner)}/{quote(name)}/pages',
                                   {'source': {'branch': 'main', 'path': '/'}})
            result['pages'] = {'status': 'enabled', 'url': pages.get('html_url')}
        except SystemExit as exc:
            result['pages'] = {'status': 'blocked', 'reason': str(exc)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
