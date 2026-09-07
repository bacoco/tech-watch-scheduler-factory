"""Local receipt validation and one-time T0 freeze; not a research executor."""
from pathlib import Path
import os
import re
import shutil
import tempfile
from .common import (SHA_RE, atomic_json, digest, instant, lock, no_symlinks,
                     read_json, relative, require)
from .render import validate_pack
from .discovery import validate_discovery


def receipt(root, data, kind, profile):
    require(data.get('schema_version') == 1 and data.get('kind') == kind,
            'invalid receipt schema/kind')
    require(data['repository'] == profile['repository'], 'receipt repository mismatch')
    require(bool(SHA_RE.fullmatch(data['repo_sha'])), 'invalid receipt repo SHA')
    require(bool(re.fullmatch(r'[A-Za-z0-9_-]{1,100}', data['run_id'])), 'invalid run ID')
    require(instant(data['started_at']) <= instant(data['finished_at']), 'reversed run dates')
    require(data['status'] == 'complete' and data['blockers'] == [], 'run incomplete/blocked')
    require(data['delivery']['status'] == 'verified'
            and bool(data['delivery']['evidence'].strip()), 'delivery proof required')
    require(isinstance(data['artifacts'], list) and data['artifacts'], 'artifacts required')
    inventory = {}
    for a in data['artifacts']:
        path = relative(a['path'])
        require(path.parts[0] == 'runs' and len(path.parts) >= 3,
                'artifact must be under runs/<run-id>/')
        require(path.parts[1] == data['run_id'], 'artifact belongs to another run')
        require(path.name != 'receipt.json', 'receipt.json is reserved, not a source artifact')
        require(a['path'] not in inventory, 'duplicate artifact')
        source = Path(root) / path
        no_symlinks(source)
        require(source.is_file() and source.stat().st_size <= 2_000_000, 'invalid artifact')
        require(digest(source.read_bytes()) == a['sha256'], 'artifact hash mismatch')
        inventory[a['path']] = a['sha256']
    research_path = data.get('research')
    require(research_path in inventory, 'hashed external research artifact required')
    research = read_json(Path(root) / research_path)
    validate_discovery(research, {j['id'] for j in profile['usage']['journeys']},
                       kind, data['repo_sha'])
    require(not research['synthetic'] or profile['repository'].startswith('example/'),
            'synthetic research is example-only')
    require(instant(data['started_at']) <= instant(research['started_at'])
            <= instant(research['finished_at']) <= instant(data['finished_at']),
            'research evidence belongs to another execution window')
    required = {q['id'] for q in profile['questions']}
    seen = set()
    for c in data['coverage']:
        require(c['question_id'] in required and c['question_id'] not in seen,
                'unknown/duplicate coverage question')
        seen.add(c['question_id'])
        require(c['status'] == 'covered' and c['evidence'] in inventory
                and bool(c['note'].strip()), 'unproven coverage')
    require(seen == required, 'incomplete declared question coverage')
    if kind == 't0':
        require(instant(data['cutoff_at']) <= instant(data['finished_at']), 'cutoff after finish')
    return inventory


def verify_t0(root):
    root = Path(root)
    no_symlinks(root, recursive=True)
    state = read_json(root / 'state.json')
    b = state.get('baseline')
    require(isinstance(b, dict), 'no frozen baseline')
    manifest = root / 'baseline' / 'manifest.json'
    require(digest(manifest.read_bytes()) == b['manifest_sha256'], 'T0 manifest changed')
    data = read_json(manifest)
    require(data['repository'] == state['repository'], 'baseline identity mismatch')
    expected_files = {'manifest.json'}
    for path, expected_hash in data['files'].items():
        relative(path)
        expected_files.add(path)
        require(digest((root / 'baseline' / path).read_bytes()) == expected_hash,
                f'T0 artifact changed: {path}')
    actual = {p.relative_to(root / 'baseline').as_posix()
              for p in (root / 'baseline').rglob('*') if p.is_file()}
    require(actual == expected_files, 'baseline file inventory changed')
    return data


def freeze_t0(root, data):
    root = Path(root)
    p = validate_pack(root)
    require(p['status'] == 'ready', 'draft profile: finish semantic analysis first')
    with lock(root):
        state = read_json(root / 'state.json')
        require(state['phase'] in {'T0_REQUIRED', 'T0_RUNNING'}, 'T0 not eligible')
        require(state['baseline'] is None and not (root / 'baseline').exists(),
                'baseline already exists; never regenerate T0')
        inventory = receipt(root, data, 't0', p)
        temp = Path(tempfile.mkdtemp(prefix='.baseline-', dir=root))
        try:
            for path in inventory:
                dest = temp / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(root / path, dest)
            manifest = {'schema_version': 1, 'repository': p['repository'],
                        'cutoff_at': data['cutoff_at'], 'repo_sha': data['repo_sha'],
                        'receipt': data, 'files': inventory}
            atomic_json(temp / 'manifest.json', manifest)
            fingerprint = digest((temp / 'manifest.json').read_bytes())
            os.rename(temp, root / 'baseline')
            state['baseline'] = {'manifest_sha256': fingerprint, 'cutoff_at': data['cutoff_at']}
            state['phase'] = 'UPDATE_READY'
            atomic_json(root / 'state.json', state)
        finally:
            if temp.exists():
                shutil.rmtree(temp)
    verify_t0(root)
    return state
