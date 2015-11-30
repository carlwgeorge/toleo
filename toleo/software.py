import asyncio
import re
import bs4

import aiohttp

from toleo.version import Version


class BaseSoftware:
    """Base software class for creating software classes.

    Derivative classes must define __init and _load methods.
    """

    def __init__(self):
        raise NotImplementedError()

    def __str__(self):
        return self.name

    def __repr__(self):
        return '{}(\'{}\')'.format(self.__class__.__name__, self.name)

    def latest(self):
        self.versions.sort()
        return self.versions[-1]

    async def _load(self):
        raise NotImplementedError()


class GenericSoftware(BaseSoftware):
    """Software source using generic regex scraper."""

    _default_pattern = '{}[-_]([\d.]+)\.(?:t(?:ar\.)?(?:[glx]z|bz2?)|zip)'

    def __init__(self, name, url, pattern=None):
        self.name = name
        self.url = url
        self.pattern = pattern or self._default_pattern.format(name)

    async def _load(self):
        response = await aiohttp.get(self.url)
        result = await response.text()
        matches = set(re.findall(self.pattern, result, flags=re.IGNORECASE))
        self.versions = [Version(match) for match in matches]


class PyPISoftware(BaseSoftware):
    """Software source in PyPI (Python Package Index)."""

    _pypi = 'https://pypi.python.org/pypi'

    def __init__(self, name):
        self.name = name
        self.url = '/'.join([self._pypi, name])

    async def _load(self):
        api = '{}/json'.format(self.url)
        response = await aiohttp.get(api)
        data = await response.json()
        self.versions = [Version(r) for r in data['releases'].keys()]


class PECLSoftware(BaseSoftware):
    """Software source in PECL (PHP Extension Community Library)."""

    _pecl = 'https://pecl.php.net'

    def __init__(self, name):
        self.name = name
        self.url = '{}/package/{}'.format(self._pecl, name)

    async def _load(self):
        api = '{}/rest/r/{}/allreleases.xml'.format(self._pecl, self.name)
        response = await aiohttp.get(api)
        result = await response.text()
        soup = bs4.BeautifulSoup(result, 'xml')
        self.versions = [v.text for v in soup.find_all('v')]


class GitHubSoftware(BaseSoftware):
    """Software source on GitHub."""

    _github = 'https://github.com'

    def __init__(self, name, trim=None):
        self.name = name
        try:
            self.owner, self.repo = name.split('/')
        except ValueError:
            raise Exception('name must be in "owner/repo" format')
        self.url = '/'.join([self._github, self.owner, self.repo])
        self._trim = trim or ''

    async def _load(self):
        response = await aiohttp.get('/'.join([self.url, 'tags']))
        result = await response.text()
        soup = bs4.BeautifulSoup(result, 'lxml')
        self.versions = [Version(tag.text.replace(self._trim, ''))
                         for tag in soup.find_all('span', class_='tag-name')]


class BitbucketSoftware(BaseSoftware):

    _bitbucket = 'https://bitbucket.org'
    _api = 'https://api.bitbucket.org/1.0'

    def __init__(self, name, trim=None):
        self.name = name
        try:
            self.owner, self.repo = name.split('/')
        except ValueError:
            raise Exception('name must be in "owner/repo" format')
        self.url = '/'.join([self._bitbucket, self.owner, self.repo])
        self._trim = trim or ''

    async def _load(self):
        api = '/'.join([self._api, 'repositories', self.owner, self.repo])
        response = await aiohttp.get('/'.join([api, 'tags']))
        data = await response.json()
        self.versions = [Version(v) for v in data.keys()]
