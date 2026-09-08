"""Cadence contract with separate watch/post-mortem hypotheses."""
from zoneinfo import ZoneInfo

from .fields import text
from .common import require


def _stream(value, name, default_interval=None):
    require(isinstance(value, dict), f'{name} cadence must be an object')
    for key in ('recommendation', 'reason'):
        text(value[key], f'{name} {key}')
    interval = value.get('interval_days', default_interval)
    minimum = value.get('min_interval_days', interval)
    maximum = value.get('max_interval_days', interval)
    require(type(interval) is int and 1 <= interval <= 365, f'invalid {name} interval_days')
    require(type(minimum) is int and 1 <= minimum <= interval,
            f'invalid {name} min_interval_days')
    require(type(maximum) is int and interval <= maximum <= 730,
            f'invalid {name} max_interval_days')
    result = dict(value)
    result.update(interval_days=interval, min_interval_days=minimum,
                  max_interval_days=maximum)
    return result


def cadence_model(cadence):
    require(isinstance(cadence, dict), 'cadence must be an object')
    ZoneInfo(cadence['timezone'])
    require(type(cadence['max_new_issues']) is int
            and 0 <= cadence['max_new_issues'] <= 10,
            'issue ceiling must be 0..10')
    if 'watch' not in cadence and 'postmortem' not in cadence:
        for key in ('recommendation', 'reason'):
            text(cadence[key], key)
        watch = _stream({'recommendation': cadence['recommendation'],
                         'reason': cadence['reason'], 'interval_days': 7,
                         'min_interval_days': 1, 'max_interval_days': 30}, 'watch')
        postmortem = _stream({'recommendation': 'monthly review after several runs',
                              'reason': 'legacy profile: accumulate evidence before adapting cadence',
                              'interval_days': 30, 'min_interval_days': 14,
                              'max_interval_days': 90}, 'postmortem')
        return {'timezone': cadence['timezone'], 'watch': watch,
                'postmortem': postmortem, 'max_new_issues': cadence['max_new_issues'],
                'adaptation': {'min_runs_before_change': 3,
                               'decrease_after_consecutive_low_value': 3},
                'legacy_flat': True}
    watch = _stream(cadence['watch'], 'watch')
    postmortem = _stream(cadence['postmortem'], 'postmortem')
    adaptation = cadence.get('adaptation', {})
    require(isinstance(adaptation, dict), 'cadence adaptation must be an object')
    min_runs = adaptation.get('min_runs_before_change', 3)
    poor_runs = adaptation.get('decrease_after_consecutive_low_value', 3)
    require(type(min_runs) is int and 2 <= min_runs <= 20,
            'min_runs_before_change must be 2..20')
    require(type(poor_runs) is int and min_runs <= poor_runs <= 20,
            'decrease_after_consecutive_low_value must be >= min_runs and <=20')
    return {'timezone': cadence['timezone'], 'watch': watch,
            'postmortem': postmortem, 'max_new_issues': cadence['max_new_issues'],
            'adaptation': {'min_runs_before_change': min_runs,
                           'decrease_after_consecutive_low_value': poor_runs},
            'legacy_flat': False}


def runtime_model(profile):
    runtime = profile.get('runtime', {'mode': 'dedicated', 'reason': 'legacy default'})
    require(isinstance(runtime, dict), 'runtime must be an object')
    require(runtime.get('mode') in {'dedicated', 'multiplexed'}, 'invalid runtime mode')
    text(runtime.get('reason', ''), 'runtime reason')
    result = {'mode': runtime['mode'], 'reason': runtime['reason']}
    if runtime['mode'] == 'multiplexed':
        group = runtime.get('group_id')
        text(group, 'runtime group_id')
        require('/' not in group and len(group) <= 80, 'invalid runtime group_id')
        result['group_id'] = group
    return result
