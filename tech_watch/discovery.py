"""Check declared external research evidence, NOT the truth or depth of an LLM report."""
from urllib.parse import urlsplit
from .common import SHA_RE, instant, require
from .fields import text, texts


def validate_discovery(d, usage_ids, stage, repo_sha, complete=True):
    require(isinstance(d, dict) and d.get('schema_version') == 1, 'research record required')
    require(d.get('stage') == stage, 'wrong research stage; generation is not T0 or UPDATE')
    require(d.get('repo_sha') == repo_sha and bool(SHA_RE.fullmatch(repo_sha)),
            'research belongs to another repository revision')
    require(d.get('status') in {'complete', 'partial', 'blocked'}, 'invalid research status')
    require(type(d.get('synthetic')) is bool, 'declare synthetic versus real evidence')
    start, end = instant(d['started_at']), instant(d['finished_at'])
    require(start <= end, 'reversed research dates')
    text(d['scope'], 'declared research scope')
    text(d['stop_reason'], 'research stopping rationale')
    texts(d['blocking_gaps'], 'blocking research gaps')
    if complete:
        require(d['status'] == 'complete' and not d['blocking_gaps'],
                'external research incomplete or blocked')
    require(isinstance(d['sources'], list) and len(d['sources']) <= 100, 'bounded source list required')
    sources, urls = {}, set()
    for s in d['sources']:
        text(s['id'], 'external source id')
        require(s['id'] not in sources, 'duplicate external source id')
        text(s['url'], 'source URL')
        u = urlsplit(s['url'])
        require(u.scheme in {'https', 'http'} and u.hostname and not u.username
                and not u.password, 'absolute public URL without credentials required')
        canonical = s['url'].split('#')[0].rstrip('/')
        require(canonical not in urls, 'duplicate external URL')
        urls.add(canonical)
        require(d['synthetic'] or not u.hostname.endswith('.invalid'),
                'fixture URL is not real research')
        for key in ('publisher', 'family', 'locator', 'finding', 'limitations'):
            text(s[key], key)
        require(s['status'] in {'read', 'candidate', 'blocked'}, 'invalid source status')
        require(s['origin'] in {'seed', 'discovered'}, 'invalid source origin')
        texts(s['usage_ids'], 'source usage_ids', True)
        require(set(s['usage_ids']) <= usage_ids, 'unknown source usage link')
        require(start <= instant(s['accessed_at']) <= end, 'source not read during this research')
        sources[s['id']] = s
    require(isinstance(d['searches'], list) and len(d['searches']) <= 100, 'search log required')
    phases, search_ids, attached = set(), set(), set()
    for s in d['searches']:
        text(s['id'], 'search id')
        require(s['id'] not in search_ids, 'duplicate search id')
        search_ids.add(s['id'])
        require(s['phase'] in {'initial', 'expansion', 'challenge'}, 'invalid exploration phase')
        phases.add(s['phase'])
        for key in ('query', 'reason', 'trace'):
            text(s[key], key)
        require(s['outcome'] in {'results', 'no_results', 'blocked'}, 'invalid search outcome')
        texts(s['source_ids'], 'search source ids', s['outcome'] == 'results')
        require(set(s['source_ids']) <= sources.keys(), 'unknown search source reference')
        if s['outcome'] != 'results':
            require(not s['source_ids'], 'no-results/blocked search cannot claim sources')
        require(start <= instant(s['executed_at']) <= end, 'search outside research period')
        attached.update(s['source_ids'])
    read = {k: v for k, v in sources.items() if v['status'] == 'read'}
    conclusions, covered = d['conclusions'], set()
    require(isinstance(conclusions, list) and len(conclusions) <= 100, 'usage conclusions required')
    for c in conclusions:
        require(c['usage_id'] in usage_ids, 'unknown conclusion usage')
        texts(c['source_ids'], 'conclusion sources', True)
        require(set(c['source_ids']) <= read.keys(), 'conclusions require sources actually read')
        for sid in c['source_ids']:
            require(c['usage_id'] in read[sid]['usage_ids'], 'unrelated source in usage conclusion')
        for key in ('finding', 'consequence'):
            text(c[key], key)
        require(c['decision'] in {'retain', 'reject', 'uncertain'}, 'invalid research decision')
        covered.add(c['usage_id'])
    require(isinstance(d['new_directions'], list) and len(d['new_directions']) <= 30,
            'new directions must be explicit; an empty list is legitimate')
    for n in d['new_directions']:
        text(n['direction'], 'new direction')
        text(n['why'], 'new direction relevance')
        texts(n['source_ids'], 'new direction sources', True)
        require(set(n['source_ids']) <= read.keys(), 'new direction lacks read sources')
    if complete:
        require(phases == {'initial', 'expansion', 'challenge'},
                'initial, open expansion and challenge searches are mandatory each cycle')
        for phase in phases:
            require(any(s['phase'] == phase and s['outcome'] != 'blocked' for s in d['searches']),
                    'an exploration phase is blocked')
        require(len({s['publisher'].casefold() for s in read.values()}) >= 2,
                'at least two distinct publishers must actually be read')
        require(any(s['family'] not in {'github', 'arxiv'}
                    and urlsplit(s['url']).hostname not in {'github.com', 'arxiv.org', 'www.arxiv.org'}
                    for s in read.values()), 'research cannot stop at GitHub/arXiv')
        require(set(read) <= attached, 'read source without search/discovery trace')
        require(any(s['phase'] == 'expansion' and any(
                    sid in read and read[sid]['origin'] == 'discovered'
                    for sid in s['source_ids']) for s in d['searches']),
                'open exploration must read beyond the seed list')
        require(covered == usage_ids, 'usage research coverage incomplete')
    return d
