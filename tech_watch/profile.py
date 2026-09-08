"""Structural contract; semantic truth remains the agent's responsibility."""
import re
from .fields import text, texts
from .usage import validate_usage
from .discovery import validate_discovery
from .common import SHA_RE, instant, relative, repository, require
from .scheduling import cadence_model, runtime_model

CHANNELS = {'arxiv', 'github', 'official', 'models', 'products', 'community', 'personal', 'web_open'}


def validate_profile(p):
    require(isinstance(p, dict), "profile must be an object")
    require(p.get('schema_version') == 2,
            "profile v2 required: reanalyse usage and external discovery; do not relabel v1")
    repository(p['repository'])
    text(p['default_branch'], 'default_branch')
    require(bool(SHA_RE.fullmatch(p['analyzed_sha'])), 'invalid analyzed SHA')
    instant(p['analyzed_at'])
    require(p['status'] in {'draft', 'ready'}, 'invalid profile status')
    for key in ('objective', 'repo_type'):
        text(p[key], key)
    texts(p['constraints'], 'constraints', True)
    texts(p['unknowns'], 'unknowns')
    require(p['status'] != 'ready' or not p['unknowns'],
            'ready profile cannot have unresolved blocking unknowns')
    require(isinstance(p['evidence'], list) and p['evidence'], 'evidence required')
    require(len(p['evidence']) <= 20, 'scope evidence: max 20')
    evidence_ids = set()
    for e in p['evidence']:
        text(e['id'], 'evidence id')
        require(e['id'] not in evidence_ids, 'duplicate evidence id')
        evidence_ids.add(e['id'])
        relative(e['path'])
        require(type(e['start_line']) is int and type(e['end_line']) is int
                and 1 <= e['start_line'] <= e['end_line'], 'invalid evidence lines')
        text(e['claim'], 'claim')
        require(e['kind'] in {'code', 'documentation', 'inference'}, 'invalid kind')
    require(isinstance(p['questions'], list) and 1 <= len(p['questions']) <= 10,
            'one to ten focused research questions required')
    question_ids = set()
    for q in p['questions']:
        text(q['id'], 'question id')
        require(q['id'] not in question_ids, 'duplicate question id')
        question_ids.add(q['id'])
        for key in ('question', 'why', 'acceptance'):
            text(q[key], key)
        texts(q['evidence_ids'], 'evidence_ids', True)
        require(set(q['evidence_ids']) <= evidence_ids, 'unknown evidence reference')
    require(isinstance(p['channels'], list), 'channels must be a list')
    require(CHANNELS <= {c['id'] for c in p['channels']},
            'decide core source families including open web')
    require(len(p['channels']) <= 20, 'too many families; split scope')
    seen = set()
    for c in p['channels']:
        require(isinstance(c['id'], str)
                and re.fullmatch(r'[a-z][a-z0-9_-]{0,49}', c['id'])
                and c['id'] not in seen, 'invalid/duplicate channel')
        seen.add(c['id'])
        require(c['mode'] in {'primary', 'secondary', 'excluded'}, 'invalid source mode')
        require(c['access'] in {'unknown', 'verified', 'blocked'}, 'invalid access state')
        text(c['reason'], 'source reason')
        active = c['mode'] != 'excluded'
        texts(c['queries'], 'queries', active)
        texts(c['targets'], 'targets', active)
    require(any(c['mode'] != 'excluded' for c in p['channels']), 'no active source')
    integration = p['integration']
    require(integration['mode'] in {'none', 'coexist', 'reuse-existing'},
            'invalid integration')
    text(integration['reason'], 'integration reason')
    texts(integration['paths'], 'integration paths', integration['mode'] != 'none')
    for path in integration['paths']:
        relative(path)
    require(integration['mode'] != 'none' or not integration['paths'],
            'none cannot have existing paths')
    cadence_model(p['cadence'])
    runtime_model(p)
    usage_ids = validate_usage(p, evidence_ids)
    require(isinstance(p.get('discovery'), dict), 'external discovery record required')
    validate_discovery(p['discovery'], usage_ids, 'generation', p['analyzed_sha'],
                       complete=p['status'] == 'ready')
    if p['discovery'].get('synthetic'):
        require(p['repository'].startswith('example/'), 'synthetic evidence is example-only')
    require(instant(p['discovery']['finished_at']) <= instant(p['analyzed_at']),
            'profile predates its discovery')
    return p
