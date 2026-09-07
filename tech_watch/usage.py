"""Usage, not implementation language, determines the intelligence purpose."""
from .common import require
from .fields import text, texts


def validate_usage(p, evidence_ids):
    u = p.get('usage')
    require(isinstance(u, dict), 'usage model required; stack is insufficient')
    require(u['watch_purpose'] in {'product_improvement', 'domain_intelligence', 'both'},
            'invalid watch purpose')
    texts(u['audiences'], 'audiences', True)
    text(u['value_delivered'], 'value delivered')
    text(u['information_output'], 'information output')
    texts(u['limits'], 'usage evidence limits')
    require(isinstance(u['journeys'], list) and 1 <= len(u['journeys']) <= 10,
            'one to ten concrete usage journeys required')
    ids = set()
    for j in u['journeys']:
        text(j['id'], 'journey id')
        require(j['id'] not in ids, 'duplicate journey')
        ids.add(j['id'])
        for key in ('actor', 'goal', 'workflow'):
            text(j[key], key)
        texts(j['pain_points'], 'pain points', True)
        texts(j['success_criteria'], 'usage success criteria', True)
        texts(j['evidence_ids'], 'usage evidence', True)
        require(set(j['evidence_ids']) <= evidence_ids, 'unknown usage evidence')
        require(j['status'] in {'observed', 'documented', 'inferred'}, 'invalid usage status')
        texts(j['observation_refs'], 'authorized observation references')
        require(j['status'] != 'observed' or bool(j['observation_refs']),
                'observed usage requires direct observation references, not source code')
    intents = set()
    covered = set()
    for q in p['questions']:
        texts(q.get('usage_ids'), 'question usage_ids', True)
        require(set(q['usage_ids']) <= ids, 'unknown question usage link')
        covered.update(q['usage_ids'])
        require(q.get('intent') in {'improve_service', 'domain_information'},
                'question needs an improvement or domain-information purpose')
        intents.add(q['intent'])
    require(covered == ids, 'every declared usage needs a research question')
    expected = {'product_improvement': {'improve_service'},
                'domain_intelligence': {'domain_information'},
                'both': {'improve_service', 'domain_information'}}
    require(intents == expected[u['watch_purpose']], 'questions do not match watch purpose')
    require(any(c['id'] == 'web_open' and c['mode'] != 'excluded' for c in p['channels']),
            'open web exploration cannot be replaced with a closed source list')
    return ids
