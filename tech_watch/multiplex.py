"""Pure multiplex scheduler state machine: deterministic dispatch, bounded retry."""
from copy import deepcopy
from datetime import timedelta
from hashlib import sha256
import re
from zoneinfo import ZoneInfo

from .common import instant, relative, repository, require
from .fields import text

JOB_RE = re.compile(r'[a-z0-9][a-z0-9_.-]{1,119}\Z')
JOB_FIELDS = {'schema_version', 'job_id', 'repository', 'kind', 'instructions_path',
              'timezone', 'schedule', 'priority', 'max_lateness_minutes',
              'max_retries', 'lease_minutes', 'enabled', 'guard', 'schedule_anchor_note'}
REQUIRED_JOB_FIELDS = JOB_FIELDS - {'schedule_anchor_note'}
DISPATCH_FIELDS = {'schema_version', 'dispatch_id', 'job_id', 'due_at', 'attempt',
                   'reserved_at', 'lease_until'}


def validate_job(job):
    require(isinstance(job, dict), 'job must be an object')
    require(REQUIRED_JOB_FIELDS <= set(job),
            f'missing job fields: {sorted(REQUIRED_JOB_FIELDS - set(job))}')
    require(set(job) <= JOB_FIELDS, f'unknown job fields: {sorted(set(job) - JOB_FIELDS)}')
    require(job.get('schema_version') == 1, 'job schema_version=1 required')
    require(isinstance(job.get('job_id'), str) and JOB_RE.fullmatch(job['job_id']),
            'invalid job_id')
    repository(job['repository'])
    require(job['kind'] in {'watch', 'postmortem'}, 'invalid job kind')
    relative(job['instructions_path'])
    require(job['instructions_path'].startswith('scheduler-techno/'),
            'job instructions must stay under scheduler-techno/')
    schedule = job['schedule']
    require(isinstance(schedule, dict) and set(schedule) == {'anchor_at', 'interval_days'},
            'job schedule only accepts anchor_at and interval_days')
    anchor = instant(schedule['anchor_at'])
    interval = schedule['interval_days']
    require(type(interval) is int and 1 <= interval <= 365, 'invalid interval_days')
    text(job['timezone'], 'job timezone'); ZoneInfo(job['timezone'])
    require(type(job['priority']) is int and 0 <= job['priority'] <= 100,
            'priority must be 0..100')
    require(type(job['max_lateness_minutes']) is int and job['max_lateness_minutes'] >= 0,
            'invalid max_lateness_minutes')
    require(type(job['max_retries']) is int and 0 <= job['max_retries'] <= 10,
            'max_retries must be 0..10')
    require(type(job['lease_minutes']) is int and 5 <= job['lease_minutes'] <= 1440,
            'lease_minutes must be 5..1440')
    require(type(job['enabled']) is bool, 'enabled must be boolean')
    expected_guard = 'baseline-or-completed-run' if job['kind'] == 'postmortem' else 'none'
    require(job['guard'] == expected_guard, f'invalid guard for {job["kind"]}')
    return anchor


def validate_registry(registry):
    require(isinstance(registry, dict) and registry.get('schema_version') == 1,
            'registry schema_version=1 required')
    require(set(registry) == {'schema_version', 'mode', 'migration', 'jobs'},
            'registry contains unknown fields')
    require(registry.get('mode') == 'multiplexed', 'registry must be multiplexed')
    migration = registry.get('migration')
    require(isinstance(migration, dict)
            and set(migration) == {'dedicated_tasks_disabled'}, 'invalid migration object')
    require(type(migration.get('dedicated_tasks_disabled')) is bool,
            'migration dedicated_tasks_disabled must be boolean')
    jobs = registry.get('jobs')
    require(isinstance(jobs, list) and 1 <= len(jobs) <= 200,
            'registry requires 1..200 jobs')
    ids = set()
    for job in jobs:
        validate_job(job); require(job['job_id'] not in ids, 'duplicate job_id'); ids.add(job['job_id'])
    return {job['job_id']: job for job in jobs}


def initial_state():
    return {'schema_version': 1, 'current': None, 'completed': {},
            'failed': {}, 'attempts': {}}


def _occurrences(job, now):
    anchor = validate_job(job); now_dt = instant(now) if isinstance(now, str) else now
    if now_dt < anchor: return []
    step = timedelta(days=job['schedule']['interval_days'])
    count = int((now_dt - anchor) // step)
    return [anchor + step * i for i in range(count + 1)]


def due_jobs(registry, state, now):
    jobs = validate_registry(registry)
    require(isinstance(state, dict) and state.get('schema_version') == 1,
            'invalid runtime state')
    now_dt = instant(now) if isinstance(now, str) else now; due = []
    for job_id, job in jobs.items():
        if not job['enabled']: continue
        completed = set(state.get('completed', {}).get(job_id, []))
        failed = set(state.get('failed', {}).get(job_id, []))
        for occurrence in _occurrences(job, now_dt):
            due_at = occurrence.isoformat()
            if due_at in completed or due_at in failed: continue
            lateness = (now_dt - occurrence).total_seconds() / 60
            if lateness <= job['max_lateness_minutes']:
                due.append((occurrence, -job['priority'], job_id, due_at))
    due.sort(key=lambda x: (x[0], x[1], x[2]))
    return [(jobs[job_id], due_at) for _, _, job_id, due_at in due]


def dispatch_id(job_id, due_at):
    return sha256(f'{job_id}|{due_at}'.encode()).hexdigest()[:24]


def _dispatch_job(jobs, dispatch):
    require(isinstance(dispatch, dict) and set(dispatch) == DISPATCH_FIELDS,
            'dispatch may not carry executable paths or extra authority')
    require(dispatch['schema_version'] == 1 and dispatch['job_id'] in jobs,
            'unknown dispatch job')
    require(type(dispatch['attempt']) is int and dispatch['attempt'] >= 1, 'invalid attempt')
    require(dispatch['dispatch_id'] == dispatch_id(dispatch['job_id'], dispatch['due_at']),
            'dispatch identity mismatch')
    reserved = instant(dispatch['reserved_at']); lease = instant(dispatch['lease_until'])
    require(reserved < lease, 'invalid dispatch lease')
    return jobs[dispatch['job_id']]


def _recover_expired(jobs, state, now_dt):
    current = state.get('current')
    if not current: return False
    job = _dispatch_job(jobs, current)
    if now_dt <= instant(current['lease_until']): return False
    if current['attempt'] > job['max_retries']:
        state.setdefault('failed', {}).setdefault(current['job_id'], []).append(current['due_at'])
    state['current'] = None
    return True


def reserve(registry, state, now):
    jobs = validate_registry(registry)
    require(registry['migration']['dedicated_tasks_disabled'],
            'migration guard: dedicated tasks must be disabled before multiplexing')
    result = deepcopy(state); now_dt = instant(now) if isinstance(now, str) else now
    recovered = _recover_expired(jobs, result, now_dt)
    if result.get('current'):
        return result, {'status': 'busy', 'dispatch': result['current']}
    candidates = due_jobs(registry, result, now_dt)
    if not candidates: return result, {'status': 'idle', 'dispatch': None}
    job, due_at = candidates[0]; did = dispatch_id(job['job_id'], due_at)
    attempt = result.setdefault('attempts', {}).get(did, 0) + 1
    require(attempt <= job['max_retries'] + 1, 'retry budget exhausted')
    result['attempts'][did] = attempt
    dispatch = {'schema_version': 1, 'dispatch_id': did, 'job_id': job['job_id'],
                'due_at': due_at, 'attempt': attempt, 'reserved_at': now_dt.isoformat(),
                'lease_until': (now_dt + timedelta(minutes=job['lease_minutes'])).isoformat()}
    result['current'] = dispatch
    return result, {'status': 'reserved', 'dispatch': dispatch, 'recovered_expired': recovered}


def resolve_dispatch(registry, dispatch):
    jobs = validate_registry(registry); job = _dispatch_job(jobs, dispatch)
    return {'repository': job['repository'], 'kind': job['kind'],
            'instructions_path': job['instructions_path'], 'guard': job['guard'], 'job': job}


def finish(registry, state, success):
    jobs = validate_registry(registry); result = deepcopy(state)
    dispatch = result.get('current'); require(dispatch is not None, 'no current dispatch')
    job = _dispatch_job(jobs, dispatch); bucket = 'completed' if success else 'failed'
    if not success and dispatch['attempt'] <= job['max_retries']:
        result['current'] = None
        return result, {'status': 'retry', 'dispatch_id': dispatch['dispatch_id']}
    result.setdefault(bucket, {}).setdefault(dispatch['job_id'], []).append(dispatch['due_at'])
    result['current'] = None
    return result, {'status': bucket, 'dispatch_id': dispatch['dispatch_id']}
