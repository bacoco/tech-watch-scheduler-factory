"""Non-destructive local installation; no git push or task activation."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
from urllib.parse import urlsplit
from .common import no_symlinks, read_json, repository, require
from .render import validate_pack, render_files


def origin_repository(value):
    value = value.strip()
    if value.startswith('git@github.com:'):
        name = value[len('git@github.com:'):]
    else:
        u = urlsplit(value)
        require(u.scheme in {'https', 'ssh'} and u.hostname == 'github.com'
                and not u.query and not u.fragment and not u.password,
                'unsupported or ambiguous git origin')
        name = u.path.lstrip('/')
    if name.endswith('.git'):
        name = name[:-4]
    return repository(name)


def git(root, *args):
    r = subprocess.run(['git', '-C', str(root), *args], check=True,
                       capture_output=True, text=True, timeout=15)
    return r.stdout.strip()


def install(pack, target, apply=False):
    source = Path(pack).absolute()
    root = Path(target).absolute()
    no_symlinks(source, recursive=True)
    no_symlinks(root)
    p = validate_pack(source)
    require(root.is_dir(), 'target checkout missing')
    require(Path(git(root, 'rev-parse', '--show-toplevel')).resolve() == root.resolve(),
            'target must be the repository root')
    actual = origin_repository(git(root, 'remote', 'get-url', 'origin'))
    require(actual.lower() == p['repository'].lower(), 'target origin mismatch')
    require(git(root, 'rev-parse', 'HEAD') == p['analyzed_sha'],
            'checkout SHA differs from analyzed profile; refresh analysis before installation')
    require(not git(root, 'diff', 'HEAD', '--name-only'),
            'tracked local changes differ from analyzed commit; reconcile before installation')
    require(set(x.name for x in source.iterdir()) == set(render_files(p)),
            'only a fresh generated instruction pack may be installed')
    state = read_json(source / 'state.json')
    require(state['baseline'] is None and state['external_task']['status'] == 'not_created'
            and state['phase'] in {'T0_REQUIRED', 'INTEGRATION_REQUIRED'},
            'cannot install a pack carrying runtime state')
    dest = root / 'scheduler-techno'
    no_symlinks(dest, recursive=True)
    if dest.exists():
        require(dest.is_dir(), 'existing target is not a directory')
        same = set(x.name for x in source.iterdir()) == set(x.name for x in dest.iterdir())
        require(same and all((dest / x.name).is_file()
                and (dest / x.name).read_bytes() == x.read_bytes() for x in source.iterdir()),
                'installed directory differs; use a reviewed update, preserve state')
        return {'status': 'unchanged', 'path': str(dest)}
    if not apply:
        return {'status': 'preview', 'path': str(dest),
                'files': sorted(x.name for x in source.iterdir())}
    staging = Path(tempfile.mkdtemp(prefix='.scheduler-techno-', dir=root))
    try:
        for item in source.iterdir():
            shutil.copyfile(item, staging / item.name)
        validate_pack(staging)
        require(not dest.exists(), 'target appeared during installation')
        os.rename(staging, dest)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return {'status': 'installed-locally', 'path': str(dest), 'pushed': False}
