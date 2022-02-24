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


# Stores page-content hashes.
_hashes = {}


# Update flag. True if we've added new hashes.
_updated = False


# Stores the filepath for the cached-hashes file.
_file = None


# Returns true if `filepath` is an existing file whose hash matches that of
# the content string.
def match(filepath: str, content: str) -> bool:
    key = os.path.relpath(filepath, site.out())
    old_hash = _hashes.get(key)
    new_hash = hashlib.sha1(content.encode()).hexdigest()
    if new_hash == old_hash:
        return os.path.exists(filepath)
    else:
        global _updated
        _updated = True
        _hashes[key] = new_hash
        return False


# Clear the cache and delete any existing cache file.
def clear():
    _hashes.clear()
    if os.path.isfile(_cachefile()):
        os.remove(_cachefile())


# Returns the name of the cache file for the curent site.
def _cachefile() -> str:
    global _file
    if _file is None:
        name = hashlib.sha1(site.home().encode()).hexdigest() + '.pickle'
        if os.name == 'nt':
            root = os.getenv('LOCALAPPDATA', os.path.expanduser('~'))
            root = os.path.join(root, 'Ivy')
        else:
            root = os.path.expanduser('~/.cache/ivy')
        _file = os.path.join(root, name)
    return _file


# Load cached page hashes from the last build run.
@events.register(events.Event.INIT)
def _load():
    if os.path.isfile(_cachefile()):
        with open(_cachefile(), 'rb') as file:
            global _hashes
            _hashes = pickle.load(file)


# Cache page hashes to disk for the next build run.
@events.register(events.Event.EXIT)
def _save():
    if _updated:
        if not os.path.isdir(os.path.dirname(_cachefile())):
            os.makedirs(os.path.dirname(_cachefile()))
        with open(_cachefile(), 'wb') as file:
            pickle.dump(_hashes, file)
