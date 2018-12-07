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
from . import hooks


# Stores page hashes from the previous and current build runs.
_hashes = { 'old': {}, 'new': {} }


# Returns the name of the cachefile for the curent site.
def cachefile() -> str:
    if not 'cachefile' in _hashes:
        name = hashlib.sha1(site.home().encode()).hexdigest() + '.pickle'
        home = os.path.expanduser('~')
        _hashes['cachefile'] = os.path.join(home, '.cache', 'ivy', name)
    return _hashes['cachefile']


# Returns true if filepath is an existing file whose hash matches that of
# the content string. We use the relative filepath as the key to avoid
# leaking potentially sensitive information.
def match(filepath: str, content: str) -> bool:
    key = os.path.relpath(filepath, site.out())
    _hashes['new'][key] = hashlib.sha1(content.encode()).hexdigest()
    if os.path.exists(filepath):
        return _hashes['old'].get(key) == _hashes['new'][key]
    else:
        return False


# Load cached page hashes from the last build run.
@hooks.register('init_build')
def _load():
    if os.path.isfile(cachefile()):
        with open(cachefile(), 'rb') as file:
            _hashes['old'] = pickle.load(file)


# Cache page hashes to disk for the next build run.
@hooks.register('exit_build')
def _save():
    if _hashes['new'] and _hashes['new'] != _hashes['old']:
        if not os.path.isdir(os.path.dirname(cachefile())):
            os.makedirs(os.path.dirname(cachefile()))
        with open(cachefile(), 'wb') as file:
            pickle.dump(_hashes['new'], file)
