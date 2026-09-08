"""CLI: explicit local effects, no scheduler creation and no hidden LLM calls."""
import argparse
from pathlib import Path
import sys

from .common import atomic_json, json_text, read_json, require
from .github import GitHub
from .install import install
from .multiplex import initial_state, reserve, finish, validate_registry
from .render import generate, validate_pack
from .snapshot import snapshot
from .state import freeze_t0, verify_t0
from .updates import record_update
from .website import render_public_site


def parser():
    p = argparse.ArgumentParser(prog='python -m tech_watch')
    s = p.add_subparsers(dest='command', required=True)
    d = s.add_parser('discover', help='read repositories, do not change them')
    d.add_argument('--owner', required=True); d.add_argument('--limit', type=int, default=10)
    d.add_argument('--out', required=True)
    d = s.add_parser('snapshot', help='bounded fact collection, not semantic analysis')
    d.add_argument('--repo', required=True); d.add_argument('--out', required=True)
    d.add_argument('--max-files', type=int, default=18)
    d = s.add_parser('generate', help='render profiles analyzed by the host agent')
    group = d.add_mutually_exclusive_group(required=True)
    group.add_argument('--profile'); group.add_argument('--profile-dir')
    d.add_argument('--out', required=True)
    d = s.add_parser('install', help='preview local installation; --apply to write')
    d.add_argument('pack'); d.add_argument('target'); d.add_argument('--apply', action='store_true')
    d = s.add_parser('website-render', help='render one validated public edition into a static site')
    d.add_argument('--source-repo', required=True); d.add_argument('--edition', required=True)
    d.add_argument('--out', required=True); d.add_argument('--replace-existing', action='store_true')
    d = s.add_parser('multiplex-validate', help='validate a multiplex registry without effects')
    d.add_argument('registry')
    d = s.add_parser('multiplex-reserve', help='simulate one deterministic reservation')
    d.add_argument('registry'); d.add_argument('--state'); d.add_argument('--now', required=True)
    d = s.add_parser('multiplex-finish', help='simulate completion/retry of current dispatch')
    d.add_argument('registry'); d.add_argument('state')
    outcome = d.add_mutually_exclusive_group(required=True)
    outcome.add_argument('--success', action='store_true'); outcome.add_argument('--failure', action='store_true')
    for name in ('validate', 'verify-t0', 'freeze-t0', 'record-update'):
        d = s.add_parser(name); d.add_argument('watch_directory')
        if name in {'freeze-t0', 'record-update'}: d.add_argument('--receipt', required=True)
    return p


def batch(args):
    paths = [Path(args.profile)] if args.profile else sorted(Path(args.profile_dir).glob('*.json'))
    require(1 <= len(paths) <= 100, 'provide one to 100 profiles')
    report = {'schema_version': 1, 'task_created': False, 'results': []}
    for path in paths:
        try:
            profile = read_json(path); dest, status = generate(profile, args.out)
            report['results'].append({'profile': str(path), 'repository': profile['repository'],
                                      'status': status, 'directory': str(dest)})
        except (ValueError, OSError, KeyError, TypeError) as exc:
            report['results'].append({'profile': str(path), 'status': 'blocked', 'reason': str(exc)})
    atomic_json(Path(args.out) / 'generation-report.json', report)
    return report, 2 if any(x['status'] == 'blocked' for x in report['results']) else 0


def main(argv=None):
    a = parser().parse_args(argv); code = 0
    try:
        if a.command == 'generate': result, code = batch(a)
        elif a.command == 'discover':
            require(not Path(a.out).exists(), 'output exists'); result = GitHub().discover(a.owner, a.limit)
            atomic_json(a.out, result)
        elif a.command == 'snapshot': result = snapshot(GitHub(), a.repo, a.out, a.max_files)
        elif a.command == 'install': result = install(a.pack, a.target, a.apply)
        elif a.command == 'website-render':
            result = render_public_site(a.source_repo, read_json(a.edition), a.out, a.replace_existing)
        elif a.command == 'multiplex-validate':
            jobs = validate_registry(read_json(a.registry)); result = {'valid': True, 'jobs': len(jobs)}
        elif a.command == 'multiplex-reserve':
            registry = read_json(a.registry); state = read_json(a.state) if a.state else initial_state()
            new_state, event = reserve(registry, state, a.now); result = {'event': event, 'state': new_state}
        elif a.command == 'multiplex-finish':
            new_state, event = finish(read_json(a.registry), read_json(a.state), a.success)
            result = {'event': event, 'state': new_state}
        elif a.command == 'validate':
            profile = validate_pack(a.watch_directory)
            result = {'structurally_valid': True, 'repository': profile['repository'],
                      'semantic_analysis_status': profile['status'], 'task_created': False}
        elif a.command == 'verify-t0': result = verify_t0(a.watch_directory)
        elif a.command == 'freeze-t0': result = freeze_t0(a.watch_directory, read_json(a.receipt))
        else: result = record_update(a.watch_directory, read_json(a.receipt))
        print(json_text(result), end=''); return code
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'BLOCKED: {exc}', file=sys.stderr); return 2
