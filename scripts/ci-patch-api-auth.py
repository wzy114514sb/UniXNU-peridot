#!/usr/bin/env python3
"""Let the base repo's prepare-xnu-source.py use an authenticated GitHub API.

The upstream script calls api.github.com anonymously, which hits the 60/hour
per-IP limit on shared CI runners. Prepending an Authorization header raises
it to 5000/hour.
"""
from pathlib import Path
import sys

target = Path(sys.argv[1] if len(sys.argv) > 1 else 'base/scripts/prepare-xnu-source.py')
text = target.read_text()
if '_auth_urlopen' in text:
    print('already patched')
    raise SystemExit(0)

inject = '''
_orig_urlopen = urllib.request.urlopen
def _auth_urlopen(url, *a, **k):
    if isinstance(url, str) and url.startswith('https://api.github.com'):
        tok = os.environ.get('GITHUB_TOKEN', '')
        req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + tok})
        return _orig_urlopen(req, *a, **k)
    return _orig_urlopen(url, *a, **k)
urllib.request.urlopen = _auth_urlopen
'''
text = text.replace('import urllib.request', 'import urllib.request' + inject, 1)
target.write_text(text)
print(f'patched {target}')
