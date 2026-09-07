from copy import deepcopy
from pathlib import Path
import json
import subprocess
from tech_watch.common import digest, atomic_json
from tech_watch.render import generate

ROOT = Path(__file__).resolve().parents[1]


def profile():
    return json.loads((ROOT / 'examples/image-product.json').read_text())


def pack(temp, p=None):
    selected = deepcopy(p or profile())
    selected['discovery']['repo_sha'] = selected['analyzed_sha']
    return generate(selected, Path(temp) / 'generated')[0]


def receipt(root, kind='t0', run_id='t0-1'):
    path = f'runs/{run_id}/report.md'
    dest = root / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text('# Synthetic test only\nNo real research or publication.\n')
    research = deepcopy(profile()['discovery'])
    research.update(stage=kind, started_at='2026-09-07T08:00:00+02:00',
                    finished_at='2026-09-07T09:00:00+02:00')
    for s in research['sources']:
        s['accessed_at'] = '2026-09-07T08:30:00+02:00'
    for s in research['searches']:
        s['executed_at'] = '2026-09-07T08:15:00+02:00'
    research_path = f'runs/{run_id}/research.json'
    atomic_json(root / research_path, research)
    return {'schema_version': 1, 'kind': kind, 'run_id': run_id,
        'repository': 'example/image-product', 'repo_sha': 'a' * 40,
        'started_at': '2026-09-07T08:00:00+02:00',
        'finished_at': '2026-09-07T09:00:00+02:00',
        'cutoff_at': '2026-09-07T08:00:00+02:00', 'status': 'complete',
        'blockers': [], 'research': research_path,
        'artifacts': [{'path': path, 'sha256': digest(dest.read_bytes())},
                      {'path': research_path, 'sha256': digest((root / research_path).read_bytes())}],
        'coverage': [{'question_id': q, 'status': 'covered', 'evidence': path,
                      'note': 'Synthetic declared coverage.'} for q in ('q1', 'q2')],
        'delivery': {'status': 'verified', 'evidence': 'Synthetic test, no external publication.'},
        'previous_run_id': None, 'source_checkpoints': {'github': {'cursor': 'test-only'}}}


def checkout(path, repo='example/image-product'):
    path.mkdir()
    for args in [('init', '-b', 'main'), ('remote', 'add', 'origin', f'https://github.com/{repo}.git')]:
        subprocess.run(['git', '-C', str(path), *args], check=True, capture_output=True)
    (path / 'product.txt').write_text('do not touch\n')
    for args in [('config', 'user.name', 'Test Fixture'),
                 ('config', 'user.email', 'test@example.invalid'),
                 ('add', 'product.txt'), ('commit', '-m', 'synthetic fixture')]:
        subprocess.run(['git', '-C', str(path), *args], check=True, capture_output=True)
    return path
