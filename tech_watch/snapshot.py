"""Bounded evidence sampling, explicitly not semantic analysis or audit."""
from pathlib import Path
import base64
import re
from .common import atomic_json, no_symlinks, relative, require

TEXT_SUFFIXES = {'.md', '.toml', '.json', '.yml', '.yaml', '.py', '.ts', '.tsx', '.jsx', '.html', '.swift'}
BANNED_PARTS = {'.git', 'node_modules', '.venv', 'vendor', 'data', 'datasets',
                'customer', 'customers', 'secrets', 'credentials', 'backups', 'uploads'}


def safe_candidate(path):
    relative(path)
    p = Path(path)
    lower = [x.lower() for x in p.parts]
    return (not any(x in BANNED_PARTS or x.startswith('.env') for x in lower)
            and not re.search(r'(secret|credential|private[-_]?key|token)', p.name, re.I)
            and p.suffix.lower() in TEXT_SUFFIXES)


def priority(path):
    name = Path(path).name.lower()
    if name in {'readme.md', 'agents.md', 'claude.md'}:
        return (0, len(path), path)
    if re.search(r'(usage|user[-_]?guide|getting.started|workflow|journey|product|metier|onboard)', path, re.I):
        return (1, len(path), path)
    if name in {'package.json', 'pyproject.toml', 'cargo.toml', 'package.swift'}:
        return (4, len(path), path)
    if re.search(r'(architect|research|scout|scheduler|decision|test)', path, re.I):
        return (2, len(path), path)
    return (4, len(path), path)


def snapshot(client, repo, out, max_files=18):
    require(1 <= max_files <= 50, 'max-files must be 1..50')
    dest = Path(out)
    no_symlinks(dest)
    require(not dest.exists(), 'snapshot output already exists')
    meta = client.metadata(repo)
    require(not meta['archived'], 'archived repository: no automatic preparation')
    sha = client.head(repo, meta['default_branch'])
    tree = client.get(f'/repos/{repo}/git/trees/{sha}', recursive='1')
    require(not tree.get('truncated'), 'tree truncated; use targeted connector reads')
    entries = {x['path']: x for x in tree['tree'] if x['type'] == 'blob'
               and x.get('mode') != '120000' and safe_candidate(x['path'])}
    chosen = sorted(entries, key=priority)[:max_files]
    dest.mkdir(parents=True)
    facts = {'repository': repo, 'analyzed_sha': sha, 'default_branch': meta['default_branch'],
        'private': meta['private'], 'fork': meta['fork'], 'pushed_at': meta['pushed_at'],
        'semantic_analysis_done': False, 'selection': 'bounded heuristic sample',
        'candidate_count': len(entries), 'max_files': max_files, 'files': [], 'gaps': []}
    for index, path in enumerate(chosen):
        entry = entries[path]
        if entry.get('size', 0) > 24000:
            facts['gaps'].append({'path': path, 'reason': 'file over 24 KB, read targeted lines'})
            continue
        blob = client.get(f'/repos/{repo}/git/blobs/{entry["sha"]}')
        try:
            require(blob.get('encoding') == 'base64', 'unsupported blob encoding')
            data = base64.b64decode(blob['content']).decode('utf-8')
        except (UnicodeError, ValueError):
            facts['gaps'].append({'path': path, 'reason': 'not readable UTF-8'})
            continue
        local = f'evidence-{index:02d}.txt'
        (dest / local).write_text(data, encoding='utf-8')
        facts['files'].append({'path': path, 'blob_sha': entry['sha'],
            'local_file': local, 'line_count': len(data.splitlines())})
    for label, endpoint in [('issues_and_prs', 'issues'), ('commits', 'commits')]:
        try:
            params = {'state': 'all', 'sort': 'updated', 'per_page': 30} if label == 'issues_and_prs' else {'sha': sha, 'per_page': 10}
            values = client.get(f'/repos/{repo}/{endpoint}', **params)
            # Metadata only: avoid copying issue bodies and private correspondence.
            fields = ('number', 'title', 'state', 'html_url', 'updated_at', 'pull_request')
            compact = [{k: v.get(k) for k in fields} for v in values] if label == 'issues_and_prs' else [{'sha': v['sha'], 'html_url': v['html_url']} for v in values]
            atomic_json(dest / f'{label}.json', compact)
        except ValueError as exc:
            facts['gaps'].append({'path': endpoint, 'reason': str(exc)})
    facts['gaps'].append({'path': 'issues/pulls',
        'reason': 'recent metadata sample only; agent must read relevant bodies and history'})
    atomic_json(dest / 'snapshot.json', facts)
    (dest / 'ANALYSE-A-FAIRE.md').write_text(
        '# Analyse à effectuer par l’agent\n\nLire les preuves et approfondir les zones utiles.\n'
        'Ne pas confondre ce snapshot avec un T0. Produire le profil selon docs/PROFILE.md.\n'
        'Ne pas envoyer ces captures privées dans des recherches web.\n', encoding='utf-8')
    return facts
