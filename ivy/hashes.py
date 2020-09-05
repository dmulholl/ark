# ------------------------------------------------------------------------------
# This module handles Ivy's file hashing mechanism.
#
# Before writing a page file to disk we check if there is an existing file of
# the same name left over from a previous build. If there is, we compare the
# hash of the new page's content with the cached hash of the old page's
# content. If they are identical, we skip writing the new page to disk.
#
# This has two effects:
#
#   * We save on disk IO, which is more expensive than comparing hashes.
#   * We avoid unnecessarily bumping the file modification time.
# ------------------------------------------------------------------------------

import os
import hashlib
import pickle

from . import site
from . import events


# Stores page hashes from the previous and current build runs.
_hashes = { 'old': {}, 'new': {} }


# Returns true if `filepath` is an existing file whose hash matches that of
# the content string.
def match(filepath: str, content: str) -> bool:
    key = os.path.relpath(filepath, site.out())
    _hashes['new'][key] = hashlib.sha1(content.encode()).hexdigest()
    if os.path.exists(filepath):
        return _hashes['old'].get(key) == _hashes['new'][key]
    else:
        return False


# Returns the name of the cache file for the curent site.
def _cachefile() -> str:
    if not 'cachefile' in _hashes:
        name = hashlib.sha1(site.home().encode()).hexdigest() + '.pickle'
        if os.name == 'nt':
            root = os.getenv('LOCALAPPDATA', os.path.expanduser('~'))
            root = os.path.join(root, 'Ivy')
        else:
            root = os.path.expanduser('~/.cache/ivy')
        _hashes['cachefile'] = os.path.join(root, name)
    return _hashes['cachefile']


# Load cached page hashes from the last build run.
@events.register('init_build')
def _load():
    if os.path.isfile(_cachefile()):
        with open(_cachefile(), 'rb') as file:
            _hashes['old'] = pickle.load(file)


# Cache page hashes to disk for the next build run.
@events.register('exit_build')
def _save():
    if _hashes['new'] and _hashes['new'] != _hashes['old']:
        if not os.path.isdir(os.path.dirname(_cachefile())):
            os.makedirs(os.path.dirname(_cachefile()))
        with open(_cachefile(), 'wb') as file:
            pickle.dump(_hashes['new'], file)
