#!/usr/bin/env python3
"""Adapt the base tree to the runner's toolchain.

Two changes:
  * prepare-xnu-source.py authenticates api.github.com calls (rate limits).
  * newer-clang-only -Wno-* options are replaced, because the Xcode clang on
    the runner does not know them and -Werror turns that into a build failure.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'base')
NEWER_FLAGS = [
    '-Wno-unnecessary-virtual-specifier',
    '-Wno-missing-designated-field-initializers',
    '-Wno-suggest-destructor-override',
    '-Wno-suggest-override',
    '-Wno-c99-designator',
    '-Wno-reorder-init-list',
    '-Wno-pre-c11-compat',
    '-Wno-ms-bitfield-padding',
    '-Wno-reserved-identifier',
]

AUTH = '''
_orig_urlopen = urllib.request.urlopen
def _auth_urlopen(url, *a, **k):
    if isinstance(url, str) and url.startswith('https://api.github.com'):
        tok = os.environ.get('GITHUB_TOKEN', '')
        req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + tok})
        return _orig_urlopen(req, *a, **k)
    return _orig_urlopen(url, *a, **k)
urllib.request.urlopen = _auth_urlopen
'''

prepare = root / 'scripts' / 'prepare-xnu-source.py'
if prepare.is_file():
    text = prepare.read_text()
    if '_auth_urlopen' not in text:
        prepare.write_text(text.replace('import urllib.request', 'import urllib.request' + AUTH, 1))
        print('auth patch: prepare-xnu-source.py')

patched = 0
targets = list((root / 'scripts').glob('*.py')) + list((root / 'scripts').glob('*.sh'))
for path in targets:
    text = path.read_text(errors='replace')
    original = text
    for flag in NEWER_FLAGS:
        text = text.replace(flag + ' ', '').replace(' ' + flag, '').replace(flag, '')
    if text != original:
        path.write_text(text)
        patched += 1
        print(f'flag patch: {path.name}')
print(f'patched {patched} scripts')
