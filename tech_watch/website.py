"""Deterministic static website renderer for public watch outputs."""
from html import escape
from pathlib import Path
import re

from .common import atomic_json, read_json, repository, require

SITE_TEMPLATES = Path(__file__).resolve().parent.parent / 'templates' / 'site'
SLUG_RE = re.compile(r'[a-z0-9][a-z0-9-]{1,119}\Z')
DATE_RE = re.compile(r'20\d\d-\d\d-\d\d\Z')
ACTIVE_HTML = re.compile(
    r'<\s*(script|iframe|object|embed|form|base|meta)\b|javascript:|srcdoc\s*=|\son[a-z]+\s*=', re.I)


def website_repository(source_repository):
    source = repository(source_repository)
    owner, name = source.split('/', 1)
    return f'{owner}/{name}-website'


def validate_edition(value):
    require(isinstance(value, dict), 'edition must be an object')
    required = {'slug', 'date', 'title', 'excerpt', 'body_html'}
    require(required <= set(value), f'missing edition fields: {sorted(required - set(value))}')
    require(isinstance(value['slug'], str) and SLUG_RE.fullmatch(value['slug']), 'invalid slug')
    require(isinstance(value['date'], str) and DATE_RE.fullmatch(value['date']), 'invalid date')
    for key in ('title', 'excerpt', 'body_html'):
        require(isinstance(value[key], str) and value[key].strip(), f'invalid {key}')
    require(len(value['title']) <= 240 and len(value['excerpt']) <= 1200,
            'edition metadata too long')
    require(len(value['body_html'].encode('utf-8')) <= 750_000, 'edition body too large')
    require(not ACTIVE_HTML.search(value['body_html']), 'active HTML is forbidden')
    return {key: value[key].strip() for key in required}


def _shell(title, body, depth=0):
    prefix = '../' * depth
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title><link rel="stylesheet" href="{prefix}assets/style.css"></head>
<body><header class="site-header"><div class="shell nav"><a class="brand" href="{prefix}">Watch</a>
<nav><a href="{prefix}">Latest</a><a href="{prefix}archive/">Archive</a></nav></div></header>
{body}
<footer><div class="shell">Evidence-led public research · generated from a separate source repository.</div></footer>
</body></html>'''


def _edition_page(source_repository, edition):
    body = f'''<main><section class="hero"><div class="shell"><p class="eyebrow">{escape(edition['date'])}</p>
<h1>{escape(edition['title'])}</h1><p class="standfirst">{escape(edition['excerpt'])}</p></div></section>
<section class="reading"><article class="shell article">{edition['body_html']}</article></section></main>'''
    return _shell(edition['title'], body, depth=1)


def _cards(editions, prefix=''):
    cards = []
    for item in editions:
        cards.append(f'''<article class="card"><p class="eyebrow">{escape(item['date'])}</p>
<h2><a href="{prefix}{escape(item['slug'])}/">{escape(item['title'])}</a></h2>
<p>{escape(item['excerpt'])}</p><a class="more" href="{prefix}{escape(item['slug'])}/">Read →</a></article>''')
    return '\n'.join(cards)


def _home(source_repository, editions):
    latest = editions[0]
    cards = _cards(editions[1:7])
    body = f'''<main><section class="hero"><div class="shell"><p class="eyebrow">LATEST · {escape(latest['date'])}</p>
<h1>{escape(latest['title'])}</h1><p class="standfirst">{escape(latest['excerpt'])}</p>
<a class="button" href="{escape(latest['slug'])}/">Read the full brief →</a></div></section>
<section class="shell section"><div class="section-head"><h2>Recent intelligence</h2><a href="archive/">View archive →</a></div>
<div class="grid">{cards}</div></section></main>'''
    return _shell(f'{source_repository} — public intelligence', body)


def _archive(source_repository, editions):
    body = f'''<main><section class="hero compact"><div class="shell"><p class="eyebrow">ARCHIVE</p>
<h1>{escape(source_repository)}</h1><p class="standfirst">Dated public watch editions.</p></div></section>
<section class="shell section"><div class="grid">{_cards(editions, '../')}</div></section></main>'''
    return _shell(f'{source_repository} — archive', body, depth=1)


def render_public_site(source_repository, edition, output, replace_existing=False):
    source = repository(source_repository)
    item = validate_edition(edition)
    root = Path(output)
    root.mkdir(parents=True, exist_ok=True)
    manifest_path = root / 'site.json'
    if manifest_path.exists():
        manifest = read_json(manifest_path)
        require(manifest.get('source_repository') == source, 'site source mismatch')
    else:
        manifest = {'schema_version': 1, 'source_repository': source,
                    'public_repository': website_repository(source), 'editions': []}
    page = _edition_page(source, item)
    edition_path = root / item['slug'] / 'index.html'
    if edition_path.exists():
        same = edition_path.read_text(encoding='utf-8') == page
        require(same or replace_existing,
                'edition exists with different public content; explicit replacement required')
        if not same:
            edition_path.write_text(page, encoding='utf-8')
    else:
        edition_path.parent.mkdir(parents=True, exist_ok=True)
        edition_path.write_text(page, encoding='utf-8')
    existing = {e['slug']: e for e in manifest['editions']}
    meta = {k: item[k] for k in ('slug', 'date', 'title', 'excerpt')}
    if item['slug'] in existing and existing[item['slug']] != meta:
        require(replace_existing, 'edition metadata changed; explicit replacement required')
    existing[item['slug']] = meta
    editions = sorted(existing.values(), key=lambda e: (e['date'], e['slug']), reverse=True)
    manifest['editions'] = editions
    assets = root / 'assets'; assets.mkdir(exist_ok=True)
    style = (SITE_TEMPLATES / 'style.css').read_text(encoding='utf-8')
    (assets / 'style.css').write_text(style, encoding='utf-8')
    (root / 'index.html').write_text(_home(source, editions), encoding='utf-8')
    archive = root / 'archive'; archive.mkdir(exist_ok=True)
    (archive / 'index.html').write_text(_archive(source, editions), encoding='utf-8')
    (root / '.nojekyll').write_text('', encoding='utf-8')
    atomic_json(manifest_path, manifest)
    return {'source_repository': source, 'public_repository': manifest['public_repository'],
            'edition': item['slug'], 'edition_count': len(editions), 'root': str(root),
            'replaced': bool(replace_existing)}
