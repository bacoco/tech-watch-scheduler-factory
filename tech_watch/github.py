"""Read-only GitHub REST client. Never prints credential values."""
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote
from urllib.request import Request, HTTPRedirectHandler, build_opener
import json
import os
from .common import repository, require


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("GitHub API redirect refused; re-resolve repository metadata")


class GitHub:
    def __init__(self, opener=None):
        self.opener = opener or build_opener(NoRedirect()).open
        self.token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')

    def get(self, endpoint, **params):
        require(endpoint.startswith('/') and '://' not in endpoint, 'relative API endpoint required')
        url = 'https://api.github.com' + endpoint
        if params:
            url += '?' + urlencode(params)
        headers = {'Accept': 'application/vnd.github+json',
                   'User-Agent': 'tech-watch-scheduler-factory/0.1'}
        if self.token:
            headers['Authorization'] = 'Bearer ' + self.token
        request = Request(url, headers=headers, method='GET')
        try:
            with self.opener(request, timeout=30) as response:
                require(response.geturl().startswith('https://api.github.com/'),
                        'unexpected API redirect')
                data = response.read(5_000_001)
                require(len(data) <= 5_000_000, 'API response exceeds 5 MB cap')
                return json.loads(data)
        except HTTPError as exc:
            raise ValueError(f'GitHub read failed: HTTP {exc.code} for {endpoint}') from None
        except URLError:
            raise ValueError(f'GitHub network unavailable for {endpoint}') from None

    def discover(self, owner, limit=10):
        repository(owner + '/validation')
        require(1 <= limit <= 100, 'limit must be 1..100')
        found = []
        for page in range(1, 11):
            if self.token:
                batch = self.get('/user/repos', affiliation='owner', sort='pushed',
                                 direction='desc', per_page=100, page=page)
            else:
                batch = self.get(f'/users/{owner}/repos', sort='pushed', direction='desc',
                                 per_page=100, page=page)
            for r in batch:
                if r['owner']['login'].lower() != owner.lower() or r['archived']:
                    continue
                if r['name'] == 'tech-watch-scheduler-factory':
                    continue
                found.append({k: r.get(k) for k in ('full_name', 'default_branch',
                    'pushed_at', 'updated_at', 'private', 'fork', 'description')})
            if len(found) >= limit or len(batch) < 100:
                return {'selection': 'recently-pushed, not usage',
                        'visibility': 'authenticated' if self.token else 'public-only',
                        'repositories': found[:limit]}
        raise ValueError('pagination cap reached before selection completed')

    def metadata(self, repo):
        repository(repo)
        return self.get('/repos/' + repo)

    def head(self, repo, branch):
        repository(repo)
        return self.get(f'/repos/{repo}/commits/{quote(branch, safe="")}')['sha']
